#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------#
#                                                                       #
# This file is part of the Horus Project                                #
#                                                                       #
# Copyright (C) 2014 Mundo Reader S.L.                                  #
#                                                                       #
# Date: June 2014                                                       #
# Author: Jesús Arroyo Torrens <jesus.arroyo@bq.com>                    #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                       #
#-----------------------------------------------------------------------#

__author__ = "Jesús Arroyo Torrens <jesus.arroyo@bq.com>"
__license__ = "GNU General Public License v3 http://www.gnu.org/licenses/gpl.html"

import wx

import os
import glob

from horus.util import profile
from horus.util import resources

class PreferencesDialog(wx.Dialog):
	def __init__(self, parent):
		super(PreferencesDialog, self).__init__(None, title=_("Preferences"))

		wx.EVT_CLOSE(self, self.onClose)

		self.main = parent

		#-- Graphic elements
		self.conParamsStaticText = wx.StaticText(self, -1, _("Connection Parameters"), style=wx.ALIGN_CENTRE)
		self.serialNameLabel = wx.StaticText(self, label=_("Serial Name"))
		self.serialNames = self.main.serialList()
		self.serialNameCombo = wx.ComboBox(self, choices=self.serialNames, size=(140,-1))
		self.cameraIdLabel = wx.StaticText(self, label=_("Camera Id"))
		self.cameraIdNames = self.main.videoList()
		self.cameraIdCombo = wx.ComboBox(self, choices=self.cameraIdNames, size=(143,-1))

		self.languageLabel = wx.StaticText(self, label=_("Language"))
		self.languages = [row[1] for row in resources.getLanguageOptions()]
		self.languageCombo = wx.ComboBox(self, choices=self.languages, value=profile.getPreference('language') , size=(110,-1))


		self.updateFirmware = wx.Button(self, -1, _("Update Firmware"))
		self.okButton = wx.Button(self, -1, _("Ok"))

		#-- Events
		self.serialNameCombo.Bind(wx.EVT_TEXT, self.onSerialNameTextChanged)
		self.cameraIdCombo.Bind(wx.EVT_TEXT, self.onCameraIdTextChanged)
		self.languageCombo.Bind(wx.EVT_COMBOBOX, self.onLanguageComboChanged)
		self.okButton.Bind(wx.EVT_BUTTON, lambda e: self.Close())
		self.updateFirmware.Bind(wx.EVT_BUTTON, self.onUpdateFirmware)

		#-- Fill data
		currentSerial = profile.getProfileSetting('serial_name')
		if len(self.serialNames) > 0:
			if currentSerial not in self.serialNames:
				self.serialNameCombo.SetValue(self.serialNames[0])
			else:
				self.serialNameCombo.SetValue(currentSerial)

		currentVideoId = profile.getProfileSetting('camera_id')
		if len(self.cameraIdNames) > 0:
			if currentVideoId not in self.cameraIdNames:
				self.cameraIdCombo.SetValue(self.cameraIdNames[0])
			else:
				self.cameraIdCombo.SetValue(currentVideoId)		

		#-- Call Events
		self.onSerialNameTextChanged(None)
		self.onCameraIdTextChanged(None)

		#-- Layout
		vbox = wx.BoxSizer(wx.VERTICAL)
		    
		vbox.Add(self.conParamsStaticText, 0, wx.ALL, 10)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.serialNameLabel, 0, wx.ALL^wx.RIGHT, 10)
		hbox.Add(self.serialNameCombo, 0, wx.ALL, 5)
		vbox.Add(hbox)
		hbox = wx.BoxSizer(wx.HORIZONTAL)   
		hbox.Add(self.cameraIdLabel, 0, wx.ALL, 10)
		hbox.Add(self.cameraIdCombo, 0, wx.ALL, 5)
		vbox.Add(hbox)

		vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL^wx.TOP, 5)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.languageLabel, 0, wx.ALL, 10)
		hbox.Add(self.languageCombo, 0, wx.ALL, 5)
		vbox.Add(hbox)

		vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL^wx.TOP, 5)

		vbox.Add(self.updateFirmware, 0, wx.ALL, 10) 

		vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL^wx.TOP, 5)

		vbox.Add(self.okButton, 0, wx.ALL, 10)

		self.SetSizer(vbox)
		self.Centre()

		self.Fit()

	def onSerialNameTextChanged(self, event):
		if len(self.serialNameCombo.GetValue()):
			profile.putProfileSetting('serial_name', self.serialNameCombo.GetValue())

	def onCameraIdTextChanged(self, event):
		if len(self.cameraIdCombo.GetValue()) > 0:
			profile.putProfileSetting('camera_id', self.cameraIdCombo.GetValue())

	def onUpdateFirmware(self, event):
		self.main.updateFirmware()

	def onLanguageComboChanged(self, event):
		if profile.getPreference('language') is not self.languageCombo.GetValue():
			profile.putPreference('language', self.languageCombo.GetValue())
			resources.setupLocalization(profile.getPreference('language'))
			wx.MessageBox(_("You have to restart the application to make the changes effective."), 'Info', wx.OK | wx.ICON_INFORMATION)

	def onClose(self, e):
		self.Destroy()

