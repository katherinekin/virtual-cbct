import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
import astra_cbct as cbct

LARGE_FONT = ("Verdana", 14)

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.formatGUI()
		self.createWidgets()
		self.cbct_obj = cbct.Virtual_Cbct()

	def createWidgets(self):
		#Title of application
		title = tk.Label(
			self.table, text = "Welcome to virtual-cbct\n\n",
			font=LARGE_FONT)
		title.grid(padx = 5, row = 0)

		# Create a label frame for x-ray parameters
		xraySettingsFrame = tk.LabelFrame(self.table, text = "X-ray Settings")
		self.parameters = [
			("Distance to x-ray source (mm)", 300),
			("Distance to x-ray detector (mm)", 100),
			("Detector pixel size (mm)", 1.05),
			("Detector rows", 200),
			("Detector columns", 200),
			("Number of projections", 180)
		]

		rowcount = 0
		self.entries = {} # Hash each entry element by field name
		for parameter in self.parameters:
			tk.Label(xraySettingsFrame, text = parameter[0]).grid(row = rowcount, column = 0)
			entry = tk.Entry(xraySettingsFrame)
			entry.insert(tk.END, parameter[1])
			entry.grid(row = rowcount, column = 1)
			self.entries[parameter[0]] = entry
			rowcount += 1

		buttonFrame = tk.Frame(xraySettingsFrame)
		#RESET button to set back to default values
		self.resetButton = ttk.Button(buttonFrame, text = "RESET")
		self.resetButton["command"] = self.resetTable
		self.resetButton.grid(row = 0, column = 0)
		# SAVE button to save new xray settings
		self.saveXrayButton = ttk.Button(buttonFrame, text = "SAVE")
		self.saveXrayButton["command"] = self.saveXraySettings
		self.saveXrayButton.grid(row = 0, column = 1)

		buttonFrame.grid(row = rowcount, column = 1, pady = 5)
		rowcount += 1

		xraySettingsFrame.grid(padx = 5, row = 1)

		self.submitButton = ttk.Button(self.table, text = "SUBMIT")
		self.submitButton["command"] = self.submitReq
		self.submitButton.grid(row = 2, column = 3)


	def saveXraySettings(self):
		for entry in self.entries:
			if "source" in entry:
				self.cbct_obj.distance_source_origin = int(self.entries[entry].get())
			elif "distance" in entry and "detector" in entry:
				self.cbct_obj.distance_origin_detector = int(self.entries[entry].get())
			elif "pixel" in entry:
				self.cbct_obj.detector_pixel_size = float(self.entries[entry].get())
			elif "rows" in entry:
				self.cbct_obj.detector_rows = int(self.entries[entry].get())
			elif "columns" in entry:
				self.cbct_obj.detector_cols = int(self.entries[entry].get())
			elif "projections" in entry:
				self.cbct_obj.num_of_projections = int(self.entries[entry].get())
		print("Saved Xray settings.")

	def autoSave(self):
		self.saveXraySettings()

	def submitReq(self):
		self.autoSave()
		self.cbct_obj.start_run()
		print("Run complete.")

	def resetTable(self):
		for parameter in self.parameters:
			self.entries[parameter[0]].delete(0, 'end')
			self.entries[parameter[0]].insert(0, parameter[1])

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