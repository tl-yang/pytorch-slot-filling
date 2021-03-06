# coding=utf8
import torch
import torch.nn as nn
from torch import optim

from data_util import load_data
from model import SlotRNN
from evaluate import conlleval

embedding_size = 100
n_epochs = 20
learning_rate = 0.01

def var2np(variable):
    return torch.max(variable, 1)[1].data.squeeze(1).numpy()

def train():
    train_dataset, val_dataset = load_data()

    model = SlotRNN(train_dataset.vocab_size, embedding_size, train_dataset.n_classes)
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    criterion = nn.NLLLoss()
    print (model)

    for epoch in range(n_epochs):
        # get batch data
        print_loss = 0
        train_pred_label = []
        for data_x, data_y in train_dataset:
            # zero_grad
            optimizer.zero_grad()
            #forward
            pred = model(data_x)
            train_pred_label.append(var2np(pred))
            # compute loss
            loss = criterion(pred, data_y)
            print_loss += loss.data[0]
            # backward
            loss.backward()
            optimizer.step()

        # print ('epoch: (%d / %d) loss: %.4f' % (epoch+1, n_epochs, print_loss/len(train_dataset)))
        train_pred = [list(map(lambda x: train_dataset.idx2labels[x], y)) for y in train_pred_label]
        eval(model, train_dataset, train_pred)
        eval(model, val_dataset)

def eval(model, dataset, pred_res=None):
    model.eval()
    if pred_res is None:
        pred_label = []
        for data_x, data_y in dataset:
            pred = model(data_x)
            pred_label.append(var2np(pred))
        pred_res = [list(map(lambda x: dataset.idx2labels[x], y)) for y in pred_label]
    print conlleval(pred_res, dataset.groundtruth, dataset.words, 'tmp.txt')
    model.train()

if __name__ == '__main__':
    train()
