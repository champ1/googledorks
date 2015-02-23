import csv, sys
import os.path
from collections import deque
from output_base import OutputBase

# Generates the csv with google dorks in it
class Csv(OutputBase):
    def __init__(self, args):
        self.args       = args
        self.filename   = 'google_dorks.csv'

    def set(self, data):
        self.data = data

    def save(self):
        with open('google_dorks.csv', 'w+') as csvfile:
            fieldnames = ['id', 'title', 'dork', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            [ writer.writerow(row) for row in self.data ]
    
    def getCsvFilePath(self):
        os.chdir('.')
        application_path = os.getcwd()
        return application_path + os.sep + self.filename
    
    def getLastRow(self, csvfile):
        with open(csvfile, 'rb') as f:
            reader = csv.reader(f)
            return deque(reader, 1)[0][0] #We only need id of the last dork entry in the csv file     

    def getLastDork(self):
        csvfile = self.getCsvFilePath()
        if os.path.isfile(csvfile):
            return int(self.getLastRow(csvfile))
        else:
            print("File %s not found at path %s. Please make sure the file exist for updation.") % (self.filename, os.getcwd())
            sys.exit()
