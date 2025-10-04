import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape(df):
    api_nos = df.api_no.tolist()
    api_dict = {'name':[], 'api_no':[], 'well_status':[], 'well_type':[], 'closest_city':[], 'county':[], 'lat_long':[]}
    oil_prod = []
    gas_prod = []

    for api_no in api_nos:
        url = f'https://www.drillingedge.com/search?type=wells&operator_name=&well_name=&api_no={api_no}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for a in soup.find_all('a', href=True):
            if api_no in a['href']:
                link = a['href']
                break

        api_response = requests.get(link)
        api_soup = BeautifulSoup(api_response.text, 'html.parser')
        key_val_dict = {}
        selection = ['Well Name', 'API No.', 'Well Status', 'Well Type', 'Closest City', 'County', 'Latitude / Longitude']

        for tr in api_soup.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in tr.find_all(['th', 'td'])]
            
            for i in range(0, len(cells) - 1, 2):
                key = cells[i]
                val = cells[i + 1]
                if key in selection:
                    key_val_dict[key] = val
        
        for key, val in zip(api_dict.keys(), key_val_dict.values()):
            api_dict[key].append(val)

        spans = api_soup.find_all('span', class_='dropcap')
        production_values = []
        
        for span in spans:
            elem = span.text.strip().split(' ')
            
            try:
                if len(elem) == 1:
                    production_values.append(float(elem[0]))
                else:
                    production_values.append(float(elem[0]) * 1000)
            except:
                production_values.append(0)

        # Assume first value is oil, second is gas (adjust based on actual data structure)
        oil_prod.append(production_values[0] if len(production_values) > 0 else 0)
        gas_prod.append(production_values[1] if len(production_values) > 1 else 0)
    
    api_dict['oil_prod'] = oil_prod
    api_dict['gas_prod'] = gas_prod

    api_df = pd.DataFrame(api_dict)
    
    print('Finished scraping..')
    print('\nExporting csv..')
    api_df.to_csv('../data/scraped_data.csv', index=False) 
    print('File location: data/scraped_data.csv')

if __name__ == '__main__':
    path = '../data/stimulated_data.csv'
    df = pd.read_csv(path)
    print('Start scraping..')
    scrape(df)