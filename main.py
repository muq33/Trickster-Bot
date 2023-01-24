from pymem import *
from pymem.process import *
from sys import exit
from memory_manage import getPointerAddr
from win32gui import GetWindowText, GetForegroundWindow, FindWindow, GetWindowRect
from utilities import *
import pyautogui as py
import time
import math
import pygetwindow as gw
import pandas as pd
import random


#import keyboard



mem = Pymem('Trickster.bin')
module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
offsetsx = [0x3B8, 0xF8, 0x258,0x678]
offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
offsetsmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]

# PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
# PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
# Mana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetsmana))
def verify_window(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())
def find_char():
    head_pos = py.locateOnScreen('./resources/headacess.png', confidence=0.9)
    if head_pos == None:
        pos = get_window_sizepos(activate_window('LifeTO', True))
        head_pos = (pos[0][0] + pos[1][0]/2,pos[0][1] + pos[1][1]/2 )
        return(head_pos)
    else:
        return(head_pos)

def walk(map_pos:tuple, desired_pos:tuple, memory_distance = 0):#map_pos:tuple, desired_pos:tuple
    head_pos = find_char()
    char_screen_pos = (head_pos[0]+10,head_pos[1]+108)
    char_pos = map_pos
    py.moveTo(char_screen_pos)
    dist = math.dist(char_pos, desired_pos)
    if(dist > 250 and memory_distance > 20):
        if((desired_pos[1]-char_pos[1]) == 0):
            incrementx = desired_pos[0]-char_pos[0]
            #signal = (desired_pos[1]-char_pos[1])/(abs(desired_pos[1]-char_pos[1]))
            
            py.moveTo(char_screen_pos[0]+incrementx, char_screen_pos[1])
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
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
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
    elif memory_distance < 20:
        random_walkx = random.sample([-1,1],1)
        random_walky = random.sample([-1,1],1)
        py.moveTo(char_screen_pos[0] + 100*random_walkx[0], char_screen_pos[1] + 100*random_walky[0])
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
        char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
        return(False, math.dist(char_pos, char_pos2))
    else:
        incrementx = desired_pos[0]-char_pos[0]
        incrementy = desired_pos[1]-char_pos[1]
        py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
        char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
        return(True, math.dist(char_pos, char_pos2))
        
        
def get_window_sizepos(window_name):
    win_handle = FindWindow(None,window_name)
    rect = GetWindowRect(win_handle)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    return((x,y),(w,h))

def activate_window(name,args:bool):
    if(args == True):
        windows = gw.getAllWindows()
        win_titles = [win.title for win in windows]
        win_name = [title for title in win_titles if name in title]
        return(win_name[0])
    else:
        windows = gw.getAllWindows()
        win_titles = [win.title for win in windows]
        win_name = [title for title in win_titles if name in title]
        win = gw.getWindowsWithTitle(win_name[0])[0]
        win.activate()
def bot():
    if(verify_window('Trickster.bin') == True):
        if('LifeTO' in GetWindowText(GetForegroundWindow())):
            print(get_window_sizepos(activate_window('LifeTO',True)))
        else:
            activate_window('LifeTO', False)
            bot()
    else:
        print('Jogo não encontrado. Finalizando aplicação')
        exit()
#bot()
if __name__ == '__main__':
    df = pd.read_csv('./routes/route.csv')
    df2 = df.values.tolist()
    #print(df[0])
    time.sleep(2)
    i = 0
    j = 0
#     walk((PosX, PosY),(df2[i][0],df2[i][1]))
    while True:
        PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
        PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
        Mana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetsmana))
        if j == 0:
            a = walk((PosX, PosY),(df2[i][0],df2[i][1]), 0)
        else:
            print(a[1])
            a = walk((PosX, PosY),(df2[i][0],df2[i][1]), a[1])
        
        j+=1
        if a[0] == True:
            i += 1
        if(i == len(df2)):
            break
#     for i in	 range(len(df2)):
#         a = walk((PosX, PosY),(df2[i][0],df2[i][1]))
#         print(a)
#         if a == False:
#             i-=1
#             print(i)
    #print(list(df.loc[:,["X","Y"]]))
    #print(list())

