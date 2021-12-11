import json
from fastapi import FastAPI

app = FastAPI()

sig_dict = {}
ext_dict = {}

# Open two jsons and read their contents into the dictionary
with open('signatures.json', 'r') as file:
    sig_dict = json.load(file)

with open('extensions.json', 'r') as file:
    ext_dict = json.load(file)

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get('/extensions')
async def get_all_signatures():
    return ext_dict

@app.get('/extensions/{extension}')
async def get_signature(extension):
    extension = extension.lower()
    signature = ext_dict.get(extension.lower())
    return {extension: signature}

@app.get('/signatures')
async def get_all_extensions():
    return sig_dict

@app.get('/signatures/{signature}')
async def get_extension(signature):
    extension = sig_dict.get(signature)
    return {signature: extension}
