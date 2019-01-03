# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:37:56 2019

@author: Xingguang
"""

import wx
import wx.xrc
import cv2
###########################################################################
## Class MyFrame
## wxPython module: pip install wxPython
###########################################################################

class MyFrame ( wx.Frame ):
	def __init__( self, parent, video_path ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, \
                     size = wx.Size( 1047,662 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )   
        
        #Define choice lists and initial parameters
		self.surgeme = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
		self.s_f = ['Success', 'Fail']
		self.FrameNumber = 0
		self.FrameTime = 33
		self.video_path = video_path
		self.OneRow = []
		self.IndexSurgeme = 0
		self.IndexSF = 0     
        
        #Define the framework
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_load = wx.Button( self, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_load, 1, wx.ALL, 5 )
		
		self.Inform_bar = wx.StaticText( self, wx.ID_ANY, u"Information is shown here", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Inform_bar.Wrap( -1 )
		self.Inform_bar.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.Inform_bar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer2.Add( self.Inform_bar, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_toggleBtn2 = wx.ToggleButton( self, wx.ID_ANY, u"Choose Start Frame", wx.Point( -1,-1 ), wx.Size( 200,-1 ), 0 )
		self.m_toggleBtn2.SetValue( True ) 
		bSizer2.Add( self.m_toggleBtn2, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"PlayVideo" ), wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap = wx.StaticBitmap( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 640,480 ), 0 )
		bSizer4.Add( self.m_bitmap, 0, wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Choose Surgeme", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText.Wrap( -1 )
		bSizer5.Add( self.m_staticText, 0, wx.ALL, 5 )
		
		m_listBoxChoices = self.surgeme
		self.m_listBox = wx.ListBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 120,240 ), \
                              m_listBoxChoices, wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB|wx.LB_SINGLE )
		self.m_listBox.SetFont( wx.Font( 16, 70, 90, 90, False, "Candara" ) )
		self.m_listBox.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer5.Add( self.m_listBox, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText2 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Success or Fail", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer5.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		m_choiceChoices = self.s_f
		self.m_choice = wx.Choice( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceChoices, 0 )
		self.m_choice.SetSelection( 0 )
		bSizer5.Add( self.m_choice, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer5.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_Write = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Write To File", wx.Point( -1,-1 ), wx.Size( 140,35 ), 0 )
		self.m_Write.SetMinSize( wx.Size( 130,35 ) )
		self.m_Write.SetMaxSize( wx.Size( 160,40 ) )
		
		bSizer5.Add( self.m_Write, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_delete = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Delete Last Record", wx.DefaultPosition, wx.Size( 140,35 ), 0 )
		self.m_delete.SetMinSize( wx.Size( 130,35 ) )
		self.m_delete.SetMaxSize( wx.Size( 160,40 ) )
		
		bSizer5.Add( self.m_delete, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Current annotations" ), wx.VERTICAL )
		
		self.AnnotationArea = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.AnnotationArea.Wrap( -1 )
		self.AnnotationArea.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Cambria" ) )
		self.AnnotationArea.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
		
		sbSizer2.Add( self.AnnotationArea, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		
		sbSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( sbSizer3, 15, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_slider = wx.Slider( self, wx.ID_ANY, 0, 0, 4000, wx.DefaultPosition, wx.Size( -1,40 ), wx.SL_LABELS|wx.SL_TOP )
		self.m_slider.SetMinSize( wx.Size( -1,30 ) )
		self.m_slider.SetMaxSize( wx.Size( -1,50 ) )
		
		bSizer5.Add( self.m_slider, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_buttonSlow = wx.Button( self, wx.ID_ANY, u"0.5X", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		bSizer6.Add( self.m_buttonSlow, 0, wx.ALL, 5 )
		
		self.m_buttonBefore = wx.Button( self, wx.ID_ANY, u"Last Frame", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		bSizer6.Add( self.m_buttonBefore, 0, wx.ALL, 5 )
		
		self.m_toggleBtn = wx.ToggleButton( self, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.Size( 270,-1 ), 0 )
		bSizer6.Add( self.m_toggleBtn, 0, wx.ALL, 5 )
		
		self.m_buttonNext = wx.Button( self, wx.ID_ANY, u"Next Frame", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		bSizer6.Add( self.m_buttonNext, 0, wx.ALL, 5 )
		
		self.m_buttonFast = wx.Button( self, wx.ID_ANY, u"2X", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		bSizer6.Add( self.m_buttonFast, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_load.Bind( wx.EVT_BUTTON, self.OnLoad )
		self.m_toggleBtn2.Bind( wx.EVT_TOGGLEBUTTON, self.ToggleSaveFrame )
		self.m_listBox.Bind( wx.EVT_LISTBOX, self.SurgemeChosed )
		self.m_choice.Bind( wx.EVT_CHOICE, self.s_fChosed )
		self.m_Write.Bind( wx.EVT_BUTTON, self.SurgemeWrite )
		self.m_delete.Bind( wx.EVT_BUTTON, self.RecordDelete )
		self.m_slider.Bind( wx.EVT_SCROLL, self.OnSliderScroll )
		self.m_buttonSlow.Bind( wx.EVT_BUTTON, self.OnSlow )
		self.m_buttonBefore.Bind( wx.EVT_BUTTON, self.LastFrame )
		self.m_toggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self.Play_Pause )
		self.m_buttonNext.Bind( wx.EVT_BUTTON, self.NextFrame )
		self.m_buttonFast.Bind( wx.EVT_BUTTON, self.OnFast )
		self.Bind( wx.EVT_TIMER, self.OnTime, id=wx.ID_ANY )
	
        #Set flags
		self.PAUSE_FLAG = False
		self.PROCESSING_FLAG = False
		self.SurgemeChosed_FLAG = False
		self.S_fChosed_FLAG = False
        
	def __del__( self ):
		self.m_timer1.Stop()
		pass	
        
	# Virtual event handlers, overide them in your derived class
	def OnLoad( self, event ):
		self.PROCESSING_FLAG = True
		self.videoCapture = cv2.VideoCapture(self.video_path)
		if(self.videoCapture == None):
		    wx.SafeShowMessage('start', 'Open Failed')
		    return
		self.TotalFrame = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
		self.m_slider.SetMax(int(self.TotalFrame))
		self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
		self.FrameTime = 1000 / self.fps
		self.m_timer1.Start(self.FrameTime)
		event.Skip()
	
	def OnStop( self, event ):
		self.m_timer1.Stop()
		event.Skip()

	def ToggleSaveFrame( self, event ):
		if self.PROCESSING_FLAG:
		    self.EndFrame = event.GetEventObject().GetValue()
		    if not self.EndFrame and not self.OneRow:
		        self.OneRow.append(str(int(self.FrameNumber)))
		        event.GetEventObject().SetLabel("Choose End Frame")
		        print(self.EndFrame, self.OneRow)
		    elif self.EndFrame and len(self.OneRow) == 1:
		        self.OneRow.append(str(int(self.FrameNumber)))
		        event.GetEventObject().SetLabel("Choose Start Frame")
		        print(self.EndFrame, self.OneRow)
		else:
		    print('Please load the video!')
		event.Skip()
	
	def SurgemeWrite( self, event ):
		if self.PROCESSING_FLAG:
		    print(self.PROCESSING_FLAG)
		else:
		    print('Please load the video!')
		event.Skip()
        
	def SurgemeChosed( self, event ):
		self.IndexSurgeme = self.m_listBox.GetSelections()
		if len(self.IndexSurgeme) == 1:
		    IndexSurgeme = str(int(self.IndexSurgeme[0]) + 1)
		    if len(self.OneRow) == 2:
		        self.OneRow.append(IndexSurgeme)
		else:
		    print('Please only choose one surgeme!')
		print(IndexSurgeme)
		event.Skip()
	
	def s_fChosed( self, event ):
		self.IndexSF = self.m_choice.GetSelection()
		if self.IndexSF == 0 and len(self.OneRow) == 3:
		    self.OneRow.append('S')
		    print('S')
		elif self.IndexSF == 1 and len(self.OneRow) == 3:
		    self.OneRow.append('F')
		    print('F')
		event.Skip()
        
	def RecordDelete( self, event ):
		event.Skip()
        
	def OnSlow( self, event ):
		if self.FrameTime >= 200:
		    self.FrameTime = self.FrameTime * 2
		    self.m_timer1.Start(self.FrameTime)
		    print('Current fps:', self.FrameTime)
		else:
		    print('Minimum fps reached!')
		event.Skip()
        
	def OnSliderScroll( self, event ):
		if self.PROCESSING_FLAG:
		    self.FrameNumber = self.m_slider.GetValue()
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.FrameNumber)
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success):
		        self.MyImshow()
		else:
		    event.Skip()
        
	def LastFrame( self, event ):
		try:
		    self.FrameNumber -= 1
		    print(self.FrameNumber)
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES , self.FrameNumber)
		except AttributeError:
		    print('Please load the video!')
		else:
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success) :
		        self.MyImshow()
		event.Skip()
	
	def Play_Pause( self, event ):
		if self.PROCESSING_FLAG:
		    self.PAUSE_FLAG = event.GetEventObject().GetValue()
		    if self.PAUSE_FLAG:
		        self.m_timer1.Stop()
		        event.GetEventObject().SetLabel("Play")
		    else:
		        self.m_timer1.Start(self.FrameTime)
		        event.GetEventObject().SetLabel("Pause")
		else:
		    print('Please load the video!')
		event.Skip()
	
	def NextFrame( self, event ):
		try:
		    self.FrameNumber += 1
		    print(self.FrameNumber)
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES , self.FrameNumber)
		except AttributeError:
		    print('Please load the video!')
		else:
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success) :
		        self.MyImshow()
		event.Skip()
	
	def OnFast( self, event ):
		if self.FrameTime <= 10:
		    self.FrameTime = self.FrameTime * 0.5
		    self.m_timer1.Start(self.FrameTime)
		    print('Current fps:', self.FrameTime)
		else:
		    print('Maximum fps reached!')
		event.Skip()

	def OnTime( self, event ):
		if self.PROCESSING_FLAG:
		    success, self.CurrentFrame = self.videoCapture.read()
		    self.FrameNumber = self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES)
		    if(success):
		        self.MyImshow()
		else:
		    event.Skip()
        
	def MyImshow(self, width = 640, height = 480):
		image = cv2.cvtColor(self.CurrentFrame, cv2.COLOR_BGR2RGB)
		pic = wx.Bitmap.FromBuffer(width, height, image) 
		self.m_bitmap.SetBitmap(pic)
		self.m_slider.SetValue(int(self.FrameNumber))
        
        
if __name__ =='__main__':
    video_path = r'D:\S\Project\data\temp.mp4'
    write_path = r'D:\S\Project\data'
    app = wx.App()
    frame = MyFrame(None, video_path)
    frame.Show()
    app.MainLoop()
    del app
