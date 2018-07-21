import numpy as np
from data_manipulation import *
from difflib import SequenceMatcher
import editdistance
from sklearn.cluster import DBSCAN

def get_base_content(sequence_data):
    #get content percentage of each base ATGC and return matrix in dimensions sample x base
    length = len(sequence_data[0])
    return np.array([np.char.count(sequence_data,'A')/length,np.char.count(sequence_data,'T')/length,np.char.count(sequence_data,'G')/length,np.char.count(sequence_data,'C')/length]).T

##def get_base_content_list(subset_list):
##    base_content_list = []
##    for subset in subset_list:
##        base_content_list.append(get_base_content(subset))
##    return base_content_list

def similarity_str(string1,string2):
    return SequenceMatcher(None, string1, string2).ratio()

def similarity(string,subset):
    #get the similarity between a string sample and a subset for a particular sigma
    #we will use these similarity percentages as feature inputs in a neural net (one for each sigma)
    array = np.random.rand(subset.shape[0])
    for i in range(subset.shape[0]):
        array[i] = similarity_str(string,subset[i])
    return array #same length as subset, each row denoting the percentage similarity between the string in that row compared to the sample string

def get_similarity_matrix(training_set,sigma_subset):
    #create a sample x feature matrix, where each feature is the similarity percentage to the corresponding string in the sigma_subset
    #training_set contains all the data (not subsetted)
    #sigma_subset contains all string sequences that are classified as 1 for a particular sigma
    array = np.random.rand(training_set.shape[0],sigma_subset.shape[0])
    for i in range(training_set.shape[0]):
        if i % 100 == 0:
            print(i)
        array[i,:] = similarity(training_set[i],sigma_subset)
    return array

def get_distance_str(string1,string2):
    raw_distance = editdistance.eval(string1,string2) #the higher the number, the further apart they are
    #convert raw distance so that a 1.0 means they are identical, and 0.0 means the two strings are 51 operations apart
    #51 is the maximum distance apart for comparing two 51-character length strings
    return (51-raw_distance)/51

def get_distance(string,subset):
    array = np.random.rand(subset.shape[0])
    for i in range(subset.shape[0]):
        array[i] = get_distance_str(string,subset[i])
    return array

def get_distance_matrix(training_set,sigma_subset):
    array = np.random.rand(training_set.shape[0],sigma_subset.shape[0])
    for i in range(training_set.shape[0]):
        if i % 100 == 0:
            print(i)
        array[i,:] = get_distance(training_set[i],sigma_subset)
    return array

def convert_to_AA(dna_sequence,dictionary):
    pass
def get_all_AA(dna_sequence):
    dictionary = {} #to fill in
    AA_list = []
    for i in range(3):
        AA_list.append(convert_to_AA(dna_sequence[i:],dictionary))
    return AA_list

def cluster_compare(sigma_vector,matrix):
    #a way to evaluate whether our feature engineering produced any meaningful features that can be used to distinguish between different sigma factors
    #cluster the matrix and check the cluster labels for the sample rows in which the ground truth is 1
    #ideally, they should all be in the same cluster;
    #i.e. the more samples that have the same cluster label, the more likely our similarity_matrix has meaningful features
    #i.e. the better the string comparison function we used
    e = ((15530020.81200376 + 12489561.48592462 + 7567121.666848466 + 5327285.068442004)/5774901)/4
    model = DBSCAN(eps=15530020.81200376/5774901,min_samples=50)
    cluster_labels = model.fit_predict(matrix)
    #return the cluster assignments and counts for each sample row with ground truth 1, then do the same for sample rows with ground truth 0
    return np.unique(cluster_labels[sigma_vector==1],return_counts=True),np.unique(cluster_labels[sigma_vector==0],return_counts=True)

if __name__ == '__main__':
    sigma_headers,sigma_data,sequence_data = load_train()
    subset_list = get_subsets(sigma_data,sequence_data)   

