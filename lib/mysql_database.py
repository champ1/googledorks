import MySQLdb, datetime, errno, sys
from output_base import OutputBase

class MysqlDatabase(OutputBase):
    def __init__(self, args):
        self.cmd_args = args
        self.db       = self.connect(self.cmd_args)
        self.cursor   = self.db.cursor()
        self.table    = 'db_google_dorks'
        
    def connect(self, params):
        try:
            host        = "localhost"
            username    = str(params[3])
            password    = str(params[4])
            database    = str(params[5])
            
            if password == "no":
                password = ""

            return MySQLdb.connect(host, username, password, database)
        except Exception:
            print("Couldn't able to connect to the database with following params: \
                    Host: %s \
                    Username: %s \
                    Password: %s \
                    Database: %s" % ( host, username, password, database ))
            sys.exit()
    
    def create_table(self):
            drop_query = "DROP TABLE IF EXISTS " + self.table
            self.cursor.execute(drop_query)
            
            print "Creating table " + self.table + "..."
            create_query = "CREATE TABLE " + self.table + "( \
                    id INT AUTO_INCREMENT PRIMARY KEY, \
                    title VARCHAR(255) NOT NULL, \
                    dork  VARCHAR(255) NOT NULL, \
                    description TEXT NOT NULL, \
                    created_at TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00', \
                    updated_at TIMESTAMP NOT NULL DEFAULT now() on update now())"

            self.cursor.execute(create_query)

    # close everything
    def close(self):
        self.cursor.close()
        self.db.close()

    def escape(self, value):
        string = u' '.join(MySQLdb.escape_string(value)).encode('utf-8').strip()
        return string

    def insert(self, row):
            now  = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")

            title = self.escape(row['title'])
            dork  = self.escape(row['dork'])
            description = self.escape(row['description'])

            insert = "INSERT INTO " + self.table + " \
                    (title, dork, description, created_at, updated_at) \
                    VALUES \
                    ('%s', '%s', '%s', '%s', '%s')" % \
                    (title , dork , description, date, date)

            try:
                self.cursor.execute(insert) 
                print "Inserted row id:" + str(self.cursor.lastrowid)    
                self.db.commit()
            except:
                self.db.rollback()
                print("Error Occured while inserting the record with following data: \
                        Title-%s Dork-%s Description-%s") % (title, dork, description)
                sys.exit()
    
    def set(self, data):
            self.data = data

    def save(self):
        count = 0

        if str(self.cmd_args[1]) == "init":
            self.create_table()
            count = count + 1

        [ self.insert(row) for row in self.data ]

        self.close()

        return "Successful Inserted " + str(count) + "rows."

    # Gets the id of last inserted dork
    def getLastDork(self):
        query = "SELECT MAX(id) FROM " + self.table

        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            for row in data:
                return row[0]
        except:
            print("Failed to fetch the last dork entry from database.")
            sys.exit()
            
