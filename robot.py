#!/usr/bin/env python2

import re
from robobrowser import RoboBrowser

br = RoboBrowser(history=True, parser="html.parser")

# Data for form post
data=dict(
    username="xxxxxxxxx@yyyyyyy.zzz",
    password="..."
)

# Start immediately with login
br.open(url='https://alifeatlethics.sportbitapp.nl/cbm/account/inloggen/?post=1', method='post', data=data)

# We parse the table and select all the possible dates
# To do this, we select all the lines with 'href="training-info/' that also contain 'data-time-start="07:00"'
date_options = list()
course_urls = list()
for line in str(br.parsed).splitlines():
    if 'href="training-info/' in line:
        if 'data-time-start="07:00"' in line:
            regex = re.search('training-info/(.+?)/07:00/(.+?)/', line)
            date = regex.group(1)
            course_id = regex.group(2)
            date_options.append(date)
            course_urls.append('training-info/' + date + '/07:00/' + course_id)

# We now let the user select the date
print("Please select the date for which you would like to log in: ")
for date in date_options:
    print("{}. {}".format(date_options.index(date)+1, date))

user_input = raw_input("Selection: ")
try:
    val = int(user_input) - 1
    if val < 0 or val >= len(date_options):
        print("That is not a valid selection, go fuck yourself, bye")
        exit()
except ValueError:
    print("That is not a number, go fuck yourself, bye")
    exit()

# We now grab the relevant course url
course = "https://alifeatlethics.sportbitapp.nl/cbm/" + course_urls[val]
print("\nOpening course with url {}".format(course))
br.open(course)


# Finally we look for the Aanmelden/Afmelden button and take the appropriate action
if "AFMELDEN" in str(br.parsed):
    print("You are already enrolled for this date")
    exit()

if "AANMELDEN" in str(br.parsed):
    print("Now trying to enroll you for the selected course")
    br.open(course + "/aanmelden")
else:
    print("Could not find the AANMELDEN button on page '{}'".format(course))
    exit()

# To wrap it up we check if the button has changed to AFMELDEN to confirm that we are enrolled
if "AFMELDEN" in str(br.parsed):
    print("\n----------------------------------------------")
    print("You have been properly enrolled for the course")
    print("----------------------------------------------")
else:
    print("\n--------------------------------")
    print("Something went terribly wrong :(")
    print("--------------------------------")

