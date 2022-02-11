import json


def getText(key: str):
    with open('gettext.json', encoding='utf-8') as f:
        read = json.load(f)
    if key in read:
        return read[key]
    return 'none text'