#
#	Contest Parser v1.0
#	
#	shauryachats@gmail.com

import sys
import urllib
import urllib2
import os
import datetime
from bs4 import BeautifulSoup

def download_page(url, file_name, redownload = False):
	file_path = ".contests/" + file_name
	try:
		os.remove(file_path)
	except OSError:
		pass
	try:
		urllib.urlretrieve(url , file_path)
	except IOError:
		return False

	return True

CODECHEF_SAVE_PATH = ".contests/codechef.html"
HOURS_FOR_REDOWNLOADING = 2

#First, we'll check if this program has been run before.
if (not os.path.exists(".contests")):
	os.makedirs(".contests")

download_webpage = True

#The time stamp when the page was downloaded
downloaded_time = None

if (os.path.exists(CODECHEF_SAVE_PATH)):
	downloaded_time = datetime.datetime.fromtimestamp(os.path.getmtime(CODECHEF_SAVE_PATH))
	time_diff = datetime.datetime.now() - downloaded_time
	if (int(time_diff.seconds / 3600) < HOURS_FOR_REDOWNLOADING):
		download_webpage = False

if (download_webpage):
	print "Attempting to download webpage..."
	x = download_page("http://codechef.com/contests","codechef.html")	
else:
	print "Webpage already downloaded."

if (download_webpage and not x):
	print "Failed to download webpage. Please retry again."
	sys.exit(1)
elif (download_webpage):
	print "Webpage downloaded."
print "Preparing to parse webpage."

try:
	parsed_page = BeautifulSoup(open(CODECHEF_SAVE_PATH))
	h3_tag = parsed_page.h3
except IOError:
	print "Failed to parse webpage. Please retry again."
	sys.exit(2)

print "Website parsed."

#Manually tallying with the HTML to form a relationship path.
contest_data = h3_tag.next_sibling.next_sibling.table.tr

contest_code = []
contest_name = []
#Stores start times as a "datetime" object
start_time = []
end_time = []

#Traversing through the parsed HTML to handpick items.
while (contest_data is not None and contest_data.next_sibling is not None and contest_data.next_sibling.next_sibling is not None):
	contest_data = contest_data.next_sibling.next_sibling
	
	field = contest_data.td
	
	contest_code.append(field.getText())
	#print field.getText()

	field = field.next_sibling.next_sibling	

	contest_name.append(field.getText())
	#print field.getText()	
	
	field = field.next_sibling.next_sibling
	
	start_time.append(datetime.datetime.strptime(field.getText(),"%Y-%m-%d %H:%M:%S"))
	#print field.getText()
	
	field = field.next_sibling.next_sibling
	
	end_time.append(datetime.datetime.strptime(field.getText(),"%Y-%m-%d %H:%M:%S"))
	#print field.getText()

#All data fetched, now to present it in a palatable form.

"""TODO: Add description support"""

number_of_contests = len(contest_code)

print "\nCODECHEF : UPCOMING CONTESTS\n"

for i in range(number_of_contests):
	print "**************************************"
	print "Contest Name:" , contest_name[i]
	print "Contest Code:" , contest_code[i], "\n"
	print "The contest starts on" , start_time[i].strftime("%d %b %Y") , "at" , start_time[i].strftime("%I:%M %p")
	length_of_contest = end_time[i] - start_time[i]
	print "The contest is", 
	if (length_of_contest.days != 0):
		print length_of_contest.days, "days and"
	print str(length_of_contest.seconds / 3600) , "hours long."
	time_from_now  = start_time[i] - datetime.datetime.now()
	print "\nThe contest will start", 
	if (time_from_now.days != 0):
		print str(time_from_now.days), "days and",
	print str(int(time_from_now.seconds / 3600)), "hours from now."
 
print "**************************************"



