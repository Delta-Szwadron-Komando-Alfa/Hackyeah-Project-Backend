import json
import shutil
from typing import List
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, UploadFile

from droid.droid_handler import Client

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

@app.post('/upload')
async def upload(files: List[UploadFile] = File(...)):
    random_path = f'temp/{uuid4().hex}'
    Path(random_path).mkdir(parents=True, exist_ok=True)

    for file in files:
        with open(f'{random_path}/{file.filename}', 'wb+') as file_object:
            file_object.write(file.file.read())

    output = Client.indentify_files(f'{random_path}')
    shutil.rmtree(random_path)
    
    return json.loads(output)
