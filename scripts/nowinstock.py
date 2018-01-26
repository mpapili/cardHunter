#! /usr/bin/python
import sys
import os
import urllib2
import datetime



class urlHandler(object):

    def __init__(self, url):
        self.url=url

    def returnResponse(self):
        httpresponse = urllib2.urlopen(self.url).read()
        return httpresponse

def getCardDicts():
    cards = []
    for line in open('cards.csv'):
        entries = line.split(",")
	cardDict = {
	    'name': entries[0],
	    'url': entries[1],
	    'prices': entries[2].split(" "),
	}
	cards.append(cardDict)
    return cards


def getDateString():
    myDate = datetime.datetime.now()
    monthNames = {
	'01': 'Jan',
	'02': 'Feb',
	'03': 'Mar',
	'04': 'Apr',
	'05': 'May',
	'06': 'Jun',
	'07': 'Jul',
	'08': 'Aug',
	'09': 'Sep',
	'10': 'Oct',
	'11': 'Nov',
	'12': 'Dec',
    }
    return "{0} {1}".format(monthNames[myDate.strftime('%m')], myDate.strftime('%d'))
    

def loopCheck(url, desc, prices):
	currentDate = getDateString()
	killbool = False
	while True:
		myHandler=urlHandler(url)
		httpresponse = myHandler.returnResponse()
		lines=httpresponse.split(currentDate)
		if len(lines) > 2:
		    lineToRead = lines[1]
		elif len(lines) == 2:
		    lineToRead = lines[0]
		if "in stock" in lines[1].lower():
		    foundBool = False
		    for price in prices:
		        if "${0}".format(price.rstrip()) in lineToRead.lower():
		            print "IT'S IN STOCK!"
		            os.system('/usr/bin/mpg123 /home/mike/Downloads/plucky.mp3')
			    print "FOUND IN STOCK FOR:"
			    for word in lineToRead.split(" "):
			        if "$" in word:
					print word
			    print description
			    print url
			    killbool = True
			    foundBool = True
		            break
		    if foundBool:
		        return True
		    else:
		        print "in-stock, but did not match prices"
			return False
		elif "out of stock" in lines[1].lower():
		    print "out of stock"
		    return False
		elif "preorder" in lines[1].lower():
		    for price in prices:
		    	if "${0}".format(price.rstrip()) in lineToRead.lower():
			    print lines[1]
			    print "IT'S FOR PREORDER"
		            os.system('mpg123 plucky.mp3')
		            print lines[1]
			    print "FOUND PREORDER FOR:"
			    print description
			    killbool = True
		            return True
		os.system("sleep 2")
		if killbool:
		    return True
	return False

### Main

cardDicts = getCardDicts()
exitBool = False
while True:
	for card in cardDicts:
	    print "Checking stock on {0} price starting in ${1}".format(card['name'], card['prices'])
	    try:
		    if loopCheck(card['url'], card['name'], card['prices']):
			exitBool = True
	    except Exception as error:
		if "list index" in str(error):
		    print "no stock updates for today yet - please wait until today's date has a change... retrying..."
		else:
		    print "ERROR OCCURRED - RETRYING\n{0}".format(error)
		os.system("sleep 1")
	if exitBool:
		break
