from pymem import *
from pymem.process import *
from window_functions import *
from memory_manage import getPointerAddr
from pynput.keyboard import Key, Controller
from main import *
import cv2 as cv2
import numpy as np
import pygetwindow as gw
import pyautogui as py
import math
import random
import time

def use_memory_port(pos:int):
    keyboard = Controller()
    inv_ref = identify('./resources/stuff/inv_ref.jpg',  0.65)
    if inv_ref == None:
        keyboard.press('i')
        time.sleep(0.3)
        keyboard.release('i')
        time.sleep(0.3)
        inv_ref = identify('./resources/stuff/inv_ref.jpg',  0.65)
    
    py.moveTo(inv_ref[0]+45, inv_ref[1]+25)
    py.mouseDown()
    time.sleep(0.25)
    py.mouseUp()
    port = identify('./resources/stuff/Memory_Port.gif',0.75, iter = 3)
    py.moveTo(port)
    py.doubleClick()
    time.sleep(0.3)
    port2 = identify('./resources/stuff/memory_port.jpg',  0.65, iter = 2)
    py.moveTo(port2[0]+10, port2[1]-(pos*40))
    py.mouseDown()
    time.sleep(0.25)
    py.mouseUp()
    py.moveTo(port2[0]+145, port2[1])
    py.mouseDown()
    time.sleep(0.25)
    py.mouseUp()
    time.sleep(6)
    keyboard.press('i')
    time.sleep(0.3)
    keyboard.release('i')
def identify(template:str, min_confidence, show_result = 0, iter = 1):
    #Take screenshot
    i = 0
    cap = cv2.VideoCapture(template)
    ret, template = cap.read()
    cap.release()
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    while i < iter:
#         window_location = get_window_sizepos(activate_window('LifeTO', True))
        screenshot = py.screenshot()
#         screenshot = screenshot.crop((window_location[0][0],window_location[0][1],
#                                        window_location[0][0]+window_location[1][0], window_location[0][1]+window_location[1][1]))
#         Convert the screenshot to a numpy array
        screenshot = np.array(screenshot)
        
        #Convert screenshot to grayscale
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = min_confidence

        # Threshold the result
        loc = np.where(res >= threshold)
        if show_result == 1:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(screenshot, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0,0,255), 2)
            # Show the result
            cv2.imshow("Faces", screenshot)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        if len(loc[0]) > 0:
            return(loc[1][0], loc[0][0])
        else:
            i+=1
    if i > iter:
        return(None)
def walk(map_pos:tuple, desired_pos:tuple, memory_distance = 25, precision = 250):#map_pos:tuple, desired_pos:tuple
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetsx = [0x3B8, 0xF8, 0x258,0x678]
    offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
    head_pos = find_char()
    char_screen_pos = (head_pos[0]+10,head_pos[1]+108)
    char_pos = map_pos
    py.moveTo(char_screen_pos)
    dist = math.dist(char_pos, desired_pos)
    interval = 0.4
    if(dist > precision and memory_distance > 20):
        if((desired_pos[1]-char_pos[1]) == 0):
            incrementx = desired_pos[0]-char_pos[0]
            py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1])
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
            incrementx = 190*math.sin(theta)*signaly
            incrementy = 190*math.cos(theta)*signaly
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

def get_item(item_range = 3):
    window_location = get_window_sizepos(activate_window('LifeTO', True))
#     i = 0
#     item_pos = identify('./resources/equipments/e{}.gif'.format(i), 0.7)
#     while True:
#         item_pos2 = identify('./resources/equipments/e{}.gif'.format(i), 0.7)
#         if len(item_pos2) > len(item_pos):
#             item_pos = item_pos2
#         elif item_pos2 == None:
#             False
#         for i in range(0,
#         if item_pos != None:
#             py.moveTo(item_pos[0]+10, item_pos[1]+15)
#             py.mouseDown()
#             time.sleep(0.25)
#             py.mouseUp()
#             time.sleep(0.8)
#         
#         i += 1
    
    
    for i in range(0, item_range+1):
        while identify('./resources/equipments/e{}.gif'.format(i), 0.7) != None:
            print('item {} encontrado'.format(i)) 
            item_pos = identify('./resources/equipments/e{}.gif'.format(i), 0.6)
            if item_pos != None:
                py.moveTo(item_pos[0]+10, item_pos[1]+15)
                py.mouseDown()
                time.sleep(0.25)
                py.mouseUp()
                time.sleep(0.8)
            
