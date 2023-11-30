from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pandas import DataFrame

from static.public import REVIEWS_XPATH


class DefaultSetter:
    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def get_driver(cls, URL) -> WebDriver:
        driver = Chrome(service = ChromeService(ChromeDriverManager().install()))
        driver.set_window_size(1920, 1080)
        driver.get(URL)

        return driver


class Crawler:
    __data: DataFrame = None
    __list: list = None
    __filename = None

    @classmethod
    def __init__(cls, filename):
        cls.__filename = filename
        cls.__list = []

    @classmethod
    def get_data(cls):
        return cls.__list

    @classmethod
    def save_data(cls):
        cls.__data = DataFrame(data = cls.__list, columns = ['title', 'score', 'text'])
        cls.__data.to_csv(f'crawling/data/{cls.__filename}_review.csv', sep = ',', index = False)

    @classmethod
    def process(cls, driver):
        reviews = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, REVIEWS_XPATH))
        )
        for item in reviews[:-1]:
            score = item.find_element(by = By.CSS_SELECTOR, value = 'svg.UctUV.d.H0')
            review = item.find_elements(by = By.CSS_SELECTOR, value = 'span.yCeTE')
            score = score.get_attribute(name = 'aria-label')[-3:]
            title = review[0].text
            review = review[1].text

            cls.__list.append([title, score, review])
