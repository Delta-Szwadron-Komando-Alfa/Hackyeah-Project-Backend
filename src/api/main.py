import json
import shutil
import uvicorn
from typing import List
from pathlib import Path
from uuid import uuid4
from lxml import etree
import requests

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from droid.droid_handler import Client
from parse_xml_binary import parse_xml_binary
from validate_xml import validate_xml_with_xsd

middleware = [Middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)]

app = FastAPI(middleware=middleware)

@app.get('/')
async def root():
    return RedirectResponse('/docs')

# Files format
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
###

# Validate XML
@app.post('/validate')
async def validate(file: UploadFile = File(...)):
    random_path = f'temp/{uuid4().hex}'
    Path(random_path).mkdir(parents=True, exist_ok=True)

    filepath = f'{random_path}/file.xml' 

    with open(filepath, 'wb+') as file_object:
        file_object.write(file.file.read())

    xml_doc = etree.parse(filepath)
    nsmap = {}
    for ns in xml_doc.xpath('//namespace::*'):
        if ns[0]: # Removes the None namespace, neither needed nor supported.
            nsmap[ns[0]] = ns[1]

    schema_location = xml_doc.xpath('//wnio:Dokument', namespaces=nsmap)[0].attrib
    schema_location = [x for x in str(schema_location).split() if '.xsd' in x][0]

    resp = requests.get(schema_location, allow_redirects=True)
    cont = resp.content.decode('utf-8')
    
    if 'nie posiada pliku' not in cont:
        with open(f'{random_path}/file.xsd', 'wb+') as file_object:
            file_object.write(resp.content)
        resp = validate_xml_with_xsd(filepath, f'{random_path}/file.xsd')
        return {file.filename: resp}

    return {file.filename: 'No schema to validate'}

# Binary
@app.post('/binary')
async def binary(file: UploadFile = File(...)):
    random_path = f'temp/{uuid4().hex}'
    Path(random_path).mkdir(parents=True, exist_ok=True)

    filepath = f'{random_path}/file.xml' 

    with open(filepath, 'wb+') as file_object:
        file_object.write(file.file.read())
    
    return parse_xml_binary(filepath)

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
