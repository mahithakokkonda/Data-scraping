import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_country_population(soup):
    countries = []
    table = soup.find('table', class_='wikitable')
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        columns = row.find_all('td')
        country = columns[1].text.strip()
        population_text = columns[2].text.strip().replace(',', '')  # Remove commas
        if '%' in population_text:  # Check if population contains percentage
            population = population_text
        else:
            population = int(population_text)  # Convert population to integer
        countries.append({'country': country, 'population': population})
    return countries

def main():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_population'
    countries = []

    # Fetch page content
    html_content = fetch_page_content(url)
    if html_content:
        # Parse HTML content
        soup = parse_html_content(html_content)
        # Extract country population data
        countries = extract_country_population(soup)

    # Save the data to a CSV file
    df = pd.DataFrame(countries)
    df.to_csv('country_population.csv', index=False)
    print("Data extracted and saved to 'country_population.csv'")

if __name__ == '__main__':
    main()
