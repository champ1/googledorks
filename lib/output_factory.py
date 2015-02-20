from __future__ import generators
import sys
from csv_generator import Csv
from mysql_database import MysqlDatabase
from dumper import Dumper

class OutputFactory(object):
    
    types = {
                'mysqldb' : 'MysqlDatabase',
                'csv'     : 'Csv',
                'dump'    : 'Dumper',
            }

    def create(type):
        print"Creating output of format " + type
        constructor = globals()[OutputFactory.types[type]]
        return constructor(sys.argv)
    create = staticmethod(create)


