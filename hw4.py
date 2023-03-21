# -*- coding: utf-8 -*-
"""Hw4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rIiPUnPFAsTmG_h9rm4CWsPXzQfZEMay
"""

import numpy as np
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import torch
import time

#Clubs all transforms together
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.5,), (0.5,)),
                                ])
input_size = 784
hidden_layer_size = 300
output_size = 10
losses = []
accuracies = []

class MyNeuralModel():
    def __init__(self, sizes, epochs=20, alpha=0.01):
        self.sizes = sizes
        self.epochs = epochs
        self.alpha = alpha
        self.init_params()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def softmax(self, x):
        exes = np.exp(x)
        deno = np.sum(exes, axis=1)
        deno.resize(exes.shape[0], 1)
        return exes / deno

    def init_params(self):
        input_layer = int(self.sizes[0])
        hidden_1 = int(self.sizes[1])
        hidden_2 = int(self.sizes[2])
        output_layer = int(self.sizes[3])
        # Random initialization of weights between -1 and 1
        self.w1 = np.random.uniform(low=-1, high=1, size=(input_layer, hidden_1))
        self.w2 = np.random.uniform(low=-1, high=1, size=(hidden_1, hidden_2))
        self.w3 = np.random.uniform(low=-1, high=1, size=(hidden_2, output_layer))
        # Zero initialization of weights
        # self.w1 = np.zeros((input_layer, hidden_1))
        # self.w2 = np.zeros((hidden_1, hidden_2))
        # self.w2 = np.zeros((hidden_,2 output_layer))

    def forward(self, inputs):
        inputs = inputs.numpy()
        self.linear_1 = inputs.dot(self.w1)
        self.out1 = self.sigmoid(self.linear_1)
        self.linear_2 = self.out1.dot(self.w2)
        self.out2 = self.sigmoid(self.linear_2)
        self.linear3=self.out2.dot(self.w3)
        self.out3 = self.softmax(self.linear3)
        return self.out3

    def backward(self, x_train, y_train, output):
        x_train = x_train.numpy()
        y_train = y_train.numpy()
        batch_size = y_train.shape[0]
        d_loss = output - y_train
        delta_w3 = (1. / batch_size) * np.matmul(self.out2.T, d_loss)
        d_out_1 = np.matmul(d_loss, self.w3.T)
        d_linear_2 = d_out_1 * self.sigmoid(self.linear_2) * (1 - self.sigmoid(self.linear_2))
        delta_w2 = (1. / batch_size) * np.matmul(self.out1.T, d_linear_2)
        d_out_2 = np.matmul(d_linear_2, self.w2.T)
        d_linear_1 = d_out_2 * self.sigmoid(self.linear_1) * (1 - self.sigmoid(self.linear_1))
        delta_w1 = (1. / batch_size) * np.matmul(x_train.T, d_linear_1)
        return delta_w1, delta_w2 ,delta_w3

    def update_weights(self, w1_update, w2_update,w3_update):
        self.w1 -= self.alpha * w1_update
        self.w2 -= self.alpha * w2_update
        self.w3 -=self.alpha * w3_update

    def calculate_loss(self, y, y_hat):
        batch_size = y.shape[0]
        y = y.numpy()
        loss = np.sum(np.multiply(y, np.log(y_hat)))
        loss = -(1. / batch_size) * loss
        return loss

    def calculate_metrics(self, data_loader):
        losses = []
        correct = 0
        total = 0

        for i, data in enumerate(data_loader):
            x, y = data
            y_onehot = torch.zeros(y.shape[0], 10)
            y_onehot[range(y_onehot.shape[0]), y] = 1
            flattened_input = x.view(-1, 28 * 28)
            output = self.forward(flattened_input)
            predicted = np.argmax(output, axis=1)
            correct += np.sum((predicted == y.numpy()))
            total += y.shape[0]
            loss = self.calculate_loss(y_onehot, output)
            losses.append(loss)
        return (correct / total), np.mean(np.array(losses))

    def train(self, train_loader, data_loader):
        start_time = time.time()
        global losses, accuracies
        for iteration in range(self.epochs):
            for i, data in enumerate(train_loader):
                x, y = data
                y_onehot = torch.zeros(y.shape[0], 10)
                y_onehot[range(y_onehot.shape[0]), y] = 1
                flat_input = x.view(-1, 28 * 28)
                output = self.forward(flat_input)
                w1_update, w2_update, w3_update = self.backward(flat_input, y_onehot, output)
                self.update_weights(w1_update, w2_update,w3_update)
            accuracy, loss = self.calculate_metrics(data_loader)
            losses.append(loss)
            accuracies.append(accuracy)
            print('Epoch: {0}, Test Error Percent: {1:.2f}, Loss: {2:.2f}'.format(
                iteration + 1, 100 - accuracy * 100, loss
            ))

