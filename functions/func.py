import json, requests

def blacklist():
    BLACKLIST = []
    with open(r"db\config.json") as arquivo:
        data = json.load(arquivo)
        for item in data["blacklist"].values():
            BLACKLIST.append(item)
    return BLACKLIST


def define(champion, a=True):
    taporra = {
        "Aurelionsol":"AurelionSol",
        "Drmundo":"DrMundo",
        "Jarvaniv":"JarvanIV",
        "Kogmaw":"KogMaw",
        "Wukong":"MonkeyKing",
        "Xinzhao":"XinZhao",
        "Reksai":"RekSai",
        "Bardo":"Bard",
        "Masteryi":"MasterYi",
        "Missfortune":"MissFortune"
    }
    if a:
        if champion in taporra.keys():
            return taporra[champion]
        else:
            return champion
    else:
        for k, v in taporra.items():
            if champion == v:
                return k
        return champion
    
    
def json_read(path):
    with open(path) as arquivo:
        data = json.load(arquivo)
        return data
    
    
def json_dump(path, data):
    with open(path, "w") as krl:
        json.dump(data, krl, indent=3)
        
        
def champ(name, a=True):
    name = str(name)
    if a and not name.isnumeric():
        return requests.get("http://ddragon.leagueoflegends.com/cdn/12.1.1/data/en_US/champion.json").json()['data'][define(name.replace(" ", "").replace("'", "").capitalize())]['key']
    else:
        r = requests.get("http://ddragon.leagueoflegends.com/cdn/12.1.1/data/en_US/champion.json").json()['data']
        for c in r:
            if r[c]['key'] == name:
                return c
