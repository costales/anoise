# -*- coding: utf-8 -*-
# ANoise 0.0.33 (Ambient Noise) https://costales.github.io/projects/anoise/
# Copyright (C) 2015-2020 Marcos Alvarez Costales https://costales.github.io/
#
# ANoise is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# ANoise is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ANoise; if not, see http://www.gnu.org/licenses
# for more information.

import gi, os, threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, GObject, Gst
from dbus.mainloop.glib import DBusGMainLoop
from utils import *
from sound_menu import SoundMenuControls
from preferences import Preferences
try:
    from view import GUI
except ImportError:
    pass

# i18n
import gettext
gettext.textdomain('anoise')
_ = gettext.gettext

# playbin breaks in Kubuntu 14.04 > Needs Gst 0.10
try:
    gi.require_version('Gst', '1.0')
except:
    gi.require_version('Gst', '0.10')
    PLAYBIN = "playbin2"
else:
    PLAYBIN = "playbin"


class ANoise:
    """Control the sound indicator"""
    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        Gst.init(None)
        
        self.sound_menu = SoundMenuControls('anoise')
        self.noise = Noise()
        self.win_preferences = Preferences(self)
        
        # Need in a few DE
        try:
            self.window = GUI(self)
        except:
            pass
        
        self.player = Gst.ElementFactory.make(PLAYBIN, "player")
        self.player.connect("about-to-finish", self._loop)
        
        self.player.set_property('uri', self.noise.get_current_filename())
        self.is_playing = True
        
        dummy_i18n = (_("Coffee Shop"), _("Fire"), _("Forest"), _("Night"), _("Rain"), _("River"), _("Sea"), _("Storm"), _("Wind")) # Need i18n
        
        # Overwrite libraty methods
        self.sound_menu._sound_menu_is_playing = self._sound_menu_is_playing
        self.sound_menu._sound_menu_play       = self._sound_menu_play
        self.sound_menu._sound_menu_pause      = self._sound_menu_pause
        self.sound_menu._sound_menu_next       = self._sound_menu_next
        self.sound_menu._sound_menu_previous   = self._sound_menu_previous
        self.sound_menu._sound_menu_raise      = self._sound_menu_raise
        
        # Autostart when click on sound indicator icon
        threading.Timer(2, self._sound_menu_play).start()
    
    def _loop(self, message):
        """Start again the same sound in the EOS"""
        self.player.set_property('uri', self.noise.get_current_filename())
    
    def _sound_menu_is_playing(self):
        """Called in the first click"""
        return self.is_playing
    
    def _sound_menu_play(self):
        """Play"""
        self.is_playing = True # Need to overwrite this for an issue with autstart
        self.sound_menu.song_changed('', '', self.noise.get_name(), self.noise.get_icon())
        self.player.set_state(Gst.State.PLAYING)
        self.sound_menu.signal_playing()
    
    def _sound_menu_pause(self):
        """Pause"""
        self.is_playing = False # Need to overwrite this for an issue with autstart
        self.player.set_state(Gst.State.PAUSED)
        self.sound_menu.signal_paused()
    
    def _set_new_play(self, what):
        """Next or Previous"""
        self.noise.refresh_all_ogg()
        # Get Next/Previous
        if what == 'next':
            self.noise.set_next()
        if what == 'previous':
            self.noise.set_previous()
        # From pause?
        self.player.set_state(Gst.State.READY)
        if not self.is_playing:
            self.is_playing = True
        # Set new sound
        self.player.set_property('uri', self.noise.get_current_filename())
        # Play
        self._sound_menu_play()
    
    def _sound_menu_previous(self):
        """Previous"""
        self._set_new_play('previous')
    
    def _sound_menu_next(self):
        """Next"""
        self._set_new_play('next')
    
    def _sound_menu_raise(self):
        """Click on player"""
        self.win_preferences.show()
    
    def set_timer(self, enable, seconds):
        if enable:
            self.timer = threading.Timer(seconds, self._set_future_pause)
            self.timer.start()
        else:
            self.timer.cancel()
    
    def _set_future_pause(self):
        self.win_preferences.set_show_timer()
        self._sound_menu_pause()
    

if __name__ == "__main__":
    Lock()
    anoise = ANoise()
    Gtk.main()
