import win32gui
import win32api
import win32con
import time


EMPTY_INV_SLOT_1 = 3489865
INV_SLOT_1_X = 708
INV_SLOT_1_Y = 260

TIN_ROCK = 7698050
IRON_ROCK = (790818,1252150,1120818,1318457,1452861,1449789,792866)
MINED_ROCK = 1516096

MINE_X = 383
MINE_Y = 172

MINE_X2 = 357
MINE_Y2 = 203

RED_COMPASS_TIP = 723587
COMPASS_NORTH_X = 691
COMPASS_NORTH_Y = 45

#RED at 691,45 means pointing north



class Window:

    def __init__(self):
        self.osrs_window_id = win32gui.FindWindow(0, "Old School RuneScape")
        if self.osrs_window_id is None:
            raise Exception("Could not find OSRS window")
        win32gui.MoveWindow(self.osrs_window_id, 0, 0, 1024, 768, True)
        self.osrs_window = win32gui.GetWindowDC(self.osrs_window_id)
        self.align_window()
    
    def reinitialize(self):
        self.osrs_window = win32gui.GetWindowDC(self.osrs_window_id)

    def align_window(self):
        win32api.SetCursorPos((COMPASS_NORTH_X, COMPASS_NORTH_Y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,COMPASS_NORTH_X, COMPASS_NORTH_Y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,COMPASS_NORTH_X, COMPASS_NORTH_Y,0,0)

        win32api.keybd_event(win32con.VK_UP, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0) #press
        win32api.Sleep(1000)
        win32api.keybd_event(win32con.VK_UP, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0) #release

class Spot:

    def __init__(self, active_colours, x, y, window):
        self.active_colours = active_colours
        self.x = x
        self.y = y
        self.window = window
        self.active = self.poll_status()

    def poll_status(self):
        colour = win32gui.GetPixel(self.window.osrs_window, self.x, self.y)
        self.window.reinitialize()

        colour = int(colour)
        if self.is_active_colour(colour):
            self.active = True
        else:
            self.active = False
        
        return self.active

    def is_active_colour(self, colour):
        if colour in self.active_colours:
            return True
        print('inactive colour: ' + format_to_RGB_string(colour))
        print('int colour: ' + str(colour))
        print('x: ' + str(self.x) + ", y: " + str(self.y))
        return False

def format_to_RGB_string(int_colour):
    return (str(int_colour & 0xff) + " " + str((int_colour >> 8) & 0xff) + " " + str((int_colour >> 16) & 0xff))

def main():
    bot_window = Window()
    bot_window.reinitialize()
    colour = win32gui.GetPixel(bot_window.osrs_window, MINE_X, MINE_Y)
    bot_window.reinitialize()

    int_colour = int(colour)
    print(int_colour)
    print(format_to_RGB_string(int_colour))
    win32api.SetCursorPos((MINE_X, MINE_Y))
    
    mining = False
    mining_spots = [Spot(IRON_ROCK, MINE_X, MINE_Y, bot_window), Spot(IRON_ROCK, MINE_X2, MINE_Y2, bot_window)]
    current_spot = None

    while(True):

        if current_spot !=None:
            #look at current rock
            if not current_spot.poll_status():
                mining = False

        if not mining:

            #look at bag
            colour = win32gui.GetPixel(bot_window.osrs_window, INV_SLOT_1_X, INV_SLOT_1_Y)
            bot_window.reinitialize()
            colour = int(colour)

            if colour != EMPTY_INV_SLOT_1:
                #drop rock
                win32api.SetCursorPos((INV_SLOT_1_X,INV_SLOT_1_Y))
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,INV_SLOT_1_X,INV_SLOT_1_Y,0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,INV_SLOT_1_X,INV_SLOT_1_Y,0,0)

                win32api.SetCursorPos((INV_SLOT_1_X,INV_SLOT_1_Y+40))
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,INV_SLOT_1_X,INV_SLOT_1_Y+40,0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,INV_SLOT_1_X,INV_SLOT_1_Y+40,0,0)
                
            #look for available rock and start mining it
            
            for spot in mining_spots:
                if spot.poll_status():
                    current_spot = spot
                    win32api.SetCursorPos((current_spot.x,current_spot.y))
                    time.sleep(0.1)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,current_spot.x,current_spot.y,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,current_spot.x,current_spot.y,0,0)
                    mining = True
                    break
        
        time.sleep(0.5)

if __name__ == '__main__':
    main()