import pandas as pd
import numpy as np
import argparse
import sys

# Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inpath',help = 'the path to input csv file', required=True)
parser.add_argument('-o1','--outpath1',help = 'the path to output csv file for class1', required=True)
parser.add_argument('-o2','--outpath2',help = 'the path to output csv file for class2', required=True)
args = parser.parse_args()

# Check the input/output files are .csv files
if not(args.inpath.endswith('csv') and args.outpath1.endswith('csv') and args.outpath2.endswith('csv')):
    sys.exit("Invalid filenames, please check your arguments")

# Read the input csv file
df = pd.read_csv(args.inpath, header=None) 

# Numpy array to store '不良-著色不佳' and '不良-炭疽病'(Class1)
array1 = np.full(df.shape, np.NaN).astype('str')

# Numpy array to store '不良-乳汁吸附' and '不良-機械傷害' and '不良-黑斑病'(Class2)
array2 = np.full(df.shape, np.NaN).astype('str')

for index, row in df.iterrows():
    start_index1= 5
    start_index2= 5
    # Each time is 5 steps
    for i in range(5, len(row), 5):
        # Match class1
        if(row[i] == '不良-著色不佳' or row[i] == '不良-炭疽病'):
            array1[index][0] = row[0]
            array1[index][start_index1-4:start_index1] = row[i-4:i]
            array1[index][start_index1] = row[i]
            start_index1 += 5
        # Match class2
        elif(row[i] == '不良-乳汁吸附' or row[i] == '不良-機械傷害' or row[i] == '不良-黑斑病'):
            array2[index][0] = row[0]
            array2[index][start_index2-4:start_index2] = row[i-4:i]
            array2[index][start_index2] = row[i]
            start_index2 += 5

# Replace string 'nan' to np.NaN
out1 = pd.DataFrame(array1)
out1.replace('nan', np.nan, inplace=True)
out2 = pd.DataFrame(array2)
out2.replace('nan', np.nan, inplace=True)

# Get the index of NaN in image section
deleteIndex1 = out1[out1[0].isnull()].index
deleteIndex2 = out2[out2[0].isnull()].index

# Delete the redundant rows
out1.drop(deleteIndex1 , inplace=True)
out2.drop(deleteIndex2 , inplace=True)

# Write in csv files
out1.to_csv(args.outpath1, header=None, index=None, encoding='utf_8_sig')
out2.to_csv(args.outpath2, header=None, index=None, encoding='utf_8_sig')