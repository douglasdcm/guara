This Python script scrapes flight arrival data from the AENA (Spanish airport authority) website for a list of predefined airports. It automates browser interactions using Selenium, extracts flight data using BeautifulSoup, and saves the information to a JSON file for historical reference.

```
# Python3.11
python examples/crawler/main.py
```

---

### **Breakdown of the Script**
#### **1. Imports**
The script uses:
- **Selenium** (for browser automation)
- **BeautifulSoup** (for parsing HTML)
- **JSON and File Handling** (to read/write flight data)
- **Datetime** (for timestamps)
- **Guara Transaction Framework** (to structure automated tasks)
- **WebDriver Manager** (to manage ChromeDriver installation)

---

#### **2. Constants**
- **`AIRPORTS`**: A predefined list of Spanish airports.
- **`HISTORY_DAYS`**: Keeps only the last 5 days of flight data.

---

#### **3. Helper Functions**
- **`read_json_file(file_name, default_value)`**: Reads a JSON file; returns a default value if the file is missing or invalid.
- **`write_json_file(file_name, data)`**: Writes structured data to a JSON file.

---

#### **4. Transaction Classes**
Each class represents a step in the web scraping process, using the **AbstractTransaction** pattern from Guara.

1. **`OpenAenaPage`**
   - Opens the AENA flight arrivals page.
   - Hides a modal footer that might block interaction.

2. **`ProcessAirportData`**
   - Selects an airport from the search field.
   - Clicks **"See More"** until all flight data is loaded.
   - Extracts flight details using **BeautifulSoup**.
   - Stores extracted flights with a timestamp.

3. **`SaveFlightData`**
   - Reads existing data from `flights_data.json`.
   - Filters out data older than **5 days**.
   - Saves the updated flight data.

4. **`CloseBrowser`**
   - Closes the Chrome WebDriver after scraping.

---

#### **5. Main Function - `get_aena_data()`**
- **Initializes Chrome WebDriver** (headless mode for efficiency).
- **Creates an application transaction flow**.
- **Iterates over the list of airports**, scrapes data, and stores it.
- **Saves the final results** and updates the script execution status.

---

### **Execution**
When run (`__main__` block), `get_aena_data()` starts the process, collecting and saving flight data.

---
### **Key Features**
✅ **Automated Web Scraping**: Uses Selenium to fetch dynamic flight data.  
✅ **Transaction-based Architecture**: Uses **Guara Transactions** to structure execution.  
✅ **Data Persistence**: Maintains a JSON-based historical record.  
✅ **Error Handling**: Catches missing elements & timeout issues.  
