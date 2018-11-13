# This python script preps xml eComma data for manual tagging.
# It adds a tag for Chapter to each comment node
# It merges the data from 7 songs/chapters into a single file.
# It redacts data based on a list of students who did not sign consent forms.
# It anonymizes the student names in the remaining data to randomly generated fake names.
# It produces a reference mapping fake names to real names.
# It counts the number of words in each comment and adds this number to a new Wordcount tag.
# It adds a tag for Language with a default value of English.
# It adds empty tags for Affordance and Speech-Act.

from xml.dom import minidom, getDOMImplementation
from xml.dom.minidom import parse, parseString
from faker import Faker
from collections import defaultdict
import re
import json

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

# Add a Chapter node to each comment
for node in ch2doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Chapter')) == 0:
        ChapterNode = ch2doc.createElement('Chapter')
        chapter = ch2doc.createTextNode('2')
        tab = ch2doc.createTextNode('  ')
        node.appendChild(tab)
        node.appendChild(ChapterNode)
        node.lastChild.appendChild(chapter)
        newline = ch2doc.createTextNode('\n    ')
        node.appendChild(newline)
for node in ch3doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Chapter')) == 0:
        ChapterNode = ch3doc.createElement('Chapter')
        chapter = ch3doc.createTextNode('3')
        tab = ch3doc.createTextNode('  ')
        node.appendChild(tab)
        node.appendChild(ChapterNode)
        node.lastChild.appendChild(chapter)
        newline = ch3doc.createTextNode('\n    ')
        node.appendChild(newline)
for node in ch4doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Chapter')) == 0:
        ChapterNode = ch4doc.createElement('Chapter')
        chapter = ch4doc.createTextNode('4')
        tab = ch4doc.createTextNode('  ')
        node.appendChild(tab)
        node.appendChild(ChapterNode)
        node.lastChild.appendChild(chapter)
        newline = ch4doc.createTextNode('\n    ')
        node.appendChild(newline)
for node in ch5doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Chapter')) == 0:
        ChapterNode = ch5doc.createElement('Chapter')
        chapter = ch5doc.createTextNode('5')
        tab = ch5doc.createTextNode('  ')
        node.appendChild(tab)
        node.appendChild(ChapterNode)
        node.lastChild.appendChild(chapter)
        newline = ch5doc.createTextNode('\n    ')
        node.appendChild(newline)
# for node in ch6doc.getElementsByTagName('node'):
#     if len(node.getElementsByTagName('Chapter')) == 0:
#         ChapterNode = ch6doc.createElement('Chapter')
#         chapter = ch6doc.createTextNode('6')
#         tab = ch6doc.createTextNode('  ')
#         node.appendChild(tab)
#         node.appendChild(ChapterNode)
#         node.lastChild.appendChild(chapter)
#         newline = ch6doc.createTextNode('\n    ')
#         node.appendChild(newline)
# for node in ch7doc.getElementsByTagName('node'):
#     if len(node.getElementsByTagName('Chapter')) == 0:
#         ChapterNode = ch7doc.createElement('Chapter')
#         chapter = ch7doc.createTextNode('7')
#         tab = ch7doc.createTextNode('  ')
#         node.appendChild(tab)
#         node.appendChild(ChapterNode)
#         node.lastChild.appendChild(chapter)
#         newline = ch7doc.createTextNode('\n    ')
#         node.appendChild(newline)

# Create new xml which merges comments from all the chapters
impl = getDOMImplementation()
doc = impl.createDocument(None, "nodes", None)
for node in ch2doc.getElementsByTagName('node'):
    doc.firstChild.appendChild(node)
for node in ch3doc.getElementsByTagName('node'):
    doc.firstChild.appendChild(node)
for node in ch4doc.getElementsByTagName('node'):
    doc.firstChild.appendChild(node)
for node in ch5doc.getElementsByTagName('node'):
    doc.firstChild.appendChild(node)
# for node in ch6doc.getElementsByTagName('node'):
#     doc.firstChild.appendChild(node)
# for node in ch7doc.getElementsByTagName('node'):
#     doc.firstChild.appendChild(node)

# Get list of students to redact from the data
with open('redactlist_%s.txt' % coursenumber) as f:
    redactlist = f.read().splitlines()

# Redact comments by students on the redactlist
NodesToRedact = [node for node in doc.getElementsByTagName("Author") if node.firstChild.nodeValue in redactlist]
for node in NodesToRedact:
    doc.documentElement.removeChild(node.parentNode);

# Change student names to fake names
# First, get the list of student names
studentlist = []
for node in doc.getElementsByTagName('Author'):
    studentlist.append(node.firstChild.nodeValue)
def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]
studentlist = unique(studentlist)

# Next, create a dictionary where each name is assigned a fake value
fake = Faker()
fake.seed(coursenumber) #Use the same seed every time, but a different seed for each course
studentdict = {i:fake.name() for i in studentlist}
with open('fakenames_%s.txt' % coursenumber, 'w') as f:
    f.write(json.dumps(studentdict))

# Add wordcount node to each comment
for node in doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Wordcount')) == 0:
        WordcountNode = doc.createElement('Wordcount')
        CommentNode = node.childNodes[9]
        CommentText = CommentNode.firstChild.nodeValue
        countthewords = str(len(CommentText.split(" ")))
        wordcount = doc.createTextNode(countthewords)
        node.appendChild(WordcountNode)
        node.lastChild.appendChild(wordcount)
        newline = doc.createTextNode('\n    ')
        node.appendChild(newline)
        
# Add Language node to each comment
for node in doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Language')) == 0:
        LanguageNode = doc.createElement('Language')
        defaultlanguage = doc.createTextNode('English')
        node.appendChild(LanguageNode)
        node.lastChild.appendChild(defaultlanguage)
        newline = doc.createTextNode('\n    ')
        node.appendChild(newline)
        
# Add Affordance node to each comment
for node in doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Affordance')) == 0:
        AffordanceNode = doc.createElement('Affordance')
        node.appendChild(AffordanceNode)
        newline = doc.createTextNode('\n    ')
        node.appendChild(newline)

# Add Speech Act node to each comment
for node in doc.getElementsByTagName('node'):
    if len(node.getElementsByTagName('Speech-Act')) == 0:
        SpeechActNode = doc.createElement('Speech-Act')
        node.appendChild(SpeechActNode)
        newline = doc.createTextNode('\n')
        node.appendChild(newline)

# Write the data to a new file
with open('ecomma_prepped_%s.xml' % coursenumber,'w+', encoding="UTF-8") as newfile:
    doc.writexml(newfile)

# Define function for replacing names with fake names
def find_replace_multi(string, dictionary):
    for item in dictionary.keys():
        # sub item for item's paired value in string
        string = re.sub(item, dictionary[item], string)
    return string

# Replace names with fake names, and fix encoding of some special characters
with open('ecomma_prepped_%s.xml' % coursenumber, "r+", encoding = "UTF-8") as f:
    data = f.read()
    data = data.replace('&quot;','"')
    data = data.replace("&#039;","'")
    data = find_replace_multi(data, studentdict)
    f.seek(0)
    f.write(data)
    f.truncate()
