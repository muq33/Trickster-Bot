from sys import exit
from memory_manage import getPointerAddr
from character_functions import *
from pynput.keyboard import Key, Controller
import pyautogui as py
import pandas as pd
# import random


#import keyboard


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
if __name__ == '__main__':
    py.FAILSAFE = False
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetsx = [0x3B8, 0xF8, 0x258,0x678]
    offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
    offsetscmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]
    offsetsmax_mana = [0x1C, 0x60, 0x128, 0x4AC, 0x18C]
    offsetspeso = [0x1C, 0x174, 0x4B8, 0xF8, 0xC0]
    df = pd.read_csv('./routes/route_cerberus.csv')
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
                    if j == 0:
                        walke = walk_point(route, 300)
                    else:
                        walke = walk_point(route, 300, walke)
                    queue_start += 1
                    j+=1
                elif queue_start == 2:
                    skills = {'f1':'self-cast','f2':'self-cast'}
                    cast_skill(skills,1)
                    queue_start += 1
                    
                elif queue_start == 3:
                    verify_mana_level()
                    queue_start += 1
                    
                elif queue_start ==4:
                    verify_buffs((1,5))
                    queue_start += 1
                    
#                 elif queue_start == 5:
#                     get_item()
#                     queue_start += 1
#                 elif queue_start == 6:
#                     weight_test = verify_weigth()
#                     if weight_test == True:
#                         sell_items()
#                     queue_start+= 1
                        
            else:
                activate_window('LifeTO', False)

        else:
            print('Jogo não encontrado. Finalizando aplicação')
            exit()
    #activate_window('LifeTO(EN)', False)

