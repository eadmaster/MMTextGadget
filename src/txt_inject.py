
# This script intakes a .csv translation file and exports a translated Million Monkeys iso

# Path related helpers
import os
from pathlib import Path
# Reading / Converting binary data
import struct
import csv
# Custom built solutions
from mmtxtlib   import *

# Extract the translation csv file containing our english strings
def extract_trans_dict():
    outTransDict = []
    with open(IN_TRANS_CSV_FILENAME, newline='', encoding='utf16') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            outTransDict.append(row)
    return outTransDict

# Write out a new DATA0.BIN file that we will work on before injecting into the iso
def write_header_file():
    with open(f"{BIN_INPUT_PATH}DATA0/{IN_HEADER_FILENAME}", 'rb') as f_in:
        with open(f"{BIN_INT_PATH}{IN_HEADER_FILENAME}", 'wb') as f_out:
            f_out.write(f_in.read())
                        
# Write out compressed data files
def write_dat_files(inTransDict):
    for filename in inFiles:
        intBinFile = MMDatFile()
        
        if intBinFile.read_dat_file(f"{BIN_INPUT_PATH}DATA1/{filename}", filename):
            newInFiles.append(filename)
        else:
            continue
        
        # The pad entry will be used to pad out the file to fit within the same
        # number of bytes as the original
        padEntry = None
        bFoundPadEntry = False
        for strEntry in intBinFile.stringEntries:
        
            # Now we need to get the matching hash from the csv
            thisDict = None
            for z in inTransDict:
                if strEntry.strHash == z['hash']:
                    thisDict = z
                    break
                    
            if thisDict == None:
                print("Unable to match hash to translation table, somethings wrong!")
                exit(1)
                
            # First we should check if we already have our pad entry
            if bFoundPadEntry == False:
                if strEntry.strHash == "82b62b49457fbfb72e5d0acb3a8487071a8e1cacf4faa1edea7e78a19748baa8":
                    bFoundPadEntry = True
                    
                    # We're gonna set the bytes here to 0 so we don't accidentally include these
                    # in our new pad calculation
                    strEntry.strLen = 0
                    strEntry.strbytes = bytearray()
                    
                    padEntry = strEntry
                    continue # We'll go back and update this entry at the end
 
            # Now that we have the dict, if we have an english string write that
            if thisDict["en"] != '':
                strEntry.readString(thisDict["en"])
            #... or we haven't written this string yet so keep it as is
            else: 
                pass
                          
        # Now we need to go back in and patch up the pad entry
        
        # First make sure we ended up grabbing an entry
        if bFoundPadEntry == False:
            print("WARNING! Never set pad entry")
            exit(1)
            
        newStrCount = 0
        for strEntry in intBinFile.stringEntries:
            newStrCount += strEntry.strLen
            
        print(f"[{BIN_INPUT_PATH}DATA1/{intBinFile.filename}] - OLD STR COUNT: {intBinFile.TransByteCount} NEW STR COUNT: {newStrCount} DIFF: {intBinFile.TransByteCount - newStrCount}")
        
        if intBinFile.TransByteCount - newStrCount <= 0:
            print("RAN OUT OF SPACE!!! ISO WONT WORK!!!")
            ErrorFileStr = f"{intBinFile.filename}_ERROR.txt"
            print(f"Review the following file for a string to null out: {ErrorFileStr}")
                
            with open(ErrorFileStr, 'w', encoding='utf16') as file:
                for strEntry in intBinFile.stringEntries:
                    file.write(decode_jp(strEntry.strbytes) + "\n")
            
            exit(1)     
        
        tempCount = intBinFile.TransByteCount - newStrCount

        newOutStr = ""
        for i in range(0, (tempCount - (tempCount % 2)), 2):
            newOutStr += "W"
        if tempCount % 2 == 1:
            newOutStr += "[BREAK]"
        
        for strEntry in intBinFile.stringEntries:
            if strEntry.strHash == padEntry.strHash:
                strEntry.readString(newOutStr)
                break
        
        newStrCount = 0
        for strEntry in intBinFile.stringEntries:
            newStrCount += strEntry.strLen
        
        if intBinFile.TransByteCount != newStrCount:
            print("STRING SIZE MISMATCH!!! ISO WONT WORK!!!")
            exit(1)
        
        intBinFile.write_dat_file()
 
# Validate we can fit the new data within the old data's space 
def validate_new_file_size():
    newOutFiles = []
    with open(f"{BIN_INT_PATH}{IN_HEADER_FILENAME}", 'r+b') as f_out:
        s = f_out.read()
        for filename in newInFiles:
            entryname = Path(f"{BIN_INT_PATH}{filename}").stem
            
            namePatternBytes = bytearray.fromhex(entryname)
            namePatternBytes.reverse()
            print(entryname, namePatternBytes.hex(), s.find(namePatternBytes))
            
            fullpath = os.path.relpath(f"{BIN_INT_PATH}{filename}.gz")
            try:
                fpsize = os.path.getsize(fullpath)
            except:
                print(f"Tried pulling file that doesn't exist??? {fullpath}")
                exit(1)
            
            f_out.seek( s.find(namePatternBytes) + 8, 0)
            
            ogFileSize = (struct.unpack('I', f_out.read(4)))[0]
            availableSpace = 0x800 * round(ogFileSize/0x800)
            
            # Sometimes it can underround for some reason
            if availableSpace < ogFileSize:
                availableSpace += 0x800
                
            print(f"[{BIN_INT_PATH}{IN_HEADER_FILENAME}] - og file size: {ogFileSize} rounded up {availableSpace} new file size: {fpsize}")
            
            if availableSpace < fpsize:
                print(f"THERE ISN'T ENOUGH SPACE TO INSERT THE NEW DATA!!! {filename}")
                errorFiles.append(filename)
                continue
             
            else:
                newOutFiles.append(filename)
            
    return newOutFiles
 
