import xml.etree.ElementTree as ET

def print_xml_nodes(element, indent=0):
    """Recursively print XML nodes and sub-nodes."""
    print(' ' * indent + f"Node: {element.tag}, Text: {element.text}")
    for child in element:
        print_xml_nodes(child, indent + 2)

def read_and_print_xml(file_path):
    """Read XML file and print all nodes and sub-nodes."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        print(f"Root Node: {root.tag}")
        print_xml_nodes(root)
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")

# Replace 'your_file.xml' with the actual file path
file_path = '/Users/mukulsherekar/pythonProject/DatabaseProject/dbprojectxmlfiles/AT_sec_1_tile_9.xml'
read_and_print_xml(file_path)
