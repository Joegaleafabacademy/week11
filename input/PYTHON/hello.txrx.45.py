#
# hello.txrx.45.py
#
# receive and display transmit-receive step response
# hello.step.45.py serial_port
#
# Neil Gershenfeld
# CBA MIT 11/6/11
#
# (c) Massachusetts Institute of Technology 2011
# Permission granted for experimental and personal use;
# license for commercial sale available from MIT
#

from Tkinter import *
import serial

WINDOW = 600 # window size
eps = 0.75 # filter fraction
filt = 0.0 # filtered value


def idle(parent,canvas):
   global filt, eps
   #
   # idle routine
   #
   byte2 = 0
   byte3 = 0
   byte4 = 0
   ser.flush()
   #
   # find framing 
   #
   while 1:
      byte1 = byte2
      byte2 = byte3
      byte3 = byte4
      byte4 = ord(ser.read())
      if ((byte1 == 1) & (byte2 == 2) & (byte3 == 3) & (byte4 == 4)):
         break
   #
   # read and plot
   #
   up_low = ord(ser.read())
   up_high = ord(ser.read())
   down_low = ord(ser.read())
   down_high = ord(ser.read())
   up_value = 256*up_high + up_low
   down_value = 256*down_high + down_low
   value = (up_value - down_value)
   filt = (1-eps)*filt + eps*value
   x = int(.2*WINDOW + (.9-.2)*WINDOW*filt/10000.0)
   canvas.itemconfigure("text",text="%.1f"%filt)
   canvas.coords('rect1',.2*WINDOW,.05*WINDOW,x,.2*WINDOW)
   canvas.coords('rect2',x,.05*WINDOW,.9*WINDOW,.2*WINDOW)
   canvas.update()
   parent.after_idle(idle,parent,canvas)

#
#  check command line arguments
#
if (len(sys.argv) != 2):
   print "command line: hello.txrx.45.py serial_port"
   sys.exit()
port = sys.argv[1]
#
# open serial port
#
ser = serial.Serial(port,9600)
ser.setDTR()
#
# set up GUI
#
root = Tk()
root.title('hello.txrx.45.py (q to exit)')
root.bind('q','exit')
canvas = Canvas(root, width=WINDOW, height=.25*WINDOW, background='white')
#
canvas.create_text(.1*WINDOW,.125*WINDOW,text="1",font=("Helvetica", 24),tags="text",fill="#0000b0")
canvas.create_rectangle(.2*WINDOW,.05*WINDOW,.3*WINDOW,.2*WINDOW, tags='rect1', fill='#b00000')
canvas.create_rectangle(.3*WINDOW,.05*WINDOW,.9*WINDOW,.2*WINDOW, tags='rect2', fill='#0000b0')
canvas.pack()
#
# start idle loop
#
root.after(100,idle,root,canvas)
root.mainloop()
