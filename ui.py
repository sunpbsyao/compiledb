# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.1.0-0-g733bf3d)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class UiFrame
###########################################################################

class UiFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"compiledb", pos = wx.DefaultPosition, size = wx.Size( 525,180 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 525,180 ), wx.Size( 525,180 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_project_label = wx.StaticText( self, wx.ID_ANY, u"工程目录", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_project_label.Wrap( -1 )

		bSizer4.Add( self.m_project_label, 0, wx.ALL, 5 )

		self.m_project_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_project_text, 1, wx.ALL, 5 )

		self.m_openfile_btn = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_openfile_btn, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		m_projtype_radioboxChoices = [ u"IAR", u"Keil", u"Make" ]
		self.m_projtype_radiobox = wx.RadioBox( self, wx.ID_ANY, u"工程类型", wx.DefaultPosition, wx.DefaultSize, m_projtype_radioboxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.m_projtype_radiobox.SetSelection( 1 )
		bSizer5.Add( self.m_projtype_radiobox, 1, wx.ALL, 5 )


		bSizer5.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_convert_btn = wx.Button( self, wx.ID_ANY, u"转换", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_convert_btn, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer1.Add( bSizer5, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_openfile_btn.Bind( wx.EVT_BUTTON, self.m_openfile_btnOnButtonClick )
		self.m_convert_btn.Bind( wx.EVT_BUTTON, self.m_convert_btnOnButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def m_openfile_btnOnButtonClick( self, event ):
		event.Skip()

	def m_convert_btnOnButtonClick( self, event ):
		event.Skip()


