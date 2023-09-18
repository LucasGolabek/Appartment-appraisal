import requests
import statistics
import math

from bs4 import BeautifulSoup
from geopy import distance
from django.conf import settings

from apartments.models import CollectedApartment


BASE_URL = "https://www.otodom.pl"
APARTMENTS_URL = BASE_URL + "/pl/oferty/sprzedaz/mieszkanie/wroclaw?distanceRadius=0&page={}&limit=72"

GEOCODING_REQUEST_BASE = "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json"
GEOCODING_API_TOKEN = getattr(settings, "GEOCODING_API_TOKEN", None)
APARTMENT_MEASUREMENT_TOLERANCE = getattr(settings, "APARTMENT_MEASUREMENT_TOLERANCE", None)
APARTMENT_DISTANCE_TOLERANCE = getattr(settings, "APARTMENT_DISTANCE_TOLERANCE", None)
NUMBER_OF_APARTMENTS_EXAMPLES = getattr(settings, "NUMBER_OF_APARTMENTS_EXAMPLES", None)


class Error(Exception):
    pass


class Apartment:
    BASE_URL = "https://www.otodom.pl"

    def __init__(self, url):
        self.url = url
        self.price = None
        self.location = None
        self.measurement = None
        self.rooms = None
        self.heating = None
        self.is_checked = True

    def get_apartment(self):
        dictionary = dict()
        dictionary["url"] = self.url
        dictionary["price"] = self.price
        dictionary["location"] = self.location
        dictionary["measurement"] = self.measurement
        dictionary["rooms"] = self.rooms
        dictionary["heating"] = self.heating
        dictionary["is_checked"] = self.is_checked
        return dictionary

    def scrap(self):
        response = requests.get(self.BASE_URL + self.url)
        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.ChunkedEncodingError:
            return False

        price = soup.find("strong", {"aria-label": "Cena"})
        try:
            self.price = float("".join(price.text.split()[:-1]).replace(" ", "").replace(",", "."))
        except (ValueError, AttributeError):
            return False

        location = soup.find("a", {"aria-label": "Adres"})
        try:
            self.location = location.text
        except AttributeError:
            return False

        measurement = soup.find("div", {"aria-label": "Powierzchnia"})
        try:
            self.measurement = float(measurement.findChild("div", {"class": "css-1wi2w6s estckra5"}).text.split()[0].
                                     replace(",", "."))
        except ValueError:
            return False

        rooms = soup.find("div", {"aria-label": "Liczba pokoi"})
        try:
            self.rooms = int(rooms.findChild("div", {"class": "css-1wi2w6s estckra5"}).text)
        except ValueError:
            return False

        heating = soup.find("div", {"aria-label": "Ogrzewanie"})
        try:
            self.heating = heating.findChild("div", {"class": "css-1wi2w6s estckra5"}).text
        except AttributeError:
            self.heating = None

        return True


def get_geographical_coordinates(location_string):
    request_params = {"access_token": GEOCODING_API_TOKEN,
                      "limit": 1}

    try:
        response = requests.get(GEOCODING_REQUEST_BASE.format(location_string), params=request_params)
    except requests.exceptions.ConnectTimeout:
        print("connection timeout 97")
        return False

    try:
        possibility = response.json()["features"][0]
        if possibility["relevance"] < 0.5:
            print("Relevance 103")
            return False
        elif len(possibility["geometry"]["coordinates"]) != 2 or type(possibility["geometry"]["coordinates"]) != list:
            print("coordinates problem 106")
            return False
        else:
            longitude, latitude = possibility["geometry"]["coordinates"]
            return latitude, longitude
    except KeyError:
        print("key error 112")
        return False


def add_geographical_coordinates_where_needed():
    print("\nSetting geographical coordinates for newly found apartments...")

    apartments_without_geographical_coordinates = CollectedApartment.objects.filter(latitude=None, longitude=None)
    number_of_empty_coordinates = len(apartments_without_geographical_coordinates)

    count = 1
    for apartment in apartments_without_geographical_coordinates:
        print(f"{count}/{number_of_empty_coordinates}", end=" ")
        current_apartment_geographical_coordinates = get_geographical_coordinates(apartment.location)
        current_apartment = CollectedApartment.objects.get(url=apartment.url)
        if current_apartment_geographical_coordinates:
            current_apartment.latitude = current_apartment_geographical_coordinates[0]
            current_apartment.longitude = current_apartment_geographical_coordinates[1]
            current_apartment.save()
            print(f"Geographical coordinates set for {apartment.url}: {current_apartment_geographical_coordinates}")
        else:
            current_apartment.delete()
            print(f"Cannot set geographical coordinates, removing: {apartment.url}")
        count += 1


