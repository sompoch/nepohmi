# Borrowed from the PyWine project
import gtk
import os

def file_browse(self, dialog_action, file_name=""):
	"""This function is used to browse for a pyWine file.
	It can be either a save or open dialog depending on
	what dialog_action is.
	The path to the file will be returned if the user
	selects one, however a blank string will be returned
	if they cancel or do not select one.
	dialog_action - The open or save mode for the dialog either
	gtk.FILE_CHOOSER_ACTION_OPEN, gtk.FILE_CHOOSER_ACTION_SAVE
	@param file_name - Default name when doing a save
	@returns - File Name, or None on cancel.
	"""

	if (dialog_action==gtk.FILE_CHOOSER_ACTION_OPEN):
		dialog_buttons = (gtk.STOCK_CANCEL
			, gtk.RESPONSE_CANCEL
			, gtk.STOCK_OPEN
			, gtk.RESPONSE_OK)
		dlg_title = "Open Post"
	else:
		dialog_buttons = (gtk.STOCK_CANCEL
			, gtk.RESPONSE_CANCEL
			, gtk.STOCK_SAVE
			, gtk.RESPONSE_OK)
		dlg_title = "Save Post"

	file_dialog = gtk.FileChooserDialog(title=dlg_title
		, action=dialog_action
		, buttons=dialog_buttons)
	"""set the filename if we are saving"""
	if (dialog_action==gtk.FILE_CHOOSER_ACTION_SAVE):
		file_dialog.set_current_name(file_name)
	"""Create and add the pywine filter"""
	filter = gtk.FileFilter()
	filter.set_name("WordPy Post")
	filter.add_pattern("*." + FILE_EXT)
	file_dialog.add_filter(filter)
	if (dialog_action==gtk.FILE_CHOOSER_ACTION_OPEN):
		"""Create and add the 'all files' filter"""
		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		file_dialog.add_filter(filter)

	"""Init the return value"""
	result = None
	if file_dialog.run() == gtk.RESPONSE_OK:
		result = file_dialog.get_filename()
		if (dialog_action==gtk.FILE_CHOOSER_ACTION_SAVE):
			result, extension = os.path.splitext(result)
			result = result + "." + FILE_EXT
	file_dialog.destroy()

	return result

if __name__ == '__main__':
    file_browse(gtk.FILE_CHOOSER_ACTION_OPEN,"")
