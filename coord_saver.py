import keyboard
from memory_manage import getPointerAddr

positions = []
mem = Pymem('Trickster.bin')
module = module_from_name(mem.process_handle, 'Trickster.bin').lpBaseOfDll
offsetsx = [0x3B8, 0xF8, 0x258,0x678]
offsetsy = [0x3F0, 0x470, 0x1EC, 0x110, 0x67C]
offsetsmana = [0x78, 0x6E4, 0x1B4, 0xB8, 0x1DC]

PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
while True:  # making a loop
    if keyboard.is_pressed('t'):  # if key 'q' is pressed 
        positions.append((PosX,PosY))
    elif keboard.is_pressed('q'):
        with open("./", 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(mylist)
        break
