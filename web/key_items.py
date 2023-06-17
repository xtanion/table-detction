import pandas as pd
import json


# if __name__ == "__main__":
df = pd.read_csv('filters/data/inci_list.csv', index_col='INCI name')

def filter_text(text=None):
    # text = text.replace('\n', ' ').replace('\r', '')
    text = text.lower()
    ingredients = text.split('ingredients:')
    output = {}
    ingredients = ingredients[1]
    ingredients = ingredients.split('\n\n')[0]
    # print(ingredients)
    comps = ingredients.split(',')
    comp_set = set(comps)
    if len(comp_set) == len(comps):
        output['repeated'] = "Yes"
    else:
        output['repeated'] = "No"
    
    bad_comp = []
    for compound in comps:
        compound = compound[1:]
        pdobj = locate_compound(compound)
        if pdobj is None:
            bad_comp.append(compound)
    output['inci_not'] = bad_comp
    output['aqua'] = "Yes"
    output['preservatives'] = "Yes"

    output = json.dumps(output, indent=4)
    return output


def locate_compound(name=None):
    if not name is None:
        name = name.upper()
        try:
            pdobj = df.loc[name]
        except KeyError as e:
            pdobj = None
        return pdobj
    else:
        return None


# # test run
# file1 = open('filters/data/myfile.txt', 'r')
# text = file1.read()
# out = filter_text(text)
# print(out)