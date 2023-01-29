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






def verify_window(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())

def find_char():
    window_location = get_window_sizepos(activate_window('LifeTO', True))
    head_pos = py.locateOnScreen('./resources/headacess.png', confidence=0.9 , region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
    if head_pos == None:
        pos = get_window_sizepos(activate_window('LifeTO', True))
        
        head_pos = (pos[0][0] + pos[1][0]/2,pos[0][1] + pos[1][1]/2 )
        return(head_pos)
    else:
        head_pos = (head_pos[0]+10,head_pos[1]+108)
        return(head_pos)
    
def verify_buffs(buffs_index:tuple):
    keyboard = Controller()
    window_location = get_window_sizepos(activate_window('LifeTO', True))
    for i in range(buffs_index[0] ,buffs_index[1]+1):
        buff_pos = py.locateOnScreen('./resources/buffs/buff{}.png'.format(i), confidence=0.8, region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
        if(buff_pos == None):
            keyboard.press('2')
            time.sleep(0.4)
            keyboard.release('2')
            buff_pos2 = py.locateOnScreen('./resources/buffs/buff{}.png'.format(i), confidence=0.8, region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
            if buff_pos2 == None:
                return
            else:
                py.moveTo(buff_pos2[0], buff_pos2[1])
                py.doubleClick(interval=0.1)
                time.sleep(0.4)
                keyboard.press('1')
                time.sleep(0.2)
                keyboard.release('1')
                time.sleep(0.2)
    return

def get_item(item_range = 11):
    keyboard = Controller()
    window_location = get_window_sizepos(activate_window('LifeTO', True))
    for i in range(1, item_range+1):
        item_pos = py.locateOnScreen('./resources/equipments/e{}.png'.format(i), confidence=0.65, region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
        if(item_pos != None):
            py.moveTo(item_pos[0], item_pos[1])
            py.mouseDown()
            time.sleep(0.2)
            py.mouseUp()
            time.sleep(1)

def cast_skill(keys_to_press:dict, which_to_cast:int):# {key: type} ----> {'f5': 'region', 'f3': 'self-cast'}
    keyboard = Controller()
    buttons = list(keys_to_press.keys())
    types = list(keys_to_press.values())
    interval1 = 0.2
    keyboard.press('1')
    time.sleep(interval1)
    keyboard.release('1')
    if types[which_to_cast-1] == 'region':
        head_pos = find_char()
        incrementx = random.randint(-70,70)
        incrementy = random.randint(-70,70)
        py.moveTo(head_pos [0] + incrementx, head_pos[1] + incrementy)
        eval('keyboard.press(Key.{})'.format(buttons[which_to_cast-1]))
        time.sleep(interval1 + 0.1)
        eval('keyboard.release(Key.{})'.format(buttons[which_to_cast-1]))
        py.mouseDown()
        time.sleep(0.2)
        py.mouseUp()
        time.sleep(interval1 * 6)
    elif types[which_to_cast-1] == 'self-cast':
        eval('keyboard.press(Key.{})'.format(buttons[which_to_cast-1]))
        time.sleep(interval1 + 0.1)
        eval('keyboard.release(Key.{})'.format(buttons[which_to_cast-1]))
        time.sleep(interval1 + 0.2)
    else:
        return
#     if skill_index == 1:
#         keyboard.press('1')
#         time.sleep(0.4)
#         keyboard.release('1')
#         head_pos = find_char()
#         char_screen_pos = head_pos
#         incrementx = random.randint(-70,70)
#         incrementy = random.randint(-70,70)
#         py.moveTo(char_screen_pos)
#         keyboard.press(Key.f3)
#         time.sleep(0.3)
#         keyboard.release(Key.f3)
#         py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
#         py.mouseDown()
#         time.sleep(0.2)
#         py.mouseUp()
#         time.sleep(2)
#         return
#     else:
#         keyboard.press(Key.f4)
#         time.sleep(0.3)
#         keyboard.release(Key.f4)
#         return
    
def walk(map_pos:tuple, desired_pos:tuple, memory_distance = 25, precision = 250):#map_pos:tuple, desired_pos:tuple
    head_pos = find_char()
    char_screen_pos = (head_pos[0]+10,head_pos[1]+108)
    char_pos = map_pos
    py.moveTo(char_screen_pos)
    dist = math.dist(char_pos, desired_pos)
    interval = 0.5
    if(dist > precision and memory_distance > 20):
        if((desired_pos[1]-char_pos[1]) == 0):
            incrementx = desired_pos[0]-char_pos[0]
            py.moveTo(char_screen_pos[0]+incrementx, char_screen_pos[1])
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
            time.sleep(interval)
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)),
                         mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
        
        elif((desired_pos[0]-char_pos[0]) == 0):
            incrementy = desired_pos[1]-char_pos[1]
            py.moveTo(char_screen_pos[0], char_screen_pos[1]+incrementy)
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
            time.sleep(interval)
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)),
                         mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
            
        else:
            signalx = (desired_pos[0]-char_pos[0])/(abs(desired_pos[0]-char_pos[0]))
            signaly = (desired_pos[1]-char_pos[1])/(abs(desired_pos[1]-char_pos[1]))
            theta = math.atan(((desired_pos[0]-char_pos[0])/(desired_pos[1]-char_pos[1])))
            incrementx = 210*math.sin(theta)*signaly
            incrementy = 210*math.cos(theta)*signaly
            py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
            time.sleep(interval)
            char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)),
                         mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
            return(False, math.dist(char_pos, char_pos2))
    elif memory_distance < 20:
        random_walkx = random.sample([-1,1],1)
        random_walky = random.sample([-1,1],1)
        py.moveTo(char_screen_pos[0] + 150*random_walkx[0], char_screen_pos[1] + 150*random_walky[0])
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
        time.sleep(interval)
        char_pos2 = (mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx)),
                     mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy)))
        return(False, math.dist(char_pos, char_pos2))
    else:
        incrementx = desired_pos[0]-char_pos[0]
        incrementy = desired_pos[1]-char_pos[1]
        py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
        time.sleep(interval/2)
        return(True, 25)
        
        
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