def get_urls(max_n_batch):
    current_page = 1
    while True:
        if current_page > max_n_batch:
            break
        print(f"\nApartment batch: {current_page}\n")
        response = requests.get(APARTMENTS_URL.format(current_page))
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("div", {"data-cy": "no-search-results"}):
            break
        list_tags = {item['href'] for item in soup.findAll('a', href=True) if "oferta" in item['href']}
        current_page += 1
        yield list_tags


def update_apartments(delete_outdated=False, max_n_batch=math.inf):
    print("Updating database...")
    CollectedApartment.objects.all().update(is_checked=False) # set is_checked field in all objects to False

    scraped_urls = {apartment.url for apartment in CollectedApartment.objects.all()}
    for apartment_batch in get_urls(max_n_batch=max_n_batch):
        current_new_urls = apartment_batch - scraped_urls
        print(f"Batch new urls: {len(current_new_urls)}/75")

        # set is_checked field in found objects present in db to True
        current_scraped_urls = apartment_batch.intersection(scraped_urls)
        for apartment_url in current_scraped_urls:
            CollectedApartment.objects.get(url=apartment_url).is_checked = True

        # add newly found apartments
        for apartment_url in current_new_urls:
            current_apartment = Apartment(apartment_url)
            if current_apartment.scrap():
                q = CollectedApartment(**current_apartment.get_apartment())
                q.save()
                print(f"Saved: \t\t\t{apartment_url}")
            else:
                print(f"Failed to scrap: \t{apartment_url}")
    
    if delete_outdated:
        # remove outdated (not found) apartments
        CollectedApartment.objects.filter(is_checked=False).delete()

    print(f"Number of apartments in database: {len(CollectedApartment.objects.all())}")
    add_geographical_coordinates_where_needed()
    return True


def range_search(location, apartments):
    matching = {}
    for apartment in apartments:
        current_distance = distance.distance([location[0], location[1]], [apartment.latitude, apartment.longitude]).kilometers
        if current_distance <= APARTMENT_DISTANCE_TOLERANCE:
            matching[apartment.url] = [apartment.price, current_distance]
    matching = dict(sorted(matching.items(), key=lambda item: item[1][1]))
    return matching


def get_apartments_suggestions_and_estimation(apartment_data):
    apartment_geographical_coordinates = get_geographical_coordinates(apartment_data["location"])
    if not apartment_geographical_coordinates:
        return False

    if apartment_data["heating"]:
        possible_apartments = CollectedApartment.objects.filter(rooms=apartment_data["rooms"], 
                                                                heating=apartment_data["heating"],
                                                                measurement__gt=apartment_data["measurement"]-APARTMENT_MEASUREMENT_TOLERANCE,
                                                                measurement__lt=apartment_data["measurement"]+APARTMENT_MEASUREMENT_TOLERANCE)
    else:
        possible_apartments = CollectedApartment.objects.filter(rooms=apartment_data["rooms"], 
                                                                measurement__gt=apartment_data["measurement"]-APARTMENT_MEASUREMENT_TOLERANCE,
                                                                measurement__lt=apartment_data["measurement"]+APARTMENT_MEASUREMENT_TOLERANCE)

    matching_apartments = range_search(apartment_geographical_coordinates, possible_apartments)
    if not matching_apartments:
        print("matching apartments not found 213")
        return False
    
    prices = [matching_apartments[item][0] for item in matching_apartments]
    
    result = {}
    result["price"] = statistics.mean(prices)
    result["median"] = statistics.median(prices)
    result["stdev"] = statistics.stdev(prices)
    result["probe"] = len(matching_apartments)
    result["examples"] = list(matching_apartments.keys())[:min(NUMBER_OF_APARTMENTS_EXAMPLES, len(matching_apartments))]
    return result
