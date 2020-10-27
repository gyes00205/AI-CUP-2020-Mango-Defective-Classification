import os
import cv2
import argparse
import csv
# from lobster_core import LobsterCore

# PIG_MODEL_PATH = 'out_graph_dir/gray_models/saved_models_132c/saved_models_rhf/frozen_inference_graph.pb'

# PIG_THRESH = 0.5
# core = LobsterCore(lobster_model_path=PIG_MODEL_PATH,
#                     lobster_th=PIG_THRESH,
#                     scale=1
#                     )
# core.warmup()
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inpath',help = 'the path to folder of input images', required=True)
parser.add_argument('-o','--outpath',help = 'the path to folder of output images', required=True)
parser.add_argument('-c','--csvpath',help = 'the path to csv ', required=True)
# parser.add_argument('-n','--numImg',help = 'number Image', required=True)
args = parser.parse_args()

FROM_PATH = args.inpath
TO_PATH = args.outpath

# os.makedirs(TO_PATH, exist_ok=True)
cnt = 0
with open(args.csvpath, newline='', encoding="utf-8-sig") as csvfile:
    rows = csv.reader(csvfile)
    i = 0
    
    for row in rows:
        # if(cnt==int(args.numImg)):
        #     break
        rowlen = len(row)
        img_n = row[0]
        xml_n = img_n[:-4]+".xml"
        xml_path = TO_PATH+xml_n
        img_path = FROM_PATH+img_n
        img = cv2.imread(img_path)
        print("Processing file " + img_n)
        if img is None:
            continue
        w = img.shape[1]
        h = img.shape[0]
        c = img.shape[2]

        f = open(xml_path, "w")
        # Headers
        f.write("<annotation>\n")
        f.write("\t<folder>"+FROM_PATH+"</folder>\n")
        f.write("\t<filename>"+str(row[0])+"</filename>\n")
        f.write("\t<path>"+img_path+"</path>\n")
        f.write("\t<source>\n")
        f.write("\t\t<database>Unknown</database>\n")
        f.write("\t</source>\n")
        f.write("\t<size>\n")
        f.write("\t\t<width>"+str(w)+"</width>\n")
        f.write("\t\t<height>"+str(h)+"</height>\n")
        f.write("\t\t<depth>"+str(c)+"</depth>\n")
        f.write("\t</size>\n")
        f.write("\t<segmented>0</segmented>\n")
        for i in range(1,rowlen,5):
            if(row[i]==''):
                break
            f.write("\t<object>\n")
            if(row[i+4]=='不良-著色不佳'):
                f.write("\t\t<name>"+'poor-color'+"</name>\n")
            elif(row[i+4]=='不良-炭疽病'):
                f.write("\t\t<name>"+'anthracnose'+"</name>\n")
            elif(row[i+4]=='不良-乳汁吸附'):
                f.write("\t\t<name>"+'milk-adsorption'+"</name>\n")
            elif(row[i+4]=='不良-機械傷害'):
                f.write("\t\t<name>"+'mechanical-damage'+"</name>\n")
            else:
                f.write("\t\t<name>"+'black-spot'+"</name>\n")
            
            xmin = int(float(row[i]))
            ymin = int(float(row[i+1]))
            xmax = int(float(row[i]))+int(float(row[i+2]))
            ymax = int(float(row[i+1]))+int(float(row[i+3]))
            f.write("\t\t<pose>Unspecified</pose>\n")
            f.write("\t\t<truncated>0</truncated>\n")
            f.write("\t\t<difficult>0</difficult>\n")
            f.write("\t\t<bndbox>\n")
            f.write("\t\t\t<xmin>"+str(xmin)+"</xmin>\n")
            f.write("\t\t\t<ymin>"+str(ymin)+"</ymin>\n")
            f.write("\t\t\t<xmax>"+str(xmax)+"</xmax>\n")
            f.write("\t\t\t<ymax>"+str(ymax)+"</ymax>\n")
            f.write("\t\t</bndbox>\n")
            f.write("\t</object>\n")
        cv2.imwrite(TO_PATH+img_n, img)
        f.write("</annotation>\n")
        f.close()
        cnt = cnt + 1

