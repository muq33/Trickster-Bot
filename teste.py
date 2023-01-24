import win32gui
import pygetwindow as gw
import time

def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))

def main():
    win32gui.EnumWindows(callback, None)

if __name__ == '__main__':
    #print(list(map(gw.getAllWindows(),)))
    #hwnd = gw.getAllWindows()[3]
    windows = gw.getAllWindows()
    win_titles = [win.title for win in windows]
    win_name = [title for title in win_titles if 'LifeTO' in title]
    win = win_name[0]
    a = win32gui.FindWindow(None,win)
    print(a)
    #win_titles = [win.title for win in windows]
    #win_name = [title for title in win_titles if name in title]
    time.sleep(2)
    rect = win32gui.GetWindowRect(a)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(a))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))