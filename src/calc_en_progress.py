
import csv
from mmtxtlib   import *

def extract_trans_dict():
    outTransDict = []
    with open(IN_TRANS_CSV_FILENAME, newline='', encoding='utf16') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            outTransDict.append(row)
    return outTransDict

if __name__ == '__main__':
    inTransDict = extract_trans_dict()
    enTrans = 0
    for entry in inTransDict:
        if entry["en"] != "":
            enTrans += 1
    
    print(f"{enTrans} / {len(inTransDict)}")

    perc = enTrans / len(inTransDict)
    perc *= 100
    perc = round(perc, 2)
    print(f"{perc}")