import cv2
import csv
import argparse
filenames = []
# Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inpath',help = 'the path to folder of input images', required=True)
parser.add_argument('-o','--outpath',help = 'the path to folder of output images', required=True)
parser.add_argument('-c','--csvpath',help = 'the path to csv ', required=True)
args = parser.parse_args()

with open(args.csvpath, newline='', encoding="utf-8-sig") as csvfile:
    rows = csv.reader(csvfile)
    i = 0
    for row in rows:
        rowlen = len(row)
        detail = []
        detail.append(str(row[0]))
        # print(rowlen)
        for i in range(1,rowlen,5):
            if(row[i]==''):
                break
            if(row[i]=='不良-著色不佳'):
                detail.append('poor color')
            elif(row[i]=='不良-炭疽病'):
                detail.append('anthracnose')
            elif(row[i]=='不良-乳汁吸附'):
                detail.append('milk adsorption')
            elif(row[i]=='不良-機械傷害'):
                detail.append('mechanical damage')
            else:
                detail.append('black spot')
            # print(row[i+1])
            # print(type(row[i+1]))
            detail.append((int(float(row[i+1])), int(float(row[i+2]))))
            detail.append((int(float(row[i+1]))+int(float(row[i+3])), int(float(row[i+2]))+int(float(row[i+4]))))
        filenames.append(detail)
        

for afile in filenames:
    print('filename: ', afile)
    img = cv2.imread(args.inpath+afile[0])
    for i in range(1,len(afile),3):
        cv2.rectangle(img, afile[i+1], afile[i+2], (0, 0, 255), 2)
        cv2.putText(img, afile[i], (afile[i+1][0], afile[i+1][1]-5), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4, cv2.LINE_AA)
        
    cv2.imwrite(args.outpath+afile[0], img)
