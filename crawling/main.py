import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm

from lib.utils import DefaultSetter, Crawler
from static.public import URL, REVIEW_NEXT_XPATH, CARD_NEXT_XPATH, CARDS_XPATH


def main():
    setter = DefaultSetter()

    driver = setter.get_driver(URL = URL)

    for i in range(1):
        cards = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, CARDS_XPATH))
        )

        for j in tqdm(range(len(cards)), leave = True):
            cards[j].click()
            driver.switch_to.window(driver.window_handles[1])

            filename = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h1.biGQs._P.fiohW.eIegw'))
            )[0].text

            print(filename)
            crawler = Crawler(filename = filename)

            for k in range(30):
                try:
                    page_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, REVIEW_NEXT_XPATH))
                    )
                except TimeoutException:
                    continue
                crawler.process(driver = driver)

                page_btn.click()

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            crawler.save_data()

        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, CARD_NEXT_XPATH))
        )

        btn.click()


if __name__ == '__main__':
    main()

