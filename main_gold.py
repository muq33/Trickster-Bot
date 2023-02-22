from sys import exit
from memory_manage import getPointerAddr
from character_functions import *
import time
from pynput.keyboard import Key, Controller
import pyautogui as py
import pandas as pd



    
if __name__ == '__main__':
    py.FAILSAFE = False
    mem = Pymem('Trickster.bin')
    module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
    offsetsx = [0x3B8, 0xF8, 0x258,0x678]
    offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
    offsetscmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]
    offsetsmax_mana = [0x1C, 0x60, 0x128, 0x4AC, 0x18C]
    offsetspeso = [0x1C, 0x174, 0x4B8, 0xF8, 0xC0]
#     trickster_memory = storage(mem, offsetsx, offsetsy, offsetscmana,
#                                offsetsmax_mana, offsetspeso)
    df = pd.read_csv('./routes/route_gold.csv')
    route = df.values.tolist()
    i = 0
    j = 0
    queue_start = 1
    while True:
        if queue_start > 5:
            queue_start = 1
            window_open = identify('./resources/stuff/cross.jpg', 0.7)
            print(window_open)
            if  window_open != None:
                py.moveTo(window_open[0]+5,window_open[1]+5)
                py.mouseDown()
                time.sleep(0.25)
                py.mouseUp()
        if(verify_window('Trickster.bin') == True):
            if('LifeTO' in GetWindowText(GetForegroundWindow())):
                if queue_start == 1:
                    get_item()
                    if j == 0:
                        walke = walk_point(route, 300)
                    else:
                        walke = walk_point(route, 300, walke)
                    get_item()
                    queue_start += 1
                    j+=1
                elif queue_start == 2:
                    get_item()
                    skills = {'f1':'self-cast','f2':'self-cast'}
                    cast_skill(skills,(j%2)+1)
                    get_item()
                    queue_start += 1
                    
                elif queue_start == 3:
                    get_item()
                    verify_mana_level()
                    get_item()
                    queue_start += 1
                    
                elif queue_start ==4:
                    get_item()
                    verify_buffs((1,4))
                    get_item()
                    queue_start += 1
                    
                elif queue_start == 5:
                    weight_test = verify_weigth()
                    if weight_test == True:
                        sell_items()
                    queue_start+= 1
                        
            else:
                activate_window('LifeTO', False)

        else:
            print('Jogo não encontrado. Finalizando aplicação')
            exit()
    #activate_window('LifeTO(EN)', False)

