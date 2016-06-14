import zipfile
import os
from os import walk
from os import path

dir = 'datafiles'
outputDir = path.join(dir, 'output')
os.mkdir(outputDir)

for folder in os.listdir(dir):
  if os.path.isdir(folder):
    outFolder = path.join(outputDir, folder)
    os.mkdir(outFolder)
    for file in os.listdir(folder):
        textRTF = open(file), "a")
        textPlain = open(path.join(outFolder, file),'w+')
        for oldLine in textRTF:
          newLine = oldLine.rstrip().split('')
          textPlain.write(" ".join(newLine))  