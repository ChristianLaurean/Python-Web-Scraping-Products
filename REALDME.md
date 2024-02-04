# Web Scraping Tool

This Python script performs web scraping to extract product information from various web pages and saves it to a CSV file.

## Requirements

- Python
- Python Libraries: `requests`, `csv`, `time`, `datetime`, `config`, `pathlib`, `bs4`

## Setup

1.  Clone the repository:

    ```bash
    git clone https://github.com/ChristianLaurean/Python-Web-Scraping-Products.git
    cd your_project
    ```

2.Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.Create a config.yml file with the necessary configuration. An example configuration is provided below:

## Usage

Run the main.py script to start the web scraping process:

    ```bash
    Copy code
    python main.py
    ```

The script will extract data from the configured web pages and save the results in a CSV file in the data folder.

## Advanced Configuration

You can customize the web scraping behavior by adjusting the parameters in the config.yml file. The key configurations include:

urls: List of URLs of the web pages you want to analyze.
pages: Number of pages to extract for each URL.
time: Waiting time between requests (in seconds).
selectors: You can modify and add CSS selectors in the `config.yml` file to extract specific information from the HTML content.

## Automated Execution

To schedule automated execution of the web scraping script at various times during the day, you can use the included cron.sh file.
