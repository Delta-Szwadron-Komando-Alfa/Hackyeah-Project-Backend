import base64
from lxml import etree


def parse_xml_binary(xml_file):
    xml_doc = etree.parse(xml_file)
    nsmap = {}
    for ns in xml_doc.xpath('//namespace::*'):
        if ns[0]: # Removes the None namespace, neither needed nor supported.
            nsmap[ns[0]] = ns[1]
    
    element = xml_doc.xpath('//str:DaneZalacznika', namespaces=nsmap)[0].text
    file_name = xml_doc.xpath('//str:Zalacznik', namespaces=nsmap)[0].attrib['nazwaPliku']
    decoded_element = base64.b64decode(element)
    for attach in xml_doc.xpath('//str:Zalaczniki', namespaces=nsmap)[0]:
        it = attach.iter()
        file_name = next(it).attrib.get('nazwaPliku')
        data = next(it).text
        decoded_data = base64.b64decode(data)

        with open(file_name, 'wb') as file:
            file.truncate(0)
            file.write(decoded_data)
