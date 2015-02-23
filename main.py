import requests, re, sys
from bs4 import BeautifulSoup
from lib.output_factory import OutputFactory
import threading

# Dorks mail page
google_dorks_url = 'http://www.exploit-db.com/google-dorks/'

# Dork Url
google_dork_url  = 'http://www.exploit-db.com/ghdb/'

# Dork Categories
categories = ['Footholds', 
              'Files containing usernames',
              'Sensitive Directories', 
              'Web Server Detection',
              'Vulnerable Files',
              'Vulnerable Servers',
              'Error Messages',
              'Files containing juicy info',
              'Files containing passwords',
              'Sensitive Online Shopping Info',
              'Network or vulnerability data', 
              'Pages containing login portals', 
              'Various Online Devices',
              'Advisories and Vulnerabilities']

# Gets the latest dork entry from the exploit-db
def latest_dork(url):
    google_dorks   = requests.get(url)
    beautiful_soup = BeautifulSoup(google_dorks.content)

    links   = beautiful_soup.select("table a")
    pattern = re.compile(ur"\w*://[a-z.-]*/\w*/(\d*)/")

    data    = []

    for link in links:
        href  = link.attrs['href']
        match = re.search(pattern, 'u"' + href + '"')

        if match is not None:
            data.append(match.group(1))

    return int(max(data))

# Update the dork
def update(latest_dork, url, args):
    print "Updating.."

    medium      = OutputFactory.create(str(args[2]))
    last        = medium.getLastDork()
    collection  = fetchDorks(int(last) + 1, latest_dork + 1, url)

    medium.set(collection)
    print "Saving the data.."
    medium.save()

# intialize the dork
def initialize(latest_dork, url, args):
    print "Initialized.."

    start       = 1
    end         = latest_dork + 1
    collection  = fetchDorks(start, end, url)
    
    medium = OutputFactory.create(str(args[2]))
    medium.set(collection)
    print("Saving the data..")
    medium.save()

def dorkWorker(dork_url, dork_id, collection):
    print("Dork URL: %s" % dork_url)

    google_dork     = requests.get(dork_url)
    beautiful_soup  = BeautifulSoup(google_dork.content)
    
    collection.append(extract_data(dork_id, beautiful_soup))

def fetchDorks(start, end, url):
    collection  = []
    threads     = []

    try:
        for i in range(start, end):
            print("Fetching the dork %d from %d" % (i, end) )
            dork_url        = url + str(i) + '/'
            
            t = threading.Thread(target=dorkWorker, args=(dork_url, i, collection))
            threads.append(t)
            t.start()
            t.join()

    except ConnectionError:
        print("Connection Error has occured while requesting the resource.")

    except RequestException as e:
        print("Request Error occured with %s : %s ") % (e.errno, e.strerror)

    finally:            
        return collection

def extract_data(dork_id, beautiful_soup):
    
    data  = {}
    print("Extracting the dork with id: %d" % dork_id)
    title = beautiful_soup.select("h1").pop()
    print("Title: %s" % title)
    dork  = beautiful_soup.select("h2").pop()
    desc  = beautiful_soup.select(".text").pop()
    
    data['id']          = dork_id
    data['title']       = title.get_text()
    data['dork']        = dork.a.extract().get_text()
    data['description'] = desc.get_text()    

    return data

def help():
        print "########################################\n#             GOOGLE DORKS             #\n#            BY AMAR MYANA             #\n########################################"
        print "\nAccumulate's all the google dorks and gives you option to \nsave to database or write to csv or dump it.\n"
        print "There are only two operation init and update.\n"
        print "1. init      Downloaded all the google dorks."
        print "2. update    Updates the google dorks from last dork to latest one."

        print "\nCurrently it supports to save to mysql database or write to csv file. \nIf you want any other implemention feel free to mail me at amar92@outlook.com  \nor you can make a pull request."
        print "\n###Save to Mysql Database###"
        print "$ python main.py init/update mysqldb <username> <password> <database>"
        
        print "\n###Write to csv###"
        print "$ python main.py init/update csv"

        print "\n###Dump on the terminal###"
        print "$ python main.py init dump"

def main():
    args_length = len(sys.argv)
    cmd_args    = sys.argv

    if str(cmd_args[1]) == 'help':
        help()
        sys.exit()

    if args_length < 3:
        print("Minimum 3 arguments are required.")
        help()
        sys.exit()

    if str(cmd_args[2]) == "mysqldb" and args_length != 6:
        print("Minimum 5 arguments are required for mysql database process.")
        help()
        sys.exit()

    if str(cmd_args[1]) == "init":
        print "Initializing.."
        initialize(latest_dork(google_dorks_url), google_dork_url, sys.argv)

    elif str(cmd_args[1]) == "update":
        update(latest_dork(google_dorks_url), google_dork_url, sys.argv)

    else:
        print "Please enter the correct operation."
        help()
        sys.exit()

if __name__ == "__main__":
    main()
