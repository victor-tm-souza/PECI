from cmath import isnan
from pathlib import Path
from typing import List
import numpy as np
import os.path
import math
import os
import glob

def main():



    for filesonpath in glob.glob("D:\\presil-export\\object\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("D:\\presil-export\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("E:\\testar\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath)
        print("\nFile: ",filesonpath)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        #output_path = "C:\\Users\\Leandro\\Desktop\\Presil\\PreSIL_Output\\bintoply\\" + file_split[0] + ".ply"
        output_path = "D:\\presil-export\\pointcloud-treatment\\bin-results\\"
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

    label_name = "D:\\presil-export\\object\\label_aug_2\\"  + str(name) + ".txt"
    label_file = open(label_name, 'r')
    lines = label_file.readlines() 
    lines_atribute_list = []  
    
    for line in lines:
        atribute_list = line.split(" ")
        lines_atribute_list.append(atribute_list)

    dictio = {}
    point_tuple_list = []


    if include_luminance:
        points = points[:, :4]  # exclude luminance

        for i in range(len(points)):
            id = points[i][3]

            if(id > 0 and id != 2818):
                if id in dictio:
                    dictio[id].append((points[i][0], points[i][1], points[i][2], points[i][3]))
                else:
                    dictio[id] = [(points[i][0], points[i][1], points[i][2], points[i][3])]
    
            elif(id == 0):
                point_tuple_list.append((points[i][0], points[i][1], points[i][2], points[i][3]))
    else:
        points = points[:, :3]  # exclude luminance

        for i in range(len(points)):
            point_tuple_list.append((points[i][0], points[i][1], points[i][2],))

    if(len(dictio.keys()) == 0):
        first_output_file = output_file + "scenarios\\" + name + "_empty"
        print("\nOutput path: ", first_output_file)
        print("\n")
        saveBinFile(first_output_file, point_tuple_list)
    else:
        for key_val in dictio.keys():
            entity_atr = []
            for line in lines_atribute_list:
                if (str(line[15]) == str(int(key_val))):
                    entity_atr = line
                    break
            
            entity_width = float(entity_atr[9])
            entity_height = float(entity_atr[8])
            entity_length = float(entity_atr[10])

            entity_vel_pos_x = float(entity_atr[11])
            entity_vel_pos_y = float(entity_atr[12])
            entity_vel_pos_z = float(entity_atr[13])

            entity_pc_pos_x = entity_vel_pos_z
            entity_pc_pos_y = -entity_vel_pos_x
            entity_pc_pos_z = -entity_vel_pos_y

            r = np.sqrt(((entity_length/2)**2) + ((entity_width/2)**2))

            x=[]
            y=[]
            z=[]
            for t in dictio[key_val]:
                x.append(t[0])
                y.append(t[1])
                z.append(t[2])

            mean_x = np.nanmean(x)
            mean_y = np.nanmean(y)
            min_z = min(z)
            
            '''if (key_val == 204546):
                print(type(min_z))
                print(entity_pc_pos_z)
            '''
            
            indexes = len(dictio[key_val])
            i = 0

            while i < indexes:
                #tuple_to_list[0] -= mean_x
                tuple_to_list = list(dictio[key_val][i])
            
                #circle equation: (x - a)² + (y - b)² = r²
                circle_value = (-tuple_to_list[1] - (-entity_pc_pos_y))**2 + (tuple_to_list[0] - entity_pc_pos_x)**2 - r**2
                #margin of error will be 0.5 for ramps
                if (circle_value > 0 or tuple_to_list[2] < (entity_pc_pos_z - 0.5) or tuple_to_list[2] > (entity_pc_pos_z + entity_height + 0.5)):
                    del dictio[key_val][i]
                    indexes -= 1
                else:
                    tuple_to_list[1] -= mean_y
                    tuple_to_list[2] -= np.float32(entity_pc_pos_z)
                    #tuple_to_list[2] -= min_z
                    '''
                    if (key_val == 204546):
                        print(type(tuple_to_list[2]))
                    '''
                    dictio[key_val][i] = tuple(tuple_to_list)
                    i+=1
                    
            #if (key_val == 3074):
            #    print(len(dictio[key_val]))
            sec_output_file = output_file + "cars\\" + name + "_" + str(int (key_val))
            print("\nOutput path: ", sec_output_file)
            print("\n")
            saveBinFile(sec_output_file, dictio[key_val])


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
