import numpy as np
import csv

def load_train():
    #load the training data
    sigma_data = []
    with open('SigmaTrain.csv','r') as csvfile:
        reader_object = csv.reader(csvfile)
        for row in reader_object:
            sigma_data.append(row)
    sequence_data = []
    with open('PromoterTrain.csv','r') as csvfile:
        reader_object = csv.reader(csvfile)
        for row in reader_object:
            sequence_data.append(row)
    return sigma_data[0][1:],np.array(sigma_data[1:]).astype(int)[:,1:],np.array(sequence_data[1:])[:,1] #sigma_headers,sigma_data,sequence_data

def load_test():
    #load the test data
    sequence_data = []
    with open('PromoterTest.csv','r') as csvfile:
        reader_object = csv.reader(csvfile)
        for row in reader_object:
            sequence_data.append(row)
    return np.array(sequence_data[1:])[:,1] #sequence_data


def get_subsets(sigma_data,sequence_data):
    #split the sequence_data into subsets for each sigma factor
    #sequences that have binding affinity to multiple sigma factors will be included in each of those corresponding subsets
    all_subsets = []
    for sigma in range(sigma_data.shape[1]):
        all_subsets.append(sequence_data[sigma_data[:,sigma]==1])
    return all_subsets

if __name__ == '__main__':
    sigma_headers,sigma_data,sequence_data = load_train()
    sequence_test = load_test()
    subset_list = get_subsets(sigma_data,sequence_data)
