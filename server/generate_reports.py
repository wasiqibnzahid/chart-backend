import subprocess
import json
import time
from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from lxml import html
import feedparser


def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')


def fetch_feed_urls(feed_url):

    try:
        # Fetch the feed
        response = requests.get(feed_url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the feed
        feed = feedparser.parse(response.content)

        # Extract and sort entries by the latest update
        entries = feed.entries
        sorted_entries = sorted(
            entries, key=lambda x: x.updated_parsed, reverse=True)

        # Extract URLs
        urls = [entry.link for entry in sorted_entries]

        return urls

    except requests.RequestException as e:
        print(f"An error occurred while fetching the feed: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def fetch_data(url):
    if ("html" in url or "txt" in url):
        return url
    retry = 0
    while retry < 3:
        try:
            retry += 1
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            parsed_data = ET.fromstring(response.content)
            return parsed_data
        except requests.RequestException as error:
            print(f"Error accessing {url}. Retrying... ({error})")
            time.sleep(3)
    return None


def get_latest_urls(parsed_data, is_xml=True):
    if (parsed_data is None):
        return []
    if is_xml:
        # Handle XML sitemaps
        namespaces = {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                      'ns2': 'http://www.google.com/schemas/sitemap-video/1.1'}
        urls = []

        entries = parsed_data.findall(".//ns0:url", namespaces)
        if(len(entries) == 0):
            entries = parsed_data.findall(".//ns0:sitemap", namespaces)
        url_date_pairs = []
        
        for entry in reversed(entries):
            loc = entry.find("ns0:loc", namespaces)
            time = entry.find("ns0:lastmod", namespaces)
            if loc is not None and loc.text:
                date = time.text if time is not None and time.text else ''
                url_date_pairs.append((loc.text, date))

        # Sort by the date in descending order
        url_date_pairs.sort(key=lambda x: x[1], reverse=True)

        # Extract sorted URLs
        sorted_urls = [url for url, _ in url_date_pairs]
        # if not sorted_urls:
        #     print("No URLs found in the XML data.")

        return sorted_urls

    elif ("txt" in parsed_data):
        # Fetch the content from the URL
        url = parsed_data
        response = requests.get(url)

        # Ensure the request was successful
        if response.status_code != 200:
            print("Failed to fetch the file")
            return

        # Split the content into lines (each line contains a URL)
        lines = response.text.splitlines()

        # Separate URLs with and without the word "video"
        video_urls = []
        note_urls = []

        # Iterate over the lines from the bottom up
        for line in reversed(lines):
            if "video" in line and len(video_urls) < 10:
                video_urls.append(line)
            elif "video" not in line and len(note_urls) < 10:
                note_urls.append(line)

            # Stop if we have collected 10 of each type
            if len(video_urls) == 10 and len(note_urls) == 10:
                break

        return video_urls, note_urls
    else:
        return fetch_feed_urls(parsed_data)
def get_sorted_rss_items(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    parsed_data = ET.fromstring(response.content)

    # Define the namespaces used in the RSS feed
    namespaces = {
        'dc': 'http://purl.org/dc/elements/1.1/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dcterms': 'http://purl.org/dc/terms/',
        'atom': 'http://www.w3.org/2005/Atom',
        'media': 'http://search.yahoo.com/mrss/'
    }

    # Find all <item> elements
    items = parsed_data.findall(".//item")

    url_date_pairs = []

    for item in items:
        # Extract the <link> and <pubDate> for each item
        link = item.find("link").text if item.find("link") is not None else ''
        pub_date_text = item.find("pubDate").text if item.find("pubDate") is not None else ''

        # Parse the pubDate into a datetime object for sorting
        try:
            pub_date = datetime.strptime(pub_date_text, '%a, %d %b %Y %H:%M:%S %Z')
        except (ValueError, TypeError):
            pub_date = None  # Handle missing or invalid pubDate

        if link and pub_date:
            url_date_pairs.append((link, pub_date))

    # Sort the URLs by pubDate in descending order
    url_date_pairs.sort(key=lambda x: x[1], reverse=True)

    # Extract sorted URLs
    sorted_urls = [url for url, _ in url_date_pairs]

    return sorted_urls


# tv_azteca_companies = {
#     'aztecauno': {
#         'notaLink': 'https://www.tvazteca.com/aztecauno/sitemap-content.xml',
#         'videoLink': 'https://www.tvazteca.com/aztecauno/sitemap-video.xml',
#     },
#     'azteca7': {
#         'notaLink': 'https://www.tvazteca.com/azteca7/sitemap-content.xml',
#         'videoLink': 'https://www.tvazteca.com/azteca7/sitemap-video.xml',
#     },
#     'aztecadeportes': {
#         'notaLink': 'https://www.tvazteca.com/aztecadeportes/sitemap-content.xml',
#         'videoLink': 'https://www.tvazteca.com/aztecadeportes/sitemap-video.xml',
#     },
#     'adn40': {
#         'notaLink': 'https://www.adn40.mx/sitemap-content.xml',
#         'videoLink': 'https://www.adn40.mx/sitemap-video.xml',
#     },
#     'aztecanoticias': {
#         'notaLink': 'https://www.tvazteca.com/aztecanoticias/sitemap-content.xml',
#         'videoLink': 'https://www.tvazteca.com/aztecanoticias/sitemap-video.xml',
#     },
#     'amastv': {
#         'notaLink': 'https://www.tvazteca.com/amastv/sitemap-content.xml',
#         'videoLink': 'https://www.tvazteca.com/amastv/sitemap-video.xml',
#     }
# }

# result_file = 'lighthouse_results.txt'
# current_date = get_current_date()

# with open(result_file, 'w') as f:
#     f.write(f"{current_date}\n\n")

# for company, links in tv_azteca_companies.items():
#     nota_urls = []
#     video_urls = []

#     try:
#         nota_xml = fetch_data(links['notaLink'])
#         video_xml = fetch_data(links['videoLink'])
#         extracted_nota_urls = get_latest_urls(
#             nota_xml, is_xml="html" not in links["notaLink"])
#         extracted_video_urls = get_latest_urls(
#             video_xml, is_xml="html" not in links["videoLink"])

#         print(f"Extracted Nota URLs for {company}: {len(extracted_nota_urls)}")
#         print(f"Extracted Video URLs for {company}: {len(extracted_video_urls)}")

#         nota_urls.extend(extracted_nota_urls)
#         video_urls.extend(extracted_video_urls)

#         if not nota_urls:
#             print(f"No nota URLs found for {company}")
#         if not video_urls:
#             print(f"No video URLs found for {company}")
#     except Exception as error:
#         print(f"Error fetching URLs for {company}: {error}")
#         continue

#     nota_scores = []
#     video_scores = []
