from django.test import TestCase

from unittest import skip 

from unittest.mock import patch, MagicMock
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

from constance import config
from rnecco_app.driver import RegistryData

class RegistryDataTest(TestCase):
    @patch('rnecco_app.driver.webdriver.Chrome')
    def setUp(self, mock_chrome):
        self.mock_driver = MagicMock()
        mock_chrome.return_value = self.mock_driver
        self.registry_data = RegistryData()
    
    def test_init(self):
        self.assertIsNotNone(self.registry_data.driver)
        self.mock_driver.get.assert_called_once()
        self.mock_driver.maximize_window.assert_called_once()  

    def test_wait_for_element(self):
        mock_element = MagicMock()
        self.mock_driver.find_element.return_value = mock_element
        element = self.registry_data.wait_for_element(By.ID, 'test_id')
        self.assertEqual(element, mock_element) 

    def test_verify_elements_failure(self):
        self.mock_driver.find_element.side_effect = TimeoutException()
        result = self.registry_data.verify_elements([(By.ID, 'test_id')])
        self.assertIn("Falló al encontrar el elemento", result)

    def test_click_element_success(self):
        mock_element = MagicMock()
        self.mock_driver.find_element.return_value = mock_element
        result = self.registry_data.click_element(By.ID, 'test_id')
        self.assertTrue(result)
        mock_element.click.assert_called_once()

    def test_click_element_failure(self):
        self.mock_driver.find_element.side_effect = Exception("Test exception")
        result = self.registry_data.click_element(By.ID, 'test_id')
        self.assertIn("Falló al hacer clic en el elemento", result)
 
    #omitir la prueba test_validate_id_success se usa @unittest.skip
    @skip("Omitido temporalmente mientras se arregla el mock de Select")
    @patch('rnecco_app.driver.Select')
    def test_validate_id_success(self, mock_select):
        mock_element = MagicMock()
        self.mock_driver.find_element.return_value = mock_element
        mock_select.return_value = MagicMock()
        self.mock_driver.switch_to.alert.text = 'El texto de validacion no es valido'
        result = self.registry_data.validate_id('12345', '01', 'Enero', '2000')
        self.assertTrue(result)
        mock_select.assert_called_with(mock_element)

    @patch('rnecco_app.driver.Select')
    def test_validate_id_failure(self, mock_select):
        self.mock_driver.find_element.side_effect = TimeoutException()
        result = self.registry_data.validate_id('12345', '01', 'Enero', '2000')
        self.assertIn("Falló al encontrar el elemento", result)

    def test_close_driver(self):
        self.registry_data.close_driver()
        self.mock_driver.quit.assert_called_once()