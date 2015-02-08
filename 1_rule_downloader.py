#!/usr/bin/env python

# This program downloads rule information from reginfo.gov.  Reginfo provides the data as xml so a file is first downloaded for each rule and then the xml is parsed to create a csv that contains the RIN, a dummy for whether the rule was completed (final_action), the number of actions it took to complete the rule, the agency, subagency, priority, date the rule was commenced, and date the rule was completed.  It outputs a file called final_fixed.csv.  Refer to the program flow document.

from __future__ import division
import string
from elementtree.ElementTree import parse
import csv
import os
import urllib2
import time

dir1='/Users/austinc/Desktop/rules/'

def download(url):
    print url
    file_name = url.split('/')[-1]
    try:
        with open('/Users/austinc/Desktop/rules/%s' % (file_name)) as f:
            return(file_name)
    except IOError as e:
        try:
            u = urllib2.urlopen(url)
            filer=open('/Users/austinc/Desktop/rules/%s' % (file_name),'wb')
            filer.write(u.read())
            return(file_name)
        except:
            time.sleep(30)
            print 'beat'
            print url
            download(url)
    
def parse_xml(file):
    file_out=[]
    dates=[]
    actions=[]
    dates_trimmed=[]
    pos=-1
    print file
    tree=parse(file)
    doc=tree.getroot()
    rin=doc.find('RIN_INFO/RIN')
    agency=doc.find('RIN_INFO/PARENT_AGENCY/ACRONYM')
    sub_agency=doc.find('RIN_INFO/AGENCY/ACRONYM')
#   rule_title=doc.find('RIN_INFO/RULE_TITLE')
    priority=doc.find('RIN_INFO/PRIORITY_CATEGORY')
    for action in doc.findall('RIN_INFO/TIMETABLE_LIST/TIMETABLE/TTBL_ACTION'):
       actions.append(action.text.rstrip())
    for date in doc.findall('RIN_INFO/TIMETABLE_LIST/TIMETABLE/TTBL_DATE'):
       dates.append(date.text.rstrip())
    for position, item in enumerate(actions):
        if (item.lower()[0:12]=='final action' or item.lower()[0:10]=='final rule') and (item.lower()[0:20]!='final rule effective' or item.lower()[0:22]!='final action effective'):
            pos=position
    if pos==-1:
        file_out.append('0')
    else:
        file_out.append('1')
    file_out.append(str(len(dates)))
    try:
        dates_trimmed=[dates[0],dates[pos]]
    except:
        dates_trimmed=['.','.']
    try:
        file_out.append(rin.text.rstrip())
    except:
        file_out.append('.')
    try:
        file_out.append(agency.text.rstrip())
    except:
        file_out.append('.')
    try:
        file_out.append(sub_agency.text.rstrip())
    except:
        file_out.append('.')
#     try:
#         file_out.append(rule_title.text.rstrip())
#     except:
#         file_out.append('')
    try:
        file_out.append(priority.text.rstrip())
    except:
        file_out.append('.')
    file_out.append(dates_trimmed[0])
    file_out.append(dates_trimmed[1])
    return(file_out)

writer=csv.writer(open('/Users/austinc/Desktop/final_fixed.csv','wb'),delimiter='*')
writer.writerow(['Final_action','Actions','RIN','Agency','Subagency','Priority','Init_date','Final_date'])
filereader=csv.reader(open('/Users/austinc/Desktop/rule_codes.csv','rU'), delimiter=',')
for row in filereader:
    arg1=row[0]
    arg2=row[1]
    url='http://www.reginfo.gov/public/do/eAgendaViewRule?pubId=%s&RIN=%s&operation=OPERATION_EXPORT_XML' % (arg2,arg1)
    xml=download(url)
    parsed_row=parse_xml('/Users/austinc/Desktop/rules/%s' % (xml))
    writer.writerow(parsed_row)
