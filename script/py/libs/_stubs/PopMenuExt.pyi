# This file and all related intellectual property rights are
# owned by Derivative Inc. ("Derivative").  The use and modification
# of this file is governed by, and only permitted under, the terms
# of the Derivative [End-User License Agreement]
# [https://www.derivative.ca/Agreements/UsageAgreementTouchDesigner.asp]
# (the "License Agreement").  Among other terms, this file can only
# be used, and/or modified for use, with Derivative's TouchDesigner
# software, and only by employees of the organization that has licensed
# Derivative's TouchDesigner software by [accepting] the License Agreement.
# Any redistribution or sharing of this file, with or without modification,
# to or with any other person is strictly prohibited [(except as expressly
# permitted by the License Agreement)].
#
# Version: 099.2017.30440.28Sep
#
# _END_HEADER_

# PopMenuExt

TDFunctions = op.TDModules.mod.TDFunctions

# Note that selection style is currently locked to "Click" because of Windows
# issues. Setting to "Press" can cause problems when clicking on a menu that is
# floating above a non-TouchDesigner area.

class PopMenuExt:
	"""
	An easy to use pop up menu. See the Open method for instructions or set up
	using parameters.
	"""

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.configComp = ownerComp.par.Configcomp.eval()
		self.itemsTable = ownerComp.op('itemsIn')
		self.layoutTable = ownerComp.op('itemsLayout')
		self.insertTitleDAT = ownerComp.op('insertTitle')
		self.insertTitleDAT.bypass = not ownerComp.par.Title.eval()
		self.buttonFormat = self.configComp.op('buttonPress')
		self.Scaler = ownerComp.op('scaler')
		self.Window = ownerComp.par.Windowcomp.eval()
		self.Lister = ownerComp.op('lister')
		self.colDefine = ownerComp.op('colDefine')
		self.mouseMonitorChan = \
							op.TDDevices.op('mouse/deviceOut').chan('monitor')
		self.mouseXChan = op.TDDevices.op('mouse/deviceOut').chan('abs_mouse_x')
		self.mouseYChan = op.TDDevices.op('mouse/deviceOut').chan('abs_mouse_y')
		self.LastCell = self.SubMenuCell = None
		self.CallbackDetails = None

		# offset for size
		TDFunctions.createProperty(self, 'OffsetX', 0, dependable=True)
		TDFunctions.createProperty(self, 'OffsetY', 0, dependable=True)
		# offset for keeping on screen
		TDFunctions.createProperty(self, 'ScreenAdjustX', 0, dependable=True)
		TDFunctions.createProperty(self, 'ScreenAdjustY', 0, dependable=True)
		# one-time position offset
		TDFunctions.createProperty(self, 'TempAdjustX', 0, dependable=True)
		TDFunctions.createProperty(self, 'TempAdjustY', 0, dependable=True)
		# list of submenu type cells
		TDFunctions.createProperty(self, 'SubMenuItems', [], dependable=True)
		# store parent menu if this is a submenu
		TDFunctions.createProperty(self, 'ParentMenu', None, dependable=True)
		# selection value for output
		TDFunctions.createProperty(self, 'Selected', -1, dependable=True)
		# optimal menu height
		TDFunctions.createProperty(self, 'OptimalHeight', 23, dependable=True,
								   readOnly=True)
		# optimal menu width
		TDFunctions.createProperty(self, 'OptimalWidth', 23, dependable=True,
								   readOnly=True)
		# item column width
		TDFunctions.createProperty(self, 'ColumnWidth', 23, dependable=True,
								   readOnly=True)
		# item column width
		TDFunctions.createProperty(self, 'ShortcutWidth', 23, dependable=True,
								   readOnly=True)
		# if True, show scrollbar
		TDFunctions.createProperty(self, 'ShowScrollbar', False, 
								   dependable=True, readOnly=True)
		# checked items list or dict
		TDFunctions.createProperty(self, 'CheckedItems', [], dependable=True,
								   readOnly=True)

		self._openDelay = None # run ob for delay before opening

		self.setAttachPars()

		#self.Window.par.winclose.pulse()
		run('args[0].ext.PopMenuExt.refresh() if args[0] else None' ,
			ownerComp, delayFrames=1, delayRef=op.TDResources)

	# IMPORTANT! Any changes to arguments need to be reflected in OpenSubMenu
	def Open(self, items=None, callback=None, callbackDetails=None,
			 highlightedItems=None, disabledItems=None, dividersAfterItems=None,
			 checkedItems=None, subMenuItems=None, autoClose=None,
			 shortcuts=None,
			 rolloverCallback=None, allowStickySubMenus=None,
			 title=None, scale=None):
		"""
		Open the menu.

		items: a list of item strings for the menu. Default is to use the
			items set up in the comp. These options will replace the ones in the
			component's Items parameter.
			If this is None, use parameters for defaults.
		callback: a method that will be called when a selection is made. If not
			provided, Callback DAT will be searched.
		callbackDetails: will be passed to callbacks in addition to item chosen.
		highlightedItems: list of strings for items to highlight
		disabledItems: list of strings for greyed out, unselectable items.
		dividersAfterItems: list of strings for items with dividers below them.
		checkedItems: list of strings for items with check marks next to them.
			Will show the 'check' graphic in configComp.
			Also accepts a dict of strings with 'item': bool. Will show the
				'checkOn' or 'checkOff' graphic depending on bool.
			Also accepts a string which will be used as an EXPRESSION to
				continually evaluate.
		subMenuItems: list of strings for items with indicator and will select
			on rollOver instead of click. Always use OpenSubMenu in handler
			function. Set SubMenu parameter to another popMenu comp. Default is
			[]... no parameter available for submenus.
		autoClose: 0: no autoClose, 1: will close after selection or click away,
			2: will close after click away
		rolloverCallback: will be called when a cell is rolledOver. A callback
			with cell -1 will be called when mouse leaves menu or menu closes.
			Uses same callbackDetails as selection callback. If not provided,
			Callback DAT will be searched
		allowStickySubMenus: if True, clicking on subMenu items will lock their
			submenus open
		title: automatically add this string as a disabled title item at top of 
			menu
		scale: scales the popup menu created
		"""
		if items is not None:
			if not isinstance(items, list):
				raise TypeError (
						"PopMenu items must be list of strings",
						 self.ownerComp)
			self.ownerComp.par.Items.val = str(items)
			# change parameter defaults
			if disabledItems is None:
				disabledItems = []
			if dividersAfterItems is None:
				dividersAfterItems = []
			if checkedItems is None:
				checkedItems = []
			if shortcuts is None:
				shortcuts = {}
			if subMenuItems is None:
				subMenuItems = []
			if highlightedItems is None:
				highlightedItems = []
			if autoClose is None:
				autoClose = 1
			if allowStickySubMenus is None:
				allowStickySubMenus = True
			if title is None:
				title = ''
			if scale is None:
				scale = 1
		if scale is not None:
			self.ownerComp.par.Scale = scale
		if disabledItems is not None:
			if not isinstance(disabledItems, list):
				raise TypeError (
						"PopMenu disabled items must be list of strings",
						self.ownerComp)
			self.ownerComp.par.Disableditems.val = str(disabledItems)
		if highlightedItems is not None:
			if not isinstance(highlightedItems, list):
				raise TypeError(
					"PopMenu highlighted items must be list of strings",
					self.ownerComp)
			self.ownerComp.par.Highlighteditems.val = str(highlightedItems)
		if dividersAfterItems is not None:
			if not isinstance(dividersAfterItems, list):
				raise TypeError (
						"PopMenu dividersAfterItems must be list of strings",
						self.ownerComp)
			self.ownerComp.par.Dividersafteritems.val = str(dividersAfterItems)
		if checkedItems is not None:
			if not isinstance(checkedItems, (list, dict, str)):
				raise TypeError (
						"PopMenu checkedItems must be list of strings, dict"
						" of 'item':bool or a str expression that evaluates to "
						"one of those.", self.ownerComp)
			if isinstance(checkedItems, str):
				self.ownerComp.par.Checkeditems.expr = checkedItems
			else:
				self.ownerComp.par.Checkeditems.val = str(checkedItems)
		if shortcuts is not None:
			if not isinstance(shortcuts, dict):
				raise TypeError (
						"PopMenu shortcuts must be a dict of item: shortcut.",
						self.ownerComp)
			self.ownerComp.par.Shortcuts.val = str(shortcuts)
		if subMenuItems is not None:
			self.SubMenuItems = subMenuItems.copy()
		else:
			self.SubMenuItems = []
		if callback:
			self.SetCallback(callback, "onSelect")
		else:
			self.SetCallback(None, "onSelect")
		if rolloverCallback:
			self.SetCallback(rolloverCallback, "onRollover")
		else:
			self.SetCallback(None, "onRollover")
		self.SubMenuCell = None
		if autoClose is not None:
			self.ownerComp.par.Autoclose.menuIndex = autoClose
		if allowStickySubMenus is not None:
			self.ownerComp.par.Allowstickysubmenus = allowStickySubMenus
		if title is not None:
			self.ownerComp.par.Title = str(title)
		self.CallbackDetails = callbackDetails
		self.updateCheckedItems(self.ownerComp.par.Checkeditems.eval())
		self.Lister.par.Refresh.pulse()
		self.Selected = -1
		#self.winOpen()
		self._openDelay = run(
		 		'op("' + self.ownerComp.path + '").ext.PopMenuExt.winOpen()',
		 		delayFrames=1, delayRef=op.TDResources)

	def SetCallback(self, callback, callbackName="onSelect"):
		self.ownerComp.ext.CallbacksExt.SetAssignedCallback(callbackName,
											 				callback)

	def winOpen(self):
		self.Close()
		self.setDimensions()
		self.RecalculateOffsets()
		ext.CallbacksExt.DoCallback('onOpen', self.infoDict())
		self.Lister.Refresh()
		self.Window.par.winopen.pulse()
		if not self.ParentMenu:
			self.Scaler.setFocus()


	def OpenSubMenu(self, items=None, callback=None, callbackDetails=None,
			 highlightedItems=None, disabledItems=None, dividersAfterItems=None,
			 checkedItems=None,
			 subMenuItems=None, autoClose=1, shortcuts=None,
			 rolloverCallback=None, allowStickySubMenus=None, title=None,
			 scale=None):
		"""
		Open this menu's sub-menu (uses op in subMenu parameter by default).
		Takes all the same arguments as Open()
		"""
		if scale is None:
			scale = self.ownerComp.par.Scale
		self._subMenuArgs = (items, callback, callbackDetails, highlightedItems,
							 disabledItems, dividersAfterItems, checkedItems,
							 subMenuItems, autoClose, shortcuts,
							 rolloverCallback, allowStickySubMenus, title, 
							 scale)
		self.SubMenu.Close()
		self.Scaler.setFocus()
		self.doOpenSubMenu()

	def doOpenSubMenu(self):
		"""
		Do the actual opening called for in OpenSubMenu, which can be delayed to
		prevent frame-rate drop when dragging mouse over submenuitems quickly.
		"""
		self.SubMenu.ParentMenu = self.ownerComp
		self.SubMenu.Open(*self._subMenuArgs)
		self.SubMenuCell = self.LastCell
		# HACK focus is lost so we have to restore rollover
		#debug('openSubMenu', self.LastCell)
		self.Lister.ext.ListerExt.onRollover(
										self.LastCell, 0, (0,0), -1, -1, (0,0))

	def SetPlacement(self, hAlign='Left', vAlign='Top', alignOffset=(0,0),
					 		buttonComp=None, hAttach='Left', vAttach='Bottom',
					 		matchWidth=False):
		"""
		Set up placement parameters for the popMenu.
		hAlign: set Horizontal Align
		vAlign: set Vertical Align
		alignOffset: set Align Offset
		buttonComp: set Button COMP
		hAttach: set Horizontal Attach
		vAttach: set Vertical Attach
		matchWidth: match width of menu to width of button Comp
		"""
		self.ownerComp.par.Horizontalalign = hAlign
		self.ownerComp.par.Verticalalign = vAlign
		self.ownerComp.par.Alignoffset1 = alignOffset[0]
		self.ownerComp.par.Alignoffset2 = alignOffset[1]
		self.ownerComp.par.Buttoncomp = buttonComp
		self.ownerComp.par.Horizontalattach = hAttach
		self.ownerComp.par.Verticalattach = vAttach
		if matchWidth:
			self.ownerComp.par.w = buttonComp.par.w
		else:
			self.ownerComp.par.w.expr = 'me.OptimalWidth'


	@property
	def SubMenu(self):
		"""
		Delayed because window location is not ready until next frame
		"""
		return self.ownerComp.par.Submenu.eval()

	def CloseAll(self):
		"""
		Utility for submenus... close all open menus
		"""
		topMenu = self.ownerComp
		while topMenu.ParentMenu:
			topMenu = topMenu.ParentMenu
		topMenu.Close()

	def Close(self):
		"""
		Close the menu
		"""
		try:
			self._openDelay.kill()
		except:
			pass
		self._openDelay = None
		if self.IsOpen:
			ext.CallbacksExt.DoCallback('onRollover', self.infoDict(-1))
			ext.CallbacksExt.DoCallback('onClose', self.infoDict())
			self.ownerComp.par.Checkeditems.mode = ParMode.CONSTANT
			self.Window.par.winclose.pulse()
			if self.ParentMenu:
				if not self.ParentMenu.Scaler.panel.focusselect:
					self.ParentMenu.Scaler.setFocus()
				self.ParentMenu = None
			self.TempAdjustX = self.TempAdjustY = 0
		self.callback = None

	def checkMenuRoll(self, cell):
		if cell == self.LastCell:
			self.OnSelect(cell, doautoClose=False, menuRoll=True)

	def OnRollover(self, cell):
		"""
		Called by panel exec when mouse is over a new cell.
		-1: mouse is not over a cell
		"""
		# if not self.Scaler.panel.focusselect:
		# 	self.Scaler.setFocus()
		self.LastCell = cell
		# sanity check
		if self.ParentMenu and not self.ParentMenu.IsOpen:
			self.Close()
		try:
			ext.CallbacksExt.DoCallback('onRollover', self.infoDict(cell))
		except:
			self.Close()
			raise
		# deal with submenu closing and opening
		if self.SubMenu and cell != -1:
			if self.infoDict(cell)['item'] in self.SubMenuItems and \
						self.infoDict(cell)['item'] not in self.DisabledItems:
				if cell == self.SubMenuCell:
					# going back to current submenu cell. Close sub sub menu
					if self.SubMenu.SubMenu and self.SubMenu.SubMenu.IsOpen:
						self.SubMenu.SubMenu.Close()
						self.SubMenu.SubMenuCell = None
				elif not self.SubMenu.IsOpen \
						or self.SubMenu.par.Autoclose.menuIndex == 1 \
						or not self.ownerComp.par.Allowstickysubmenus.eval():
					# new submenu cell
					run('args[0].checkMenuRoll(args[1])', self, cell, 
							delayMilliSeconds=300)
					# self.OnSelect(cell, doautoClose=False, menuRoll=True)
			else:
				if self.SubMenu.IsOpen and (
						self.SubMenu.par.Autoclose.menuIndex == 1
						or not self.ownerComp.par.Allowstickysubmenus.eval()):
					self.SubMenu.Close()
					self.SubMenuCell = None
					# self.Scaler.setFocus()

	def OnSelect(self, cell, doautoClose=True, menuRoll=False):
		"""
		Item selected according to Select Style parameter.
		"""
		infoDict = self.infoDict(cell)
		infoDict['subMenuRoll'] = menuRoll
		# disabled items
		if cell is not None and infoDict['item'] in self.DisabledItems:
			return
		# submenus
		if self.SubMenu and self.SubMenu.IsOpen:
			if self.SubMenuCell == cell:
				if self.ownerComp.par.Allowstickysubmenus.eval():
					self.SubMenu.par.Autoclose = \
								0 if self.SubMenu.par.Autoclose.menuIndex else 1
				return
			else:
				if infoDict['item'] in self.SubMenuItems and \
								not self.SubMenu.par.Autoclose.eval() and \
								self.ownerComp.par.Allowstickysubmenus.eval():
				# 	run("op('" + self.SubMenu.path + "').par.Autoclose=False",
				# 		delayFrames=1, delayRef=op.TDResources)
				# else:
					self.SubMenu.par.Autoclose = 0
				self.SubMenu.Close()
				#print(project.pythonStack())
		elif self.SubMenuCell == cell:
			return
		# ordinary selects...
		try:
			ext.CallbacksExt.DoCallback('onSelect', infoDict)
		except:
			self.Close()
			import traceback; print(traceback.format_exc())
		self.Selected = cell
		if self.ownerComp.par.Autoclose.menuIndex == 1 and doautoClose and \
				cell != self.SubMenuCell:
			parentMenu = self.ParentMenu
			self.autoClose()
			if parentMenu:
				# close all parents until one doesn't have autoClose
				while parentMenu:
					if parentMenu.par.Autoclose.menuIndex == 1:
						parentMenu.SubMenuCell = None
						pm = parentMenu.ParentMenu # close destroys value
						parentMenu.Close()
						parentMenu = pm
					else:
						parentMenu = None

	def OnMouseUp(self, cell):
		"""
		Called by panel exec when mouse is released. No cell is provided.
		"""
		ext.CallbacksExt.DoCallback('onMouseUp', self.infoDict(cell))

	def OnClick(self, cell):
		# button style click
		ext.CallbacksExt.DoCallback('onClick', self.infoDict(cell))
		# if self.ownerComp.par.Selectionstyle.eval() == 'Click':
		self.OnSelect(cell)

	def OnMouseDown(self, cell):
		"""
		Called by panel exec when mouse is pressed.
		"""
		if cell == -1:
			if self.ownerComp.par.Autoclose.menuIndex:
				self.autoClose()
			else:
				return
		ext.CallbacksExt.DoCallback('onMouseDown', self.infoDict(cell))
		# if self.ownerComp.par.Selectionstyle.eval() == 'Press':
		# 	self.OnSelect(cell)

	def infoDict(self, cell=None):
		"""
		Return info dict for a given cell. Used for callbacks.
		"""
		if cell is not None:
			return {'index': cell,
					'item': self.GetLabel(cell),
					'row': self.GetItemRow(cell),
					'details': self.CallbackDetails,
					'menu': self.ownerComp}
		else:
			return {'details': self.CallbackDetails,
					'menu': self.ownerComp}

	def GetLabel(self, cell):
		"""
		Returns the label of a given cell id
		"""
		try:
			return self.itemsTable[cell, 0].val
		except:
			# no corresponding data. Means empty cell or -1
			return None

	def GetItemRow(self, cell):
		"""
		Returns the table row of a given cell id
		"""
		try:
			return self.ownerComp.op('rowTable').row(cell)
		except:
			# no corresponding data. Means empty cell or -1
			None

	@property
	def IsOpen(self):
		return self.Window.isOpen

	@property
	def Items(self):
		try:
			items = [row[0].val for row in self.itemsTable.rows()]
		except:
			items = []
		# if self.Title:
		# 	items = [self.Title] + items
		return items

	@property
	def DisabledItems(self):
		parVal = self.ownerComp.par.Disableditems.eval()
		if parVal.strip():
			items = eval(parVal.strip())
		else:
			items = []
		return items

	@property
	def HighlightedItems(self):
		parVal = self.ownerComp.par.Highlighteditems.eval()
		if parVal.strip():
			return eval(parVal.strip())
		else:
			return []

	@property
	def DividersAfterItems(self):
		if self.NumCols > 1:
			return []
		parVal = self.ownerComp.par.Dividersafteritems.eval()
		if parVal.strip():
			items = eval(parVal.strip())
		else:
			items = []
		return items			

	@property
	def CheckedItems(self):
		return self._CheckedItems.val

	def updateCheckedItems(self, val=None):
		if val is None:
			val = self.ownerComp.par.Checkeditems.eval()
		if self.NumCols > 1:
			self._CheckedItems.val = []
		if val.strip():
			try:
				self._CheckedItems.val = eval(val.strip())
			except:
				self._CheckedItems.val = []
		else:
			self._CheckedItems.val = []

	@property
	def Shortcuts(self):
		if self.NumCols > 1:
			return {}
		parVal = self.ownerComp.par.Shortcuts.eval()
		if parVal.strip():
			return eval(parVal.strip())
		else:
			return {}

	@property
	def Title(self):
		if self.NumCols > 1:
			return None
		return self.ownerComp.par.Title.eval()

	@property
	def NumCols(self):
		return self.ownerComp.par.Columns.eval()

	@property
	def ConfigComp(self):
		return self.configComp

	def setDimensions(self):
		self.CalculateOptimalDimensions()
		self.Lister.par.w = self.ownerComp.par.w.eval()
		self.Lister.par.h = self.ownerComp.par.h.eval()
		if not self.Window.isOpen:
			self.RecalculateOffsets()

	def CalculateOptimalDimensions(self):
		# if self.Window.isOpen:
		# 	self.Window.par.winclose.pulse()
		# items
		iwidth = 10
		# oldBold = self.buttonFormat.par.bold.eval()
		# self.buttonFormat.par.bold = True
		for i in self.Items:
			textSize = self.buttonFormat.evalTextSize(i)[0]
			if textSize > iwidth:
				iwidth = textSize
		offset = self.buttonFormat.par.position1.eval() \
				if hasattr(self.buttonFormat.par, 'position1') else \
					self.buttonFormat.par.textoffsetx.eval()
		self._ColumnWidth.val = iwidth + offset * 3
		width = self.NumCols * self.ColumnWidth
		#self.buttonFormat.par.bold = oldBold

		# shortcuts
		swidth = 10
		for i in self.Shortcuts.values():
			textSize = self.buttonFormat.evalTextSize(i)[0]
			if textSize > iwidth:
				swidth = textSize
		self._ShortcutWidth.val = swidth + \
								offset + 34
		if self.NumCols==1 and self.Shortcuts:
			width += self.ShortcutWidth

		# symbols
		if self.NumCols==1 and (self.CheckedItems or self.SubMenuItems or \
					self.ownerComp.par.Checkeditems.mode == ParMode.EXPRESSION):
			width += int(self.colDefine['width', 'Symbol'])

		self._OptimalWidth.val = max(16, width)
		rowHeight = self.configComp.op('master').height
		optimalHeight = rowHeight * (self.layoutTable.numRows 
						+ (1 if self.Title else 0))

		if self.ownerComp.par.Maxheightmode == 'Pixels':
			maxHeight = self.ownerComp.par.Maxheight.eval()
		else:
			maxHeight = rowHeight * self.ownerComp.par.Maxheight.eval()
		if self.ownerComp.par.Maxheight.eval() and optimalHeight > maxHeight:
			self._OptimalWidth.val += 13 # lister scrollbar size
			self._OptimalHeight.val = maxHeight
			self._ShowScrollbar.val = True
		else:
			self._OptimalHeight.val = optimalHeight
			self._ShowScrollbar.val = False

	def CellLocationY(self, cell):
		if cell < 0 or cell > len(self.Items):
			return 0 # just fake it
		baseLocation = cell * self.configComp.op('master').height \
						* self.ownerComp.par.Scale
		return baseLocation 

	def LostFocus(self):
		if self.Scaler.panel.rollover:
			self.Scaler.setFocus()
			return
		if self.ownerComp.par.Autoclose.menuIndex:
			if self.SubMenu and self.SubMenu.IsOpen:
				# recurse to bottom subMenu
				subMenu = self.SubMenu
				while subMenu.SubMenu and subMenu.SubMenu.IsOpen:
					# if subMenu.panel.inside:
					# 	doClose = False
					subMenu = subMenu.SubMenu
				if not subMenu.panel.inside:
					self.Close()
			else:
				ext.CallbacksExt.DoCallback('onLostFocus', self.infoDict())
				self.autoClose()

	def autoClose(self):
		if self.SubMenu and self.SubMenu.IsOpen:
			return
		self.Close()

	def RecalculateOffsets(self):
		"""
		Recalculate the window offsets. This is called when parent window moves
		or alignment changes. This is a bit slow, but shouldn't matter when
		moving windows is involved.
		"""
		halfWidth = self.Window.par.winw * 0.5
		halfHeight = self.Window.par.winh * 0.5
		if not self.Window.isOpen:
			mouseX = self.mouseXChan.eval()
			mouseY = self.mouseYChan.eval()
		else:
			mouseX = self.Window.x - self.Window.par.winoffsetx.eval()
			mouseY = self.Window.y - self.Window.par.winoffsety.eval()

		monitor = monitors[int(self.mouseMonitorChan.eval())]
		self.ScreenAdjustX = self.OffsetX = 0
		self.ScreenAdjustY = self.OffsetX = 0
		buttonComp = self.ownerComp.par.Buttoncomp.eval() if \
				self.ownerComp.par.Buttoncomp.eval() and \
				self.ownerComp.par.Buttoncomp.eval().panel.inside else None
		if self.ParentMenu:
			# submenu placement
			self.OffsetX = \
					self.ParentMenu.Window.x \
					+ self.ParentMenu.Window.par.winw
			self.OffsetY = \
					self.ParentMenu.Window.y\
					+ self.ParentMenu.Window.par.winh\
					- self.ParentMenu.CellLocationY(self.ParentMenu.LastCell) \
					- 2 * halfHeight

		else:
			# mouse relative
			if self.ownerComp.par.Horizontalalign == 'Center':
				self.OffsetX = 0
			elif self.ownerComp.par.Horizontalalign == 'Left':
				self.OffsetX = halfWidth
			elif self.ownerComp.par.Horizontalalign == 'Right':
				self.OffsetX = -halfWidth
			if self.ownerComp.par.Verticalalign == 'Center':
				self.OffsetY = 0
			elif self.ownerComp.par.Verticalalign == 'Top':
				self.OffsetY = -halfHeight
			elif self.ownerComp.par.Verticalalign == 'Bottom':
				self.OffsetY = halfHeight
			if buttonComp:
				# button relative adjustments
				# store values in case we need to screen-correct
				toButton = (-int(buttonComp.panel.insideu * buttonComp.width),
							-int(buttonComp.panel.insidev * buttonComp.height))
				# first set offsets to button's 0,0
				self.OffsetX += toButton[0]
				self.OffsetY += toButton[1]
				if self.ownerComp.par.Horizontalattach == 'Center':
					self.OffsetX += buttonComp.width * 0.5
				elif self.ownerComp.par.Horizontalattach == 'Right':
					self.OffsetX += buttonComp.width
				if self.ownerComp.par.Verticalattach == 'Center':
					self.OffsetY += buttonComp.height * 0.5
				elif self.ownerComp.par.Verticalattach == 'Top':
					self.OffsetY += buttonComp.height

		# force menu onto screen
		if self.ParentMenu:
			winLeft = self.Window.par.winoffsetx.eval()
			winRight = winLeft + 2 * halfWidth
			winBottom = self.Window.par.winoffsety.eval()
			winTop = winBottom + 2 * halfHeight
		else:
			winLeft = mouseX + self.Window.par.winoffsetx.eval() - halfWidth
			winRight = winLeft + 2 * halfWidth
			winBottom = mouseY + self.Window.par.winoffsety.eval() - halfHeight
			winTop = winBottom + 2 * halfHeight
		# if winLeft < monitor.scaledLeft:
		# 	if buttonComp:
		# 		self.OffsetX = toButton[0] + halfWidth + buttonComp.width
		# 	# else:
		# 	# 	self.ScreenAdjustX = monitor.left - winLeft
		# if winRight > monitor.scaledRight:
		# 	if self.ParentMenu:
		# 		# move to other side of menu
		# 		self.OffsetX -= 2 * halfWidth + self.ParentMenu.width - 1
		# 	elif buttonComp:
		# 		self.OffsetX = toButton[0] - halfWidth
		# 	# else:
		# 	# 	self.ScreenAdjustX = monitor.right - winRight + 1
		# if winTop > monitor.scaledTop:
		# 	if buttonComp:
		# 		self.OffsetY = toButton[1] - halfHeight
		# 	# else:
		# 	# 	self.ScreenAdjustY = monitor.top - winTop
		# if winBottom < monitor.scaledBottom:
		# 	if buttonComp:
		# 		self.OffsetY = toButton[1] + halfHeight + buttonComp.par.h
		# 	# else:
		# 	# 	self.ScreenAdjustY = monitor.bottom - winBottom

	def setAttachPars(self):
		enable = self.ownerComp.par.Buttoncomp.eval()
		self.ownerComp.par.Horizontalattach.enable = \
				self.ownerComp.par.Verticalattach.enable = enable

	def refresh(self):
		"""
		Update menu display
		"""
		self.updateCheckedItems()
		self.setDimensions()
		if hasattr(self.Lister, 'Refresh'):
			self.Lister.Refresh()
		# hack to make sure par execs cook properly
		# run('op(' + str(self.ownerComp.id) + ').cook(force=True)',
		# 	delayFrames=1, delayRef=op.TDResources)

	def onParValueChange(self, par, val, prev):
		if par.name in ['Horizontalalign', 'Verticalalign']:
			self.RecalculateOffsets()
		elif par.name == 'Columns':
			self.ownerComp.par.Checkeditems.enable = par.eval() == 1
			self.ownerComp.par.Dividersafteritems.enable = par.eval() == 1
			self.Lister.ext.ListerExt.setupAutoColDefine(True)
			self.Lister.Refresh()
		elif par.name in ['Items','Dividersafteritems', 'Checkeditems',
						  'Disableditems', 'Highlighteditems', 'w', 'h',
						  'Shortcuts', 'Itemtextalign', 'Title']:
			if par.name == 'Title':
				self.insertTitleDAT.bypass = not par.eval()
				self.Lister.cook(force=True)
			self.Lister.ext.ListerExt.setupAutoColDefine(True)
			if self.IsOpen or self.ownerComp.viewer:
				self.refresh()
		elif par.name == 'Buttoncomp':
			self.setAttachPars()
			
	def onParPulse(self, par):
		if par.name == 'Open':
			self.Open()
		elif par.name == 'Close':
			self.Close()
		elif par.name == 'Editcallbacks':
			dat = self.ownerComp.par.Callbackdat.eval()
			dat.par.edit.pulse()
		elif par.name == 'Helppage':
			ui.viewFile('https://docs.derivative.ca/index.php?'
						'title=Palette:popMenu')
		elif par.name == 'Refreshlookconfig':
			self.Lister.par.Refresh.pulse()




