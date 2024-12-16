import json

def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def sort(data, method):
    sortierte_liste = sorted(data, key=lambda x: list(x.values())[method])
    return sortierte_liste

def write_json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def __main__():
    data = load_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/correlation_out.json')
    pearson = sort(data, 0)
    spearman = sort(data, 2)
    write_json(pearson, 'corr_sort_pearson.json')
    write_json(spearman, 'corr_sort_spearman.json')

if __name__ == "__main__":
    __main__()