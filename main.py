import requests, re, sys
from bs4 import BeautifulSoup
from lib.output_factory import OutputFactory

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

    data  = []

    for link in links:
        href  = link.attrs['href']
        match = re.search(pattern, 'u"' + href + '"')

        if match is not None:
            data.append(match.group(1))

    return int(max(data))

# Update the dork
def update(last_dork, url):
    print "Updating"

# intialize the dork
def initialize(latest_dork, url, args):
    start = 1
    end   = latest_dork + 1
    print "Initialized.."
    collection = []

    for i in range(start, end):
        print("Fetching the dork %d from %d" % (i, end) )
        dork_url        = url + str(i) + '/'
        print("URL: %s" % dork_url)
        google_dork     = requests.get(dork_url)
        beautiful_soup  = BeautifulSoup(google_dork.content)
        
        collection.append(extract_data(i, beautiful_soup))
    
    print args
    print("Fetching the medium instance..")
    medium = OutputFactory.create(str(args[2]))
    medium.set(collection)
    print("Saving the data..")
    medium.save()

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
        print "Make yourslef comfortable"

def main():
    args_length = len(sys.argv)
    cmd_args    = str(sys.argv)

    if cmd_args[1] == 'help':
        help()
        sys.exit()

    if args_length < 3:
        print("Minimum required arguments are three.")
        help()
        sys.exit()

    if cmd_args[2] == "mysqldb" and args_length != 5:
        print("Minimum 5 arguments are required for mysql database process.")
        help()
        sys.exit()
    print "Initializing.."
    initialize(latest_dork(google_dorks_url), google_dork_url, sys.argv)

if __name__ == "__main__":
    main()
