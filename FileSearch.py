#authour: Andrew Garner
#version: 1.0
from pdf2image import convert_from_path
import os
import sys
import glob
import smbclient
import time

# start timer to return time taken
start = time.time()

accNo = sys.argv[1]
accNo = accNo.upper()
records = set()
folderContents = set()


# Create Connection to SMB shared drive
smb = smbclient.SambaClient(server="", share="", username="", password="", domain="")

# Check to see if file exists, if it does adds it to a set
folderPath = "/exampleFolderName/" + letter + "/"

try:
    if smb.glob(folderPath):
        folderGlob = smb.glob(folderPath + accNo + "*")
        for eachFile in folderGlob:
            accFolder = folderPath + eachFile[0]
        filePath = smb.glob(accFolder + "/*")
        for eachFile in filePath:
            records.add(accFolder + "/" + eachFile[0])
            folderContents.add(eachFile[0])
except:
    print("Error - Account Does not Exist")

sortRec = sorted(records)

# if length of set is greater than 0, convert files in set to jpegs
if len(records) > 0:
    i = 0
    for eachFile in sortRec:
        # Check to make sure format of file is pdf
        if eachFile[-3:] == "pdf":
            smb.download(eachFile, "/example/of/download/path/" + str(i) + ".pdf")	
            try:
                images = convert_from_path("/example/of/download/path/" + str(i) + ".pdf")
                for page in images:
                    filePath = '/example/of/newFolder/path/' + str(i) + '.jpg'
                    page.save(filePath, 'JPEG')
                    i += 1
            except:
                print("Error: Unable to convert files.")
    end = time.time() - start
    # print HTML code to show results as list in browser (HTML tags are ommited in this case)
    print(str(i) + " Results Found in " + str(end) + "s" )
    print("#enter HTML tag here" + " List of Files for " + accNo + "#close HTMl tags here")
    for eachLine in folderContents:
        print("#enter HTML li tag here" + eachLine + "#close HTML li tag here")
    print("#close HTML ul and div tags here")
else:
    end = time.time() - start
    print("0 Results Found in " + str(end) +"s")