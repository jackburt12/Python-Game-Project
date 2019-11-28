import random, csv

class FoundItem():

    def __init__(self, item_id, item_type):
        self.item_id = item_id
        self.item_type = item_type

def Scavenge(skill):

    found_items = []

    file = "resources/scavengable.csv"

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        rows = list(csv_reader)

        for i in range(skill):
            for row in rows:
                if random.random() < float(row[2]):
                    found_items.append(FoundItem(row[0],row[1]))

        return found_items
