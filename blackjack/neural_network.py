import torch
import torch.nn as nn
import torch.nn.functional as F
from data_generation import *

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(15,8)
##        self.fc2 = nn.Linear(8,8)
##        self.fc3 = nn.Linear(8,8)
##        self.fc4 = nn.Linear(8,8)
##        self.fc5 = nn.Linear(8,8)
##        self.fc6 = nn.Linear(8,8)
##        self.fc7 = nn.Linear(8,8)
##        self.fc8 = nn.Linear(8,8)
##        self.fc9 = nn.Linear(8,8)
        self.fc10 = nn.Linear(8, 4)

    def forward(self, x):
        x = F.relu(self.fc1(x))
##        x = F.relu(self.fc2(x))
##        x = F.relu(self.fc3(x))
##        x = F.relu(self.fc4(x))
##        x = F.relu(self.fc5(x))
##        x = F.relu(self.fc6(x))
##        x = F.relu(self.fc7(x))
##        x = F.relu(self.fc8(x))
##        x = F.relu(self.fc9(x))
        x = F.softmax(self.fc10(x),dim=1)
        return x

def train(net,training_set,truth,alpha=0.01,max_iter=1000):
    param = list(net.parameters())
    cost = nn.MSELoss()
    i = 0

    while i <= max_iter:
        out = cost(net(training_set),truth)
        if i % 1000 == 0:
            print('Iteration: {}, Cost: {}'.format(i,out))
        net.zero_grad()
        out.backward()
        for p in param:
            p.data -= p.grad.data*alpha
        i += 1

def train_batch(net,alpha=0.01,max_iter=10000,min_deck=20,max_deck=52):
    #call train function for each deck size between min_deck and max_deck (inclusive)
    deck = Deck()
    player = Player('Bob')
    dealer = Dealer()
    for deck_size in range(min_deck,max_deck+1):
        print('Generating data for deck_size {}...'.format(deck_size))
        feature_list,truth_vector = simulate_rounds(deck,deck_size,player,dealer,n=1) #list of list[features,truth]
        training_set = torch.Tensor(feature_list)
        truth = torch.Tensor(truth_vector)
        print('Training for deck_size {}...'.format(deck_size))
        train(net,training_set,truth,alpha,max_iter)
        print()

def generate_data(deck_size=52):
    deck = Deck()
    player = Player('Bob')
    dealer = Dealer()
    feature_list,truth_vector = simulate_rounds(deck,deck_size,player,dealer,n=1) #list of list[features,truth]
    return torch.Tensor(feature_list),torch.Tensor(truth_vector)

def test(net,training_set,truth):
    #test accuracy by comparing predicted value with truth
    predicted_truth = net(training_set)
    predicted_truth = torch.argmax(predicted_truth,dim=1) #[index of highest value for sample row 1, ... sample row 2, ... ,]
    #because there are ties possible, we use torch.argwhere to find indices of all columns that aren't 0
    truth = np.argwhere(truth.numpy()) #first column is the index of the row, second column is an index of the column in which the value was not 0
    correct = 0
    #iterate through every
    for i in range(predicted_truth.shape[0]):
        #for row i, subset for the indices in that row for which the column values were not equal to 0
        if predicted_truth[i] in truth[truth[:,0]==i,1]:
            #if the predicted value is in that subset, then the AI predicted correctly
            correct += 1
    return correct/predicted_truth.shape[0]
    
        

if __name__ == '__main__':
    net = Net()
    while True:
        train_batch(net,alpha=1,max_iter=10000,min_deck=20,max_deck=52)
    
    #data sets are generated randomly (essentially test sets)
    training_set,truth = generate_data(deck_size=52)
    print(test(net,training_set,truth))

    

    
    

    
    

    
