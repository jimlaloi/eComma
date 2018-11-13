# This python script takes a set of eComma xml data files and produces a list of student names who participated.
# From this list, those who have signed a consent form can have their names manually removed.
# This leaves a list of students to redact from the data.


from xml.dom.minidom import parse, parseString

# Put the course number here before saving and running the script
coursenumber = '36360'

# Open the files and parse them with minidom
ch2data = open('ecomma_comments_export_%s_Ch2.xml' % coursenumber, encoding="UTF-8")
ch2doc = parse(ch2data)
ch3data = open('ecomma_comments_export_%s_Ch3.xml' % coursenumber, encoding="UTF-8")
ch3doc = parse(ch3data)
ch4data = open('ecomma_comments_export_%s_Ch4.xml' % coursenumber, encoding="UTF-8")
ch4doc = parse(ch4data)
ch5data = open('ecomma_comments_export_%s_Ch5.xml' % coursenumber, encoding="UTF-8")
ch5doc = parse(ch5data)
#ch6data = open('ecomma_comments_export_%s_Ch6.xml' % coursenumber, encoding="UTF-8")
#ch6doc = parse(ch6data)
#ch7data = open('ecomma_comments_export_%s_Ch7.xml' % coursenumber, encoding="UTF-8")
#ch7doc = parse(ch7data)

# Get list of student author names from each chapter
studentlist = []
for node in ch2doc.getElementsByTagName('Author'):
    studentlist.append(node.firstChild.nodeValue)
for node in ch3doc.getElementsByTagName('Author'):
    studentlist.append(node.firstChild.nodeValue)
for node in ch4doc.getElementsByTagName('Author'):
    studentlist.append(node.firstChild.nodeValue)
for node in ch5doc.getElementsByTagName('Author'):
    studentlist.append(node.firstChild.nodeValue)
# for node in ch6doc.getElementsByTagName('Author'):
#     studentlist.append(node.firstChild.nodeValue)
# for node in ch7doc.getElementsByTagName('Author'):
#     studentlist.append(node.firstChild.nodeValue)
    
# Write each name once to a txt file
with open('studentlist_%s.txt' % coursenumber, 'w') as f:
    for item in set(studentlist):
        f.write("%s\n" % item)
