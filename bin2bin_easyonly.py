from cmath import isnan
from pathlib import Path
from typing import List
import numpy as np
import os.path
import math
import os
import glob
import shutil

def main():
    for filesonpath in glob.glob("/media/peciml/My Passport/PECI/training_set/dataset_3500/velodyne_full/*.bin"):
    #for filesonpath in glob.glob("D:\\presil-export\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("E:\\testar\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath)
        print("\nFile: ",filesonpath)
        file_split=file_name.split(".")
        print("Split: ", n_cnt)
        #output_path = "C:\\Users\\Leandro\\Desktop\\Presil\\PreSIL_Output\\bintoply\\" + file_split[0] + ".ply"
        output_path = "/media/peciml/My Passport/PECI/cropped_training_set/velodyne/"
        #print("\nOutput path: ", output_path)
        print("\n\n\n")
        loadKittiVelodyneFile(filesonpath,file_split[0],output_path)
        #values_f=augmentationAttempt("D:\\presil-export\\object\\velodyne\\000013.bin",values)
        #saveBinFile(output_path,values)
    print("Done\n")



def loadKittiVelodyneFile(file_path, name, output_file, include_luminance=True):
    '''
    Loads a kitti velodyne file (ex: 000000.bin) into a list of tuples, where each tuple has (x, y, z) or (x, y, z, l)
    Right now it discards the 4th vaule of each point, i.e. the luminance
    Argument:
        - include_luminance: if the function should also store the point intensisty value in the list of points
    '''
    # Source: https://github.com/hunse/kitti/blob/master/kitti/velodyne.py

    points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)

    label_name = "/media/peciml/My Passport/PECI/training_set/dataset_3500/label_aug_2_full/"  + str(name) + ".txt"

    dictio = {}
    point_tuple_list = []


    if include_luminance:
        points = points[:, :4]  # exclude luminance

        for i in range(len(points)):
            id = points[i][3]

            if(id > 0):
                if id in dictio:
                    dictio[id].append((points[i][0], points[i][1], points[i][2], np.float32(0)))
                else:
                    dictio[id] = [(points[i][0], points[i][1], points[i][2], np.float32(0))]
    
            elif(id == 0):
                point_tuple_list.append((points[i][0], points[i][1], points[i][2], np.float32(0)))

    else:
        points = points[:, :3]  # exclude luminance

        for i in range(len(points)):
            point_tuple_list.append((points[i][0], points[i][1], points[i][2],))
    
    global n_cnt
    label_2_old = "/media/peciml/My Passport/PECI/training_set/dataset_3500/label_2_full/"  + name + ".txt"
    label_2_new = "/media/peciml/My Passport/PECI/cropped_training_set/label_2/"  + "{number:06}".format(number=n_cnt) + ".txt"
    shutil.copyfile(label_2_old,label_2_new)

    with open(label_name) as f:
        content = f.readlines()
        empty = True
        #print (content)


        for line in content:
            #print (line)
            if (line.startswith("Car") or line.startswith("Bus") or line.startswith("Truck") or line.startswith("Motorbike") or line.startswith("Trailer")):
                #print (line)
                det= line.split(" ")
                det[1]=float(det[1])
                det[2]=float(det[2])
                det[5]=float(det[5])
                det[7]=float(det[7])
                det[15]=float(det[15])
                height=math.fabs(det[7]-det[5])

                
                #print ("easy")
                for k in dictio.keys():
                    if det[15]==k:
                        if (det[1] >=0 and det[1] <= 0.15 and det[2] ==0.0 and height >=40):
                            empty = False
                            point_tuple_list.extend(dictio[det[15]])
                            break
                        else:
                            with open(label_2_new, "r") as f_2:
                                lines_2 = f_2.readlines()
                            f_2 = open(label_2_new, "w")
                            for line_2 in lines_2:
                                line_at = line_2.split(" ")
                                if line_at[11] != det[11] or line_at[12] != line_at[12] or line_at[13] != det[13]:
                                    f_2.write(line_2)         
                                else:
                                    print("deleted: " + line_at[0] + ", " + line_at[1] + ", " + line_at[2] + ", " + line_at[3] + ", " + line_at[4])        
                            f_2.close()           


    if(not empty):
        output_file = output_file + "{number:06}".format(number=n_cnt)
        saveBinFile(output_file, point_tuple_list)
        n_cnt+=1
    else:
        os.remove(label_2_new)

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
    n_cnt = 0
    main()
