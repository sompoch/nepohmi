from animation import animationColor

#
name = 'test'
prop = animationColor(tag = 'OPCDA2.0',
                        name= 'myOPC',
                        color1='black',
                        color2='black') # link to data structure [animation.py]
                                
                                
                                
#t = property[0].codition_fill_color[0]['Equal'] = 20

print prop.fill_color
print prop.chg_fill_color_state,prop.chg_fill_color_value

''' ---Property---[0]--
                        |_Codition_fill_color[0]----True  . Value
                                                            -False . Value
                                                            -None . Value
                                                            ....'''
print 'End'