# Fix up DATA0.BIN file sizes  
def update_header_offsets():   
    with open(f"{BIN_INT_PATH}{IN_HEADER_FILENAME}", 'r+b') as f_out:
        s = f_out.read()
        for filename in newInFiles:
            entryname = Path(f"{BIN_INT_PATH}{filename}").stem
            
            namePatternBytes = bytearray.fromhex(entryname)
            namePatternBytes.reverse()
            print(entryname, namePatternBytes.hex(), s.find(namePatternBytes))
            
            fullpath = os.path.relpath(f"{BIN_INT_PATH}{filename}.gz")
            try:
                fpsize = os.path.getsize(fullpath)
            except:
                print(f"Tried pulling file that doesn't exist??? {fullpath}")
                exit(1)
            
            f_out.seek( s.find(namePatternBytes) + 8, 0)
            

            fpsize = fpsize.to_bytes(4, 'little') 
            f_out.write(fpsize)
  
# Generate dictionary for matching file name to sector offet
def extract_header_dict():
    outFileDict = {}
    with open(f"{BIN_INT_PATH}{IN_HEADER_FILENAME}", 'r+b') as f_out:
        for i in range(786):
            dat = (struct.unpack('II', f_out.read(8)))
            outFileDict[dat[0]] = dat[1]
            f_out.seek(4, 1)
            
        for filename in inFiles:
            entryname = Path(f"{BIN_INT_PATH}{filename}").stem
            entryname = int(entryname, 16)
            
    return outFileDict
    
# Create a new Million Monkeys iso
# NOTE: This only needs to be called once if there isn't an iso already in the output directory
# We don't need to create a new one everytime we update translation text
# as long as we don't accidentally start writting outside of DATA0.BIN & DATA1.BIN
def create_new_iso():
    with open(f"{BIN_INPUT_PATH}ISO/{IN_ISO_FILENAME}", 'rb') as f_in:
        with open(f"{BIN_OUTPUT_PATH}{OUT_ISO_FILENAME}", 'wb') as f_out:
            print("Writing new iso, please wait!")
            f_out.write(f_in.read())
  
# Patch Million Monkeys iso with updated files  
def patch_iso():
    with open(f"{BIN_OUTPUT_PATH}{OUT_ISO_FILENAME}", 'r+b') as iso_out:
        # Write out new DATA0.BIN
        DATA0DATA = None
        with open(f"{BIN_INT_PATH}{IN_HEADER_FILENAME}", 'r+b') as f_out:
            DATA0DATA = f_out.read()
        
        iso_out.seek(DATA0_OFFSET, 0)
        iso_out.write(DATA0DATA)
    
        # Write out all entries
        for filename in newInFiles:
            DATDATA = None
            try:
                with open(f"{BIN_INT_PATH}{filename}.gz", 'r+b') as f_out:
                    DATDATA = f_out.read()
            except:
                print("Tried opening file that doesn't exist???")
                
            # Seek to this offset in the binary
            entryname = Path(filename).stem
            entryname = int(entryname, 16)
            datOffset = DATA1_OFFSET + (fileDict[entryname] * 0x800)
            
            iso_out.seek(0, 0)
            iso_out.seek(datOffset, 0)
            
            print(hex(DATA1_OFFSET), hex(fileDict[entryname]), hex((fileDict[entryname] * 0x800)), hex(DATA1_OFFSET + (fileDict[entryname] * 0x800)))
            
            # Overwrite it with our new data
            iso_out.write(DATDATA)
            
            # We should be a good citizen here and do some cleanup as well
            # If the new file we write is smaller than the older one, we should
            # null out the rest of the bytes for this sector of the iso
            # This isn't mandatory but worth mentioning for cleanup
            # We can't just modulus 0x800 b/c the new file might be so small
  
if __name__ == '__main__':
    newInFiles = []
    errorFiles = []
    inTransDict = extract_trans_dict()
    inFiles = extract_input_filenames()
    write_header_file()
    write_dat_files(inTransDict)
    newInFiles = validate_new_file_size()
    update_header_offsets()
    fileDict = extract_header_dict()
    if not Path(f"{BIN_OUTPUT_PATH}{OUT_ISO_FILENAME}").is_file():
        create_new_iso()
    patch_iso()
    
    if len(errorFiles) != 0:
        print("The following files were unable to be added because the new gzipped file was bigger than the original")
        for file in errorFiles:
            print(file)
    
    print("Let's go catch some monkeys")


 
 




        
        
        
        
        