import xml.etree.ElementTree as ET

def get_xml_element(element: ET.Element, name: str):
    temp = element.find(name)
    if temp is None:
        raise Exception(f"Element {name} not found")
    return temp

def is_asm_file(file: str):
    if len(file) and (file.endswith(".s") or file.endswith(".S") or file.endswith(".sx") or file.endswith(".asm")):
        return True
    return False


def is_c_file(file: str):
    if len(file) and (file.endswith(".c") or file.endswith(".cpp")):
        return True
    return False
