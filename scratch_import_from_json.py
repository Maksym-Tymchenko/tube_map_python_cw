import json

def import_from_json(filepath):
    with open(filepath,"r") as jsonfile:
        data = json.load(jsonfile)
    return data

data = import_from_json("data/london.json")
print(data.keys())