def verify_weight():
    cur_weigth = mem.read_int(getPointerAddr(mem,module + 0x0088A4C4, offsetspeso))
    if cur_weigth > 85:
        return True
    else:
        return False
    
            
def sell_items():
    window_location = get_window_sizepos(activate_window('LifeTO', True))
    portal_pos = py.locateOnScreen('./resources/map_features/portal.png', confidence=0.65, region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
    if(portal_pos != None):
        py.moveTo(portal_pos[0], portal_pos[1])
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
        keyboard = Controller()
        keyboard.press('i')
        time.sleep(0.1)
        keyboard.release('i')
        teleporter_pos = py.locateOnScreen('./resources/teleporter.png', confidence=0.75, region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
        if teleporter_pos != None:
            py.moveTo(teleporter_pos[0], teleporter_pos[1])
            py.mouseDown()
            time.sleep(0.1)
            py.mouseUp()
    
    
    
if __name__ == '__main__':
    py.FAILSAFE = False
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetsx = [0x3B8, 0xF8, 0x258,0x678]
    offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
    offsetscmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]
    offsetsmax_mana = [0x1C, 0x60, 0x128, 0x4AC, 0x18C]
    offsetspeso = [0x1C, 0x174, 0x4B8, 0xF8, 0xC0]
    df = pd.read_csv('./routes/route.csv')
    route = df.values.tolist()
    i = 0
    j = 0
    queue_start = 1
    while True:
        if queue_start > 5:
            queue_start = 1
        if(verify_window('Trickster.bin') == True):
            if('LifeTO' in GetWindowText(GetForegroundWindow())):
                if queue_start == 1:
                    p=True
                    while p == True:
                        PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
                        PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
                        activate_window('LifeTO', False)
                        if j == 0:
                            walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), 0)
                        else:
                            walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), walk_action[1]) 
                        
                        time.sleep(0.4)
                        j+=1
                        
                        
                        if walk_action[0] == True:
                            if(i >= len(route)-1):
                                i = 0
                            else:
                                i += 1
                            queue_start += 1
                            p = False
                        
                elif queue_start == 2:
                    skills = {'f3':'region', 'f4':'self-cast'}
                    cast_skill(skills,(j % 2) +1)
                    queue_start += 1
                    
                elif queue_start == 3:
                    CMana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetscmana))
                    Max_Mana = mem.read_int(getPointerAddr(mem,module + 0x0088A4C4, offsetsmax_mana))
                    verify_mana_level(CMana,Max_Mana)
                    queue_start += 1
                    
                elif queue_start ==4:
                    verify_buffs((1,2))
                    queue_start += 1
                    
                elif queue_start == 5:
                    get_item()
                    queue_start += 1
#                 elif queue_start == 6:
#                     weight_test = verify_weigth()
#                     if weighth_test == True:
                        
            else:
                activate_window('LifeTO', False)

        else:
            print('Jogo não encontrado. Finalizando aplicação')
            exit()
    #activate_window('LifeTO(EN)', False)

