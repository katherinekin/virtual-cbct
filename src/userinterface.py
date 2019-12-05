import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
import astra_cbct as cbct
import phantom as pm

LARGE_FONT = ("Verdana", 14)

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.vCommand = (self.register(self.onValidateInt), '%S' )
		self.grid()
		self.formatGUI()
		self.entries = {} # Hash each entry element by field name
		self.createWidgets()
		self.cbct_obj = cbct.Virtual_Cbct()
		self.phantomGenerator = pm.PhantomGenerator()

	def onValidateInt(self, S):
		if (S.isdigit() or S.count('.') == 1 and (S.replace('.', '')).isdigit()):
			return True
		self.bell()
		return False

	def onValidateFloat(self, S):
		for char in S:
			if char not in "0123456789.":
				return False
		return True

	def createWidgets(self):
		# Add title of application
		title = tk.Label(
			self.table, text = "Welcome to virtual-cbct\n\n",
			font=LARGE_FONT)
		title.grid(padx = 5, row = 0)

		# Create a label frame for x-ray parameters
		xraySettingsFrame = tk.LabelFrame(self.table, text = "X-ray Settings")
		self.xraySettingsWidget(xraySettingsFrame)
		xraySettingsFrame.grid(padx = 5, row = 1)

		phantomFrame = tk.LabelFrame(self.table, text = "Phantom Settings")
		self.phantomSettingsWidget(phantomFrame)
		phantomFrame.grid(padx = 5, row = 2)

		self.submitButton = ttk.Button(self.table, text = "SUBMIT")
		self.submitButton["command"] = self.submitReq
		self.submitButton.grid(row = 3, column = 3)

	def xraySettingsWidget(self, xraySettingsFrame):		
		parameters = [
			("Distance to x-ray source (mm)", 300),
			("Distance to x-ray detector (mm)", 100),
			("Detector pixel size (mm)", 1.05),
			("Detector rows", 200),
			("Detector columns", 200),
			("Number of projections", 180)
		]

		rowcount = 0		
		for parameter in parameters:
			tk.Label(xraySettingsFrame, text = parameter[0]).grid(row = rowcount, column = 0)
			if "pixel" in parameter[0]:
				entry = tk.Entry(xraySettingsFrame, validate="key", 
					validatecommand = (self.register(self.onValidateFloat), '%S' ))
			else:
				entry = tk.Entry(xraySettingsFrame, validate="key", 
					validatecommand = (self.register(self.onValidateInt), '%S' ))
			entry.insert(tk.END, parameter[1])
			entry.grid(row = rowcount, column = 1)
			self.entries[parameter[0]] = entry
			rowcount += 1

		buttonFrame = tk.Frame(xraySettingsFrame)
		#RESET button to set back to default values
		resetButton = ttk.Button(buttonFrame, text = "RESET", command = lambda: self.reset(parameters))
		
		resetButton.grid(row = 0, column = 0)
		# SAVE button to save new xray settings
		saveXrayButton = ttk.Button(buttonFrame, text = "SAVE")
		saveXrayButton["command"] = self.saveXraySettings
		saveXrayButton.grid(row = 0, column = 1)

		buttonFrame.grid(row = rowcount, column = 1, pady = 5)
		rowcount += 1

	def phantomSettingsWidget(self, phantomFrame):
		parameters = [
			("Height of phantom", 110),
			("Width of phantom", 40),			
			("Thickness of shell", 5),
			("Attenuation of shell", 1),
			("Attenuation of cavity", 0),
		]

		rowcount = 0		
		for parameter in parameters:
			tk.Label(phantomFrame, text = parameter[0]).grid(row = rowcount, column = 0)
			if "Attenuation" in parameter[0]:
				entry = tk.Entry(phantomFrame, validate="key", 
					validatecommand = (self.register(self.onValidateFloat), '%S' ))
			else:
				entry = tk.Entry(phantomFrame, validate="key", 
					validatecommand = (self.register(self.onValidateInt), '%S' ))
			entry.insert(tk.END, parameter[1])
			entry.grid(row = rowcount, column = 1)
			self.entries[parameter[0]] = entry
			rowcount += 1

		buttonFrame = tk.Frame(phantomFrame)

		#RESET button to set back to default values
		self.resetPhantomButton = ttk.Button(buttonFrame, text = "RESET", command = lambda: self.reset(parameters))		
		self.resetPhantomButton.grid(row = 0, column = 0)
		
		# SAVE button to save new xray settings
		self.savePhantomButton = ttk.Button(buttonFrame, text = "SAVE")
		self.savePhantomButton["command"] = self.savePhantomSettings
		self.savePhantomButton.grid(row = 0, column = 1)

		buttonFrame.grid(row = rowcount, column = 1, pady = 5)
		rowcount += 1

	def saveXraySettings(self):
		for entry in self.entries:
			if "source" in entry:
				self.cbct_obj.distanceFromSourceToOrigin = int(self.entries[entry].get())
			elif "distance" in entry and "detector" in entry:
				self.cbct_obj.distanceFromOriginToDetector = int(self.entries[entry].get())
			elif "pixel" in entry:
				correctedString = self.stringWithoutExtraDecimals(self.entries[entry].get())
				self.entries[entry].delete(0, tk.END)
				self.entries[entry].insert(0, correctedString)
				self.cbct_obj.pixelSize = float(correctedString)				
			elif "rows" in entry:
				self.cbct_obj.detectorRows = int(self.entries[entry].get())
			elif "columns" in entry:
				self.cbct_obj.detectorColumns = int(self.entries[entry].get())
			elif "projections" in entry:
				self.cbct_obj.numberOfProjections = int(self.entries[entry].get())
		print("Saved Xray settings.")

	def stringWithoutExtraDecimals(self, S):
		idx = S.find('.') + 1
		return S[:idx] + S[idx:].replace('.', '')

	def savePhantomSettings(self):
		for entry in self.entries:
			if "Height of phantom" in entry:
				self.phantomGenerator.height = int(self.entries[entry].get())
			elif "Width of phantom" in entry:
				self.phantomGenerator.width = int(self.entries[entry].get())
			elif "Thickness" in entry:
				self.phantomGenerator.thickness = int(self.entries[entry].get())
			elif "Attenuation" in entry:
				correctedString = self.stringWithoutExtraDecimals(self.entries[entry].get())
				self.entries[entry].delete(0, tk.END)
				self.entries[entry].insert(0, correctedString)
				if "shell" in entry:
					self.phantomGenerator.shellAttenuation = float(correctedString)
				elif "cavity" in entry:
					self.phantomGenerator.cavityAttenuation = float(correctedString)
		print("Saved Phantom settings.")

	def autoSave(self):
		self.saveXraySettings()
		self.savePhantomSettings()

	def submitReq(self):
		self.autoSave()

		phantom = self.phantomGenerator.create_phantom(
			self.cbct_obj.detectorRows,
			self.cbct_obj.detectorColumns)

		self.cbct_obj.start_run(phantom)
		print("Run complete.")

	def reset(self, parameters):
		for parameter in parameters:
			self.entries[parameter[0]].delete(0, 'end')
			self.entries[parameter[0]].insert(0, parameter[1])
		print("Reset Xray settings")

	def formatGUI(self):

		self.canvas = tk.Canvas(self , width = 700, height=500)
		#table is the frame object in canvas to populate with widgets
		self.table = tk.Frame(self.canvas)
		self.vbar = tk.Scrollbar(self,orient = "vertical")
		self.canvas.config(yscrollcommand = self.vbar.set)

		self.vbar.pack(side = "right",fill = tk.Y)
		self.vbar.config(command = self.canvas.yview)
		self.canvas.pack(side = tk.TOP, fill = tk.BOTH, expand=True)

		self.canvas.create_window(0,0, anchor = "nw", window = self.table, tags="self.table")
		self.table.bind("<Configure>", self.onFrameConfigure)

	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion = self.canvas.bbox("all"))

