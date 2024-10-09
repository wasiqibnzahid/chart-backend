import requests
import xml.etree.ElementTree as ET

def fetch_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.text

def parse_sitemap(xml_content):
    root = ET.fromstring(xml_content)
    urls = []

    for url in root.findall(".//url"):
        loc = url.find("loc").text
        lastmod = url.find("lastmod")
        lastmod_date = lastmod.text if lastmod is not None else None
        urls.append((loc, lastmod_date))

    return urls

def sort_urls_by_date(urls):
    # Sort by date; None values are treated as the earliest date
    return sorted(urls, key=lambda x: x[1] or '')

def main():
    sitemap_url = 'https://www.tvazteca.com/aztecanoticias/sitemap-content.xml'
    xml_content = fetch_sitemap(sitemap_url)
    urls = parse_sitemap(xml_content)
    sorted_urls = sort_urls_by_date(urls)

        
        
main()