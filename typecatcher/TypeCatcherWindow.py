# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Andrew Starr-Bochicchio <a.starr.b@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk  # pylint: disable=E0611
from gi.repository import WebKit
import itertools
import re
import glob
import logging
logger = logging.getLogger('typecatcher')

from typecatcher_lib import Window
from typecatcher.AboutTypeCatcherDialog import AboutTypeCatcherDialog
from typecatcher.FindFonts import FindFonts
from typecatcher_lib.xdg import fontDir
from typecatcher.DownloadFont import DownloadFont, UninstallFont, DownloadError
from typecatcher.html_preview import html_font_view, select_text_preview

from typecatcher.AlphaOneCleanUp import fix_file_names

# See typecatcher_lib.Window.py for more details about how this class works
class TypeCatcherWindow(Window):
    __gtype_name__ = "TypeCatcherWindow"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        fix_file_names() # Clean up after old release.
        self.fonts = FindFonts()
        """Set up the main window"""
        super(TypeCatcherWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutTypeCatcherDialog

        # Code for other initialization actions should be added here.
        self.toolbar = builder.get_object("toolbar")
        context = self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.view = WebKit.WebView()
        webview = builder.get_object("webview")
        webview.add(self.view)
        htmlfile = html_font_view()
        self.view.load_html_string(htmlfile, "file:///")
        webview.show_all()

        webview_settings = self.view.get_settings()
        webview_settings.set_property('enable-default-context-menu', False)

        # the data in the model
        listmodel = builder.get_object("liststore")
        # append the values in the model
        for i in range(len(self.fonts)):
            listmodel.append(self.fonts[i])

        # a treeview to see the data stored in the model
        self.listview = builder.get_object("font_list")
        cell = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Fonts"), cell, text=0)
        self.listview.append_column(col)
        self.listview.columns_autosize()
        # when a row is selected, it emits a signal
        self.listview.get_selection().connect("changed", self.on_select_changed)

        self.search_field = self.builder.get_object('search_field')
        completion = self.builder.get_object('entrycompletion')
        completion.set_model(listmodel)
        completion.set_text_column(0)
        self.search_field.set_completion(completion)
        completion.connect('match-selected', self.on_match_selected)

        self.mnu_save = self.builder.get_object('mnu_save')
        self.mnu_save.connect("activate", self.on_download_btn_clicked)

        self.text_selector = self.builder.get_object('text_selector')
        self.text_menu = self.builder.get_object('text_menu')
        self.text_selector.set_menu(self.text_menu)

        radios = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']
        for position, item in enumerate(radios):
            item = self.builder.get_object(item)
            item.connect("toggled", 
                         self.on_menu_choices_changed,
                         str(position + 1))
        self.text_content = "random"

        self.scale = self.builder.get_object('spinbutton')
        self.scale.set_value(36)
        self.scale.connect("value-changed", self.spin_moved)

    def spin_moved(self, widget):
        size = int(self.scale.get_value())
        text_size = "document.getElementById('text_preview').style.fontSize = '%s';" % size
        self.view.execute_script(text_size)

    def on_menu_choices_changed(self, button, name):
        if name == "1":
            self.text_content = "random"
        elif name == "2":
            self.text_content = "ipsum"
        elif name == "3":
            self.text_content = "kafka"
        elif name == "4":
            self.text_content = "hgg"
        elif name == "5":
            self.text_content = "ggm"
        elif name == "6":
            self.text_content = "ralph"
        elif name == "7":
            self.text_content = "jj"
        elif name == "8":
            self.text_content = "custom"
        self.set_text()

    def set_text(self):
        t = select_text_preview(self.text_content)
        js_text = "document.getElementById('text_preview').innerHTML = '%s';" % t
        self.view.execute_script(js_text)

    def js_exec(self):
        js_code = ["document.getElementById('start_page').style.display = 'None';",
                   """
                   document.getElementById('text_preview').style.fontFamily = "\'%s\'";
                   """  % (self.font)]
        font_loader = """WebFontConfig = {
        google: { families: [ '%s' ] },
        inactive: function() {
          document.getElementById('start_page').style.display = 'None';
          document.getElementById('text_preview').style.display = 'None';
          document.getElementById('no_connect').style.display = 'block';
        },
      }; 
      (function() {
        document.getElementsByTagName("html")[0].setAttribute("class","wf-loading")
        document.getElementsByTagName("html")[0].setAttribute("className","wf-loading")
        var wf = document.createElement('script');
        wf.src = ('https:' == document.location.protocol ? 'https' : 'http') +
            '://ajax.googleapis.com/ajax/libs/webfont/1.4.10/webfont.js';
        wf.type = 'text/javascript';
        wf.async = 'true';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(wf, s);
      })();""" % (self.font)
        show_text = [font_loader,
                     "document.getElementById('no_connect').style.display = 'None';",
                     "document.getElementById('text_preview').style.display = 'block';"]
        js_code.extend(show_text)
        if self.text_content == "random":
            self.set_text()
        for js in js_code:
            self.view.execute_script(js)
        self.js_installed_check()

    def js_installed_check(self):
        if glob.glob(fontDir + self.font + '_*.*'):
            js_show = "document.getElementById('installed').style.display = 'block';"
            self.view.execute_script(js_show)
        else:
            js_hide = "document.getElementById('installed').style.display = 'None';"
            self.view.execute_script(js_hide)

    def download_failed(self):
        err = ["document.getElementById('start_page').style.display = 'None';",
          "document.getElementById('text_preview').style.display = 'None';",
          "document.getElementById('no_connect').style.display = 'block';"]
        for js in err:
            self.view.execute_script(js)

    def on_search_field_activate(self, widget):
        fonts = list(itertools.chain(*self.fonts))
        entered_text = self.search_field.get_text()
        matcher = re.compile(entered_text, re.IGNORECASE)
        if any(itertools.ifilter(matcher.match, fonts)):
            for position, item in enumerate(fonts):
                if item.lower() == entered_text.lower():
                    self.listview.set_cursor(position)
        else:
            pass

    def on_match_selected(self, completion, treemodel, treeiter):
        self.font = treemodel[treeiter][completion.get_text_column()]
        self.js_exec()

    def on_select_changed(self, selection):
        (model, iter) = selection.get_selected()
        self.font = model[iter][0]
        self.js_exec()

    def on_search_field_icon_press(self, widget, icon_pos, event):
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            self.search_field.set_text("")

    def on_download_btn_clicked(self, button):
        try:
            try:
                DownloadFont(self.font, uri=None)
                self.js_installed_check()
            except DownloadError:
                self.download_failed()
        except AttributeError:
            head = _("This the install button.")
            message = _("Select a font on the left and press this button. The font will be installed for off-line use.")
            Window.info_dialog(self, head, message)

    def on_uninstall_btn_clicked(self, button):
        try:
            UninstallFont(self.font)
            self.js_installed_check()
        except AttributeError:
            head = _("This the uninstall button.")
            message = _("Select a font on the left and press this button. It will be removed from your system.")
            Window.info_dialog(self, head, message)

    def on_info_btn_clicked(self, button):
        try:
            info_url = "http://www.google.com/webfonts/specimen/" + \
                self.font.replace(' ', '+', -1)
            Gtk.show_uri(None, info_url, 0)
        except AttributeError:
            head = _("This the info button.")
            message = _("Select a font on the left and press this button. A browser will open with further information about the chosen font.")
            Window.info_dialog(self,head, message)

    def on_mnu_save_as_activate(self, button):
        try:
            dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL,
                                           Gtk.ResponseType.CANCEL,
                                           Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
            filename = self.font + ".ttf"
            dialog.set_current_name(filename)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                uri = dialog.get_filename()
                DownloadFont(self.font, uri)
            elif response == Gtk.ResponseType.CANCEL:
                pass
            dialog.destroy()
        except AttributeError:
            pass
