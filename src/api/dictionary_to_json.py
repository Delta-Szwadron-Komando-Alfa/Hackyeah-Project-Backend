import json

ext_dict = {}
sig_dict = {}

with open('signatures.txt', 'r') as file:
    data = file.read().splitlines()
    for i in data:
        signature, extension = i.split(' - ')
        signature = signature.strip()
        ext_dict.setdefault(extension, []).append(signature)
        sig_dict[signature] = extension


def dict_to_file(filename: str, dictionary: dict, clear_file=False) -> None:
    with open(filename, 'w+') as outfile:
        if clear_file:
            outfile.truncate(0)
        json.dump(dictionary, outfile)

dict_to_file('signatures.json', sig_dict, True)
dict_to_file('extensions.json', ext_dict, True)
