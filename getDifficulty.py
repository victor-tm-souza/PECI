from pathlib import Path
from typing import List
import numpy as np
import os.path
import math
import os
import glob

dif_easy=0
dif_medium=0
dif_hard=0

def main():
    global dif_easy
    global dif_medium
    global dif_hard

    for filesonpath in glob.glob("E:\\Datasets\\5\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("D:\\presil-export\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("E:\\testar\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath)
        print("\nFile: ",filesonpath)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        #output_path = "C:\\Users\\Leandro\\Desktop\\Presil\\PreSIL_Output\\bintoply\\" + file_split[0] + ".ply"
        output_path = "E:\\Datasets\\5\\velodyne\\"
        #print("\nOutput path: ", output_path)
        print("\n\n\n")
        getDifficulty(filesonpath,file_split[0],output_path)
        #values_f=augmentationAttempt("D:\\presil-export\\object\\velodyne\\000013.bin",values)
        #saveBinFile(output_path,values)
        
    t= dif_easy + dif_medium + dif_hard
    per_easy = (dif_easy/t)*100
    per_medium = (dif_medium/t)*100
    per_hard = (dif_hard/t)*100
    print("Per easy: ", per_easy)
    print("PEr medium: ", per_medium)
    print("Per hard: ", per_hard)
    print("\n\n\n")
    print("Done\n")

def getDifficulty(file_path,name,output_file):
    global dif_easy
    global dif_medium
    global dif_hard
    label_name = "E:\\Datasets\\5\\label_2\\"  + str(name) + ".txt"
    dif=0
    with open(label_name) as f:
        content = f.readlines()
        #print (content)
        for line in content:
            #print (line)
            if (line.startswith("Car") or line.startswith("Bus") or line.startswith("Truck") or line.startswith("Motorbike") or line.startswith("Trailer")):
                #print (line)
                dif=1
                det= line.split(" ")
                det[1]=float(det[1])
                det[2]=float(det[2])
                det[5]=float(det[5])
                det[7]=float(det[7])
                height=math.fabs(det[7]-det[5])
                #print ("height",height)
                #print ("trunc",det[1])
                #print ("occlu",det[2])
                if (det[1] >=0 and det[1] <= 0.15 and det[2] >=0 and det[2] <= 0.2 and height >=40):
                    #print ("easy")
                    dif=0
                elif (det[1] > 0.15 and det[1] <= 0.3 and det[2] >0.2 and det[2] <= 0.6 and height >=25):
                    #print ("medium")
                    dif=1
                elif (det[1] > 0.3 and det[1] <= 0.5 and det[2] >0.6 and height >=25):
                    #print ("hard")
                    dif=2
                else:
                    print ("Error")
                    dif=3 # para descartar o restante

            if (dif==0):
                dif_easy+=1
            elif (dif==1):
                dif_medium+=1
            elif (dif==2):
                dif_hard+=1


    print("easy: ",dif_easy)
    print("medium: ",dif_medium)
    print("hard: ",dif_hard)
    print("\n\n\n")

def saveBinFile(filepath, tuple_list):
    filepath = filepath + ".bin"
    list = np.reshape(tuple_list, (-1))
    newFileByteArray = bytearray(list)
    newFile = open(filepath,"wb")
    newFile.write(newFileByteArray)

def augmentationAttempt(file_path, scen_tuple_list, include_luminance=True):
    points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)


    if include_luminance:
        points = points[:, :4]  # exclude luminance

        for i in range(len(points)):
            if(points[i][3] == 91394):
                scen_tuple_list.append((points[i][0], points[i][1]+10, points[i][2]-1, points[i][3]))
    else:
        points = points[:, :3]  # exclude luminance

        for i in range(len(points)):
            scen_tuple_list.append((points[i][0], points[i][1], points[i][2],))

    scen_tuple_list.append(scen_tuple_list)

    return scen_tuple_list

def savePlyFile(filepath, tuple_list, attributes=None, color_for_every_point=(0, 0, 0)):
    '''
    For testing in the Main.py file
    Save list of points (possibly with attributes such as color) into a .PLY formated file
    Arguments: 
        - tuple_list: list of points and their attributes
        - attributes: to indicate what type of attributes are included in the points:
            - c: each point has position + color (r, g, b)
    '''
    with open(filepath, "w") as the_file:
        header_lines = ["ply", "format ascii 1.0"]
        header_lines.append("element vertex " + str(len(tuple_list)))
        header_lines.append("property float x")
        header_lines.append("property float y")
        header_lines.append("property float z")
        header_lines.append("property float intensity")


        # if point have color 
        if attributes == "c" or attributes == "i":
            header_lines.append("property uchar red")
            header_lines.append("property uchar green")
            header_lines.append("property uchar blue")

        header_lines.append("end_header")

        for i in range(0, len(header_lines)):
            the_file.write(header_lines[i] + "\n")

        for i in range(0, len(tuple_list)):
            if attributes == "c" and len(
                    tuple_list[i]) <= 3:  # if the points dont have color, but the attributes is set to "c"
                new_tuple = (tuple_list[i][0], tuple_list[i][1], tuple_list[i][2], color_for_every_point[0],
                             color_for_every_point[1], color_for_every_point[2])
                the_file.write(tupleToStr(new_tuple) + "\n")
            elif attributes == "i" and len(tuple_list[i]) == 4:
                # intensity values are between 0 and 1
                red_percent = int((1 - tuple_list[i][3]) * 255)
                green_percent = int(tuple_list[i][3] * 255)
                new_tuple = (tuple_list[i][0], tuple_list[i][1], tuple_list[i][2], red_percent, green_percent, 0)
                the_file.write(tupleToStr(new_tuple) + "\n")

            else:
                the_file.write(tupleToStr(tuple_list[i]) + "\n")
            
               


def tupleToStr(tuple):
    '''
    Converts a tuple of N size into a string, where each element is separated by a space.
    Arguments:
    - tuple: tuple to be converted into string
    Returns:
        - string with the tuple values
    '''
    tuple_string = ""
    for i in range(0, len(tuple)):
        if i == (len(tuple) - 1):
            tuple_string += str(tuple[i])
        else:
            tuple_string += str(tuple[i]) + " "

    return tuple_string


if __name__ == "__main__":
    main()