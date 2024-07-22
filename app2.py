import pygooglenews
import xml.etree.ElementTree as ET

# Initialize GoogleNews object
gn = pygooglenews.GoogleNews()

# Search for a topic
search = gn.search("Heatwave India")

# Create the root XML element
root = ET.Element("articles")

# Add articles to the XML
for entry in search['entries']:
    article = ET.SubElement(root, "article")
    
    title = ET.SubElement(article, "title")
    title.text = entry.title
    
    link = ET.SubElement(article, "link")
    link.text = entry.link
    
    summary = ET.SubElement(article, "summary")
    summary.text = entry.summary
    
    date = ET.SubElement(article, "date")
    date.text = entry.published
    
    if 'source' in entry:
        source = ET.SubElement(article, "source")
        source.text = entry.source.title

# Write the XML to a file
tree = ET.ElementTree(root)
with open("articles.xml", "wb") as xml_file:
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
