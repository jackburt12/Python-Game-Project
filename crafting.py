import csv
from items import GetItem

class CraftingMaterial():

    item_name = ''

    def __init__(self, item_id,item_type,quantity):
        self.item_id = item_id
        self.item_type = item_type
        self.quantity = quantity
        self.item_name = (GetItem(self.item_type, self.item_id)).name

    def serialize(self):
        return {
            'item_id': self.item_id,
            'item_type': self.item_type,
            'quantity': self.quantity,
            'item_name': self.item_name
        }


class Recipe():

    item = None

    def __init__(self,item_id,item_type,materials):
        self.item_id = item_id
        self.item_type = item_type
        self.materials = materials
        self.item = (GetItem(self.item_type, self.item_id))

    def serialize(self):

        item =  self.item.serialize()
        materials = [obj.serialize() for obj in self.materials]

        return {
            'item_id': self.item_id,
            'item_type': self.item_type,
            'materials': materials,
            'item': item
        }

def GetRecipe(recipe_id):
    file = "resources/recipes.csv"

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        #get the relevant row from the csv file
        rows=list(csv_reader)
        row = rows[int(recipe_id)-1]

        #first index of row is id of material we are trying to craft
        item_id = row[0]
        #second index of row is type of material we are trying to carft
        item_type = row[1]

        #now we need to parse the materials from a string into a list of CraftingMaterial objects
        materials_raw = row[2]
        materials=[]

        materials_raw_arr = materials_raw.split("+")

        for material in materials_raw_arr:
            material_info = material.split("/")
            materials.append(CraftingMaterial(material_info[0], material_info[1],material_info[2]))

        #return a Recipe object
        return Recipe(item_id, item_type, materials)

def GetAllRecipes():

    recipes = []

    file = "resources/recipes.csv"

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        rows=list(csv_reader)

    for i in range(len(rows)):
        recipes.append(GetRecipe(i))

    return recipes
