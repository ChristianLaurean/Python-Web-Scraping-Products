import requests
import csv
import time
from datetime import datetime
from config import load_config
from pathlib import Path
from bs4 import BeautifulSoup




def fetch_html_content(url:str, page:int = None) -> BeautifulSoup:
    """
    Fetches HTML content from the specified URL.

    Args:
        url (str): The URL of the website to extract HTML from.

    Returns:
        BeautifulSoup: Parsed HTML content using BeautifulSoup.
    """

    # Set a user agent to avoid potential blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    if page:
        # Make the request to the URL
        response = requests.get(url + str(page), headers=headers)
    else:
        response = requests.get(url, headers=headers)

    
    # Check for any HTTP errors
    response.raise_for_status()

    
    # Parse the HTML content using BeautifulSoup
    return BeautifulSoup(response.text, 'html.parser')    




def extract_links(soup: BeautifulSoup, config: dict):
    """Parses links from the BeautifulSoup object based on the specified configuration.

    Args:
        soup (BeautifulSoup): BeautifulSoup Object
        config (dict): Configuration dictionary

    Yields:
        str: links for each product
    """

    # We extract the links of all the products on the page
    for element in soup.select(config.get('homepage')):
        yield element.get('href')




def extract_text_from_selector(soup: BeautifulSoup, selector):
    """
    Extracts text content from the specified selector within a BeautifulSoup object.

    Args:
        soup (BeautifulSoup): BeautifulSoup Object.
        selector (str): CSS selector to locate the desired element.

    Returns:
        str or None: Extracted text content or None if the element is not found.
    """
        
    try:
        return soup.select_one(selector).text
    except AttributeError:
        return 'None'




def parse_links(links,config:dict):
    """
    Parses product information from a list of links.

    Args:
        links (list): List of product URLs.
        config (dict): Configuration dictionary.

    Yields:
        dict: Product information.
    """
    date = datetime.now()
    for link in links:
        #Parse the HTML content using BeautifulSoup
        soup = fetch_html_content(link)

        # load data page in dict
        for html in soup.select(config.get('home_product')):
            print(f"extracting: {extract_text_from_selector(html,config.get('product_name'))}")
            yield {
                    'product_name' : extract_text_from_selector(html,config.get('product_name')),
                    'review':extract_text_from_selector(html,config.get('review')),
                    'price': extract_text_from_selector(html,config.get('price')),
                    'discount_price': extract_text_from_selector(html,config.get('discount_price')),
                    'date': date.strftime('%Y/%m/%d')
                    }




def create_csv(list_data: list, config: dict):
    """
    Creates a CSV file and writes data to it.

    Parameters:
    - data_list (list): List of dictionaries containing data to be written to the CSV file.
    - config (dict): Configuration dictionary.
    """

    # Define the path for the CSV file
    rute = Path.cwd() / 'data' / config.get('csv_name')
     # Check if the file already exists
    if not rute.exists():
        # If not, create a new CSV file and write the header
        with open(rute, mode='a') as file_csv:
            columns = list_data[0].keys()
            archivo = csv.DictWriter(file_csv,fieldnames=columns)
            archivo.writeheader()
            archivo.writerows(list_data)
    else:
        # If the file already exists, open it and append the data
        with open(rute, mode='a') as file_csv:
            columns = list_data[0].keys()
            archivo = csv.DictWriter(file_csv,fieldnames=columns)
            archivo.writerows(list_data)

        


if __name__ == '__main__':
    # Load configuration settings
    config = load_config()
    
    # Get the number of pages to scrape
    pages = config.get('pages')

    # Initialize an empty list to store scraped data
    list_data = []

    # Iterate through the provided URLs and pages
    for url in config.get('urls'):
        for page in range(1,pages+1):
            print("extracting page:"+ str(page))

            try:
                 # Fetch HTML content from the URL
                soup = fetch_html_content(url,page)
            except Exception as err:
                print('Error: %s' % err)

            # Extract links from the HTML content
            links = extract_links(soup,config)

            # Parse data from the extracted links
            for data in parse_links(links,config):
                list_data.append(data)
        # We wait 5 seconds
        time.sleep(config.get('time'))

    # Create or append data to the CSV file
    create_csv(list_data,config)
    


