import requests

def getting_data_from_the_api():

    url = "https://covid.ourworldindata.org/data/owid-covid-data.json"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Error fetching data from API")

    return response.json()


def get_all_countries():

    data = getting_data_from_the_api()

    countries = [{'label' : country , 'value' : country } for country in data.keys()]

    return countries

def get_all_countries_data():

    data = getting_data_from_the_api()

    country_data = {}
    
    for country, info in data.items():

        country_data[country] = info.get("data", [])
    
    return country_data

def covid_data(country = "BRA" ):

    data = getting_data_from_the_api()

    if country not in data or not data[country]["data"]:
        print(f"No data found for country: {country}")  
        return None

    country_data = data[country]["data"]
    
    if not isinstance(country_data, list):
        print(f"Data for {country} is not in the expected format")  
        return None

    return country_data
