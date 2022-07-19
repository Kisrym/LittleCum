import requests, os
from dotenv import load_dotenv
from functions.func import json_read, json_dump

load_dotenv()
database = os.getenv("DATABASE")

def exportar_database():
    data = {}

    data['config'] = json_read(r"db\config.json")
    data['commands'] = json_read(r"db\commands.json")
    data['moneycum'] = json_read(r"db\moneycum.json")

    data = str(data).replace("\'", "\"")

    requests.patch(database, data = f'{data}')

def importar_database():
    r = requests.get(database).json()
    json_dump(r"db\config.json", r['config'])
    json_dump(r"db\commands.json", r['commands'])
    json_dump(r"db\moneycum.json", r['moneycum'])
