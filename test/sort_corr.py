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
    data = load_json('/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/correlation_merged.json')
    pearson = sort(data, 0)
    spearman = sort(data, 2)
    kendall = sort(data, 4)
    write_json(pearson, '/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/corr_sort_pearson.json')
    write_json(spearman, '/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/corr_sort_spearman.json')
    write_json(kendall, '/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/corr_sort_kendall.json')

if __name__ == "__main__":
    __main__()