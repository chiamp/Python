import numpy as np
from data_manipulation import *
from feature_engineering import get_similarity_matrix,get_distance_matrix
from keras.models import Sequential,load_model
from keras.layers import Dense,Activation
from keras import metrics,optimizers

def accuracy(model,training_set,truth):
    predicted = model.predict(training_set)
    predicted = np.apply_along_axis(flatten,0,predicted.reshape(1,-1))
    return np.sum(predicted==truth)/predicted.shape[0]

def flatten(x):
    #flatten predicted array to binary outputs
    if x >= 0.5:
        return 1
    else:
        return 0

def random_sample(feature_matrix,sigma_vector):
    #return a subset of feature_matrix such that half of the samples contain truth value 1
    #and half of the samples contain truth value 0 (randomly sampled)
    #return the corresponding truth vector of the new subset
    keep_ones = np.where(sigma_vector==1)[0]
    keep_zeros = np.where(sigma_vector==0)[0]
    if keep_ones.size > keep_zeros.size:
        keep_ones = np.random.choice(keep_ones,size=keep_zeros.size,replace=False)
    else:
        keep_zeros = np.random.choice(keep_zeros,size=keep_ones.size,replace=False)
    indices = np.append(keep_ones,keep_zeros)
    return feature_matrix[indices,:],sigma_vector[indices]

def random_sample_gradient_descent(model,feature_matrix,sigma_vector,epochs=4600,max_iter=1000):
    #perform gradient descent on a randomly sampled subset of the feature_matrix, repeated for max_iter iterations
    #the subset will contain all sample rows that have a truth value of 1
    #the subset will contain an equal amount of sample rows with a truth value of 0 (randomly sampled)
    training_set,training_truth,validation_set,validation_truth = get_validation_set(feature_matrix,sigma_vector,percentage=0.1)
    i = 1
    while i <= max_iter:
        print('=== ITERATION {} ==='.format(i))
        sampled_training,sampled_truth = random_sample(training_set,training_truth)
        model.fit(sampled_training, sampled_truth, validation_data=(validation_set,validation_truth), epochs=epochs, batch_size=sampled_training.shape[0], verbose=0)
        i += 1

def get_validation_set(feature_matrix,sigma_vector,percentage=0.1):
    #split the feature_matrix into a training_set and a validation_set
    #split the sigma_vector into corresponding ground truths for training_set and validation_set
    keep_ones = np.where(sigma_vector==1)[0]
    keep_zeros = np.where(sigma_vector==0)[0]
    keep_ones = np.random.choice(keep_ones,size=int(np.ceil(keep_ones.size*percentage)),replace=False)
    keep_zeros = np.random.choice(keep_zeros,size=int(np.ceil(keep_zeros.size*percentage)),replace=False)
    validation_indices = np.append(keep_ones,keep_zeros)
    training_indices = np.logical_not(np.isin(np.array([i for i in range(sigma_vector.shape[0])]),validation_indices))
    #return training_set,training_truth,validation_set,validation_truth
    return feature_matrix[training_indices,:],sigma_vector[training_indices],feature_matrix[validation_indices,:],sigma_vector[validation_indices]

def train(training_set,ground_truth,epochs=3000,max_iter=15):
    #instantiate, train, and return the model
    model = Sequential([
        Dense(500,activation='relu',input_shape=(training_set.shape[1],)),
        Dense(500,activation='relu'),
        Dense(1,activation='sigmoid')
    ])
    sgd = optimizers.SGD(lr=1e-3, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd,loss='binary_crossentropy',metrics=[metrics.binary_accuracy])
    random_sample_gradient_descent(model,training_set,ground_truth,epochs=epochs,max_iter=max_iter)
    return model

if __name__ == '__main__':
    sigma_headers,sigma_data,sequence_data = load_train()
    
    distance_matrix0 = np.loadtxt('distance_matrix0.tsv')
    distance_matrix1 = np.loadtxt('distance_matrix1.tsv')
    distance_matrix2 = np.loadtxt('distance_matrix2.tsv')
    distance_matrix3 = np.loadtxt('distance_matrix3.tsv')
    distance_matrix4 = np.loadtxt('distance_matrix4.tsv')
    
    training_set = distance_matrix0
    ground_truth = sigma_data[:,0]
    model = train(training_set,ground_truth,epochs=6000,max_iter=10)
    model.save('model0.h5')
    print('Accuracy of model, testing with training set: {}'.format(accuracy(model,training_set,ground_truth)))

    training_set = distance_matrix1
    ground_truth = sigma_data[:,1]
    model = train(training_set,ground_truth,epochs=3000,max_iter=10)
    model.save('model1.h5')
    print('Accuracy of model, testing with training set: {}'.format(accuracy(model,training_set,ground_truth)))

    training_set = distance_matrix2
    ground_truth = sigma_data[:,2]
    model = train(training_set,ground_truth,epochs=3000,max_iter=10)
    model.save('model2.h5')
    print('Accuracy of model, testing with training set: {}'.format(accuracy(model,training_set,ground_truth)))

    training_set = distance_matrix3
    ground_truth = sigma_data[:,3]
    model = train(training_set,ground_truth,epochs=3000,max_iter=10)
    model.save('model3.h5')
    print('Accuracy of model, testing with training set: {}'.format(accuracy(model,training_set,ground_truth)))

    training_set = distance_matrix4
    ground_truth = sigma_data[:,4]
    model = train(training_set,ground_truth,epochs=3000,max_iter=10)
    model.save('model4.h5')
    print('Accuracy of model, testing with training set: {}'.format(accuracy(model,training_set,ground_truth)))

