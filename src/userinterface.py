import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst

LARGE_FONT = ("Verdana", 14)

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.formatGUI()
		self.createWidgets()

	def createWidgets(self):
		#Title of application
		title = tk.Label(
			self.table, text = "Welcome to virtual-cbct\n\n",
			font=LARGE_FONT, justify='center')
		title.grid(padx = 5)

		parameters = [
			("Distance to x-ray source (mm)", 300),
			("Distance to x-ray detector (mm)", 100),
			("Detector pixel size (mm)", 1.05),
			("Detector rows", 200),
			("Detector columns", 200),
			("Number of projections", 180)
		]

		rowcount = 1

		for parameter in parameters:
			tk.Label(self.table, text = parameter[0]).grid(row = rowcount, column = 0)
			entry = tk.Entry(self.table)
			entry.insert(tk.END, parameter[1])
			entry.grid(row = rowcount, column = 1)
			rowcount += 1

		buttonFrame = tk.Frame(self.table)
		#RESET button to delete the table
		self.resetButton = ttk.Button(buttonFrame, text = "RESET")
		self.resetButton["command"] = self.resetTable
		self.resetButton.grid(row = 0, column = 0)

		#SUBMIT button will remove newLines and populate motifList
		self.submitButton = ttk.Button(buttonFrame, text = "SUBMIT")
		self.submitButton["command"] = self.submitReq
		self.submitButton.grid(row = 0, column = 1)

		buttonFrame.grid(row = rowcount, column = 1, pady = 5)

		self.pack(expand = True)  #Not sure if this is needed
        
	def submitReq(self):
	  print("submitReq called")

	def resetTable(self):
		print("resetTable called")    

	def formatGUI(self):

		self.canvas = tk.Canvas(self , width = 700, height=500)
		#table is the frame object in canvas to populate with widgets
		self.table = tk.Frame(self.canvas)
		self.vbar = tk.Scrollbar(self,orient="vertical")
		self.canvas.config(yscrollcommand=self.vbar.set)

		self.vbar.pack(side="right",fill=tk.Y)
		self.vbar.config(command=self.canvas.yview)
		self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.canvas.create_window(0,0, anchor="nw", window = self.table, tags="self.table")
		self.table.bind("<Configure>", self.onFrameConfigure)

	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# Change attenuation coefficients of generated shape
# Change resolution of cbct
# Change speed? of cbct\