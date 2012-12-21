import os
import sys
import subprocess
import math
import colorsys
import time
import re
import goocanvas

import gobject
import gtk
import gtk.gdk
import gtk.keysyms
import cairo
import pango
import pangocairo

try:
    import psyco
except:
    pass
else:
    psyco.full()

# See http://www.graphviz.org/pub/scm/graphviz-cairo/plugin/cairo/gvrender_cairo.c

# For pygtk inspiration and guidance see:
# - http://mirageiv.berlios.de/
# - http://comix.sourceforge.net/


class DotColor(object):
   
    __slots__ = ('r', 'g', 'b', 'a')
   
    def __init__(self, r, g, b, a = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
   
    @classmethod
    def parse_color(cls, string):
        """\
        Parses colors like '#RRGGBB', '#RRGGBBAA', 'H.H S.S V.V', and color 'names'
        into DotColor objects.
        """
        s = string[0]
        if s == '#':
            if len(string) == 7: # '#RRGGBB'
                return cls.parse_rgb(string)
            elif len(string) == 9: # '#RRGGBBAA'
                return cls.parse_rgba(string)
        elif s.isdigit():
            return cls.parse_hsv(string)
        else:
            return cls.parse_name(string)
   
    @classmethod        
    def parse_rgb(cls, string):
        """\
        Parses colors like #RRGGBB
        """
        color = gtk.gdk.color_parse(string)
        s = 1.0/65535.0
        return cls(color.red*s, color.green*s, color.blue*s)

    @classmethod
    def parse_rgba(cls, string):
        """\
        Parses colors like #RRGGBBAA
        """
        dot_color = cls.parse_rgb(string[0:7])
        dot_color.a = cls.__hex2float(string[8:9])
        return dot_color
       
    @classmethod
    def parse_hsv(cls, string):
        """\
        Parses colors like "H,S,V" or "H S V" or "H, S, V" or any other variation
        """
        h, s, v = map(float, replace(",", " ").split())
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return cls(r, g, b)

    @classmethod
    def parse_name(cls, string):
        """\
        Parses color 'names'
        """
        color = gtk.gdk.color_parse(string)
        s = 1.0/65535.0
        return cls(color.red*s, color.green*s, color.blue*s)
       
    @classmethod
    def __hex2float(cls, string):
        return float(int(string, 16)/255.0)
   
    def to_rgb_hex(self):
        t = (self.r * 255, self.g * 255, self.b * 255)
        return '#%02x%02x%02x' % t
       
    def to_rgba_hex(self):
        t = (self.r * 255, self.g * 255, self.b * 255, self.a * 255)
        return '#%02x%02x%02x%02x' % t
   
    def __str__(self):
        return self.to_rgba_hex()
   
    def __repr__(self):
        t = (self.r, self.g, self.b, self.a)
        return 'DotColor(%r, %r, %r, %r)' % t


class Pen:
    """Store pen attributes."""

    def __init__(self):
        # set default attributes
        self.color = DotColor(0, 0, 0)
        self.fill_color = DotColor(0, 0, 0)
        self.linewidth = 1.0
        self.fontsize = 14.0
        self.fontname = "Times-Roman"
        self.dash = ()
        

    def copy(self):
        """Create a copy of this pen."""
        pen = Pen()
        pen.__dict__ = self.__dict__.copy()
        return pen

    def highlighted(self):
        pen = self.copy()
        pen.color = DotColor(1, 0, 0)
        pen.fill_color = DotColor(1, .8, .8)
        return pen


class Shape:
    """Abstract base class for all the drawing shapes."""

    def __init__(self):
        pass

    def draw(self, cr):
        """Draw this shape with the given cairo context"""
        raise NotImplementedError

    def select_pen(self, highlight):
        if highlight:
            if not hasattr(self, 'highlight_pen'):
                self.highlight_pen = self.pen.highlighted()
            return self.highlight_pen
        else:
            return self.pen

    def highlight(self, highlight):
        pass

    def connect(self, event, callback, *params):
        pass

class TextShape(Shape):

    def __init__(self, pen, x, y, j, w, t):
        Shape.__init__(self)
        self.pen = pen.copy()
        self.x = x
        self.y = y
        self.j = j
        self.w = w
        self.t = t
        self.text = None

    def draw(self, cr):
        font = pango.FontDescription()
        font.set_family(self.pen.fontname)
        font.set_absolute_size(self.pen.fontsize * pango.SCALE)


        text = goocanvas.Text(parent = cr.get_root_item(),
                              text = self.t,
                              x = self.x,
                              y = self.y,
                              anchor = gtk.ANCHOR_CENTER,
                              fill_color = self.pen.fill_color.to_rgb_hex(),
                              use_markup = True,
                              font_desc = font,
                              visibility = goocanvas.ITEM_VISIBLE_ABOVE_THRESHOLD,
                              visibility_threshold = 0.30
                              )
       
        self.text = text
       
    def highlight(self, highlight):
        self.text.props.stroke_color = self.select_pen(highlight).color.to_rgb_hex()
        self.text.props.fill_color = self.select_pen(highlight).fill_color.to_rgb_hex()

    def connect(self, event, callback, *params):
        self.text.connect(event, callback, *params);


class EllipseShape(Shape):

    def __init__(self, pen, x0, y0, w, h, filled=False):
        Shape.__init__(self)
        self.pen = pen.copy()
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.filled = filled

    def draw(self, cr):
        ellipse = goocanvas.Ellipse(parent = cr.get_root_item(),
                                    center_x = self.x0,
                                    center_y = self.y0,
                                    radius_x = self.w,
                                    radius_y = self.h,
                                    stroke_color = self.pen.color.to_rgb_hex(),
                                    #line_dash = pen.dash,
                                    line_width = self.pen.linewidth,
                                    )
       
        if self.filled:
            ellipse.props.fill_color = self.pen.fill_color.to_rgb_hex()


class PolygonShape(Shape):

    def __init__(self, pen, points, filled=False):
        Shape.__init__(self)
        self.pen = pen.copy()
        self.points = points
        self.filled = filled
        self.polyline = None

    def draw(self, cr):
        p_points = goocanvas.Points(self.points)
        polyline = goocanvas.Polyline(parent = cr.get_root_item(),
                                      points = p_points,
                                      close_path = True,
                                      stroke_color = self.pen.color.to_rgb_hex(),
                                      )
       
        if self.filled:
            polyline.props.fill_color = self.pen.fill_color.to_rgb_hex()

        self.polyline = polyline
   
    def highlight(self, highlight):
        self.polyline.props.stroke_color = self.select_pen(highlight).color.to_rgb_hex()
        if self.filled:
            self.polyline.props.fill_color = self.select_pen(highlight).fill_color.to_rgb_hex()
       
    def connect(self, event, callback, *params):
        self.polyline.connect(event, callback, *params);


class LineShape(Shape):

    def __init__(self, pen, points):
        Shape.__init__(self)
        self.pen = pen.copy()
        self.points = points

    def draw(self, cr):
        p_points = goocanvas.Points(self.points)
           
        line = goocanvas.Polyline(parent = cr.get_root_item(),
                                  points = p_points,
                                  close_path = True,
                                  line_width = self.pen.linewidth,
                                  stroke_color = self.pen.color.to_rgb_hex(),
                                  )
       
       
class BezierShape(Shape):

    def __init__(self, pen, points, filled=False):
        Shape.__init__(self)
        self.pen = pen.copy()
        self.points = points
        self.filled = filled

    def draw(self, cr):
        x0, y0 = self.points[0]
        data = 'M%d,%d' % (x0, y0)
        for i in xrange(1, len(self.points), 3):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            x3, y3 = self.points[i + 2]
            data += 'C%d,%d %d,%d %d,%d' % (x1, y1, x2, y2, x3, y3)
           
        path = goocanvas.Path(parent = cr.get_root_item(),
                              data = data,
                              line_width = self.pen.linewidth,
                              stroke_color = self.pen.color.to_rgb_hex(),
                              )

        #cr.set_dash(pen.dash)

        if self.filled:
            path.props.fill_color = self.pen.fill_color.to_rgb_hex()
       
        self.path = path

    def highlight(self, highlight):
        self.path.props.stroke_color = self.select_pen(highlight).color.to_rgb_hex()
        if self.filled:
            self.path.props.fill_color = self.select_pen(highlight).fill_color.to_rgb_hex()
       
    def connect(self, event, callback, *params):
        self.path.connect(event, callback, *params);


class CompoundShape(Shape):
    def __init__(self, shapes):
        Shape.__init__(self)
        self.shapes = shapes
        self.cr = None

    def draw(self, cr):
        self.cr = cr
        for attr in self.shapes:
            if attr == '_ldraw_':
                continue
            for shape in self.shapes[attr]:
                shape.draw(cr)
        if '_ldraw_' in self.shapes:
            for shape in self.shapes['_ldraw_']:
                shape.draw(cr)


class Url(object):

    def __init__(self, item, url):
        self.item = item
        self.url = url


class Jump(object):

    def __init__(self, item, x, y):
        self.item = item
        self.x = x
        self.y = y


class Element(CompoundShape):
    """Base class for graph nodes and edges."""

    def __init__(self, shapes):
        CompoundShape.__init__(self, shapes)

    def get_url(self, x, y):
        return None

    def get_jump(self, x, y):
        return None


class Node(Element):

    def __init__(self, id, x, y, w, h, shapes, url):
        Element.__init__(self, shapes)

        self.id = id

        self.x = x
        self.y = y

        self.x1 = x - 0.5 * w
        self.x2 = x + 0.5 * w

        self.y1 = y - 0.5 * h
        self.y2 = y + 0.5 * h

        self.url = url


    def is_inside(self, x, y):
        return self.x1 <= x and x <= self.x2 and self.y1 <= y and y <= self.y2

    def get_url(self, x, y):
        if self.url is None:
            return None
        if self.is_inside(x, y):
            return Url(self, self.url)
        return None

    def get_jump(self, x, y):
        if self.is_inside(x, y):
            return Jump(self, self.x, self.y)
        return None

    def draw(self, cr):
        Element.draw(self, cr)
       
        for attr in self.shapes:
            for shape in self.shapes[attr]:
                shape.connect("enter_notify_event", cr.graph.node_on_enter_notify, self)
                shape.connect("leave_notify_event", cr.graph.node_on_leave_notify, self)
                shape.connect("button_press_event", cr.graph.node_on_button_press, self)

    def highlight(self, highlight):
        for shape in self.shapes['_draw_']:
            shape.highlight(highlight)

def distance(x1, y1, x2, y2):
    deltax = x2 - x1
    deltay = y2 - y1
    return math.sqrt(deltax*deltax + deltay*deltay)


class Edge(Element):

    def __init__(self, src, dst, points, shapes):
        Element.__init__(self, shapes)
        self.src = src
        self.dst = dst
        self.points = points

    RADIUS = 10

    def get_jump(self, x, y):
        if distance(x, y, *self.points[0]) <= self.RADIUS:
            return Jump(self, self.dst.x, self.dst.y)
        if distance(x, y, *self.points[-1]) <= self.RADIUS:
            return Jump(self, self.src.x, self.src.y)
        return None

    def draw(self, cr):
        Element.draw(self, cr)
       
        for attr in self.shapes:
            for shape in self.shapes[attr]:
                shape.connect("enter_notify_event", cr.graph.edge_on_enter_notify, self)
                shape.connect("leave_notify_event", cr.graph.edge_on_leave_notify, self)
                shape.connect("button_press_event", cr.graph.edge_on_button_press, self)

    def highlight(self, highlight):
        for attr in self.shapes:
            for shape in self.shapes[attr]:
                shape.highlight(highlight)


class Graph(Shape):

    def __init__(self, width=1, height=1, shapes=(), nodes=(), edges=()):
        Shape.__init__(self)
        self.width = width
        self.height = height
        self.shapes = shapes
        self.nodes = nodes
        self.edges = edges
        self.edges_by_ids = {}

        for edge in edges:
            for bi in ((edge.src.id, edge.dst.id), (edge.dst.id, edge.src.id)):
                if not self.edges_by_ids.has_key(bi[0]):
                    self.edges_by_ids[bi[0]] = {}
                if not self.edges_by_ids[bi[0]].has_key(bi[1]):
                    self.edges_by_ids[bi[0]][bi[1]] = set()
                    self.edges_by_ids[bi[0]][bi[1]].add(edge)

        self.highlights = set()

    def get_size(self):
        return self.width, self.height

    def draw(self, cr):
        cr.set_bounds(-12, -12, self.width + 12, self.height + 12)
       
        for attr in self.shapes:
            for shape in self.shapes[attr]:
                shape.draw(cr)
       
        for edge in self.edges:
            edge.draw(cr)
       
        for node in self.nodes:
            node.draw(cr)

    def get_url(self, x, y):
        for node in self.nodes:
            url = node.get_url(x, y)
            if url is not None:
                return url
        return None

    def get_jump(self, x, y):
        for edge in self.edges:
            jump = edge.get_jump(x, y)
            if jump is not None:
                return jump
        for node in self.nodes:
            jump = node.get_jump(x, y)
            if jump is not None:
                return jump
        return None
   
    def node_on_enter_notify(self, item, target, event, model):
        model.highlight(True)
   
    def node_on_leave_notify(self, item, target, event, model):
        if model not in self.highlights:
            model.highlight(False)

    def node_on_button_press(self, item, target, event, model):
        self.dehighlight()

        for ref in self.edges_by_ids[model.id]:
            for edge in self.edges_by_ids[model.id][ref]:
                self.highlights |= set((edge, edge.src, edge.dst))
               
        for i in self.highlights:
            i.highlight(True)
           
        if event.type == gtk.gdk._2BUTTON_PRESS:
            new_x = model.x - 0.5 / model.cr.get_scale() * model.cr.allocation.width
            new_y = model.y - 0.5 / model.cr.get_scale() * model.cr.allocation.height
            model.cr.scroll_to(new_x, new_y)

    def edge_on_enter_notify(self, item, target, event, model):
        for i in set((model, model.src, model.dst)):
            i.highlight(True)
   
    def edge_on_leave_notify(self, item, target, event, model):
        for i in set((model, model.src, model.dst)) - self.highlights:
            i.highlight(False)
           
    def edge_on_button_press(self, item, target, event, model):
        self.edge_on_enter_notify(item, target, event, model)
           
    def dehighlight(self):
        for i in self.highlights:
            i.highlight(False)
        self.highlights.clear()
       

class XDotAttrParser:
    """Parser for xdot drawing attributes.
    See also:
    - http://www.graphviz.org/doc/info/output.html#d:xdot
    """

    def __init__(self, parser, buf):
        self.parser = parser
        self.buf = self.unescape(buf)
        self.pos = 0
       
        self.pen = Pen()
        self.shapes = []

    def __nonzero__(self):
        return self.pos < len(self.buf)

    def unescape(self, buf):
        buf = buf.replace('\\"', '"')
        buf = buf.replace('\\n', '\n')
        return buf

    def read_code(self):
        pos = self.buf.find(" ", self.pos)
        res = self.buf[self.pos:pos]
        self.pos = pos + 1
        while self.pos < len(self.buf) and self.buf[self.pos].isspace():
            self.pos += 1
        return res

    def read_number(self):
        return int(self.read_code())

    def read_float(self):
        return float(self.read_code())

    def read_point(self):
        x = self.read_number()
        y = self.read_number()
        return self.transform(x, y)


    def read_text(self):
        num = self.read_number()
        pos = self.buf.find("-", self.pos) + 1
        self.pos = pos + num
        res = self.buf[pos:self.pos]
        while self.pos < len(self.buf) and self.buf[self.pos].isspace():
            self.pos += 1
        return res

    def read_polygon(self):
        n = self.read_number()
        p = []
        for i in range(n):
            x, y = self.read_point()
            p.append((x, y))
        return p

    def read_color(self):
        c = self.read_text()
        return DotColor.parse_color(c)

    def parse(self):
        s = self

        while s:
            op = s.read_code()
            if op == "c":
                color = s.read_color()
                if color is not None:
                    self.handle_color(color, filled=False)
            elif op == "C":
                color = s.read_color()
                if color is not None:
                    self.handle_color(color, filled=True)
            elif op == "S":
                # http://www.graphviz.org/doc/info/attrs.html#k:style
                style = s.read_text()
                if style.startswith("setlinewidth("):
                    lw = style.split("(")[1].split(")")[0]
                    lw = float(lw)
                    self.handle_linewidth(lw)
                elif style in ("solid", "dashed"):
                    self.handle_linestyle(style)
            elif op == "F":
                size = s.read_float()
                name = s.read_text()
                self.handle_font(size, name)
            elif op == "T":
                x, y = s.read_point()
                j = s.read_number()
                w = s.read_number()
                t = s.read_text()
                self.handle_text(x, y, j, w, t)
            elif op == "E":
                x0, y0 = s.read_point()
                w = s.read_number()
                h = s.read_number()
                self.handle_ellipse(x0, y0, w, h, filled=True)
            elif op == "e":
                x0, y0 = s.read_point()
                w = s.read_number()
                h = s.read_number()
                self.handle_ellipse(x0, y0, w, h, filled=False)
            elif op == "L":
                points = self.read_polygon()
                self.handle_line(points)
            elif op == "B":
                points = self.read_polygon()
                self.handle_bezier(points, filled=False)
            elif op == "b":
                points = self.read_polygon()
                self.handle_bezier(points, filled=True)
            elif op == "P":
                points = self.read_polygon()
                self.handle_polygon(points, filled=True)
            elif op == "p":
                points = self.read_polygon()
                self.handle_polygon(points, filled=False)
            else:
                sys.stderr.write("unknown xdot opcode '%s'\n" % op)
                break

        return self.shapes
   
    def transform(self, x, y):
        return self.parser.transform(x, y)

    def handle_color(self, color, filled=False):
        if filled:
            self.pen.fill_color = color
        else:
            self.pen.color = color

    def handle_linewidth(self, linewidth):
        self.pen.linewidth = linewidth

    def handle_linestyle(self, style):
        if style == "solid":
            self.pen.dash = ()
        elif style == "dashed":
            self.pen.dash = (6, )       # 6pt on, 6pt off

    def handle_font(self, size, name):
        self.pen.fontsize = size
        self.pen.fontname = name

    def handle_text(self, x, y, j, w, t):
        self.shapes.append(TextShape(self.pen, x, y, j, w, t))

    def handle_ellipse(self, x0, y0, w, h, filled=False):
        self.shapes.append(EllipseShape(self.pen, x0, y0, w, h, filled))

    def handle_line(self, points):
        self.shapes.append(LineShape(self.pen, points))

    def handle_bezier(self, points, filled=False):
        self.shapes.append(BezierShape(self.pen, points, filled))

    def handle_polygon(self, points, filled=False):
        self.shapes.append(PolygonShape(self.pen, points, filled))


EOF = -1
SKIP = -2


class ParseError(Exception):

    def __init__(self, msg=None, filename=None, line=None, col=None):
        self.msg = msg
        self.filename = filename
        self.line = line
        self.col = col

    def __str__(self):
        return ':'.join([str(part) for part in (self.filename, self.line, self.col, self.msg) if part != None])
       

class Scanner:
    """Stateless scanner."""

    # should be overriden by derived classes
    tokens = []
    symbols = {}
    literals = {}
    ignorecase = False

    def __init__(self):
        flags = re.DOTALL
        if self.ignorecase:
            flags |= re.IGNORECASE
        self.tokens_re = re.compile(
            '|'.join(['(' + regexp + ')' for type, regexp, test_lit in self.tokens]),
             flags
        )

    def next(self, buf, pos):
        if pos >= len(buf):
            return EOF, '', pos
        mo = self.tokens_re.match(buf, pos)
        if mo:
            text = mo.group()
            type, regexp, test_lit = self.tokens[mo.lastindex - 1]
            pos = mo.end()
            if test_lit:
                type = self.literals.get(text, type)
            return type, text, pos
        else:
            c = buf[pos]
            return self.symbols.get(c, None), c, pos + 1


class Token:

    def __init__(self, type, text, line, col):
        self.type = type
        self.text = text
        self.line = line
        self.col = col


class Lexer:

    # should be overriden by derived classes
    scanner = None
    tabsize = 8

    newline_re = re.compile(r'\r\n?|\n')

    def __init__(self, buf = None, pos = 0, filename = None, fp = None):
        if fp is not None:
            try:
                fileno = fp.fileno()
                length = os.path.getsize(fp.name)
                import mmap
            except:
                # read whole file into memory
                buf = fp.read()
                pos = 0
            else:
                # map the whole file into memory
                if length:
                    # length must not be zero
                    buf = mmap.mmap(fileno, length, access = mmap.ACCESS_READ)
                    pos = os.lseek(fileno, 0, 1)
                else:
                    buf = ''
                    pos = 0


            if filename is None:
                try:
                    filename = fp.name
                except AttributeError:
                    filename = None

        self.buf = buf
        self.pos = pos
        self.line = 1
        self.col = 1
        self.filename = filename

    def next(self):
        while True:
            # save state
            pos = self.pos
            line = self.line
            col = self.col

            type, text, endpos = self.scanner.next(self.buf, pos)
            assert pos + len(text) == endpos
            self.consume(text)
            type, text = self.filter(type, text)
            self.pos = endpos

            if type == SKIP:
                continue
            elif type is None:
                msg = 'unexpected char '
                if text >= ' ' and text <= '~':
                    msg += "'%s'" % text
                else:
                    msg += "0x%X" % ord(text)
                raise ParseError(msg, self.filename, line, col)
            else:
                break
        return Token(type = type, text = text, line = line, col = col)

    def consume(self, text):
        # update line number
        pos = 0
        for mo in self.newline_re.finditer(text, pos):
            self.line += 1
            self.col = 1
            pos = mo.end()

        # update column number
        while True:
            tabpos = text.find('\t', pos)
            if tabpos == -1:
                break
            self.col += tabpos - pos
            self.col = ((self.col - 1)//self.tabsize + 1)*self.tabsize + 1
            pos = tabpos + 1
        self.col += len(text) - pos


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.lexer.next()

    def match(self, type):
        if self.lookahead.type != type:
            raise ParseError(
                msg = 'unexpected token %r' % self.lookahead.text,
                filename = self.lexer.filename,
                line = self.lookahead.line,
                col = self.lookahead.col)

    def skip(self, type):
        while self.lookahead.type != type:
            self.consume()

    def consume(self):
        token = self.lookahead
        self.lookahead = self.lexer.next()
        return token


ID = 0
STR_ID = 1
HTML_ID = 2
EDGE_OP = 3

LSQUARE = 4
RSQUARE = 5
LCURLY = 6
RCURLY = 7
COMMA = 8
COLON = 9
SEMI = 10
EQUAL = 11
PLUS = 12

STRICT = 13
GRAPH = 14
DIGRAPH = 15
NODE = 16
EDGE = 17
SUBGRAPH = 18


class DotScanner(Scanner):

    # token regular expression table
    tokens = [
        # whitespace and comments
        (SKIP,
            r'[ \t\f\r\n\v]+|'
            r'//[^\r\n]*|'
            r'/\*.*?\*/|'
            r'#[^\r\n]*',
        False),

        # Alphanumeric IDs
        (ID, r'[a-zA-Z_\x80-\xff][a-zA-Z0-9_\x80-\xff]*', True),

        # Numeric IDs
        (ID, r'-?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)', False),

        # String IDs
        (STR_ID, r'"[^"\\]*(?:\\.[^"\\]*)*"', False),

        # HTML IDs
        (HTML_ID, r'<[^<>]*(?:<[^<>]*>[^<>]*)*>', False),

        # Edge operators
        (EDGE_OP, r'-[>-]', False),
    ]

    # symbol table
    symbols = {
        '[': LSQUARE,
        ']': RSQUARE,
        '{': LCURLY,
        '}': RCURLY,
        ',': COMMA,
        ':': COLON,
        ';': SEMI,
        '=': EQUAL,
        '+': PLUS,
    }

    # literal table
    literals = {
        'strict': STRICT,
        'graph': GRAPH,
        'digraph': DIGRAPH,
        'node': NODE,
        'edge': EDGE,
        'subgraph': SUBGRAPH,
    }

    ignorecase = True


class DotLexer(Lexer):

    scanner = DotScanner()

    def filter(self, type, text):
        # TODO: handle charset
        if type == STR_ID:
            text = text[1:-1]

            # line continuations
            text = text.replace('\\\r\n', '')
            text = text.replace('\\\r', '')
            text = text.replace('\\\n', '')
           
            text = text.replace('\\r', '\r')
            text = text.replace('\\n', '\n')
            text = text.replace('\\t', '\t')
            text = text.replace('\\', '')

            type = ID

        elif type == HTML_ID:
            text = text[1:-1]
            type = ID

        return type, text


class DotParser(Parser):

    def __init__(self, lexer):
        Parser.__init__(self, lexer)
        self.graph_attrs = {}
        self.node_attrs = {}
        self.edge_attrs = {}

    def parse(self):
        self.parse_graph()
        self.match(EOF)

    def parse_graph(self):
        if self.lookahead.type == STRICT:
            self.consume()
        self.skip(LCURLY)
        self.consume()
        while self.lookahead.type != RCURLY:
            self.parse_stmt()
        self.consume()


    def parse_subgraph(self):
        id = None
        if self.lookahead.type == SUBGRAPH:
            self.consume()
            if self.lookahead.type == ID:
                id = self.lookahead.text
                self.consume()
        if self.lookahead.type == LCURLY:
            self.consume()
            while self.lookahead.type != RCURLY:
                self.parse_stmt()
            self.consume()
        return id

    def parse_stmt(self):
        if self.lookahead.type == GRAPH:
            self.consume()
            attrs = self.parse_attrs()
            self.graph_attrs.update(attrs)
            self.handle_graph(attrs)
        elif self.lookahead.type == NODE:
            self.consume()
            self.node_attrs.update(self.parse_attrs())
        elif self.lookahead.type == EDGE:
            self.consume()
            self.edge_attrs.update(self.parse_attrs())
        elif self.lookahead.type in (SUBGRAPH, LCURLY):
            self.parse_subgraph()
        else:
            id = self.parse_node_id()
            if self.lookahead.type == EDGE_OP:
                self.consume()
                node_ids = [id, self.parse_node_id()]
                while self.lookahead.type == EDGE_OP:
                    node_ids.append(self.parse_node_id())
                attrs = self.parse_attrs()
                for i in range(0, len(node_ids) - 1):
                    self.handle_edge(node_ids[i], node_ids[i + 1], attrs)
            elif self.lookahead.type == EQUAL:
                self.consume()
                self.parse_id()
            else:
                attrs = self.parse_attrs()
                self.handle_node(id, attrs)
        if self.lookahead.type == SEMI:
            self.consume()

    def parse_attrs(self):
        attrs = {}
        while self.lookahead.type == LSQUARE:
            self.consume()
            while self.lookahead.type != RSQUARE:
                name, value = self.parse_attr()
                attrs[name] = value
                if self.lookahead.type == COMMA:
                    self.consume()
            self.consume()
        return attrs

    def parse_attr(self):
        name = self.parse_id()
        if self.lookahead.type == EQUAL:
            self.consume()
            value = self.parse_id()
        else:
            value = 'true'
        return name, value

    def parse_node_id(self):
        node_id = self.parse_id()
        if self.lookahead.type == COLON:
            self.consume()
            port = self.parse_id()
            if self.lookahead.type == COLON:
                self.consume()
                compass_pt = self.parse_id()
            else:
                compass_pt = None
        else:
            port = None
            compass_pt = None
        # XXX: we don't really care about port and compass point values when parsing xdot
        return node_id

    def parse_id(self):
        self.match(ID)
        id = self.lookahead.text
        self.consume()
        return id

    def handle_graph(self, attrs):
        pass

    def handle_node(self, id, attrs):
        pass

    def handle_edge(self, src_id, dst_id, attrs):
        pass


class XDotParser(DotParser):

    EDGE_DRAW_ATTRS = ("_draw_", "_ldraw_", "_hdraw_", "_tdraw_", "_hldraw_", "_tldraw_")
    NODE_DRAW_ATTRS = ("_draw_", "_ldraw_")
    GRAPH_DRAW_ATTRS = ("_draw_", "_ldraw_", "_hdraw_", "_tdraw_", "_hldraw_", "_tldraw_")

    def __init__(self, xdotcode):
        lexer = DotLexer(buf = xdotcode)
        DotParser.__init__(self, lexer)
       
        self.nodes = []
        self.edges = []
        self.shapes = {}
        self.node_by_name = {}
        self.top_graph = True
       
        self.width = 0
        self.height = 0

    def handle_graph(self, attrs):
        if self.top_graph:
            try:
                bb = attrs['bb']
            except KeyError:
                return

            if not bb:
                return

            xmin, ymin, xmax, ymax = map(float, bb.split(","))

            self.xoffset = -xmin
            self.yoffset = -ymax
            self.xscale = 1.0
            self.yscale = -1.0
            # FIXME: scale from points to pixels

            self.width = xmax - xmin
            self.height = ymax - ymin

            self.top_graph = False
       
        self.shapes = self.parse_draw_attrs_to_shapes(attrs, self.GRAPH_DRAW_ATTRS)

    def handle_node(self, id, attrs):
        try:
            pos = attrs['pos']
        except KeyError:
            return

        x, y = self.parse_node_pos(pos)
        w = float(attrs['width'])*72
        h = float(attrs['height'])*72
        shapes = self.parse_draw_attrs_to_shapes(attrs, self.NODE_DRAW_ATTRS)
        url = attrs.get('URL', None)
        node = Node(id, x, y, w, h, shapes, url)
        self.node_by_name[id] = node
        self.nodes.append(node)

    def handle_edge(self, src_id, dst_id, attrs):
        try:
            pos = attrs['pos']
        except KeyError:
            return
       
        points = self.parse_edge_pos(pos)
        shapes = self.parse_draw_attrs_to_shapes(attrs, self.EDGE_DRAW_ATTRS)
        src = self.node_by_name[src_id]
        dst = self.node_by_name[dst_id]
        edge = Edge(src, dst, points, shapes)
        self.edges.append(edge)

    def parse(self):
        DotParser.parse(self)

        return Graph(self.width, self.height, self.shapes, self.nodes, self.edges)

    def parse_node_pos(self, pos):
        x, y = pos.split(",")
        return self.transform(float(x), float(y))

    def parse_edge_pos(self, pos):
        points = []
        for entry in pos.split(' '):
            fields = entry.split(',')
            try:
                x, y = fields
            except ValueError:
                # TODO: handle start/end points
                continue
            else:
                points.append(self.transform(float(x), float(y)))
        return points

    def transform(self, x, y):
        # XXX: this is not the right place for this code
        x = (x + self.xoffset)*self.xscale
        y = (y + self.yoffset)*self.yscale
        return x, y
   
    def parse_draw_attrs_to_shapes(self, attrs, attr_list):
        """
        see http://www.graphviz.org/doc/info/output.html#d:xdot
        """
        shapes = {}
        for attr in attr_list:
            if attr in attrs:
                parser = XDotAttrParser(self, attrs[attr])
                shapes[attr] = parser.parse()
        return shapes    