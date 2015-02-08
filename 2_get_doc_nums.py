#!/usr/bin/env python
# This program takes RINs, obtained from reginfo.gov files, and tries to match them to document numbers, which is what the federal register uses to organize files on its site.  The input is a file called 'final_fixed' that should have RIN data in the third column. It uses the federalregister.gov api to search by a particular RIN, downloads the csv that this search produces, and then opens that csv and grabs the doc num.  The output is a file called 'rins_2.csv' that is identical to final_fixed but includes a column for docket id and column for doc nums.

# Files from the federal register are placed in Desktop/rule_csvs.  On occasion this process has thrown up errors on the federalregister's side, hence the check for files that already exist.  If the program exits with an error, it can be run again without losing any work.

from __future__ import division
import string
from elementtree.ElementTree import parse
import csv
import os
import urllib2
import time

def pause(url):
    try:
        b=urllib2.urlopen(url)
    except:
        time.sleep(60)
        pause(row)
    return(b)

dir1='/Users/austinc/Desktop/rule_csvs/'
all_data=[]

filereader=csv.reader(open('/Users/austinc/Desktop/final_fixed.csv','rU'), delimiter=',')
for row in filereader:
    rin=row[2]
    url='http://www.federalregister.gov/api/v1/articles.csv?fields%%5B%%5D=action&fields%%5B%%5D=docket_id&fields%%5B%%5D=document_number&per_page=20&order=relevance&conditions%%5Btype%%5D%%5B%%5D=RULE&conditions%%5Bregulation_id_number%%5D=%s' % (rin)
    file_name='%s.csv' % (rin)
    try:
        with open('/Users/austinc/Desktop/rule_csvs/%s' % (file_name)) as f:
            print 'already got it'
    except IOError as e:
        try:
            u=urllib2.urlopen(url)
        except:
            u=pause(url)
        f=open('%s%s' % (dir1,file_name), 'wb')
        file_size_dl = 0
        block_sz = 20480
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
        f.close()
    filereader2=csv.reader(open('/Users/austinc/Desktop/rule_csvs/%s' % (file_name),'rU'), delimiter=',')
    temp=[]
    temp2=[]
    keep=[]
    doc_ids=[]
    for brow in filereader2:
        if brow[0][0:10].lower()=='final rule':
            temp.append(brow[2])
            temp2.append(brow[1])
    row.append(temp2)
    row.append(temp)
    all_data.append(row)
writer=csv.writer(open('/Users/austinc/Desktop/rins_2.csv','wb'),delimiter='*')
for row in all_data:
    writer.writerow(row)