model = MyNeuralModel(sizes=[784, 300, 200, 10], epochs=50)
batchsize=32
trainset = datasets.MNIST('./dataset/MNIST/', download=True, train=True, transform=transform)
testset = datasets.MNIST('./dataset/MNIST/', download=True, train=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batchsize, shuffle=True)
dataloader = torch.utils.data.DataLoader(testset, batch_size=batchsize, shuffle=True)

examples = enumerate(testset)
batch_idx, (example_data, example_targets) = next(examples)
print(example_data.shape)

import matplotlib.pyplot as plt
fig = plt.figure()
plt.subplot(2,3,1)
plt.tight_layout()
plt.imshow(example_data[0], cmap='gray', interpolation='none')
plt.xticks([])
plt.yticks([])

"""#Question 3
##Part 2
α=0.01, \\
BatchSize = 32, \\
Epochs = 50, \\
Initialised randomly between -1 and 1

"""

model.train(train_loader=trainloader, data_loader=dataloader)

plt.xlabel('Epochs')
plt.ylabel('Test Loss')
plt.plot(losses)
plt.show()

"""##Part 2
α=0.01 \\
BatchSize=64 \\
Epochs = 50 \\


"""

model = MyNeuralModel(sizes=[784, 300, 200, 10], epochs=50)
batchsize=64
trainset = datasets.MNIST('./dataset/MNIST/', download=True, train=True, transform=transform)
testset = datasets.MNIST('./dataset/MNIST/', download=True, train=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batchsize, shuffle=True)
dataloader = torch.utils.data.DataLoader(testset, batch_size=batchsize, shuffle=True)
model.train(train_loader=trainloader, data_loader=dataloader)

plt.xlabel('Epochs')
plt.ylabel('Test Loss')
plt.plot(losses[50:])
plt.show()

"""##Part 2
α=0.001 \\
BatchSize= 32 \\
Epochs= 50

"""

model = MyNeuralModel(sizes=[784, 300, 200, 10], alpha=0.001,epochs=50)
batchsize=32
trainset = datasets.MNIST('./dataset/MNIST/', download=True, train=True, transform=transform)
testset = datasets.MNIST('./dataset/MNIST/', download=True, train=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batchsize, shuffle=True)
dataloader = torch.utils.data.DataLoader(testset, batch_size=batchsize, shuffle=True)
model.train(train_loader=trainloader, data_loader=dataloader)

plt.xlabel('Epochs')
plt.ylabel('Test Loss')
plt.plot(losses[100:])
plt.show()

"""##Part 3
Implementing using all Pytorch functionalities
α=0.01, \\
BatchSize = 32, \\
Epochs = 50, \\
Initialised randomly between -1 and 1
"""

bsize=32
rate=0.01
transform = transforms.Compose([transforms.ToTensor(),
  transforms.Normalize((0.5,), (0.5,))
])
trainset = torchvision.datasets.MNIST('data', train=True, transform=transform, download=True)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=bsize, shuffle=True)

testset = torchvision.datasets.MNIST('data', train=True, transform=transform, download=True)
testloader = torch.utils.data.DataLoader(testset, batch_size=bsize, shuffle=True)

input_size = trainloader.dataset.train_data.shape[1] * trainloader.dataset.train_data.shape[2]
hidden_layers = [300,200]
output_size = 10

def init_weights(m):
  if type(m) == nn.Linear:
    torch.nn.init.uniform_(m.weight,-1.0,1.0)
    #torch.nn.init.zeros_(m.weight)


model = nn.Sequential(
    nn.Linear(input_size, hidden_layers[0]),
    nn.Sigmoid(),
    nn.Linear(hidden_layers[0], hidden_layers[1]),
    nn.Sigmoid(),
    nn.Linear(hidden_layers[1], output_size),
    nn.LogSoftmax(dim=1)
)
model.apply(init_weights)
print(model)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=rate)

