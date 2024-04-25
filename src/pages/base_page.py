from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class SeleniumObject:
    def find_element(self, locator):
        return self.webdriver.find_element(*locator)

    def find_elements(self, locator):
        return self.webdriver.find_elements(*locator)

    def wait_presence_element(self, time, locator):
        wait = WebDriverWait(self.webdriver, time)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_visible_element(self, time, locator):
        wait = WebDriverWait(self.webdriver, time)
        return wait.until(EC.visibility_of_element_located(locator))

    def select_option_by_value(self, select_locator, value):
        select = Select(self.find_element(select_locator))
        return select.select_by_value(value)

    def wait_invisibility_of_element(self, time, locator):
        wait = WebDriverWait(self.webdriver, time)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_clickable_element(self, time, locator):
        wait = WebDriverWait(self.webdriver, time)
        return wait.until(EC.element_to_be_clickable(locator))

class BasePage(SeleniumObject):
    def __init__(self, webdriver):
        self.webdriver = webdriver
