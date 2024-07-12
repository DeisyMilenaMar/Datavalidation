from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


class RegistryData:
    def __init__(self):
        # Configurar las opciones de Chrome
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
        self.driver.get(config('REGISTRADURIA_URL'))
        self.driver.maximize_window()

def validate_id(self, cedula, issue_day, issue_month, issue_year):
        driver = self.driver
        id_number = driver.find_element(By.ID, 'ContentPlaceHolder1_TextBox1')
        search_issue_day = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_DropDownList1'))
        search_issue_month = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_DropDownList2'))
        search_issue_year = Select(driver.find_element(By.ID,'ContentPlaceHolder1_DropDownList3'))

        id_number.send_keys(cedula)
        search_issue_day.select_by_visible_text(issue_day)
        search_issue_month.select_by_visible_text(issue_month)
        search_issue_year.select_by_visible_text(issue_year)

        try:
            while True:
                catcha_text_code = driver.find_element(By.ID, 'ContentPlaceHolder1_TextBox2')
                catcha_text_code.send_keys('LANAP')
                driver.implicitly_wait(1)
                continue_button = driver.find_element(By.ID, 'ContentPlaceHolder1_Button1')
                continue_button.click()
                alert = driver.switch_to.alert
                alert_text = alert.text
                if alert_text != 'El texto de validacion no es valido':
                    raise Exception(f"Unexpected alert text: {alert_text}")
                alert.accept()
                
        except NoAlertPresentException:        
            # No se encontró alerta, continuar con el flujo normal
        
            # Esperar antes de hacer clic en el botón de generar certificado
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_Button1')))
            generate_certificate = driver.find_element(By.ID, 'ContentPlaceHolder1_Button1')
            generate_certificate.click()

        return True

def close_driver(self):
    if hasattr(self, 'driver'):
        self.driver.quit()

def __del__(self):
    self.close_driver()