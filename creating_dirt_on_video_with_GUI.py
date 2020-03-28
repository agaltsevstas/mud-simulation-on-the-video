from tkinter import Tk, Button, Listbox, Label
from tkinter import messagebox as mbox
from tkinter import filedialog
import cv2
import numpy as np
import os

dir = "/Users/mac/Desktop/cadrs"
file_overlay = 0
file_cap = 0

def callback(file, file_extension):

    global label_video, label_image
    if (file_extension == "video_loaded"):
        label_video = Label(text = file + " LOADED", fg="blue")
        label_video.place(x=110, y=10)
    if (file_extension == "image_loaded"):
        label_image = Label(text = file + " LOADED", fg="blue")
        label_image.place(x=110, y=50)
    print (file + " LOADED")

def file_replacement(list_box, file, label):
    for index in range(list_box.size()):
        if(list_box.get(index) == file):
            list_box.delete(first=index)
            label.destroy()

def Function_video(root, list_box):
    global file_cap
    if (file_cap!=0):
        file_replacement(list_box, file_cap, label_video)
    root.filename = filedialog.askopenfilename(initialdir = dir, title="Select VIDEO",
                                               filetypes=[ ("AVI files", "*.avi"),
                                                           ("FLV files", "*.flv"),
                                                           ("MKV files", "*.mkv"),
                                                           ("MP4 files", "*.mp4"),
                                                           ("WMV files", "*.wmv") ])
    if os.path.exists(root.filename):
       file_cap = root.filename
       list_box.insert(0, root.filename)
       callback(os.path.basename(root.filename), "video_loaded")

def Function_image(root, list_box):
    global file_overlay
    if (file_overlay!=0):
        file_replacement(list_box, file_overlay, label_image)
    root.filename = filedialog.askopenfilename(initialdir = dir, title="Select IMAGE",
                                               filetypes=[ ("BMP files", "*.bmp"),
                                                           ("JPEG files", "*.jpeg"),
                                                           ("JPG files", "*.jpg"),
                                                           ("GIF files", "*.gif"),
                                                           ("PNG files", "*.png") ])

    if os.path.exists(root.filename):
        file_overlay = root.filename
        list_box.insert(0, root.filename)
        # print(list_box.get(first=0))
        callback(os.path.basename(root.filename), "image_loaded")

def question_exit(root):
    ask = mbox.askquestion("Exit", "Are you sure to quit?")
    if (ask == "yes"):
       root.quit()

def open_file(list_box):
    try:
        selection = list_box.curselection()
        if(list_box.get(selection) == file_cap):
            print(file_cap+" OPEN")
            cap = cv2.VideoCapture(file_cap)
            fps = cap.get(cv2.CAP_PROP_FPS)
            success,frame = cap.read()
            while (success):
              key = cv2.waitKey(int(1/fps*1000))
              if(key == 27):
                  break
              success,frame = cap.read()
              cv2.imshow("Video", frame)
            cap.release()
            cv2.destroyAllWindows()
        if(list_box.get(selection) == file_overlay):
            print(file_overlay+" OPEN")
            image = cv2.imread(file_overlay)
            cv2.imshow("0", image)
    except:
        pass

def delete_file(list_box):
    global file_cap, file_overlay
    try:
        selection = list_box.curselection()
        print(list_box.get(selection))
        if(list_box.get(selection) == file_overlay):
            label_image.destroy()
            list_box.delete(selection)
            print(file_overlay+" DELETE")
            file_overlay = 0
        if(list_box.get(selection) == file_cap):
            label_video.destroy()
            list_box.delete(selection)
            print(file_cap+" DELETE")
            file_cap = 0
    except:
        pass
def make_gui():
    root = Tk()
    root.title('Choose FILES')
    root.geometry("300x200+400+300")
    list_box = Listbox(root, height=4, width=30)
    list_box.place(x = 5, y = 120)
    button_video = Button(root, text='Load VIDEO', activeforeground="blue", underline=10, command = lambda: Function_video(root, list_box))
    button_video.grid(row=0, column=0, sticky="w", ipadx=10, ipady=10)
    button_image = Button(root, text='Load IMAGE', activeforeground="blue", underline=10, command = lambda: Function_image(root, list_box))
    button_image.grid(row=1, column=0, sticky="w", ipadx=10, ipady=10)
    button_open = Button(text="Open", width = 8, command = lambda: open_file(list_box))
    button_open.grid(row=3, column=0)
    button_delete = Button(text="Delete", width = 8, command= lambda: delete_file(list_box))
    button_delete.grid(row=3, column=1)
    button_exit = Button(text="Exit", width = 8, command = lambda: question_exit(root))
    button_exit.grid(row=3, column=2)
    root.mainloop()

