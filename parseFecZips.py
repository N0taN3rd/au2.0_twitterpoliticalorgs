# -*- coding: utf-8 -*-
import json
import zipfile
import os
from os import walk
from os import path
from lxml import etree as ET
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def writeCount():
    datafiles = os.path.join(os.getcwd(), 'datafiles')
    outputDir = path.join(datafiles, 'output')
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    def noOutput(it):
        return it != 'output'

    dirList = []
    for root, dirs, files in os.walk(datafiles):
        for dirr in filter(noOutput, dirs):
            # print dirr
            newDir = path.join(outputDir, dirr)
            dirList.append((os.path.join(root, dirr), newDir))
            # print newDir

    pacs = ET.Element("clintonDonors")
    trumpPacs = ET.Element("trumpDonors")
    tpcs = {}
    cpcs = {}
    clintonCount = 0
    trumpCount = 0
    for oldDir, newDir in dirList:
        # if os.path.basename(oldDir).startswith("201605"):
        fileDate = os.path.basename(oldDir)
        print fileDate
        if fileDate.startswith("2016") or fileDate.startswith("201511") or fileDate.startswith("201512"):
            for root, dirs, files in os.walk(os.path.join(datafiles, oldDir)):
                # print root
                for f in files:
                    oldFile = open(os.path.join(oldDir, f), 'r')
                    lineCount = 0
                    for line in oldFile:
                        if "[BEGINTEXT]" in line:
                            break
                        lineCount = lineCount + 1
                        if lineCount == 2:
                            try:
                                pacName = line.split('')[2]
                                # print pacName
                                if pacName.lower().strip() == "donald j. trump for president, inc.":
                                    trumpCount = trumpCount + 1

                                    # print pacName
                                    # pac.text = pacName
                                    donorCount = 0
                                    for line in oldFile:
                                        donorCount = donorCount + 1
                                        if donorCount > 2:
                                            try:
                                                dataList = line.split('')
                                                if dataList[0].lower().startswith("sa"):
                                                    # print dataList[7] + " " + dataList[8] + " " + dataList[9]
                                                    count = tpcs.get(dataList[19], 0)
                                                    count += 1
                                                    tpcs[dataList[19]] = count
                                            # donor = ET.Element("donor")
                                            #         trumpPacs.append(donor)
                                            #         idXML = ET.SubElement(donor, "id")
                                            #         idXML.text = dataList[2]
                                            #         typeXML = ET.SubElement(donor, "type")
                                            #         typeXML.text = dataList[5]
                                            #         dateXML = ET.SubElement(donor, "date")
                                            #         dateXML.text = dataList[19]
                                            #         nameXML = ET.SubElement(donor, "name")
                                            #         nameXML.text = dataList[7].strip() + " " + dataList[
                                            #             8].strip() + " " + dataList[9].strip()
                                            #         amountXML = ET.SubElement(donor, "amount")
                                            #         amountXML.text = dataList[20]
                                            #         amountTotalXML = ET.SubElement(donor, "amountTotal")
                                            #         amountTotalXML.text = dataList[21]
                                            #         purposeXML = ET.SubElement(donor, "purpose")
                                            #         purposeXML.text = dataList[22].strip()
                                            #         employerXML = ET.SubElement(donor, "employer")
                                            #         employerXML.text = dataList[23].strip()
                                            #         occupationXML = ET.SubElement(donor, "occupation")
                                            #         occupationXML.text = dataList[24].strip()
                                            #         addressXML = ET.SubElement(donor, "address")
                                            #         addressXML.text = dataList[12] + " " + dataList[13] + " " + \
                                            #                           dataList[14] + " " + dataList[15] + " " + \
                                            #                           dataList[16]
                                            #
                                            except:
                                                errorList = open(os.path.join(os.getcwd(), "errors.xml"), 'w')
                                                errorList.write(line)
                                                errorList.close()

                                if pacName.lower().strip() == "hillary for america":
                                    clintonCount = clintonCount + 1

                                    print pacName
                                    # pac.text = pacName
                                    donorCount = 0
                                    for line in oldFile:
                                        donorCount = donorCount + 1
                                        if donorCount > 2:
                                            try:
                                                dataList = line.split('')
                                                if dataList[0].lower().startswith("sa"):
                                                    # print dataList[7] + " " + dataList[8] + " " + dataList[9]
                                                    count = cpcs.get(dataList[19], 0)
                                                    count += 1
                                                    cpcs[dataList[19]] = count
                                                    # print dataList[7] + " " + dataList[8] + " " + dataList[9]
                                                    # donor = ET.Element("donor")
                                                    # pacs.append(donor)
                                                    # idXML = ET.SubElement(donor, "id")
                                                    # idXML.text = dataList[2]
                                                    # typeXML = ET.SubElement(donor, "type")
                                                    # typeXML.text = dataList[5]
                                                    # dateXML = ET.SubElement(donor, "date")
                                                    # dateXML.text = dataList[19]
                                                    # nameXML = ET.SubElement(donor, "name")
                                                    # nameXML.text = dataList[7].strip() + " " + dataList[
                                                    #     8].strip() + " " + dataList[9].strip()
                                                    # amountXML = ET.SubElement(donor, "amount")
                                                    # amountXML.text = dataList[20]
                                                    # amountTotalXML = ET.SubElement(donor, "amountTotal")
                                                    # amountTotalXML.text = dataList[21]
                                                    # purposeXML = ET.SubElement(donor, "purpose")
                                                    # purposeXML.text = dataList[22].strip()
                                                    # employerXML = ET.SubElement(donor, "employer")
                                                    # employerXML.text = dataList[23].strip()
                                                    # occupationXML = ET.SubElement(donor, "occupation")
                                                    # occupationXML.text = dataList[24].strip()
                                                    # addressXML = ET.SubElement(donor, "address")
                                                    # addressXML.text = dataList[12] + " " + dataList[13] + " " + \
                                                    #                   dataList[14] + " " + dataList[15] + " " + \
                                                    #                   dataList[16]

                                            except:
                                                errorList = open(os.path.join(os.getcwd(), "errors.xml"), 'w')
                                                errorList.write(line)
                                                errorList.close()

                            except:
                                continue

    out = {
        "trumpy": tpcs,
        "hilary": cpcs,
    }

    outf = open('counting.json', "w+")
    outf.write(json.dumps(out, indent=2))
    outf.close()

    # print tpcs, cpcs

    # clintonDonorTimeline = []
    # for donor in pacs:
    #     donorDate = donor.find("date").text
    #     donorDate = donor.find("date").text
    #
    #
    #
    # pacList = open(os.path.join(os.getcwd(), "clintonDonors.xml"), 'w')
    # pacString = ET.tostring(pacs, pretty_print=True, xml_declaration=True, encoding="utf-8")
    # pacList.write(pacString)
    # pacList.close()
    # trumpList = open(os.path.join(os.getcwd(), "trumpDonors.xml"), 'w')
    # trumpString = ET.tostring(trumpPacs, pretty_print=True, xml_declaration=True, encoding="utf-8")
    # trumpList.write(trumpString)
    # trumpList.close()
    # print "clintonCount = " + str(clintonCount)
    # print "trumpCount = " + str(trumpCount)
    #
    # for folder in os.listdir(dir):
    #     # print folder
    #     print folder
    #     newDir = path.join(outputDir, folder)
    #     if not os.path.exists(newDir):
    #         os.mkdir(newDir)
    # outFolder = path.join(outputDir, folder)
    # print newDir
    # for file in os.listdir(folder):
    #     print file
    #     textRTF = open(file, "r")
    #     textPlain = open(path.join(newDir, file), 'w+')
    #     for oldLine in textRTF:
    #         newLine = oldLine.rstrip().split('')
    #         textPlain.write(" ".join(newLine))
    #     textRTF.close()
    #     textPlain.close()


if __name__ == '__main__':
    inf = open('counting.json', "r")

    data = json.load(inf)
    inf.close()

    outf = open('counting.json', "w+")
    outf.write(json.dumps(data,sort_keys=True, indent=2))
    outf.close()