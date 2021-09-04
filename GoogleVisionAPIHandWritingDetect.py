import os, io
from google.cloud import vision
import pandas as pd
import argparse

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision.ImageAnnotatorClient()

ap = argparse.ArgumentParser()
group = ap.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--path", help="Folder Path for bulk check")
group.add_argument("-f", "--file", help="Image Path for single check")
args = vars(ap.parse_args())

imageList = []

if args['file']:
    print("Checking single file: " + args['file'])
    imageList.append(os.path.join(os.getcwd(), args['file']));
    
if args['path']:
    print("Checking multiple files in folder: " + args['path'])
    imageList = os.listdir(args['path'])
    imageList = list(map(lambda x: args['path'] + '/' +  x , imageList))

backListWord = open('Blacklistwords.txt', 'r')
lines = backListWord.readlines()
lines = list(map(lambda x: x.replace('\n', ''), lines))

try:
    lines.remove('')
    lines.remove(' ')
except:
    pass

forbiddenWordDetected = False

for image in imageList:

    with io.open(image, 'rb') as image_file:
        content = image_file.read()

    imageContent = vision.Image(content=content)
    response = client.document_text_detection(image=imageContent)

    text = response.full_text_annotation.text
    print(text)
    forbiddenWordDetected = False
    for l in lines:
        if text.lower().find(l.lower()) != -1 :
            forbiddenWordDetected = True
        
    if forbiddenWordDetected:
        print ("Danger detected in: " + image)
    else:
        print("The danger could not be detected in: " + image)
