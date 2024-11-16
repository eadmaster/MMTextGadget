
# Module for ripping the strings out of the decompressed files within DATA1.BIN
# to generate a .csv
# WARNING: Will overwrite the existing jptxt.csv

import csv
from mmtxtlib import *

if __name__ == '__main__':
    inFiles = extract_input_filenames()
    outStrData = []
    for filename in inFiles:
        intBinFile = MMDatFile()
        intBinFile.read_dat_file(f"{BIN_INPUT_PATH}DATA1/{filename}", filename)
        
        for x in intBinFile.stringEntries:
            if x not in outStrData:
                outStrData.append(x)
                
    with open("jptxt.csv", 'w', encoding='utf16', newline='') as outcsvfile:
        fieldnames = ['hash', 'jp', 'en', 'jpheader', 'enheader']
        writer = csv.DictWriter(outcsvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for strEntry in outStrData:
            writer.writerow({'hash': strEntry.strHash, 'jp': decode_jp(strEntry.strbytes), 'jpheader': decode_jp_header(strEntry.header)})
