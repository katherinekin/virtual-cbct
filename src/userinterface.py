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
		#Label at top of window
		label = tk.Label(
			self.table, text = "Welcome to virtual-cbct\n\n",
			font=LARGE_FONT, justify='center')

		label.grid(padx = 5, row = 0)

		#items in textboxFrame (column at left side)
		textboxFrame = tk.Frame(self.table)

		label2 = tk.Label(textboxFrame, text = "Change input information for virtual-cbct",
		                  font = 6)
		label2.grid()

		self.e = tkst.ScrolledText(textboxFrame, width=70, height=20, undo=True)
		self.e.grid()

		#items in buttonFrame (column at right side)
		buttonFrame = tk.Frame(self.table)

		#SUBMIT button will remove newLines and populate motifList
		self.sButtonPressed = False
		self.sButton = ttk.Button(buttonFrame, text = "SUBMIT")
		self.sButton["command"] = self.submitReq
		self.sButton.grid(column=1)

		#Display button to display info about motifs
		self.displayButton = ttk.Button(buttonFrame, text = "DISPLAY")
		self.displayButton["command"] = self.displayStats
		self.displayButton.grid(column=1)

		#Clear button to delete the table
		self.deleteButton = ttk.Button(buttonFrame, text = "DELETE")
		self.deleteButton["command"] = self.deleteTable
		self.deleteButton.grid(column=1)

		#Grid manager
		textboxFrame.grid(padx=10, column=0, row=1)
		buttonFrame.grid(column=1, row=1)

		self.pack(expand = True)  #Not sure if this is needed
        
	def submitReq(self):
	  print("submitReq called")

	def displayStats(self):
		print("displayStats called")

	def deleteTable(self):
		print("deleteTable called")    

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