# Page Transactions and Page Objects Model

## Pros and Cons of Page Object Model (POM) and Page Transactions (PT)
Below is a comparison of **Page Object Model (POM)** and **Page Transactions (PT)** based on different aspects, rated from **0 to 5** (where 0 is the worst and 5 is the best).  

---

## Page Object Model (POM)
| **Criteria**           | **Pros** | **Cons** | **Rating (0-5)** |
|------------------------|---------|---------|------------------|
| **Code Maintainability** | ✅ Separates locators from tests ✅ Easy to update elements | ❌ Still tightly coupled with page structure ❌ If UI changes, all affected pages must be updated | **4** |
| **Reusability** | ✅ Page classes can be reused across multiple tests | ❌ Interactions are page-specific, not user-flow based | **4** |
| **Readability & Simplicity** | ✅ Test cases look clean with method calls | ❌ Requires writing multiple classes for different pages, which can add complexity | **3** |
| **Scalability** | ✅ Works well for large projects with many pages | ❌ Harder to manage when dealing with workflows spanning multiple pages | **4** |
| **Test Maintenance Effort** | ✅ If a locator changes, it only needs to be updated in one place | ❌ If the user workflow changes, tests might need significant updates | **3** |
| **Suitability for UI Testing** | ✅ Well-suited for UI automation with Selenium and similar tools | ❌ Not ideal for non-UI scenarios (e.g., REST API testing) | **4** |

**🔹 Overall Score: 22/30**

---

## Page Transactions (PT)
| **Criteria**           | **Pros** | **Cons** | **Rating (0-5)** |
|------------------------|---------|---------|------------------|
| **Code Maintainability** | ✅ Transactions focus on user actions rather than elements, reducing maintenance | ❌ Requires a different mindset for those used to POM | **5** |
| **Reusability** | ✅ Highly reusable since transactions are user-action based | ❌ If UI structure changes drastically, transactions might need updates | **5** |
| **Readability & Simplicity** | ✅ Tests read like human instructions, improving clarity ✅ Reduces WebDriver calls in test scripts | ❌ Requires defining multiple transaction classes for different actions | **5** |
| **Scalability** | ✅ Works well for large applications, especially where user flows span multiple pages | ❌ Slightly more setup is needed compared to POM | **5** |
| **Test Maintenance Effort** | ✅ Less maintenance required since tests are written based on **actions** rather than UI elements | ❌ If a transaction is reused across many tests, fixing one issue could impact multiple tests | **4** |
| **Suitability for UI Testing** | ✅ Works for UI, API, and asynchronous testing | ❌ Less common in traditional UI automation frameworks | **5** |

**🔹 Overall Score: 29/30**  

---

## Which Pattern is Better?
Based on the **overall scores**, **Page Transactions (PT) scores higher (29/30) than Page Object Model (POM) (22/30)**.  

**Why?**  
✔ PT focuses on user workflows, making it more maintainable and scalable.  
✔ It allows for better test organization and is more suitable for different types of automation (UI, API, async).  
✔ Tests written in PT are more readable, making them accessible to non-technical stakeholders.  

**However, POM is still a great choice** for teams already familiar with traditional UI testing methods, and it provides a structured way to manage page elements.  

If your project involves **complex user workflows** across multiple pages, **Page Transactions is the better approach**. If you need **simple UI structure representation**, POM works well.

## Tips for Migrating from Page Object Model (POM) to Page Transactions (PT)
Moving from **POM** to **PT** requires shifting from **page-centric automation** to **user action-centric automation**. Below are key steps and examples to help with the transition.

---

### Identify User Transactions
In POM, page objects represent pages. In PT, we focus on **transactions** (user actions) like:  
- **Login**
- **Logout**
- **Submit Form**
- **Change Language**
- **Navigate to a Page**

**🔹 Tip:** Instead of writing separate methods for every element on a page, create classes for each transaction.

---

### Convert POM Methods to PT Transactions
#### POM Example (Before Migration)
```python
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.ID, "username")
        self.password = (By.ID, "password")
        self.login_button = (By.ID, "login")

    def enter_username(self, user):
        self.driver.find_element(*self.username).send_keys(user)

    def enter_password(self, pwd):
        self.driver.find_element(*self.password).send_keys(pwd)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()
```
```python
def test_login():
    driver = webdriver.Chrome()
    login_page = LoginPage(driver)

    login_page.enter_username("user1")
    login_page.enter_password("password1")
    login_page.click_login()

    assert "Dashboard" in driver.title
```
---
#### PT Example (After Migration)
```python
from guara.transaction import AbstractTransaction

class LoginTransaction(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, username, password):
        self._driver.find_element(By.ID, "username").send_keys(username)
        self._driver.find_element(By.ID, "password").send_keys(password)
        self._driver.find_element(By.ID, "login").click()
        return self._driver.title
```
```python
from guara.transaction import Application
from guara import it
from selenium import webdriver

def test_login():
    driver = webdriver.Chrome()
    app = Application(driver)

    app.at(LoginTransaction, username="user1", password="password1").asserts(it.Contains, "Dashboard")
```

---

### Benefits of the PT Approach
✔ **Less boilerplate code** – No need for page-specific methods in tests  
✔ **Readable test cases** – Tests describe actions in plain English  
✔ **Easier maintenance** – UI changes don’t break all related test methods  

---

### Additional Refactoring for Other Pages
#### Example: Changing Language Transaction
Instead of:
```python
class HomePage:
    def click_language_button(self):
        self.driver.find_element(By.ID, "language").click()
```
Use:
```python
class ChangeLanguageTransaction(AbstractTransaction):
    def do(self, language):
        self._driver.find_element(By.ID, f"lang-{language}").click()
        return self._driver.find_element(By.TAG_NAME, "body").text
```
Test case:
```python
app.at(ChangeLanguageTransaction, language="pt").asserts(it.Contains, "Página inicial")
```

---

### Gradual Migration Strategy
- Start with frequently changing tests  
- Convert one transaction at a time  
- Keep old POM code until full migration is complete