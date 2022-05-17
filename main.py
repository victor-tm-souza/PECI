
import glob
import os
import cv2
import math
def AllImagesWithTreshold():
    minTresh = -1
    maxTresh = 0.9

    labelinit = "E:\\Datasets\\12_n\\label_2\\"
    imginit = "E:\\Datasets\\12_n\\image_2\\"


    for filesonpath in glob.glob("E:\\Datasets\\12_n\\label_2\\*.txt"):
        file_name = os.path.basename(filesonpath)
        filesplit = file_name.split(".")
        filenumber = filesplit[0]
        print("Label: " + str(filenumber))
        labelpath = labelinit + filenumber + ".txt"
        imgpath = imginit + filenumber + ".png"
        img = cv2.imread(imgpath)
        print("File: " + file_name)

        result = img.copy()

        with open(labelpath) as f:
            checkflag = 0
            for line in f:
                lineval = line.strip().split(' ')
                height=math.fabs(float(lineval[7])-float(lineval[5]))
                #if (height>=40):
                dif=0
                
                if (float(lineval[2])==0 and float(lineval[1])<=0.15 and height>=40):
                    
                    dif=1
                elif((float(lineval[2])==0 or float(lineval[2])==1) and float(lineval[1])<=0.3 and height>=25):
                    dif=2
                elif((float(lineval[2])==0 or float(lineval[2])==1 or float(lineval[2])==2) and float(lineval[1])<=0.5 and height>=25):
                    dif=3
                
                if (float(dif)>minTresh and float(dif)<=maxTresh and (lineval[0]=='Car'or lineval[0]=='Truck'or lineval[0]=='Misc'or lineval[0]=='Van')):
                    checkflag = 1
                    min_x = int(float(lineval[4]))
                    max_x = int(float(lineval[6]))
                    min_y = int(float(lineval[5]))
                    max_y = int(float(lineval[7]))
                    cv2.rectangle(result, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)  # add rectangle to image
                    cv2.putText(result, lineval[1], (min_x, min_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    #cv2.line(result, (min_x, min_y), (min_x, max_y), (255, 0, 0), 2)
        if (checkflag):
            winname = 'image %d' % (int(filenumber))
            cv2.namedWindow(winname)  # Create a named window
            cv2.moveWindow(winname, 10, 10)  # Move it to (40,30)
            cv2.imshow(winname, img)
            cv2.imshow(winname, result)
            while 1:
                if cv2.waitKey(0) != ord('q'):
                    break
                else:
                    exit()
            cv2.destroyAllWindows()

def DrawBB():

    imginit = "F:\\Split\\training\\image_2\\"

    filenumber = "003611"

    coorList=[1099,547,1151,566]

    imgpath = imginit + filenumber + ".png"
    img = cv2.imread(imgpath)

    result = img.copy()

    min_x = int(float(coorList[0]))
    max_x = int(float(coorList[1]))
    min_y = int(float(coorList[2]))
    max_y = int(float(coorList[3]))
    cv2.rectangle(result, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)  # add rectangle to image
    cv2.putText(result, "0", (min_x, min_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)


    cv2.imshow('image %d' % (int(filenumber)), result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def main():
    AllImagesWithTreshold()
    #DrawBB()

if __name__ == "__main__":
    main()
