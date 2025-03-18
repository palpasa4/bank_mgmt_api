import json

def load_json(file_name:str)-> list:
    try:
        with open(file_name) as file:
            data=json.load(file)
            return data
    except Exception as e:
        print(e)
        return []

def write_json(file_name:str,new_data:list):
    try:
        with open(file_name,"w") as file:
            json.dump(new_data,file,indent=4)
    except Exception as e:
        print(e)
    
def to_dict(self):
    return self.__dict__