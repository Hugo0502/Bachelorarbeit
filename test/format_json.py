import json

file_json = "/Users/HugoWienhold/Uni-Lokal/Bachelorarbeit/test/JSON/out.json"

def one():
    with open(file_json, 'r') as f:
        data = json.load(f)
    return data

def two(data):
    for key, value in data.items():
        data[key]["Layout Shifts"] = layout_shift_correction(data[key]["Layout Shifts"])
        data[key]["DOM Size"] = dom_size_correction(data[key]["DOM Size"])

    return data

def dom_size_correction(dom_size):
    if isinstance(dom_size, str):
        out = dom_size.replace(",","")
        out = int(out)
        return out
    else:
        return -100
     

def layout_shift_correction(num_of_shifts):
    if isinstance(num_of_shifts, str):
        return int(num_of_shifts)
            
def write_json(data):
    with open('out_corr.json', 'w') as f:
        json.dump(data, f, indent=4)

def main():
    read = one()
    data = two(read)
    write_json(data)

if __name__ == "__main__": 
    main()