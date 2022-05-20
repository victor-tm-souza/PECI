from pathlib import Path
import numpy as np
import os.path
import math
import os
import glob

def main():

    for filesonpath in glob.glob("D:\\presil-export\\pointcloud-treatment\\bin-results\\cars\\*.bin"):
    #for filesonpath in glob.glob("D:\\presil-export\\object\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("D:\\presil-export\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("E:\\testar\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath)
        print("\nFile: ",filesonpath)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        #output_path = "C:\\Users\\Leandro\\Desktop\\Presil\\PreSIL_Output\\bintoply\\" + file_split[0] + ".ply"
        output_path = "D:\\presil-export\\pointcloud-treatment\\ply-results\\cars\\" + file_split[0] + ".ply"
        print("\nOutput path: ", output_path)
        print("\n\n\n")
        values=loadKittiVelodyneFile(filesonpath)
        #values_f=augmentationAttempt("D:\\presil-export\\object\\velodyne\\000013.bin",values)
        savePlyFile(output_path,values)
    
    for filesonpath2 in glob.glob("D:\\presil-export\\pointcloud-treatment\\bin-results\\scenarios\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath2)
        print("\nFile: ",filesonpath2)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        output_path = "D:\\presil-export\\pointcloud-treatment\\ply-results\\scenarios\\" + file_split[0] + ".ply"
        print("\nOutput path: ", output_path)
        print("\n\n\n")
        values=loadKittiVelodyneFile(filesonpath2)
        savePlyFile(output_path,values)

    for filesonpath3 in glob.glob("D:\\presil-export\\pointcloud-treatment\\bin-results\\augmented\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath3)
        print("\nFile: ",filesonpath3)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        output_path = "D:\\presil-export\\pointcloud-treatment\\ply-results\\augmented\\" + file_split[0] + ".ply"
        print("\nOutput path: ", output_path)
        print("\n\n\n")
        values=loadKittiVelodyneFile(filesonpath3)
        savePlyFile(output_path,values)

    for filesonpath4 in glob.glob("D:\\presil-export\\object\\velodyne\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath4)
        print("\nFile: ",filesonpath4)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        output_path = "D:\\presil-export\\pointcloud-treatment\\ply-results\\raw\\" + file_split[0] + ".ply"
        print("\nOutput path: ", output_path)
        print("\n\n\n")
        values=loadKittiVelodyneFile(filesonpath4)
        savePlyFile(output_path,values)

    for filesonpath4 in glob.glob("D:\\presil-export\\pointcloud-treatment\\bin-results\\easy\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath4)
        print("\nFile: ",filesonpath4)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        output_path = "D:\\presil-export\\pointcloud-treatment\\ply-results\\easy\\" + file_split[0] + ".ply"
        print("\nOutput path: ", output_path)
        print("\n\n\n")
        values=loadKittiVelodyneFile(filesonpath4)
        savePlyFile(output_path,values)

    print("Done\n")



def loadKittiVelodyneFile(file_path, include_luminance=True):
    '''
    Loads a kitti velodyne file (ex: 000000.bin) into a list of tuples, where each tuple has (x, y, z) or (x, y, z, l)
    Right now it discards the 4th vaule of each point, i.e. the luminance
    Argument:
        - include_luminance: if the function should also store the point intensisty value in the list of points
    '''
    # Source: https://github.com/hunse/kitti/blob/master/kitti/velodyne.py

    points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)


    point_tuple_list = []


    if include_luminance:
        points = points[:, :4]  # exclude luminance

        for i in range(len(points)):
            #if(points[i][3] > 0):
            point_tuple_list.append((points[i][0], points[i][1], points[i][2], points[i][3]))
    else:
        points = points[:, :3]  # exclude luminance

        for i in range(len(points)):
            point_tuple_list.append((points[i][0], points[i][1], points[i][2],))


    return point_tuple_list

'''def augmentationAttempt(file_path, scen_tuple_list, include_luminance=True):
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
'''

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
