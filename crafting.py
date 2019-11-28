import csv

class CraftingMaterial():

    def __init__(self, item_id,item_type,quantity):
        self.item_id = item_id
        self.item_type = item_type
        self.quantity = quantity


class Recipe():

    def __init__(self,item_id,item_type,materials):
        self.item_id = item_id
        self.item_type = item_type
        self.materials = materials

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
            material.append(CraftingMaterial(material_info[0], material_info[1],material_info[2]))

        #return a Recipe object
        return Recipe(item_id, item_type, materials)
