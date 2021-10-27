import PIL
from PIL import Image
from urllib.request import urlopen
import os, glob, csv, multiprocessing, traceback
from datetime import datetime

from urllib.error import HTTPError
from PIL import UnidentifiedImageError


csvAutoria = r'/home/auto_img/autoria.csv'
csvBadAutoria = r'/home/auto_img/bad_images_autoria.csv'
csvGoodAutoria = r'/home/auto_img/good_images_autoria.csv'

csvAutoru = r'/home/auto_img/autoru.csv'
csvBadAutoru = r'/home/auto_img/bad_images_autoru.csv'
csvGoodAutoru = r'/home/auto_img/good_images_autoru.csv'

csvDrom = r'/home/auto_img/drom.csv'
csvBadDrom = r'/home/auto_img/bad_images_drom.csv'
csvGoodDrom = r'/home/auto_img/good_images_drom.csv'


folderAutoria = r'/home/auto_img/autoria'
folderBadAutoria = r'/home/auto_img/autoria_bad'

folderAutoru = r'/home/auto_img/autoru'
folderBadAutoru = r'/home/auto_img/autoru_bad'

folderDrom = r'/home/auto_img/drom'
folderBadDrom = r'/home/auto_img/drom_bad'

def removeFiles(files, badFiles):

    # Reading images in folder
    for filename in glob.glob(files + r'/*.jpg'):

        # Opening image and checking for errors
        try:
            im = Image.open(filename)
            # Checking image size
            if im.size[0] < 320 or im.size[1] < 320:
                im.close()

                imgName = filename.split('/')
                imgName = imgName[len(imgName) - 1]

                # Replacing bad image
                os.replace(filename, badFiles + '/' + imgName)
        except UnidentifiedImageError:
            im.close()

            imgName = filename.split('/')
            imgName = imgName[len(imgName) - 1]

            # Replacing bad image
            os.replace(filename, badFiles + '/' + imgName)



def addCsvData(readFile, writeBadFile, writeGoodFile):
    header = []

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
            link = str(row).split(';')[4]

            try:
                im = Image.open(urlopen(link))
            except HTTPError:
                outBad.writerow(row)
                print(link, '- 404 Error')
            except UnidentifiedImageError:
                outBad.writerow(row)

            # Checking image and adding it to csv files
            if im.size[0] < 320 or im.size[1] < 320:
                outBad.writerow(row)
            elif im.size[0] >= 320 or im.size[1] >= 320:
                outGood.writerow(row)

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
                    except UnidentifiedImageError:
                        outBad.writerow(row)

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

    # Set your stdout pointer to a file handler
    with open('logger.txt', 'a') as fh:
        try:
            print('Starting...,  {}'.format(datetime.now()), file=fh)

            # Pool for fixing folder images
            # folderData = [(folderAutoria, folderBadAutoria), (folderAutoru, folderBadAutoru),
            #               (folderDrom, folderBadDrom)]
            # folderOut = processPool.starmap(removeFiles, folderData)
            # print('Folders done, {}'.format(datetime.now()), file=fh)

            # Pool for fixing csv images
            csvData = [(csvAutoria, csvBadAutoria, csvGoodAutoria), (csvAutoru, csvBadAutoru, csvGoodAutoru),
                       (csvDrom, csvBadDrom, csvGoodDrom)]
            csvOut = processPool.starmap(addCsvData, csvData)
            print('All done, {}'.format(datetime.now()), file=fh)

        except Exception as e:
            traceback.print_exc(file=fh)
            print(e, datetime.now(), file=fh)





