import win32gui
import pygetwindow as gw
import time
import pandas as pd
from pynput.keyboard import Key, Controller
from memory_manage import getPointerAddr
from pymem import *
from pymem.process import *
from main import *
# mem = Pymem('Trickster.bin')
# module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
# columns = ['X','Y']
# positions = []

# offsetsmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]
# CMana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetsmana))
# print(CMana)
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
time.sleep(2)
buff_pos = sell_items()
print(buff_pos)