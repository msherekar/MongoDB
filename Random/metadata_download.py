import requests
from bs4 import BeautifulSoup

# Make a request to the EMPIAR webpage
empiar_webpage_url = "https://www.ebi.ac.uk/empiar/EMPIAR-11629/"
response_webpage = requests.get(empiar_webpage_url)

# Check if the request to the webpage was successful
if response_webpage.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response_webpage.text, 'html.parser')

    # Find the Download XML link on the webpage
    Download_xml_link = soup.find('a', {'href': '/pub/databases/emtest/empiar/headers/11629.xml'})

    if Download_xml_link:
        # Construct the full URL for the XML file
        xml_url = "https://ftp.ebi.ac.uk" + Download_xml_link['href']

        # Make a request to the XML file URL
        response_xml = requests.get(xml_url)

        # Check if the request to the XML file was successful
        if response_xml.status_code == 200:
            xml_data = response_xml.text
            # Process the XML data as needed
            print(xml_data)
        else:
            print(f"Error downloading XML file: {response_xml.status_code}, {response_xml.text}")
    else:
        print("Download XML link not found on the webpage.")
else:
    print(f"Error accessing EMPIAR webpage: {response_webpage.status_code}, {response_webpage.text}")
