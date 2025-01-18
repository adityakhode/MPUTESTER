import json

class LoadJson:
    
    def data():
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
            return data
