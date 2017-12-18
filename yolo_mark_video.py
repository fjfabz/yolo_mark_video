import cv2
import time
import sys,os
import glob
import numpy as np

img_counter = 0
mousex = 0
mousey = 0
bound_width = 100
bound_height = 100

frame = None
outfolder = None
img_width = 0
img_height = 0
name = None
classno = 0

def write_txt_img():
    global img_counter
    if not os.path.exists(outfolder): os.mkdir(outfolder)
    # write txt
    bounding_str = "{} {} {} {} {}".format(classno, mousex / img_width, mousey / img_height, bound_width / img_width,
                                          bound_height / img_height)
    txt_name = "{0}_{1:03d}.txt".format(name, img_counter)
    f = open(os.path.join(outfolder, txt_name), 'w')
    f.write(bounding_str)
    f.close()
    # write img
    img_name = "{0}_{1:03d}.jpg".format(name, img_counter)
    cv2.imwrite(os.path.join(outfolder, img_name), frame)
    print(img_name)
    img_counter += 1

def click_and_mark(event, x, y, flags, param):
    global mousex
    global mousey
    mousex=x
    mousey=y
    clone = frame.copy()
    cv2.putText(clone, 'class {}, [space]:mark, [s]:stop, [1]:big, [2]:small, [esc]:next'.format(classno),
                (10, img_height - 20), cv2.FONT_HERSHEY_PLAIN, 1.2,
                (255, 255, 255), 1, cv2.LINE_AA)
    if event == cv2.EVENT_MOUSEMOVE:
        cv2.rectangle(clone, (x - round(bound_width/2), y - round(bound_height/2)), (x + round(bound_width/2), y + round(bound_height/2)), (0, 255, 0), 2)
        cv2.imshow("image", clone)
    elif event == cv2.EVENT_LBUTTONDOWN:
        pass
        #write_txt_img()


def mark_process(file_path):
    global frame,clone,outfolder,img_height,img_width,name,bound_height,bound_width,classno

    folder, basename = os.path.split(file_path)
    name, ext = os.path.splitext(basename)
    outfolder = os.path.join(folder, "img")

    cam = cv2.VideoCapture(file_path)
    fps = cam.get(cv2.CAP_PROP_FPS)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_mark)

    _, frame = cam.read()
    img_height, img_width = frame.shape[:2]
    STOP = False

    while True:
        if not STOP:
            ret, frame = cam.read()

            if not ret:
                break
            clone=frame.copy()
            cv2.putText(clone, 'class {}, [space]:mark, [s]:stop, [1]:big, [2]:small, [esc]:next'.format(classno), (10, img_height-20), cv2.FONT_HERSHEY_PLAIN, 1.2,
                            (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow("image", clone)
            time.sleep(1 / fps)

        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:  # SPACE pressed. save image and crop area
            write_txt_img()
        elif k % 256 == 113:  # Q pressed
            bound_width *= 1.5
            bound_height *= 1.5
        elif k % 256 == 119:  # W pressed
            bound_width /= 1.5
            bound_height /= 1.5
        elif k % 256 == 101:  # E pressed
            bound_width *= 1.5
            #bound_height *= 1.5
        elif k % 256 == 114:  # R pressed
            bound_width /= 1.5
            #bound_height /= 1.5
        elif k % 256 == 116:  # T pressed
            #bound_width *= 1.5
            bound_height *= 1.5
        elif k % 256 == 121:  # Y pressed
            #bound_width /= 1.5
            bound_height /= 1.5
        elif k % 256 == 115:  # s pressed STOP and START
            STOP = not STOP
        elif 48<= k % 256 <=57:  # s pressed STOP and START
            classno = k % 256 - 48
        elif k != -1:
            print(k % 256)

        if cv2.getWindowProperty('image',0) < 0:
            break
    cam.release()
    cv2.destroyAllWindows()

def main():

    if os.path.isdir(sys.argv[1]):
        filelists = glob.glob(sys.argv[1]+"/*.mp4")
        for file_path in filelists :
            print(file_path)
            mark_process(file_path)
    else:
        file_path = sys.argv[1]
        mark_process(file_path)

if __name__ == '__main__':
    main()