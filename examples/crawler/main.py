# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# from zoneinfo import ZoneInfo
from guara.transaction import AbstractTransaction, Application
import json
import time

# Constants
AIRPORTS = [
    "PALMA DE MALLORCA",
    "GRAN CANARIA",
    "TENERIFE SUR",
    "TENERIFE NORTE-CIUDAD DE LA LAGUNA",
    "CÉSAR MANRIQUE-LANZAROTE",
    "FUERTEVENTURA",
    "MENORCA",
    "IBIZA",
    "MÁLAGA-COSTA DEL SOL",
    "SEVILLA",
    "JEREZ",
    "ALMERÍA",
    "JOSEP TARRADELLAS BARCELONA-EL PRAT",
    "GIRONA-COSTA BRAVA",
    "ALICANTE-ELCHE MIGUEL HERNÁNDEZ",
    "VALENCIA",
]
HISTORY_DAYS = 5


# Helper Functions
def read_json_file(file_name, default_value):
    """
    Reads a JSON file and returns its content. If the file is not found or invalid,
    returns a default value.

    Args:
        file_name (str): The name of the JSON file to read.
        default_value (any): The value to return if the file is not found or invalid.

    Returns:
        any: The content of the JSON file or the default value.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_value


def write_json_file(file_name, data):
    """
    Writes data to a JSON file.

    Args:
        file_name (str): The name of the JSON file to write.
        data (any): The data to write to the file.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Transactions
class OpenAenaPage(AbstractTransaction):
    """
    Navigates to the AENA flight information page and hides modal footer.

    Returns:
        str: A message indicating the page has been opened.
    """

    def __init__(self, driver):
        self._driver = driver

    def do(self):
        self._driver.get("https://www.aena.es/es/infovuelos.html")
        time.sleep(2)
        self._driver.execute_script(
            "document.getElementById('modal_footer').style.visibility = 'hidden';"
        )
        return "Page opened"


class ProcessAirportData(AbstractTransaction):
    """
    Collects flight data for a specific airport and updates the script status.

    Args:
        airport (str): The airport to process.
        script_status (dict): The status of the script execution.

    Returns:
        list: A list of flight information dictionaries.
    """

    def __init__(self, driver):
        self._driver = driver

    def do(self, airport, script_status):
        new_flights = []

        try:
            field = self._driver.find_element(By.ID, "Llegadasen la red Aena:")
            field.clear()
            field.send_keys(airport)
            time.sleep(2)

            # Load all flight data
            while True:
                try:
                    more_button = Wait(self._driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "btn-see-more"))
                    )
                    self._driver.execute_script("arguments[0].click();", more_button)
                except (TimeoutException, NoSuchElementException):
                    break

            # Scrape flight data
            flights_day = self._driver.find_element(By.CLASS_NAME, "listado")
            soup = BeautifulSoup(flights_day.get_attribute("outerHTML"), "html.parser")
            flight_details = soup.find_all("div", class_="fila micro")

            for flight in flight_details:
                hora = flight.find("div", class_="hora").text.strip()
                vuelo = flight.find("div", class_="vuelo").text.strip()
                aerolinea = flight.find("p", class_="d-none").text.strip()
                origen = flight.find("div", class_="origen-destino").text.strip()
                estado = flight.find("span", class_="a").text.strip() or None

                new_flights.append(
                    {
                        "aeropuerto": airport,
                        "hora_inicial": hora,
                        "vuelo": vuelo,
                        "aerolinea": aerolinea,
                        "origen": origen,
                        "estado": estado,
                        "fecha": datetime.now().strftime("%Y-%m-%d"),
                        "hora_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

            script_status["airports"][airport] = {
                "status": "Success",
                "message": "Data collected successfully",
            }
        except Exception as e:
            script_status["airports"][airport] = {"status": "Error", "message": str(e)}
        return new_flights


class SaveFlightData(AbstractTransaction):
    """
    Saves flight data to a JSON file after filtering outdated data.

    Args:
        flights_data (list): The list of flight data to save.
        history_days (int): The number of days to retain in history.

    Returns:
        str: A message indicating the data was saved.
    """

    def __init__(self, driver=None):
        self._driver = driver

    def do(self, flights_data, history_days):
        existing_data = read_json_file("flights_data.json", [])
        current_date = datetime.now().date()

        # Filter outdated data
        updated_data = [
            flight
            for flight in existing_data
            if datetime.strptime(flight["fecha"], "%Y-%m-%d").date()
            >= current_date - timedelta(days=history_days)
        ]

        # Update or add new data
        for new_flight in flights_data:
            if new_flight not in updated_data:
                updated_data.append(new_flight)

        write_json_file("flights_data.json", updated_data)
        return "Data saved"


class CloseBrowser(AbstractTransaction):
    """
    Closes the WebDriver instance.

    Returns:
        str: A message indicating the browser was closed.
    """

    def __init__(self, driver):
        self._driver = driver

    def do(self):
        self._driver.quit()
        return "Browser closed"


# Main Flow
def get_aena_data():
    """
    Main function to scrape flight information for multiple airports and save it to a JSON file.
    """
    # Initialize browser at the start of the function
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")
    service = Service(ChromeDriverManager().install())
    driver = Chrome(service=service, options=options)

    # Instantiate Application with the driver
    app = Application(driver)

    script_status = read_json_file("script_status.json", {"airports": {}, "status": None})

    # Open the AENA page
    app.then(OpenAenaPage)

    # Process data for each airport
    all_flights_data = []
    for airport in AIRPORTS:
        flights = app.then(ProcessAirportData, airport=airport, script_status=script_status).result
        all_flights_data.extend(flights)

    # Save flight data and close browser
    app.then(SaveFlightData, flights_data=all_flights_data, history_days=HISTORY_DAYS)
    app.then(CloseBrowser)

    # Update script status
    script_status["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    script_status["status"] = "Success"
    write_json_file("script_status.json", script_status)


if __name__ == "__main__":
    get_aena_data()
