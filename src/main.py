import numpy as np
import cv2
import matplotlib.pyplot as plt
import userinterface as ui

def hello() -> str:
	return "Hello world"

def run_app():
	app = ui.Application()
	app.master.title("MotifHighlighter Prototype")
	app.mainloop()

if __name__ == "__main__":  
	run_app()