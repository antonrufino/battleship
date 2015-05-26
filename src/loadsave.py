# loadsave.py
# The loadsave module is used to write and read data from files in
# JSON format.

import json

# Based on dcumentation from https://docs.python.org/2/library/json.html

# Converts data to a JSON string and saves it to a file
def saveToFile(fileName, data):
    jsonString = json.dumps(data) #convert data to json string
    fh = open(fileName, "w")
    fh.write(jsonString)
    fh.close()    

# Loads a JSON string from a file and converts it to a Python object    
def loadFromFile(fileName):
    fh = open(fileName, "r") 
    jsonString = fh.read()
    fh.close()
    
    return json.loads(jsonString) #convert json string to python obj
