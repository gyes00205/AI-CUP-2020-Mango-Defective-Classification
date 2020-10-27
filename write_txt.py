import os
import random
import argparse
'''
python write_txt.py -i TrainXml/ -o train.txt
'''
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inpath',help = 'the path to folder of images and xml', required=True)
parser.add_argument('-o','--outpath',help = 'the path to txt', required=True)
args = parser.parse_args()

files = os.listdir(args.inpath)
tTxt = open(args.outpath,'w')
random.shuffle(files)
# tFiles = files[0:int(len(files)*0.8)]
# vFiles = files[int(len(files)*0.8):]
for afile in files:
    if not afile.endswith(".xml"):
        tTxt.write(afile.replace('.jpg','').replace('.png','')+'\n')
tTxt.close()

