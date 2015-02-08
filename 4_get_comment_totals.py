#!/usr/bin/env python
# This program takes rule RINs and checks the docket on regulations.gov to find out how many comments are in the docket folder.  It uses the regulations.gov api.  The input is 'rins_3.csv' and the output is 'rins_final_presplit.csv'.  The next step is to run these through the splitter to prepare them for btscs.

# note: on occasion I have found RINs that should have associated comments but do not on regulations.gov.  This appears to be because reginfo.gov keeps records that go back further than what regulations.gov keeps.  This probably won't work for any rule that is older than 2000.  Double check.

from __future__ import division
import string
from elementtree.ElementTree import parse
import csv
import os
import urllib2
import time

dir1='/Users/austinc/Desktop/rule_csvs/'
all_data=[]
increment=1

def pause(url):
    try:
        b=urllib2.urlopen(url)
    except:
        print 'except'
        time.sleep(60)
        pause(row)
    return(b)

filereader=csv.reader(open('/Users/austinc/Desktop/rins_3.csv','rU'), delimiter='*')
for row in filereader:
    rin=row[2]
    url='http://www.regulations.gov/api/documentsearch/v1.xml?dct=PS&s=%s&api_key=b65b91d6-9daa-43c8-9314-f5d2b4d0c995&countsOnly=1' % (rin)
    try:
        u=urllib2.urlopen(url)
    except:
        u=pause(url)
    tree=parse(u)
    doc=tree.getroot()
    comments=doc[0].text
    row.append(comments)
    all_data.append(row)
    print rin, comments
writer=csv.writer(open('/Users/austinc/Desktop/rins_final_presplit.csv','wb'),delimiter='*')
for row in all_data:
    writer.writerow(row)
