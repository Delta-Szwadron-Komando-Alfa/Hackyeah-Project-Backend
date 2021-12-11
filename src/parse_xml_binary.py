import base64
from lxml import etree


def parse_xml_binary(xml_file, file_name='file.zip'):
    xml_doc = etree.parse(xml_file)
    nsmap = {}
    for ns in xml_doc.xpath('//namespace::*'):
        if ns[0]: # Removes the None namespace, neither needed nor supported.
            nsmap[ns[0]] = ns[1]
    
    element = xml_doc.xpath('//str:DaneZalacznika', namespaces=nsmap)[0].text
    decoded_element = base64.b64decode(element)

    with open(file_name, 'wb') as file:
        file.truncate(0)
        file.write(decoded_element)
        return file