def verify_buffs(buffs_index:tuple):
    keyboard = Controller()
    window_location = get_window_sizepos(activate_window('LifeTO', True))
    for i in buffs_index:
        buff_pos = py.locateOnScreen('./resources/buffs/buff{}.png'.format(i), confidence=0.8, region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
        if(buff_pos == None):
            keyboard.press('2')
            time.sleep(0.3)
            keyboard.release('2')
            
            buff_pos2 = py.locateOnScreen('./resources/buffs/buff{}.png'.format(i), confidence=0.65, region=(window_location[0][0],
                                                                                                         window_location[0][1],
                                                                                                         window_location[0][0] + window_location[1][0],
                                                                                                         window_location[0][1] + window_location[1][1]))
            if buff_pos2 != None:
                py.moveTo(buff_pos2[0], buff_pos2[1])
                py.doubleClick(interval=0.1)
                time.sleep(0.4)
                keyboard.press('1')
                time.sleep(0.2)
                keyboard.release('1')
                time.sleep(0.2)
            keyboard.press('1')
            time.sleep(0.4)
            keyboard.release('1')


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
        head_pos = (head_pos[0]+10,head_pos[1])
        return(head_pos)
    
def walk_point(route:tuple, precision = 250, i = 0, j = 0):
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetsx = [0x3B8, 0xF8, 0x258,0x678]
    offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
    p = True
    while p == True:
        PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
        PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
        activate_window('LifeTO', False)
        
        if j == 0:
            walk_action = walk((PosX, PosY),(route[i][0], route[i][1]), 0, precision)
        else:
            walk_action = walk((PosX, PosY),(route[i][0], route[i][1]), walk_action[1], precision)
        j += 1
        if walk_action[0] == True:
            if(i >= len(route)-1):
                i = 0
            else:
                i += 1
            return(i)
        
def verify_weigth():
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetspeso = [0x1C, 0x174, 0x4B8, 0xF8, 0xC0]
    cur_weigth = mem.read_int(getPointerAddr(mem,module + 0x0088A4C4, offsetspeso))
    if cur_weigth > 85:
        return True
    else:
        return False
    
def verify_mana_level():
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetscmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]
    offsetsmax_mana = [0x1C, 0x60, 0x128, 0x4AC, 0x18C]
    CMana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetscmana))
    Max_Mana = mem.read_int(getPointerAddr(mem,module + 0x0088A4C4, offsetsmax_mana))
    if(CMana/Max_Mana < 0.6):
        keyboard = Controller()
        keyboard.press(Key.f5)
        time.sleep(0.2)
        keyboard.release(Key.f5)
        time.sleep(0.2)
        keyboard.press(Key.f4)
        time.sleep(0.3)
        keyboard.release(Key.f4)
    return
def sell_items():
    #Routes
#     path_to_portal = pd.read_csv('./routes/path_to_portal.csv')
#     path_to_portal = path_to_portal.values.tolist()
#     portal_to_vendor = pd.read_csv('./routes/portal_to_vendor.csv')
#     portal_to_vendor = portal_to_vendor.values.tolist()
#     vendor_to_portal = pd.read_csv('./routes/vendor_to_portal.csv')
#     vendor_to_portal = vendor_to_portal.values.tolist()
#     
    window_location = get_window_sizepos(activate_window('LifeTO', True))
    use_memory_port(2)
#     portal_pos1 = identify("./resources/map_features/pilar1.jpg", 0.65)
#     py.moveTo(portal_pos1[0]+250, portal_pos1[1]+60)
#     py.mouseDown()
#     time.sleep(0.15)
#     py.mouseUp()
#     time.sleep(1.5)
#     walk_point(portal_to_vendor, 150)
    vendor_pos = identify("./resources/npcs/vendor_path_to_caballa.jpg",  0.55, iter = 3)
    py.moveTo(vendor_pos[0]+50,vendor_pos[1]+80)
    py.mouseDown()
    time.sleep(0.25)
    py.mouseUp()
    time.sleep(0.5)
    py.moveTo(window_location[0][0]+71, window_location[0][1]+440)
    py.mouseDown()
    time.sleep(0.15)
    py.mouseUp()
    time.sleep(1)
    equip = py.locateOnScreen('./resources/stuff/equip_sell_window.jpg', confidence = 0.75)
    py.moveTo(equip[0]+50,equip[1]+15)
    py.mouseDown()
    time.sleep(0.15)
    py.mouseUp()
    
    i = True
    while i == True:
        sell_count = py.locateAllOnScreen('./resources/stuff/sell_count.jpg', confidence = 0.80)
        sell_count_list = list(sell_count)
        print(sell_count_list)
        for pos in sell_count_list:
            py.moveTo(pos[0]+45, pos[1]+10)
            py.mouseDown()
            time.sleep(0.15)
            py.mouseUp()
        sell_button = identify("./resources/stuff/sell_button.jpg",  0.75)
        py.moveTo(sell_button)
        py.mouseDown()
        time.sleep(0.25)
        py.mouseUp()
        if sell_count_list == []:
            i = False
    time.sleep(0.6)
    use_button = identify("./resources/stuff/sell_final.jpg",  0.85)

    py.moveTo(use_button[0]+10, use_button[1]+15)
    py.mouseDown()
    time.sleep(0.25)
    py.mouseUp()
    py.moveTo(window_location[1][0] - 50,window_location[1][1] - 50)
    py.mouseDown()
    time.sleep(0.25)
    py.mouseUp()
    use_memory_port(3)

#     walk_point(vendor_to_portal)
#     portal_pos2 = identify("./resources/map_features/pilar2.jpg",  0.65)
#     py.moveTo(portal_pos2[0]-230, portal_pos2[1]+75)
#     py.mouseDown()
#     time.sleep(0.25)
#     py.mouseUp()
#     time.sleep(1.5)