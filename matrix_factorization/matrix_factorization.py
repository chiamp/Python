##the journey
##- realized that the derivative without the dependent variable should be 0
##    - which simplified the differentiation
##- forgot that i shouldn't use the zero entries to calculate the gradient
##- realized i had to change the cost function to exclude the 0 entries
##    - or else the cost function would go up, as my program would optimize the matrix product without caring about the 0 entry points
##- FINAL UPDATE: was able to fully vectorize my code, so it runs a lot faster!

import numpy as np

def cost(R,P,Qt,null_value):
    D_prime = R-np.dot(P,Qt)
    index = np.where(R==null_value) #find the indices in which R is the null value
    D_prime[index[0],index[1]] = 0 #assign these entries to 0 as they should not contribute anything when calculating the gradient
    return np.sum(D_prime**2) + np.sum(P**2) + np.sum(Qt**2) #include L2 regularization

def get_P_gradient(R,P,Qt,lamb,null_value=0):
    #R is dim ixj
    #P is dim ixk
    #Qt is dim kxj
    D_prime = R-np.dot(P,Qt) #dim ixj
    index = np.where(R==null_value) #find the indices in which R is the null value
    D_prime[index[0],index[1]] = 0 #assign these entries to 0 as they should not contribute anything when calculating the gradient
    #include L2 regularization and lambda parameter
    return -2*np.dot(D_prime,Qt.T) + lamb*2*P #dim ixk, which is the dimension of P

def get_Qt_gradient(R,P,Qt,lamb,null_value=0):
    #R is dim ixj
    #P is dim ixk
    #Qt is dim kxj
    D_prime = R-np.dot(P,Qt) #dim ixj
    index = np.where(R==null_value) #find the indices in which R is the null value
    D_prime[index[0],index[1]] = 0 #assign these entries to 0 as they should not contribute anything when calculating the gradient
    #include L2 regularization and lambda parameter
    return -2*np.dot(P.T,D_prime) + lamb*2*Qt #dim kxj, which is the dimension of Qt

def gradient_descent(R,P,Qt,lamb=1e-1,alpha=1e-3,max_iter=30000,null_value=0):
    #null_value is whatever value represents that there is no data present for that entry
    i = 0
    while i < max_iter:
##        if i % 10 == 0:
##            print('Iteration: {}, Cost: {}'.format(i,cost(R,P,Qt,null_value)))
        P -= alpha*get_P_gradient(R,P,Qt,lamb,null_value)
        Qt -= alpha*get_Qt_gradient(R,P,Qt,lamb,null_value)
        i += 1

def subset_validation_set(R,percentage=0.1,null_value=0):
    #subset the dataset R by making a copy and randomly picking indices and setting them to the null_value, so that they don't contribute to the gradient
    #then return the indices and the correpsonding original values so that they can be used for validation testing
    Rv = R.copy()
    index = np.where(Rv!=null_value)
    length = len(index[0]) #the number of non-null values in matrix R
    exclude = int(np.ceil(length*percentage)) #how many to exclude from training
    i = np.random.choice([x for x in range(length)],size=exclude,replace=False) #randomly select indices for exclusion
    original_values = Rv[index[0][i],index[1][i]]
    Rv[index[0][i],index[1][i]] = null_value
    return Rv,[index[0][i],index[1][i]],original_values #return indices,original_values

def compare_validation(PQt,indices,original_values):
    #return squared error between fitted values in reconstructed matrix PQt and original_values
    return np.sum((PQt[indices[0],indices[1]]-original_values)**2)

def get_best_k(R,start=1,stop=10,repeat=100,percentage=0.1,null_value=0,alpha=1e-3,max_iter=30000):
    #get the best k value; i.e. the number of latent features k such that it minimizes the error between training and validation sets
    #start and stop are the range
    #repeat is the number of times to repeat validation testing for a specific number k to get an average error
    #the rest of the arguments are for subset_validation_test() and gradient_descent()
    results = []
    for k in range(start,stop):
        total_cost = 0
        for x in range(1,repeat+1):
            if x % 25 == 0:
                print('Testing for k value: {}, Iteration: {}'.format(k,x))
            i = R.shape[0]
            j = R.shape[1]
            P = np.random.rand(i,k)
            Q = np.random.rand(j,k)
            Qt = Q.T

            Rv,indices,original_values = subset_validation_set(R,percentage=percentage,null_value=null_value)
            gradient_descent(Rv,P,Qt,alpha=alpha,max_iter=max_iter,null_value=null_value)
            total_cost += compare_validation(np.dot(P,Qt),indices,original_values)
        results.append([k,total_cost/repeat])
    return np.array(results) #format k_value,average_cost

def bucket_range(results,r=4):
    #assume results are sorted in increasing order
    #r is the range of each bucket
    range_list = []
    for i in range(r,results.shape[0]+1):
        subset = results[i-r:i,1] #subset data for that specific bucket range
        range_list.append(['{} to {}'.format(results[i-r,0],results[i-1,0]),np.sum(subset)/subset.shape[0]])
    return np.array(range_list)
    

if __name__ == '__main__':
    #http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/
    R = np.array([
     [5,3,0,1],
     [4,0,0,1],
     [1,1,0,5],
     [1,0,0,4],
     [0,1,5,4],
    ])
    R = np.array([
     [5,3,0,2,1],
     [4,0,3,0,1],
     [1,1,0,3,5],
     [1,2,0,0,4],
     [0,0,1,5,4],
    ])

    k = 3
    P = np.random.rand(R.shape[0],k)
    Qt = np.random.rand(k,R.shape[1])
    gradient_descent(R,P,Qt,lamb=1e-1)
    print(R)
    print(np.dot(P,Qt))

##    results = get_best_k(R,start=1,stop=20,repeat=50,percentage=0.1,null_value=0,alpha=1e-3,max_iter=20000)
##    print(results[np.argsort(results[:,1]),:])
##    range_list = bucket_range(results,r=4)
##    print(range_list[np.argsort(range_list[:,1].astype(float)),:])
