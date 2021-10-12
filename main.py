from PIL import Image
from urllib.request import urlopen
import os, glob, csv

from urllib.error import HTTPError



def removeFiles(files, badFiles):
    i = 0

    # Reading images in folder
    for filename in glob.glob(files + r'\*.jpg'):
        if i < 10000:

            # Opening image
            im = Image.open(filename)

            # Checking image size
            if im.size[0] < 320 or im.size[1] < 320:
                im.close()

                imgName = filename.split('\\')
                imgName = imgName[len(imgName) - 1]

                # Replacing and deleting bad image
                os.replace(filename, badFiles + '\\' + imgName)

            i += 1




def addCsvData(readFile, writeBadFile, writeGoodFile):
    header = []
    i = 0

    # Opening and reading csv file
    csvFile = open(readFile)
    csvReader = csv.reader(csvFile)
    header = next(csvReader)

    # Opening bad and good csv files
    csvBadWriter = open(writeBadFile, 'w', newline="")
    csvGoodWriter = open(writeGoodFile, 'w', newline="")
    outBad = csv.writer(csvBadWriter, delimiter=",")
    outGood = csv.writer(csvGoodWriter, delimiter=",")

    # Writing header to bad and good csv files
    outBad.writerow(header)
    outGood.writerow(header)

    # Reading rows
    for row in csvReader:
        if i < 1000:
            link = str(row).split(';')[4]

            try:
                im = Image.open(urlopen(link))
            except HTTPError:
                outBad.writerow(row)
                print(link, '- 404 Error')

            # Checking image and adding it to csv files
            if im.size[0] < 320 or im.size[1] < 320:
                outBad.writerow(row)
            elif im.size[0] >= 320 or im.size[1] >= 320:
                outGood.writerow(row)

            i += 1

    # Closing writers and reader
    csvBadWriter.close()
    csvGoodWriter.close()
    csvFile.close()


# addCsvData(r'C:\Users\injir\Documents\RGS\src\autoria.csv', r'C:\Users\injir\Documents\RGS\src\bad_images_autoria.csv', r'C:\Users\injir\Documents\RGS\src\good_images_autoria.csv')
removeFiles(r'C:\Users\injir\Documents\RGS\src\autoria', r'C:\Users\injir\Documents\RGS\src\autoriaBad')



