##########################################################
# PSU ECE510 Post-silicon Validation Project 1
# --------------------------------------------------------
# Filename: tap.py
# --------------------------------------------------------
# Purpose: TAP Controler Class
##########################################################

from tap.common.tap_gpio import *
from tap.log.logging_setup import *
import time

class Tap(Tap_GPIO):
	""" Class for JTAG TAP Controller"""

	def __init__(self,log_level=logging.INFO):
		""" initialize TAP """
		self.logger = get_logger(__file__,log_level)
		self.max_length = 1000

		#set up the RPi TAP pins
		Tap_GPIO.__init__(self)


	def toggle_tck(self, tms, tdi):
		""" toggle TCK for state transition 

		:param tms: data for TMS pin
		:type tms: int (0/1)
		:param tdi: data for TDI pin
		:type tdi: int (0/1)

		"""
		self.set_io_data(tms, tdi, 0)
		self.set_io_data(tms, tdi, 1)
		self.set_io_data(tms, tdi, 0)

	def reset(self):
		""" set TAP state to Test_Logic_Reset """
		# assert TMS for 5 TCKs in a row
		self.toggle_tck(1,1)
		self.toggle_tck(1,1)
		self.toggle_tck(1,1)
		self.toggle_tck(1,1)
		self.toggle_tck(1,1)

	def reset2ShiftIR(self):
		""" shift TAP state from reset to shiftIR """
		#reset to idle; tms = 0 for 1 tck
		self.toggle_tck(0,1)
	
		#idle to select DR; tms = 1 for 1 tck
		self.toggle_tck(1,1)
	
		#select DR to Select IR; tms = 1 for 1 tck
		self.toggle_tck(1,1)

		#select IR to Capture IR; tms = 0 for 1 tck
		self.toggle_tck(0,1)

		#capture IR to Shift IR; tms = 0 for 1 tck
		self.toggle_tck(0,1)
         

	def exit1IR2ShiftDR(self):
		""" shift TAP state from exit1IR to shiftDR """
		#Exit1IR to Update IR; tms = 1 for 1 tck
		self.toggle_tck(1,1)

		#Update IR to Select DR; tms = 1 for 1 tck
		self.toggle_tck(1,1)

		#select DR to Capture DR; tms = 0 for 1 tck
		self.toggle_tck(0,1)

		#Capture DR to Shift DR; tms = 0 for 1 tck
		self.toggle_tck(0,1)
        

	def exit1DR2ShiftIR(self):
		""" shift TAP state from exit1DR to shiftIR """
		#Exit1 DR to Update DR; tms = 1 for 1 tck
		self.toggle_tck(1,1)
	
		#Update DR to Select DR; tms = 1 for 1 tck
		self.toggle_tck(1,1)

		#Select DR to Select IR; tms = 1 for 1 tck
		self.toggle_tck(1,1)

		#Select IR to Capture IR; tms = 0 for 1 tck
		self.toggle_tck(0,1)

		#Capture IR to Shift IR; tms = 0 for 1 tck
		self.toggle_tck(0,1)
        

	def shiftInData(self, tdi_str):    
		""" shift in IR/DR data

		:param tdi_str: TDI data to shift in
		:type tdo_str: str

		"""
		#shift TDI data into shift IR
		#self.toggle_tck(0, *[int(i) for i in tdi_str[:-1]])
		i = 0
		while i < len(tdi_str) -1:
			self.toggle_tck(0, int(tdi_str[i]))
			i += 1
		#Shift last element of TDI data in shift IR while transitioning to Exit1 IR
		self.toggle_tck(1, int(tdi_str[-1]))


	def shiftOutData(self, length):
		""" get IR/DR data

		:param length: chain length        
		:type length: int
		:returns: int - TDO data

		"""
		#Shift data in shift DR register to TDO; tms = 0 for 1 tck
		values = []
		a = 0
		while a < length:
			values.append(str(self.read_tdo_data()))
			self.toggle_tck(0,1)
			a += 1
		#Shift DR to Exit1 DR; tms = 1 for 1 tck
		self.toggle_tck(1,1)
		#Binary string "values" is reversed and concatenated as single string and is converted into decimal integer
		return int("".join(reversed(values)),2)
   
     
	def getChainLength(self):
		""" get chain length

		:returns: int -- chain length	

		"""

		return 0