epochs = 50
lossesPy = []
for e in range(epochs):
    running_loss = 0
    for x, y in trainloader:
        
        x = x.view(x.shape[0], -1)
        
        # setting gradient to zeros
        optimizer.zero_grad()        
        output = model(x)
        loss = criterion(output, y)
        
        # backward propagation
        loss.backward()
        
        # update the gradient to new gradients
        optimizer.step()
        running_loss += loss.item()
    else:
        print("Epoch: ",e+1)
        print("Running loss: ",(running_loss/len(trainloader)))
        lossesPy.append(running_loss/len(trainloader))


correct=0
with torch.no_grad():
  for images,labels in testloader:
    logps = model(images.view(images.shape[0], -1))
    output = torch.squeeze(logps)
    pred = output.data.max(1, keepdim=True)[1]
    correct += pred.eq(labels.data.view_as(pred)).sum()
  print('\nAccuracy Percent: {}/{} ({:.0f})\n'.format(correct, len(testloader.dataset),
            100. * correct / len(testloader.dataset)))
  print('\nTest Error Percent: ({:.0f})\n'.format(100 - 100. * correct / len(testloader.dataset)))  

plt.xlabel('Epochs')
plt.ylabel('Test Loss')
plt.plot(lossesPy)
plt.show()


"""##Part 4
Initialising with 0

"""

def pytorchzero(bsize,rate):
  transform = transforms.Compose([transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
  ])
  trainset = torchvision.datasets.MNIST('data', train=True, transform=transform, download=True)
  trainloader = torch.utils.data.DataLoader(trainset, batch_size=bsize, shuffle=True)

  testset = torchvision.datasets.MNIST('data', train=True, transform=transform, download=True)
  testloader = torch.utils.data.DataLoader(testset, batch_size=bsize, shuffle=True)

  input_size = trainloader.dataset.train_data.shape[1] * trainloader.dataset.train_data.shape[2]
  hidden_layers = [300,200]
  output_size = 10

  def init_weights(m):
    if type(m) == nn.Linear:
      #Initialise with zero
      torch.nn.init.zeros_(m.weight)


  model = nn.Sequential(
      nn.Linear(input_size, hidden_layers[0]),
      nn.Sigmoid(),
      nn.Linear(hidden_layers[0], hidden_layers[1]),
      nn.Sigmoid(),
      nn.Linear(hidden_layers[1], output_size),
      nn.LogSoftmax(dim=1)
  )
  model.apply(init_weights)
  print(model)
  criterion = nn.CrossEntropyLoss()
  optimizer = optim.SGD(model.parameters(), lr=rate)

  epochs = 50
  lossesPy = []
  for e in range(epochs):
      running_loss = 0
      for x, y in trainloader:
          
          x = x.view(x.shape[0], -1)
          
          # setting gradient to zeros
          optimizer.zero_grad()        
          output = model(x)
          loss = criterion(output, y)
          
          # backward propagation
          loss.backward()
          
          # update the gradient to new gradients
          optimizer.step()
          running_loss += loss.item()
      else:
          print("Epoch: ",e+1)
          print("Running loss: ",(running_loss/len(trainloader)))
          lossesPy.append(running_loss/len(trainloader))


  correct=0
  with torch.no_grad():
    for images,labels in testloader:
      logps = model(images.view(images.shape[0], -1))
      output = torch.squeeze(logps)
      pred = output.data.max(1, keepdim=True)[1]
      correct += pred.eq(labels.data.view_as(pred)).sum()
    print('\nAccuracy Percent: {}/{} ({:.0f})\n'.format(correct, len(testloader.dataset),
              100. * correct / len(testloader.dataset)))
    print('\nTest Error Percent: ({:.0f})\n'.format(100 - 100. * correct / len(testloader.dataset)))  

  plt.xlabel('Epochs')
  plt.ylabel('Test Loss')
  plt.plot(lossesPy)
  plt.show()

"""α=0.01, \\
BatchSize = 32, \\
Epochs = 50, \\
Initialised 0
"""

pytorchzero(32,0.01)

"""α=0.01, \\
BatchSize = 64, \\
Epochs = 50, \\
Initialised randomly 0
"""

pytorchzero(64,0.01)