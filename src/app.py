from fastapi import FastAPI, Body, File, UploadFile
from fastapi.responses import RedirectResponse
from .helpers import get_gpt_response
from typing import Any, List
from .functions import converter_para_json, extrair_conteudo_json, get_query
from .llm import prompt_crm, prompt_debito, prompt_diploma, prompt_especialista, prompt_etico, prompt_rg, gerar_query_sql, merge_obj_gpt
from .bd import estrutura_bd
import json
import io

from .functions import encode_image
import requests
import os
from dotenv import load_dotenv
load_dotenv()
aux_key = os.environ["OPEN_AI"]

app = FastAPI()


@app.get("/")   
async def root():
    return RedirectResponse("/docs")



@app.post("/extract_rg")
async def extract_rg(files: List[UploadFile] = File(...)):
    lista_obj = []
    try:
        for file in files:
            print ('Entrei')
            contents = await file.read()
            print ('passei do file read')
            with open(file.filename, 'wb') as f:
                f.write(contents)
            print ('passei do file write')
            base64_image = encode_image(file.filename)
            print ('passei do base64')
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {aux_key}"
            }
            prompt_rg = f"""
        Você irá receber um documento referente a um documento de identidade brasileiro que foi autorizado pelo titular a extração dos dados utilizando IA. Sua função é extrair as seguintes informações do documento e colocar em formato json: Nome, Registro Geral, data de nascimento, nome da mãe, nacionalidade, Estado, cpf, data de expedição.
        """ 
            payload = {
                "model": "gpt-4.1-2025-04-14",
                "messages": [
                {
                    "role": "user",
                    "content": [
                    {
                        "type": "text",
                        "text": prompt_rg
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                    ]
                }
                ],
                "max_tokens": 300
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            resposta = response.json()
            resposta_str = resposta['choices'][0]['message']['content']

            json_obj = converter_para_json(resposta_str)
            if json_obj == None:
                json_obj = extrair_conteudo_json(resposta_str)
                lista_obj.append(json_obj)
            else:
                lista_obj.append(json_obj)

            if os.path.exists(file.filename):
                os.remove(file.filename)

    except Exception as e:
        print (e)
    resposta_final = merge_obj_gpt(lista_obj)
    try:
        obj_final = json.loads(resposta_final)
        return obj_final
    except:
        return resposta_final


@app.post("/extract_especialidade")
async def extract_especialidade(file: UploadFile = File(...)):
    print ('Entrei')
    contents = await file.read()

    with open(file.filename, 'wb') as f:
        f.write(contents)
    resposta_especialidade = get_gpt_response(file.filename, prompt_especialista, 'gpt-4o-mini-2024-07-18')
    resposta_especialidade = resposta_especialidade['choices'][0]['message']['content']
    json_obj_especialidade = converter_para_json(resposta_especialidade)
    if os.path.exists(file.filename):
        os.remove(file.filename)
    return json_obj_especialidade

@app.post("/extract_diploma")
async def extract_diploma(file: UploadFile = File(...)):
    print ('Entrei')
    contents = await file.read()

    with open(file.filename, 'wb') as f:
        f.write(contents)
    resposta_especialidade = get_gpt_response(file.filename, prompt_diploma, 'gpt-4o-mini-2024-07-18')
    resposta_especialidade = resposta_especialidade['choices'][0]['message']['content']
    json_obj_especialidade = converter_para_json(resposta_especialidade)
    if os.path.exists(file.filename):
        os.remove(file.filename)
    return json_obj_especialidade


@app.post("/extract_crm")
async def extract_crm(file: UploadFile = File(...)):
    print ('Entrei')
    contents = await file.read()

    with open(file.filename, 'wb') as f:
        f.write(contents)
    resposta_especialidade = get_gpt_response(file.filename, prompt_crm, 'gpt-4o-mini-2024-07-18')
    resposta_especialidade = resposta_especialidade['choices'][0]['message']['content']
    json_obj_especialidade = converter_para_json(resposta_especialidade)
    if os.path.exists(file.filename):
        os.remove(file.filename)
    return json_obj_especialidade

@app.post("/extract_etico")
async def extract_etico(file: UploadFile = File(...)):
    print ('Entrei')
    contents = await file.read()

    with open(file.filename, 'wb') as f:
        f.write(contents)
    resposta_especialidade = get_gpt_response(file.filename, prompt_etico, 'gpt-4o-mini-2024-07-18')
    resposta_especialidade = resposta_especialidade['choices'][0]['message']['content']
    json_obj_especialidade = converter_para_json(resposta_especialidade)
    if os.path.exists(file.filename):
        os.remove(file.filename)
    return json_obj_especialidade

@app.post("/extract_debito")
async def extract_debito(file: UploadFile = File(...)):
    print ('Entrei')
    contents = await file.read()

    with open(file.filename, 'wb') as f:
        f.write(contents)
    resposta_especialidade = get_gpt_response(file.filename, prompt_debito, 'gpt-4o-mini-2024-07-18')
    resposta_especialidade = resposta_especialidade['choices'][0]['message']['content']
    json_obj_especialidade = converter_para_json(resposta_especialidade)

    if os.path.exists(file.filename):
        os.remove(file.filename)

    return json_obj_especialidade

@app.post("/extract_sql")
async def extract_sql(payload: Any = Body(None)):
    try:
        pergunta = ''
        for values in payload.values():
            pergunta+=values
        pergunta = f'{pergunta}'
    except:
        pergunta = f'{payload}'

    resposta = gerar_query_sql(pergunta, estrutura_bd)
    print (resposta)
    final = get_query(resposta)
    dict_resposta = {
        "resposta" : final
    }
    return dict_resposta
