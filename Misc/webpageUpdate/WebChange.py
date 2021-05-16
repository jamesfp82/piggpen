# Hunter Thornsberry
# http://www.adventuresintechland.com

# WebChange.py
# Alerts you when a webpage has changed it's content by comparing checksums of the html.

import hashlib
import urllib.request
import random
import time
import twilio.rest

# url to be scraped
url = "http://www.onofrio.com/execpgm/fndindex?show=PL2020061006DM"

# time between checks in seconds
sleeptime = 60

# we import the Twilio client from the dependency we just installed
from twilio.rest import Client
SID = "SID"
TOKEN = "TOKEN"
TO_PHONE_NUMBER = "+15555555555"

# the following line needs your Twilio Account SID and Auth Token
client = Client(SID, TOKEN)

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to=TO_PHONE_NUMBER, 
                       from_="+19033077444", 
                       body="Monitoring activated.  When the web page updates, you will receive a text.")

def getHash():
    # random integer to select user agent
    randomint = random.randint(0,7)

    # User_Agents
    # This helps skirt a bit around servers that detect repeated requests from the same machine.
    # This will not prevent your IP from getting banned but will help a bit by pretending to be different browsers
    # and operating systems.
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
    ]

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', user_agents[randomint])]
    response = opener.open(url)
    the_page = response.read()

    return hashlib.sha224(the_page).hexdigest()

current_hash = getHash() # Get the current hash, which is what the website is now

while 1: # Run forever
    if getHash() == current_hash: # If nothing has changed
        print ("Not Changed")
    else: # If something has changed
        print ("Changed")
        client.messages.create(to=TO_PHONE_NUMBER, 
                       from_="+19033077444", 
                       body=url + " has updated in the past minute.")
        break
    time.sleep(sleeptime)