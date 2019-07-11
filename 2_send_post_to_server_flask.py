import requests
import json
import sys

json_file_name_default = "scratch.json"
api_path = 'http://localhost:5000/api/add'

def main():

    json_file_name = sys.argv[1]  if len (sys.argv) > 1 else json_file_name_default
    try:
        with open(json_file_name, "r") as read_file:
            data = json.load(read_file)
        # if data["data"] and isinstance(data["data"], list):
        if "data" in data and isinstance(data["data"], list):
            for item in data["data"]:
                res = requests.post( api_path,json=item )
        else:
            res = requests.post( api_path,json=data )
        print(res.status_code)
        read_file.close()
    except:
        print("No requests. Bad input data in file: " + json_file_name)

if __name__ == "__main__":
    main()
