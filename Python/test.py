import numpy as np
import cv2
import pyautogui
from PIL import ImageOps, Image
import win32gui
import win32ui
import win32con
import win32api
import time
import random

img1 = cv2.imread('S1.png', cv2.IMREAD_UNCHANGED) #36 - olo
#img2 = cv2.imread('S3.png', cv2.IMREAD_UNCHANGED) 

# chunk = 1110241
# p = pyaudio.PyAudio()

hwnd = 0
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()
saveBitMap = win32ui.CreateBitmap()
MoniterDev = win32api.EnumDisplayMonitors(None, None)
w = 850
h = 650

saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
saveDC.SelectObject(saveBitMap)
ttk=0
tic = time.perf_counter()
tiic = time.perf_counter()
while True:
    toc = time.perf_counter()
    if toc-tiic >= 600:
        # with pyautogui.hold('down'):
        #     time.sleep(0.2)
        # time.sleep(1)
        pyautogui.typewrite(['space'])
        time.sleep(2)
        # with pyautogui.hold('up'):
        #     time.sleep(0.11)
        # time.sleep(0.2)
        pyautogui.press('2')
        time.sleep(4)
        tiic = toc
    if toc-tic >= random.randint(140, 360):
        tic = toc
        pyautogui.typewrite(['space'])
        time.sleep(1)
    pyautogui.moveTo(random.randint(1, 15), random.randint(1, 15), 0.12)
    time.sleep(1)
    pyautogui.press('1')
    ttk=6
    time.sleep(8.5)
    while ttk > 0:
        ttk -= 1
        # time.sleep(0.5)
        # saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        im = saveBitMap.GetBitmapBits(True)  # Tried False also
        img = np.frombuffer(im, dtype=np.uint8).reshape((h, w, 4))

        result = cv2.matchTemplate(img, img1, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print('ttk: %s' % str(ttk))
        print('Best top left pos: %s' % str(max_loc))
        print('Best conf: %s' % max_val)
        if max_val >= 0.54 or (ttk < 5 and max_val >= 0.50) or (ttk < 4 and max_val >= 0.48) or (ttk < 3 and max_val >= 0.45) or (ttk < 2 and max_val >= 0.42):
            cv2.rectangle(img, max_loc, (max_loc[0]+10, max_loc[1]+15), (10,250,10), 1)
            #print(max_loc[0]+10, max_loc[1]+15)
            a = max_loc[0]+10
            b = max_loc[1]+15
            print("Detectado!")
            pyautogui.moveTo(a, b, 0.16)
            time.sleep(0.24)
            pyautogui.rightClick()
            # pyautogui.rightClick(a, b)
            time.sleep(1)
            
            ttk=0
            
            break
        
        
    cv2.imshow('img', img)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        break
