from cProfile import label
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
descartados=0

def main():
    global dif_easy
    global dif_medium
    global dif_hard
    global descartados

    for filesonpath in glob.glob("E:\\Datasets\\10\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("D:\\presil-export\\velodyne\\*.bin"):
    #for filesonpath in glob.glob("E:\\testar\\*.bin"):
        values = []
        file_name = os.path.basename(filesonpath)
        print("\nFile: ",filesonpath)
        file_split=file_name.split(".")
        print("Split: ", file_split[0])
        #output_path = "C:\\Users\\Leandro\\Desktop\\Presil\\PreSIL_Output\\bintoply\\" + file_split[0] + ".ply"
        output_path = "E:\\Datasets\\10\\velodyne\\"
        txtname = output_path.replace("\\","")+".txt"
        txtname = txtname.replace("velodyne","")
        txtname=txtname[2:]
        #print("\nOutput path: ", output_path)
        print("\n\n\n")
        getDifficulty(filesonpath,file_split[0],output_path)
        #values_f=augmentationAttempt("D:\\presil-export\\object\\velodyne\\000013.bin",values)
        #saveBinFile(output_path,values)
        
    t= dif_easy + dif_medium + dif_hard
    per_easy = (dif_easy/t)*100
    per_medium = (dif_medium/t)*100
    per_hard = (dif_hard/t)*100
    f= open(txtname,"w+")
    f.write("Dataset: " + output_path + "\n")
    f.write("Easy: " + str(dif_easy) + "\n")
    f.write("Medium: " + str(dif_medium) + "\n")
    f.write("Hard: " + str(dif_hard) + "\n")
    f.write("Descartados: " + str(descartados) + "\n")
    f.write("Total: " + str(t) + "\n")
    f.write("Percentual easy: " + str(per_easy) + "\n")
    f.write("Percentual medium: " + str(per_medium) + "\n")
    f.write("Percentual hard: " + str(per_hard) + "\n")

    print (os.path.abspath(txtname))
    f.close()
    print("Per easy: ", per_easy)
    print("PEr medium: ", per_medium)
    print("Per hard: ", per_hard)
    print("\n\n\n")
    print("Done\n")

def getDifficulty(file_path,name,output_file):
    global dif_easy
    global dif_medium
    global dif_hard
    global descartados
    label_name = "E:\\Datasets\\10\\label_2\\"  + str(name) + ".txt"
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
                if (det[1] >=0 and det[1] <= 0.15 and det[2] ==0 and height >=40):
                    #print ("easy")
                    dif=0
                elif (det[1] > 0.15 and det[1] <= 0.3 and det[2] ==1 and height >=25):
                    #print ("medium")
                    dif=1
                elif (det[1] > 0.3 and det[1] <= 0.5 and det[2] ==2 and height >=25):
                    #print ("hard")
                    dif=2
                else:
                    #print ("Error")
                    dif=3 # para descartar o restante

            if (dif==0):
                dif_easy+=1
            elif (dif==1):
                dif_medium+=1
            elif (dif==2):
                dif_hard+=1
            elif (dif==3):
                descartados+=1

            
        f.close()
    
    



if __name__ == "__main__":
    main()
