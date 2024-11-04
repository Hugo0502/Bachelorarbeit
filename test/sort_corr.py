import json

def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def sort(data):
    sortierte_liste = sorted(data, key=lambda x: list(x.values())[2])
    return sortierte_liste

def write_json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def __main__():
    data = load_json('correlation_speed.json')
    sortierte_liste = sort(data)
    write_json(sortierte_liste, 'corr_sort_spearmanr_speed.json')

if __name__ == "__main__":
    __main__()