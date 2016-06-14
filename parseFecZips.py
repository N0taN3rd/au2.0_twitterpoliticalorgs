import zipfile
import os
from os import walk
from os import path

if __name__ == '__main__':
    datafiles = os.path.join(os.getcwd(), 'datafiles')
    outputDir = path.join(datafiles, 'output')
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    def noOutput(it):
        return  it != 'output'

    dirList = []
    for root, dirs, files in os.walk(datafiles):
        for dirr in filter(noOutput, dirs):
            # print dirr
            newDir = path.join(outputDir, dirr)
            dirList.append((os.path.join(root,dirr),newDir))
            # print newDir

    for oldDir, newDir in dirList:
        if not os.path.exists(newDir):
            os.mkdir(newDir)
        for root, dirs, files in os.walk(os.path.join(datafiles, oldDir)):
            # print root
            for f in files:
                oldFile = open(os.path.join(oldDir,f),'r')
                newFile = open(os.path.join(newDir,f),'w+')
                for line in oldFile:
                    newFile.write(" ".join(line.rstrip().split('')))
                newFile.close()
                oldFile.close()
                #     newFile.write(" ".join(line.rstrip().split('')))
                # print oldFile,newFile in
                    # textRTF = open(os.path.join(root,f), "r")
                    # textPlain = open(path.join(newDir, f), 'w+')
                    # for oldLine in textRTF:
                    #     newLine = oldLine.rstrip().split('')
                    #     textPlain.write(" ".join(newLine))
                    #     textRTF.close()
                    #     textPlain.close()

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
