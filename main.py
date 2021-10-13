from PIL import Image
from urllib.request import urlopen
import os, glob, csv, multiprocessing

from urllib.error import HTTPError


csvAutoria = r'C:\Users\injir\Documents\RGS\src\autoria.csv'
csvBadAutoria = r'C:\Users\injir\Documents\RGS\src\bad_images_autoria.csv'
csvGoodAutoria = r'C:\Users\injir\Documents\RGS\src\good_images_autoria.csv'

csvAutoru = r'C:\Users\injir\Documents\RGS\src\autoru.csv'
csvBadAutoru = r'C:\Users\injir\Documents\RGS\src\bad_images_autoru.csv'
csvGoodAutoru = r'C:\Users\injir\Documents\RGS\src\good_images_autoru.csv'

csvDrom = r'C:\Users\injir\Documents\RGS\src\drom.csv'
csvBadDrom = r'C:\Users\injir\Documents\RGS\src\bad_images_drom.csv'
csvGoodDrom = r'C:\Users\injir\Documents\RGS\src\good_images_drom.csv'


folderAutoria = r'C:\Users\injir\Documents\RGS\src\autoria'
folderBadAutoria = r'C:\Users\injir\Documents\RGS\src\autoria_bad'

folderAutoru = r'C:\Users\injir\Documents\RGS\src\autoru'
folderBadAutoru = r'C:\Users\injir\Documents\RGS\src\autoru_bad'

folderDrom = r'C:\Users\injir\Documents\RGS\src\drom'
folderBadDrom = r'C:\Users\injir\Documents\RGS\src\drom_bad'



def removeFiles(files, badFiles):
    i = 0

    # Reading images in folder
    for filename in glob.glob(files + r'\*.jpg'):
        if i < 1000:

            # Opening image
            im = Image.open(filename)

            # Checking image size
            if im.size[0] < 320 or im.size[1] < 320:
                im.close()

                imgName = filename.split('\\')
                imgName = imgName[len(imgName) - 1]

                # Replacing bad image
                os.replace(filename, badFiles + '\\' + imgName)

            i += 1




def addCsvData(readFile, writeBadFile, writeGoodFile):
    header = []
    i = 0

    try:
        # Opening and reading csv file
        csvFile = open(readFile, encoding='utf-8')
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
            if i < 10:
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

    except UnicodeEncodeError:
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
                if i < 10:
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




if __name__ == '__main__':
    processPool = multiprocessing.Pool(3)

    # Pool for fixing folder images
    folderData = [(folderAutoria, folderBadAutoria), (folderAutoru, folderBadAutoru), (folderDrom, folderBadDrom)]
    folderOut = processPool.starmap(removeFiles, folderData)

    # Pool for fixing csv images
    csvData = [(csvAutoria, csvBadAutoria, csvGoodAutoria), (csvAutoru, csvBadAutoru, csvGoodAutoru), (csvDrom, csvBadDrom, csvGoodDrom)]
    csvOut = processPool.starmap(addCsvData, csvData)




