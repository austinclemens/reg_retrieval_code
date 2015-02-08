#!/usr/bin/env python
# This program takes a spreadsheet with doc_nums and downloads the appropriate file off of federalregister.gov.  Using the fr api, it finds the length of the rule and appends it to the dataset.  The input is a file called 'rins_2.csv' and the output is a file called 'rins_3.csv'.

from __future__ import division
import string
from elementtree.ElementTree import parse
import csv
import os
import urllib2
import time

dir1='/Users/austinc/Desktop/rule_csvs/'
all_data=[]
increment=0

def pause(url):
    try:
        b=urllib2.urlopen(url)
    except:
        print 'loop'
        time.sleep(30)
        pause(url)
    return(b)

filereader=csv.reader(open('/Users/austinc/Desktop/rins_2.csv','rU'), delimiter='*')
for row in filereader:
    doc_ide=row[14]
    doc_ide2=doc_ide.strip("[]")
    doc_ide3=doc_ide2.replace("'",'')
    doc_ids=doc_ide3.split(',')
    doc_ids=[doc.strip() for doc in doc_ids]
    pages_total=0
    docket=''
    for doc_id in doc_ids:
        if len(doc_id)>0:
            url='http://www.federalregister.gov/api/v1/articles/%s.csv?fields%%5B%%5D=docket_id&fields%%5B%%5D=end_page&fields%%5B%%5D=start_page' % (doc_id)
            try:
                u=urllib2.urlopen(url)
            except:
                u=pause(url)
            f=u.read()
            for brow in f.split('\n')[1:]:
                f2=brow.split(',')
                pages=0
                try:
                    docket=f2[0]
                except:
                    docket=''
                try:
                    pages=int(f2[1])-int(f2[2])+1
                except:
                    pages=0
                pages_total=pages_total+pages
    row.append(pages_total)
    row.append(docket)
    all_data.append(row)
    increment=increment+1
    print increment
writer=csv.writer(open('/Users/austinc/Desktop/rins_3.csv','wb'),delimiter='*')
for row in all_data:
    writer.writerow(row)
