# googledorks
Accumulate's all the google dorks from exploit-db and gives options to save to mysql databse or write to csv file or just dump it.

### Save to Database
It creates table called db_google_dorks in specified database.

    $ python main.py init mysqldb <username> <password> <database>
    Initializing..
    Initialized..
    Fetching the dork 1 from 3994
    URL: http://www.exploit-db.com/ghdb/1/
    Extracting the dork with id: 1
    Title: squid cache server reports
    Fetching the medium instance..
    Creating output of format mysqldb
    Saving the data..
    Creating table db_google_dorks...
    Inserted row id:1

### Write to csv
It creates google_dorks.csv file in current directory.

    $ python main.py init csv
    Initializing..
    Initialized..
    Fetching the dork 1 from 3994
    URL: http://www.exploit-db.com/ghdb/1/
    Extracting the dork with id: 1
    Title: <h1>squid cache server reports</h1>
    Fetching the medium instance..
    Creating output of format csv
    Saving the data..
    
### Dump everything on terminal

    $ python main.py init dump
    Initializing..
    Initialized..
    Fetching the dork 1 from 3994
    URL: http://www.exploit-db.com/ghdb/1/
    Extracting the dork with id: 1
    Title: <h1>squid cache server reports</h1>
    Fetching the dork 2 from 3994
    URL: http://www.exploit-db.com/ghdb/2/
    Extracting the dork with id: 2
    Title: <h1>Ganglia Cluster Reports</h1>
    etching the medium instance..
    Creating output of format dump
    Dumping the data..
    
### Todo
* Update Operation
