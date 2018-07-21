import numpy as np
from keras.models import load_model
from data_manipulation import load_train,load_test
from sklearn.metrics import roc_auc_score

def flatten(x):
    #flatten predicted array to binary outputs
    if x >= 0.5:
        return 1
    else:
        return 0

def model_predict(model_list,test_set,flatten_func):
    sigma_0_pred = model_list[0].predict(test_set[0])
    sigma_1_pred = model_list[1].predict(test_set[1])
    sigma_2_pred = model_list[2].predict(test_set[2])
    sigma_3_pred = model_list[3].predict(test_set[3])
    sigma_4_pred = model_list[4].predict(test_set[4])
    pred_array = np.concatenate((sigma_0_pred,sigma_1_pred,sigma_2_pred,sigma_3_pred,sigma_4_pred),axis=1)
    return flatten_func(pred_array)

def accuracy(pred_array,truth_array):
    return np.sum(pred_array==truth_array)/pred_array.size

def write_to_csv(array,headers,filename='predictions'):
    #write array to csv file with headers in the first row
    array_with_header = np.append(headers,array,axis=0)
    id_column = np.array(['id'] + [i for i in range(3399,4532+1)]).reshape(-1,1)
    final_array = np.append(id_column,array_with_header,axis=1)
    np.savetxt(filename+'.csv',final_array,delimiter=',',fmt='%s') #,header='id,RPOS,RPOD,RPOH,RPON,RPOF')

if __name__ == '__main__':
    model0 = load_model('model0.h5')
    model1 = load_model('model1.h5')
    model2 = load_model('model2.h5')
    model3 = load_model('model3.h5')
    model4 = load_model('model4.h5')
    model_list = [model0,model1,model2,model3,model4]

    sigma_headers,sigma_data,sequence_data = load_train()

##    distance_matrix0 = np.loadtxt('distance_matrix0.tsv')
##    distance_matrix1 = np.loadtxt('distance_matrix1.tsv')
##    distance_matrix2 = np.loadtxt('distance_matrix2.tsv')
##    distance_matrix3 = np.loadtxt('distance_matrix3.tsv')
##    distance_matrix4 = np.loadtxt('distance_matrix4.tsv')
##    training_set = [distance_matrix0,distance_matrix1,distance_matrix2,distance_matrix3,distance_matrix4]
##    pred_array = model_predict(model_list,training_set,np.vectorize(flatten))
##    print(accuracy(pred_array,sigma_data))
##    print(roc_auc_score(sigma_data,pred_array))

    test_matrix0 = np.loadtxt('test_matrix0.tsv')
    test_matrix1 = np.loadtxt('test_matrix1.tsv')
    test_matrix2 = np.loadtxt('test_matrix2.tsv')
    test_matrix3 = np.loadtxt('test_matrix3.tsv')
    test_matrix4 = np.loadtxt('test_matrix4.tsv')
    test_set = [test_matrix0,test_matrix1,test_matrix2,test_matrix3,test_matrix4]
    pred_array = model_predict(model_list,test_set,np.vectorize(flatten))

    sigma_headers = np.array(sigma_headers).reshape(1,-1)
    write_to_csv(pred_array,sigma_headers,filename='predictions')
    
