import csv, sys
import os.path
from collections import deque
from output_base import OutputBase

# Generates the csv with google dorks in it
class Csv(OutputBase):
    def __init__(self, args):
        self.args       = args
        self.filename   = 'google_dorks.csv'
        self.fieldnames = ['id', 'title', 'dork', 'description']

    def set(self, data):
        self.data = data

    def save(self):
        if str(self.args[2]) == 'init':
            self.writeToCsv('w+')
        elif str(self.args[2] == 'update'):
            self.writeToCsv('a')
        else:
            print("Not a valid operation!! Please refer to the help.")
            sys.exit()
    
    # Writes to the csv file
    def writeToCsv(self, mode):
        with open(self.filename, mode) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            [ writer.writerow(row) for row in self.data ]

    # Returns the filepath of created csv file
    def getCsvFilePath(self):
        os.chdir('.')
        application_path = os.getcwd()
        return application_path + os.sep + self.filename
    
    # Gets the last row from the csv file
    def getLastRow(self, csvfile):
        with open(csvfile, 'rb') as f:
            reader = csv.reader(f)
            return deque(reader, 1)[0][0] #We only need id of the last dork entry in the csv file     
    
    # Gets the last dork entry in the csv file
    def getLastDork(self):
        csvfile = self.getCsvFilePath()
        if os.path.isfile(csvfile):
            return int(self.getLastRow(csvfile))
        else:
            print("File %s not found at path %s. Please make sure the file exist for updation.") % (self.filename, os.getcwd())
            sys.exit()