def work_with_video():
    path = os.path.dirname(file_cap)
    name = os.path.splitext(os.path.basename(file_cap))[0]
    ext = os.path.splitext(os.path.basename(file_cap))[1]
    file_video =  path + "/" + name + "_new" + ext
    file_data = path + "/" + "data" + ".txt"
    c = 64
    d = 128
    increase = 5
    dirt_masking = False
    record = False
    click = True
    count_click = 0
    cap = cv2.VideoCapture(file_cap)
    is_frame, image = cap.read()
    width, height = image.shape[:2]
    overlay = cv2.imread(file_overlay)
    overlay = cv2.resize(overlay, (height, width))
    overlay = cv2.GaussianBlur(overlay, (0, 0), 1.8)
    overlay_copy = overlay.copy()
    a = np.min(overlay)
    b = np.max(overlay)
    threshold = b
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(file_video, fourcc, cap.get(cv2.CAP_PROP_FPS), (height, width))
    cv2.namedWindow("0", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("0", 0, 0)
    if(is_frame == False):
        print("video not found")
    dt = int(1/cap.get(cv2.CAP_PROP_FPS)*1000)
    while (1):
        modify = False
        key = cv2.waitKey(dt)
        if (key == ord('r')):
            ~click
            if(click):
                try:
                    count = 0
                    data_from_file = np.uint8([])
                    file = open(file_data, "r")
                    if (os.stat(file_data).st_size!=0):
                        for line in file:
                            if(line!="\n"):
                                data_from_file = np.append(data_from_file, np.array([int(s) for s in line.split() if s.isdigit()]))
                                print("pressed R, Read from {}, threshold = {data[0]}, c = {data[1]}, d = {data[2]}".format(file_data, data = data_from_file))
                                count+=3
                        file.close()
                        click = False
                    else:
                        print ("FILE is EMPTY!")
                except IOError:
                    print ("Could not OPEN FILE!")
            else:
                threshold = data_from_file[count_click]
                c = data_from_file[1+count_click]
                d = data_from_file[2+count_click]
                print("pressed double R, read from DATA, threshold = {}, c = {}, d = {}".format(threshold, c, d))
                count_click+=3
                if (count_click >= len(data_from_file)):
                    count_click = 0
        if (key == ord('x')):
            dirt_masking ^= 1
            if(dirt_masking):
                print ("pressed x, DIRTY")
            else:
                print ("pressed x, CLEAN")
        if (key == 27):
            print ("pressed BREAK")
            break
        if (key == 32):
            print ("pressed PAUSE")
            key = cv2.waitKey(0)
        if (key == ord('w') and threshold <= 255-increase):
            threshold+=increase
            print ("pressed w, threshold = ", threshold)
        if (key == ord('s') and threshold >= 0+increase):
            threshold-=increase
            print ("pressed s, threshold =", threshold)
        if (key == ord('d') and d <= 255 - increase):
            modify = True
            d += increase
            print ("pressed d, d =", d)
        if (key == ord('a') and d - increase > c):
            modify = True
            d -= increase
            print ("pressed a, d = ", d)
        if (key == ord('g') and c + increase < d):
            modify = True
            c += increase
            print ("pressed g, c =", c)
        if (key == ord('f') and c >= 0 + increase):
            modify = True
            c -= increase
            print ("pressed f, c = ", c)
        if(modify):
            overlay = ((d - c) / (b - a)) * (overlay_copy - a) + c
            overlay = overlay.astype(np.uint8)
        if (dirt_masking == True):
            # image32 = image.astype(np.float32)
            #rows,cols,channels = overlay.shape
            # roi = output[0:rows, 0:cols ]
            # image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(overlay, threshold, threshold, cv2.THRESH_TRUNC)
            # mask = np.array(mask, dtype=np.float32)
            mask = threshold - mask
            # mask = np.array(mask, dtype=np.uint8)
            # cv2.imshow("0" , roi)
            # cv2.waitKey(0)
            # mask_inv = cv2.bitwise_not(mask)
            # roi = np.array(roi, dtype=np.float32)
            # overlay = np.array(overlay, dtype=np.float32)
            # img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
            # img2_fg = cv2.bitwise_and(overlay,overlay,mask = mask)
            # img2_fg -= threshold
            dst = cv2.subtract(image, mask)
            # dst = image - mask
            # np.clip(dst, 0,255, out=dst)
            # dst = dst.astype('uint8')
            # dst = np.array(dst, dtype=np.uint8)
            # output[0:rows, 0:cols ] = dst
            # cv2.addWeighted(output, 0.5, image, 0.5, 0, image)
        else:
            dst = image
        if(record):
                video.write(dst)
        cv2.imshow("0", dst)
        if (key == 13):
            record ^= 1
            if(record):
                video.write(dst)
                print ("pressed ENTER, video recording to {}".format(file_video))
            else:
                video.release()
                data_to_file = np.uint8([threshold, c, d])
                file = open(file_data, "a")
                file.write(' '.join(["{}".format(item) for item in data_to_file]))
                file.write("\n")
                file.close()
                print ("pressed ENTER, video stop recorded; data recorded to {}, parametrs: threshold = {data[0]}, c = {data[1]}, d = {data[2]}".format(file_data, data = data_to_file))
                click = True
        is_frame, image = cap.read()
        if(is_frame == False):
            cap.release()
            cap.open(file_cap)
            is_frame,image = cap.read()
            if (is_frame == False):
                break
def main():
    make_gui()
    if (file_cap and file_overlay):
        work_with_video()

if __name__ == '__main__':
    main()


