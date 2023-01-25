from pymem import *
from pymem.process import *
from sys import exit
from memory_manage import getPointerAddr
from win32gui import GetWindowText, GetForegroundWindow, FindWindow, GetWindowRect
from utilities import *
from pynput.keyboard import Key, Controller
import pygetwindow as gw
import subprocess
import pyautogui as py
import time
import math
import pygetwindow as gw
import pandas as pd
import random


#import keyboard





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
    
def verify_buffs(buffs_index:int):
    keyboard = Controller()
    for i in range(1,buffs_index+1):
        buff_pos = py.locateOnScreen('./resources/buffs/buff{}.png'.format(i), confidence=0.9)
        if(buff_pos == None):
            keyboard.press('2')
            time.sleep(0.2)
            keyboard.release('2')
            buff_pos = py.locateOnScreen('./resources/buffs/buff{}.png'.format(i), confidence=0.9)
            py.moveTo(buff_pos[0], buff_pos[1])
            py.doubleClick(interval=0.1)
            time.sleep(0.4)
            keyboard.press('1')
            time.sleep(0.2)
            keyboard.release('1')
            time.sleep(0.2)
            
def cast_skill(skill_index = 1):
    keyboard = Controller()
    if skill_index == 1:
        head_pos = find_char()
        char_screen_pos = (head_pos[0]+10,head_pos[1]+108)
        incrementx = random.randint(-100,100)
        incrementy = random.randint(-100,100)
        py.moveTo(char_screen_pos)
        keyboard.press(Key.f3)
        time.sleep(0.3)
        keyboard.release(Key.f3)
        py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
        py.mouseDown()
        time.sleep(0.2)
        py.mouseUp()
        return
    else:
        keyboard.press(Key.f4)
        time.sleep(0.3)
        keyboard.release(Key.f4)
        return
    
def walk(map_pos:tuple, desired_pos:tuple, memory_distance = 0):#map_pos:tuple, desired_pos:tuple
    head_pos = find_char()
    char_screen_pos = (head_pos[0]+10,head_pos[1]+108)
    char_pos = map_pos
    py.moveTo(char_screen_pos)
    dist = math.dist(char_pos, desired_pos)
    if(dist > 40 and memory_distance > 3):
        print("a distancia é: {}".format(dist))
        if((desired_pos[1]-char_pos[1]) == 0):
            incrementx = desired_pos[0]-char_pos[0]
            py.moveTo(char_screen_pos[0]+incrementx, char_screen_pos[1])
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
            time.sleep(1)
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
        
        elif((desired_pos[0]-char_pos[0]) == 0):
            incrementy = desired_pos[1]-char_pos[1]
            py.moveTo(char_screen_pos[0], char_screen_pos[1]+incrementy)
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
            time.sleep(1)
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
            
        else:
            signalx = (desired_pos[0]-char_pos[0])/(abs(desired_pos[0]-char_pos[0]))
            signaly = (desired_pos[1]-char_pos[1])/(abs(desired_pos[1]-char_pos[1]))
            theta = math.atan(((desired_pos[0]-char_pos[0])/(desired_pos[1]-char_pos[1])))
            incrementx = 230*math.sin(theta)*signaly
            incrementy = 230*math.cos(theta)*signaly
            py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
            time.sleep(1)
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
    elif memory_distance < 3:
        random_walkx = random.sample([-1,1],1)
        random_walky = random.sample([-1,1],1)
        py.moveTo(char_screen_pos[0] + 100*random_walkx[0], char_screen_pos[1] + 100*random_walky[0])
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
        time.sleep(1)
        char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)), mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
        return(False, math.dist(char_pos, char_pos2))
    else:
        return(True, 4)
        
        
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

def verify_mana_level(current_mana, max_mana):
    if(current_mana/max_mana < 0.6):
        keyboard = Controller()
        keyboard.press(Key.f5)
        time.sleep(0.1)
        keyboard.release(Key.f5)
    return

def bot(queue_start:int, route:list, **kwargs):
    i = list(kwargs.values())[0]
    j = list(kwargs.values())[1]
    if queue_start > 3:
        queue_start = 1
    if(verify_window('Trickster.bin') == True):
        if('LifeTO' in GetWindowText(GetForegroundWindow())):
            if queue_start == 1:
                PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
                PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
                global walk_action
                if j == 0:
                    walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), 0)
                else:
                    print(walk_action[1])
                    walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), walk_action[1]) 
                j+=1
                time.sleep(0.4)
                
                if walk_action[0] == True:
                    i += 1
                if(i == len(route)):
                    print("resetou")
                    i = 0
                bot(queue_start + 1,route, k=i, p=j)
#             elif queue_start == 2:
#                 cast_skill(j % 2)
#                 time.sleep(2.5)
                bot(queue_start + 1,route, k=i, p=j)
                
            elif queue_start == 3:
                CMana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetscmana))
                Max_Mana = mem.read_int(getPointerAddr(mem,module + 0x0088A4C4, offsetsmax_mana))
                print(Max_Mana, CMana)
                verify_mana_level(j,Max_Mana)
                bot(queue_start +1,route, k=i, p= j)
            else:
                bot(queue_start +1,route, k=i, p= j)
        else:
            activate_window('LifeTO', False)
            bot(queue_start,route, k=i, p=j)

    else:
        print('Jogo não encontrado. Finalizando aplicação')
        exit()

if __name__ == '__main__':
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetsx = [0x3B8, 0xF8, 0x258,0x678]
    offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
    offsetscmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]
    offsetsmax_mana = [0x1C, 0x60, 0x128, 0x4AC, 0x18C]
    df = pd.read_csv('./routes/route.csv')
    route = df.values.tolist()
    i = 0
    j = 0
    queue_start = 1
    while True:
        if queue_start > 4:
            queue_start = 1
        if(verify_window('Trickster.bin') == True):
            if('LifeTO' in GetWindowText(GetForegroundWindow())):
                if queue_start == 1:
                    PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
                    PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
                    if j == 0:
                        walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), 0)
                    else:
                        print(walk_action[1])
                        walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), walk_action[1]) 
                    j+=1
                    time.sleep(0.4)
                    
                    if walk_action[0] == True:
                        i += 1
                    if(i == len(route)):
                        print("resetou")
                        i = 0
                    
                    queue_start += 1
                    
                elif queue_start == 2:
                    cast_skill(j % 2)
                    time.sleep(2.5)
                    queue_start += 1
                    
                elif queue_start == 3:
                    CMana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetscmana))
                    Max_Mana = mem.read_int(getPointerAddr(mem,module + 0x0088A4C4, offsetsmax_mana))
                    verify_mana_level(CMana,Max_Mana)
                    queue_start += 1
                    
                elif queue_start ==4:
                    verify_buffs(2)
                    queue_start += 1
            else:
                activate_window('LifeTO', False)

        else:
            print('Jogo não encontrado. Finalizando aplicação')
            exit()
    #activate_window('LifeTO(EN)', False)

