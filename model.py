import csv



class Model:

    def __init__(self, path):
        with open("data.csv", mode="r", encoding="utf-8") as file:
            data = csv.DictReader(file)
            data = list(data)        
            self.data = data

    def train(self):
        print("train")

    def test(self):
        print("test")