from guara.transaction import AbstractTransaction  
from appium import webdriver  

class OpenAppTransaction(AbstractTransaction):  
    """Launch Windows Calculator"""

    def do(self):  
        desired_caps = {  
            "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",  
            "platformName": "Windows",  
            "deviceName": "WindowsPC"  
        }  
        self._driver = webdriver.Remote(  
            command_executor='http://127.0.0.1:4723',  
            desired_capabilities=desired_caps  
        )  
        return self._driver  

class CloseAppTransaction(AbstractTransaction):  
    """Close Calculator"""  
    def do(self):  
        if self._driver:  
            self._driver.quit()  