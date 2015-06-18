import sys
from xml.dom import minidom
xmldoc = minidom.parse(sys.argv[1])
senselist = xmldoc.getElementsByTagName('SENSE') 
for sense in senselist:
	print sense.attributes['id'].value, sense.firstChild.data
itemlist = xmldoc.getElementsByTagName('SENTENCE') 
print "Len : ", len(itemlist)
print "Attribute id : ", itemlist[0].attributes['id'].value
print "Text : ", itemlist[0].firstChild.nodeValue
for s in itemlist :
    print "Attribute id : ", s.attributes['id'].value
    text = s.getElementsByTagName('TEXT')
    annotations = s.getElementsByTagName('ANNOTATOR')
    for a in text:
    	print "TEXT::", a.firstChild.data
    for annotation in annotations:
    	print "Annotations", annotation.attributes['id'].value, annotation.getElementsByTagName('SENSE_LABEL')[0].firstChild.data
