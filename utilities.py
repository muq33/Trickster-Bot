def verify_window(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())
def find_char():
    head_pos = py.locateOnScreen('headacess.png', confidence=0.9)
    if head_pos == None:
        pos = get_window_sizepos(activate_window('LifeTO', True))
        head_pos = (pos[0][0] + pos[1][0]/2,pos[0][1] + pos[1][1]/2 )
        return(head_pos)
    else:
        return(head_pos)

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
        incrementx = desired_pos[0]-char_pos[0]
        incrementy = desired_pos[1]-char_pos[1]
        py.moveTo(char_screen_pos[0] + incrementx, char_screen_pos[1] + incrementy)
        py.mouseDown()
        time.sleep(0.1)
        py.mouseUp()
        
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