# gooledorks
Accumulate's all the google dorks from exploit-db and gives options to save to mysql databse or write to csv file or just dump it.

### Save googledorks to database
It creates a new table called 'db_google_dorks' in specified database and saves all the googledorks in it.

    $ python main.py init mysqldb <username> <password> <database>

### Update googledorks to database
It fetches new googledorks and saves them to table.

    $ python main.py update mysqldb <username> <password> <database>
    
### Write to csv
It creates google_dorks.csv file in current directory.

    $ python main.py init csv

### Dump everything on terminal

    $ python main.py init dump

### Help

    $ python main.py help 

### Dependencies
* BeautifulSoup     [pip install beautifulsoup4]
* MySQLdb           [pip install MySQL-python]

### Todo
* Make the process of fetching dorks faster
