import requests
import csv
import os
import json
import time
from datetime import datetime
from config import load_config
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup




def fetch_html_content(url:str) -> BeautifulSoup:
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

    # Make the request to the URL
    response = requests.get(url, headers=headers)
    
    # Check for any HTTP errors
    response.raise_for_status()

    # Determine the encoding from the response
    encoding = response.encoding
    
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




def extract_text_from_selector(soup,selector):
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
        return None




def parse_links(links,config:dict):
    """
    Parses product information from a list of links.

    Args:
        links (list): List of product URLs.
        config (dict): Configuration dictionary.

    Yields:
        dict: Product information.
    """

    for link in links:
        soup = fetch_html_content(link)
        for indx,html in enumerate(soup.select(config.get('home_product'))):
            print(f"Extrayendo: {extract_text_from_selector(html,config.get('product_name'))}")
            yield {
                    "id" : indx + 1,
                    'product_name' : extract_text_from_selector(html,config.get('product_name')),
                    'review': extract_text_from_selector(html,config.get('review')),
                    'price': extract_text_from_selector(html,config.get('price')),
                    'discount_price': extract_text_from_selector(html,config.get('discount_price')),
                    'date': str(datetime.now())
                    }



def create_csv(list_data):
    rute = Path.cwd() / 'data' / 'product_ML.csv'
    if not rute.exists():
        with open(rute, mode='a') as file_csv:
            columns = list_data[0].keys()
            archivo = csv.DictWriter(file_csv,fieldnames=columns)
            archivo.writeheader()
            archivo.writerows(list_data)
    else:
        with open(rute, mode='a') as file_csv:
            columns = list_data[0].keys()
            archivo = csv.DictWriter(file_csv,fieldnames=columns)
            archivo.writerows(list_data)

        

if __name__ == '__main__':
    # Load environment variables from a .env file
    load_dotenv('.env')
    pagina = 1
    config = load_config()
    list_data = []
    for page in range(1,pagina+1):
        print("Estrayendo pagina:"+ str(page))
        URL = f'https://www.mercadolibre.com.mx/ofertas?container_id=MLM779363-1&page={page}'
        try:
            soup = fetch_html_content(URL)
        except Exception as err:
            print('Error: %s' % err)

        links = extract_links(soup,config)
        for data in parse_links(links,config):
            print(data)
            list_data.append(data)
        time.sleep(3)
        print('pagina_descansa')
    create_csv(list_data)
    


