from pymem import *
from pymem.process import *
from sys import exit
from memory_manage import getPointerAddr
#from win32gui import MoveWindow, FindWindow, GetWindowText
from cv2 import moveWindow
import subprocess
import pyautogui as py
import time
import math
import pygetwindow as gw

#import keyboard



# mem = Pymem("Trickster.bin")
# module = module_from_name(mem.process_handle, "Trickster.bin").lpBaseOfDll
# offsetsx = [0x3B8, 0xF8, 0x258,0x678]
# offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
# offsetsmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]

# PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
# PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
# Mana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetsmana))
def verify_window(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())

def find_char():
    try:
        head_pos = py.locateOnScreen('headacess.png', confidence=0.9)
    except:
        head_pos = (py.size()[0]/2, py.size()[1]/2)
    return(head_pos)

#verify_window("Trickster.bin")
def walk(map_pos:tuple, desired_pos:tuple):#map_pos:tuple, desired_pos:tuple
    head_pos = find_char()
    char_screen_pos = (head_pos[0]+10,head_pos[1]+108)
    char_pos = map_pos
    py.moveTo(char_screen_pos)
    dist = math.dist(char_pos, desired_pos)
    if(dist > 250):
        if((desired_pos[0]-char_pos[0]) == 0):
            signal = (desired_pos[1]-char_pos[1])/(abs(desired_pos[1]-char_pos[1]))
            py.moveTo(char_screen_pos[0], char_screen_pos[1] - (250*(-signal)))
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
        else:
            signalx = (desired_pos[0]-char_pos[0])/(abs(desired_pos[0]-char_pos[0]))
            signaly = (desired_pos[1]-char_pos[1])/(abs(desired_pos[1]-char_pos[1]))
            theta = math.atan(((desired_pos[0]-char_pos[0])/(desired_pos[1]-char_pos[1])))
            incrementx = 250*math.sin(theta)*signaly
            incrementy = 250*math.cos(theta)*signaly
            py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
    else:
        increment_x = desired_pos[1]-char_pos[1]
        increment_y = desired_pos[0]-char_pos[0]
        py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
def centralize_window():
    
    win = gw.getWindowsWithTitle('LifeTO(EN) -  [v01072023v3]')[0]
    win.activate()
    return
centralize_window()
def bot():
    if(verify_window("Trickster.bin") == True):
        print(1)
    else:
        print("Jogo não encontrado. Finalizando aplicação")
        exit()

