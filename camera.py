import cv2, time
import timeit
import subprocess
from subprocess import Popen, PIPE
from PIL import Image
import tkinter as tk
import _thread


window = tk.Tk()

def startFake():
    video = cv2.VideoCapture(0)
    subprocess.call(['sh', './create.sh'])
    check, frame = video.read()
    
    quality = 0
    blur = 0
    fps = 0

    if(ent_qual.get() != '' and ent_blur.get() != '' and ent_fps.get() != ''):
        quality = int(ent_qual.get()) #1-100 scale
        blur = int(ent_blur.get()) #1-100 scale
        fps = int(ent_fps.get())
    else:
        window.destroy()

    if(not(quality >= 1 and quality <= 100 and blur >= 1 and blur <= 100 and fps >= 1)):
        window.destroy()

    height, width = frame.shape[:2]
    w, h = (int(quality* width /100 ), int(quality * height/100))

    p = Popen(['ffmpeg', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-i', '-', '-vcodec', 'rawvideo', '-pix_fmt', 'yuv420p', '-f', 'v4l2', '/dev/video2'], stdin=PIPE)
    while(True):
        check, frame = video.read()
        if(quality < 100):
            frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_NEAREST)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if(blur < 100):
            frame = cv2.blur(frame, (blur, blur)) 

        im = Image.fromarray(frame)
        im.save(p.stdin, 'JPEG')
        if(fps < 10):
            time.sleep(1/fps)

def startTh():
    btn_convert.configure(state=tk.DISABLED)
    _thread.start_new_thread(startFake, ())
        

poczatek = False
    
# Set-up the window
window.title("Break your camera")
window.resizable(width=False, height=False)
window.geometry("500x185")

#title frame
lbl_title = tk.Label(window, text="WELCOME TO THE ULTIMATE WEBCAM BREAKER v.2.1")

#fps entry frame
frm_entry1 = tk.Frame(master=window)
ent_fps = tk.Entry(master=frm_entry1, width=5)
lbl_fps = tk.Label(master=frm_entry1, text="fps")

#quality entry frame
frm_entry2 = tk.Frame(master=window)
ent_qual = tk.Entry(master=frm_entry2, width=5)
lbl_qual = tk.Label(master=frm_entry2, text="quallity (1-100 scale)")

#blur entry frame
frm_entry3 = tk.Frame(master=window)
ent_blur = tk.Entry(master=frm_entry3, width=5)
lbl_blur = tk.Label(master=frm_entry3, text="blur (1-100 scale)")

#aligning
lbl_title.grid(row=0, column=0, sticky="w", padx=75, pady=20)

ent_fps.grid(row=1, column=0, sticky="e")
lbl_fps.grid(row=1, column=1, sticky="w")
ent_qual.grid(row=2, column=0, sticky="e")
lbl_qual.grid(row=2, column=1, sticky="w")
ent_blur.grid(row=3, column=0, sticky="e")
lbl_blur.grid(row=3, column=1, sticky="w")

#fake my camera button
btn_convert = tk.Button(
    master=window,
    text="Fake my camera",
    command=startTh
)

#griding
frm_entry1.grid(row=1, column=0, padx=0)
frm_entry2.grid(row=2, column=0, padx=0)
frm_entry3.grid(row=3, column=0, padx=0)
btn_convert.grid(row=4, column=0, pady=10)

# Run the application
window.mainloop()

