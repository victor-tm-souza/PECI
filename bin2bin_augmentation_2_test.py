from cmath import isnan
from pathlib import Path
from random import randint
from typing import List
import numpy as np
import os.path
import math
import os
import glob
import shutil

n_cnt = 0

def main():

    cars = glob.glob("/media/peciml/My Passport/PECI/separated_training_set/cars/*.bin")
    scenarios = glob.glob("/media/peciml/My Passport/PECI/separated_training_set/scenarios/*.bin")
    num_car_files = len(cars)
    num_scenario_files = len(scenarios)
    global n_cnt
    while n_cnt < 3500:
        index = randint(0, num_scenario_files-1)
        filesonpath = scenarios[index] 
        file_name = os.path.basename(filesonpath)
        print("\nFile: ",filesonpath)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        output_path = "/media/peciml/My Passport/PECI/augmented_set/velodyne/" + "{number:06}".format(number=n_cnt)
        print("Data number: ", "{number:06}".format(number=n_cnt))
        print("\n\n\n")

        loadKittiVelodyneFile(filesonpath,file_split[0],cars, num_car_files, output_path)

    print("Done\n")



def loadKittiVelodyneFile(file_path, name, cars, num_car_files, output_file, include_luminance=True):
    '''
    Loads a kitti velodyne file (ex: 000000.bin) into a list of tuples, where each tuple has (x, y, z) or (x, y, z, l)
    Right now it discards the 4th vaule of each point, i.e. the luminance
    Argument:
        - include_luminance: if the function should also store the point intensisty value in the list of points
    '''
    # Source: https://github.com/hunse/kitti/blob/master/kitti/velodyne.py
    global n_cnt
    points_scenario = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    point_tuple_list = []


    points_scenario = points_scenario[:, :4]  # exclude luminance
    alturamin = 10000
    alturamax = 0
    for i in range(len(points_scenario)):
        if (points_scenario[i][2] > alturamax):
            alturamaxpoint= [points_scenario[i][0], points_scenario[i][1], points_scenario[i][2] ]
            alturamax=points_scenario[i][2]
        if(points_scenario[i][2]< alturamin):
            alturaminpoint= [points_scenario[i][0], points_scenario[i][1], points_scenario[i][2] ]
            alturamin=points_scenario[i][2]

        point_tuple_list.append((points_scenario[i][0], points_scenario[i][1], points_scenario[i][2], np.float32(0)))

    vetor2pontos= [alturamaxpoint[0]-alturaminpoint[0],alturamaxpoint[1]-alturaminpoint[1],alturamaxpoint[2]-alturaminpoint[2]] 
    label_2_old = "/media/peciml/My Passport/PECI/training_set/dataset_3500/label_2_full/"  + name.split("_")[0]  + ".txt"
    label_2_new = "/media/peciml/My Passport/PECI/augmented_set/label_2/"  + "{number:06}".format(number=n_cnt) + ".txt"
    shutil.copyfile(label_2_old,label_2_new)

    with open(label_2_new, "a+") as label_2_file:
        num_cars = randint(15, 23)
        for i in range(num_cars):
            car_pc = randint(0, num_car_files-1)
            car_file = cars[car_pc]
            car_file_name = os.path.basename(car_file)
            car_scene = car_file_name.split("_")[0]
            car_id = (car_file_name.split("_")[1]).split(".")[0]
            points_cars = np.fromfile(car_file, dtype=np.float32).reshape(-1, 4)
            label_aug_name = "/media/peciml/My Passport/PECI/training_set/dataset_3500/label_aug_2_full/"  + car_scene + ".txt"
            label_aug_file = open(label_aug_name, 'r')
            lines = label_aug_file.readlines() 
        
            for line in lines:
                atribute_list = line.split(" ")
                

                if (str(atribute_list[15]) == car_id):
                    #entity_width = float(atribute_list[9])
                    #entity_height = float(atribute_list[8])
                    #entity_length = float(atribute_list[10])

                    entity_vel_pos_x = float(atribute_list[11])
                    entity_vel_pos_y = float(atribute_list[12])
                    entity_vel_pos_z = float(atribute_list[13])

                    entity_pc_pos_x = entity_vel_pos_z
                    entity_pc_pos_y = -entity_vel_pos_x
                    entity_pc_pos_z = -entity_vel_pos_y

                    
                    if include_luminance:
                        points_cars = points_cars[:, :4]  # exclude luminance
                        close_points = []


                        for i in range(len(point_tuple_list)):
                            if((point_tuple_list[i][0] > entity_pc_pos_x - 1.8) and (point_tuple_list[i][0] < entity_pc_pos_x + 1.8) and (point_tuple_list[i][1] > entity_pc_pos_y - 1.8) and (point_tuple_list[i][1] < entity_pc_pos_y + 1.8)):
                                close_points.append(point_tuple_list[i])
                        
                        if(close_points!= []):
                            lower_z = min(close_points)[2]
                            subtraction = (entity_pc_pos_z - lower_z)        
                            for i in range(len(points_cars)):
                                point_tuple_list.append((points_cars[i][0], points_cars[i][1], np.float32(points_cars[i][2]-subtraction), np.float32(0)))

                            label_2_file.seek(0)
                            l2_data = label_2_file.read(100)
                            #15 first attributes
                            label_2_file.write(atribute_list[0] + " " + atribute_list[1] + " " + atribute_list[2] + " " + atribute_list[3] + " " + atribute_list[4] + " " + atribute_list[5] + " " + atribute_list[6] + " " + atribute_list[7] + " " + atribute_list[8] + " " + atribute_list[9] + " " + atribute_list[10] + " " + atribute_list[11] + " " + atribute_list[12] + " " + atribute_list[13] + " " + atribute_list[14] + "\n")
                            
                    else:
                        points_cars = points_cars[:, :3]  # exclude luminance

                        for i in range(len(points_cars)):
                            point_tuple_list.append((points_cars[i][0], points_cars[i][1], points_cars[i][2],))
                    
                    break

    if os.stat(label_2_new).st_size != 0:
        saveBinFile(output_file, point_tuple_list)
        n_cnt += 1
    else:
        os.remove(label_2_new)

def verifyplan(vetor2pontos,entity_pc_pos_x, entity_pc_pos_y, entity_pc_pos_z):
    valuexy = (vetor2pontos[0]*entity_pc_pos_x) + (vetor2pontos[1]*entity_pc_pos_y)
    valuez= (-valuexy/entity_pc_pos_z)
    return valuez 

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
