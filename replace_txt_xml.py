import sys
import xml.dom.minidom

if len(sys.argv)!=4:
	print 'usage: %s input-txt-file input-xml-file output-xml-file'%sys.argv[0]
	sys.exit()

input_txt_file=open(sys.argv[1])
input_xml_file=open(sys.argv[2])
output_xml_filename=sys.argv[3]

input_xml=xml.dom.minidom.parse(input_xml_file)
input_txt=input_txt_file.readlines()
seg_tags=input_xml.getElementsByTagName('seg')
if len(input_txt)!=len(seg_tags):
	print 'error: number of lines in text file (%d) is different with number of seg tags (%d)'%(len(input_txt), len(seg_tags))
	sys.exit()

for i in range(len(input_txt)):
	seg_tags[i].childNodes[0].data=input_txt[i].decode('u8').rstrip('\n')

s=input_xml.toxml('UTF-8')
s=s.replace('encoding="UTF-8"?><mteval>', 'encoding="UTF-8"?>\n<mteval>')
f=open(output_xml_filename, 'wb')
f.write(s)
f.close()
