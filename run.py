import argparse
import csv
from model import Model
import random
from test import test
from train import train



# Sets arguments to accept
# data, mode
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--data")
argparser.add_argument("-m", "--mode", choices=["train", "test"])
args = argparser.parse_args()



# Retrieving data from path
with open(args.data, mode="r", encoding="utf-8") as file:
    data = csv.DictReader(file)
    data = list(data)

# Shuffle data
random.shuffle(data)

# Split data
train_ratio = 0.8
split_index = int(len(data) * train_ratio)
train_data = data[:split_index]
test_data = data[split_index:]



# List of aspects
# Consists of political topics
aspects = ["Conservative", "Democrat", "Illegal", "Immigrant", "Illegal Immigrant", "Immigration", "Liberal", "Republican", "Terrorist", "Trump"]



# Creating model
model = Model(aspects)

if args.mode == "train":
    train(model, train_data)
    print(model.aspect_correlation_matrix)

elif args.mode == "test":
    print(f"Accuracy: {test(model, test_data)}")