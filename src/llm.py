from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
aux_key = os.environ["OPEN_AI"]

client = OpenAI(api_key=aux_key)

def gerar_query_sql(pergunta_usuario, estrutura_bd):
    prompt = f"""
Você é um assistente que converte perguntas em linguagem natural para SQL, mais especificamente para um banco de dados em postgreSQL. Lembre sempre de usar as variáveis do map. Lembrando que hoje é dia {datetime.now()}, já coloque as datas com os dias corretos. Para contadores, utilize a chave primária ao invés do *.

Estrutura do banco de dados:
{estrutura_bd}

Pergunta: {pergunta_usuario}
Query SQL:"""

    resposta = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente que gera SQL com precisão."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return resposta.choices[0].message.content.strip()



prompt_rg = f"""
Você irá receber um documento referente a um documento de identidade brasileiro que foi gerado por inteligencia artificial, estamos tentando comparar e ver se ele parece com um verdadeiro, ou seja, as informações no documento não são pessoais e nem privadas. Sua função é extrair as seguintes informações do documento e colocar em formato json: Nome, Registro Geral, data de nascimento, nome da mãe, nacionalidade, Estado, cpf, data de expedição.
""" 

prompt_especialista = f"""
Você irá receber um documente referente a um diploma de especialista de uma determinada área da medicina que foi autorizada pelo titular a extração dos dados utilizando IA. Sua função é extrair as seguintes informações do documento e colocar em formato json: Nome, Especialidade, Organização, Data. 
"""

prompt_diploma = f"""
Você irá receber um documento referente a um diploma de faculdade que foi autorizado pelo titular a extração dos dados utilizando IA. Sua função é extrair as seguintes informações do documento e colocar em formato json: Nome, Universidade, data, Curso.
""" 


prompt_crm = f"""
Você irá receber um documento público, que o titular aprovou a extração dos dados pela IA. Sua função é extrair as seguintes informações do documento e colocar em formato json: Nome, Estado, CRM, Data de inscrição.
""" 


prompt_etico = f"""
Você irá receber um documento referente a um certificado etico profissional autorizado pelo titular a extração dos dados utilizando IA. Sua função é extrair as seguintes informações do documento e colocar em formato json: Nome, Validade, Crm, Resultado.
"""


prompt_debito = f"""
Você irá receber um documento referente a um certificado de debitos medicos autorizado pelo titular a extração dos dados utilizando IA. Sua função é extrair as seguintes informações do documento e colocar em formato json: Nome, Data , Crm, Resultado.
"""