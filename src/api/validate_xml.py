from lxml import etree


def validate_xml_with_xsd(xml_file, xsd_file) -> bool:
    """
    You can pass either paths to the files
    or you can pass files opened in Python
    """
    xmlschema_doc = etree.parse(xsd_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_file)
    result = xmlschema.validate(xml_doc)

    return result
