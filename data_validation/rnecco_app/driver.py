from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.chrome.options import Options
from constance import config as constance_config
from time import sleep

class RegistryData:
    def __init__(self):
        self.download_dir = config('DOWNLOAD_DIR')
        options = webdriver.ChromeOptions()
        options.add_argument(f"--force-device-scale-factor={config('FORCE_DEVICE_SCALE_FACTOR')}")
        options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        self.driver = webdriver.Chrome(executable_path=config('CHROME_DRIVER_PATH'), options=options)
        self.driver.set_page_load_timeout(constance_config.PAGE_LOAD_TIMEOUT)
        self.driver.implicitly_wait(constance_config.IMPLICIT_WAIT)
        self.driver.get(config('REGISTRADURIA_URL'))
        self.driver.maximize_window()

    def wait_for_element(self, by, value, timeout=None):

        if timeout is None:
            timeout = constance_config.EXPLICIT_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def verify_elements(self, elements_to_verify):
        """This method checks if all specified elements are present on the page.
        If any element is missing,it returns an error message."""

        for by, value in elements_to_verify:
            try:
                self.wait_for_element(by, value)
            except TimeoutException:
                return f"Falló al encontrar el elemento {by}: {value}"
        return True

    def click_element(self, by, value):
        """"This method attempts to click a specific element on the page.
        If it cannot click the element, it returns an error message."""

        try:
            element = self.wait_for_element(by, value)
            element.click()
        except Exception as e:
            return f"Falló al hacer clic en el elemento {by}: {value}. Error: {str(e)}"
        return True

    def validate_id(self, cedula, issue_day, issue_month, issue_year):
        """This method validates the entered ID by verifying elements, 
        filling in information, solving the captcha, handling alerts, and generating the certificate."""

        driver = self.driver

        elements = {
            'id_number': (By.ID, 'ContentPlaceHolder1_TextBox1'),
            'issue_day': (By.ID, 'ContentPlaceHolder1_DropDownList1'),
            'issue_month': (By.ID, 'ContentPlaceHolder1_DropDownList2'),
            'issue_year': (By.ID, 'ContentPlaceHolder1_DropDownList3'),
            'captcha': (By.ID, 'ContentPlaceHolder1_TextBox2'),
            'change_code': (By.XPATH, '//*[@id="ContentPlaceHolder1_Panel1"]/div/div[1]/center/div/div[2]/a/img'),
            'continue_button': (By.ID, 'ContentPlaceHolder1_Button1'),
            'generate_certificate': (By.ID, 'ContentPlaceHolder1_Button1')
        }

        verification_result = self.verify_elements(elements.values())
        if verification_result is not True:
            return verification_result

        self.wait_for_element(*elements['id_number']).send_keys(cedula)
        Select(self.wait_for_element(*elements['issue_day'])).select_by_visible_text(issue_day)
        Select(self.wait_for_element(*elements['issue_month'])).select_by_visible_text(issue_month)
        Select(self.wait_for_element(*elements['issue_year'])).select_by_visible_text(issue_year)

        try:
            while True:
                captcha_field = self.wait_for_element(*elements['captcha'])
                captcha_field.clear()
                captcha_field.send_keys('LANAP')
                
                click_result = self.click_element(*elements['continue_button'])
                if click_result is not True:
                    return click_result

                alert = driver.switch_to.alert
                alert_text = alert.text
                if alert_text != 'El texto de validacion no es valido':
                    raise Exception(f"Unexpected alert text: {alert_text}")
                alert.accept()
                
        except NoAlertPresentException:        
            pass
        
        click_result = self.click_element(*elements['generate_certificate'])
        if click_result is not True:
            return click_result

        return True

    def close_driver(self):
        """This method closes the browser if it is open."""

        sleep(constance_config.SLEEP_TIME)
        if hasattr(self, 'driver'):
            self.driver.quit()

    def __del__(self):
        """This special method ensures the browser closes when the RegistryData object is destroyed."""

        self.close_driver()