##    distance_matrix0 = get_distance_matrix(sequence_data,subset_list[0])
##    distance_matrix1 = get_distance_matrix(sequence_data,subset_list[1])
##    distance_matrix2 = get_distance_matrix(sequence_data,subset_list[2])
##    distance_matrix3 = get_distance_matrix(sequence_data,subset_list[3])
##    distance_matrix4 = get_distance_matrix(sequence_data,subset_list[4])
##    np.savetxt('distance_matrix0.tsv',distance_matrix0,delimiter='\t')
##    np.savetxt('distance_matrix1.tsv',distance_matrix1,delimiter='\t')
##    np.savetxt('distance_matrix2.tsv',distance_matrix2,delimiter='\t')
##    np.savetxt('distance_matrix3.tsv',distance_matrix3,delimiter='\t')
##    np.savetxt('distance_matrix4.tsv',distance_matrix4,delimiter='\t')
    distance_matrix0 = np.loadtxt('distance_matrix0.tsv')
    distance_matrix1 = np.loadtxt('distance_matrix1.tsv')
    distance_matrix2 = np.loadtxt('distance_matrix2.tsv')
    distance_matrix3 = np.loadtxt('distance_matrix3.tsv')
    distance_matrix4 = np.loadtxt('distance_matrix4.tsv')
    
    sequence_test = load_test()
##    test_matrix0 = get_distance_matrix(sequence_test,subset_list[0])
##    test_matrix1 = get_distance_matrix(sequence_test,subset_list[1])
##    test_matrix2 = get_distance_matrix(sequence_test,subset_list[2])
##    test_matrix3 = get_distance_matrix(sequence_test,subset_list[3])
##    test_matrix4 = get_distance_matrix(sequence_test,subset_list[4])
##    np.savetxt('test_matrix0.tsv',test_matrix0,delimiter='\t')
##    np.savetxt('test_matrix1.tsv',test_matrix1,delimiter='\t')
##    np.savetxt('test_matrix2.tsv',test_matrix2,delimiter='\t')
##    np.savetxt('test_matrix3.tsv',test_matrix3,delimiter='\t')
##    np.savetxt('test_matrix4.tsv',test_matrix4,delimiter='\t')
    test_matrix0 = np.loadtxt('test_matrix0.tsv')
    test_matrix1 = np.loadtxt('test_matrix1.tsv')
    test_matrix2 = np.loadtxt('test_matrix2.tsv')
    test_matrix3 = np.loadtxt('test_matrix3.tsv')
    test_matrix4 = np.loadtxt('test_matrix4.tsv')


    #OTHER IDEAS THAT DIDN'T WORK / I DIDN'T EXPLORE FULLY
    
##    base_content_matrix = get_base_content(sequence_data) 

##    similarity_matrix0 = get_similarity_matrix(sequence_data,subset_list[0])
##    similarity_matrix1 = get_similarity_matrix(sequence_data,subset_list[1])
##    similarity_matrix2 = get_similarity_matrix(sequence_data,subset_list[2])
##    similarity_matrix3 = get_similarity_matrix(sequence_data,subset_list[3])
##    np.savetxt('similarity_matrix0.tsv',similarity_matrix0,delimiter='\t')
##    np.savetxt('similarity_matrix1.tsv',similarity_matrix1,delimiter='\t')
##    np.savetxt('similarity_matrix2.tsv',similarity_matrix2,delimiter='\t')
##    np.savetxt('similarity_matrix3.tsv',similarity_matrix3,delimiter='\t')
##    similarity_matrix0 = np.loadtxt('similarity_matrix0.tsv')
##    similarity_matrix1 = np.loadtxt('similarity_matrix1.tsv')
##    similarity_matrix2 = np.loadtxt('similarity_matrix2.tsv')
##    similarity_matrix3 = np.loadtxt('similarity_matrix3.tsv')
##
##    sm0 = cluster_compare(sigma_data[:,0],similarity_matrix0)
##    sm1 = cluster_compare(sigma_data[:,1],similarity_matrix1)
##    sm2 = cluster_compare(sigma_data[:,2],similarity_matrix2)
##    sm3 = cluster_compare(sigma_data[:,3],similarity_matrix3)
##    
##    ld0 = cluster_compare(sigma_data[:,0],distance_matrix0)
##    ld1 = cluster_compare(sigma_data[:,1],distance_matrix1)
##    ld2 = cluster_compare(sigma_data[:,2],distance_matrix2)
##    ld3 = cluster_compare(sigma_data[:,3],distance_matrix3)

    

