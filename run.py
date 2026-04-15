import argparse
from model import Model



# Sets arguments to accept
# data
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--data")
args = argparser.parse_args()



model = Model(args.data)
model.train()
model.test()