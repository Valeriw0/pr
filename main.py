import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from get_product_info_fun import collect_product_info


def get_products_links(item_name, count_items, count_reviews):
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    driver.get(url='https://www.wildberries.ru/')
    time.sleep(5)

    find_input = driver.find_element(By.ID, 'searchInput')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(5)

    products_urls = []

    for page in range((count_items - 1) // 100 + 1):

        try:
            next_page_button = driver.find_element(By.CLASS_NAME, 'pagination-next')
        except:
            print(f"Страницы с товарами закончились, всего товаров: {len(products_urls)}")
            break

        i = 1
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script(f"window.scrollTo(0, {i * 2000});")

            time.sleep(3)

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
            i += 1

        time.sleep(2)

        try:
            find_links = driver.find_elements(By.CLASS_NAME, 'product-card__link')
            products_urls_on_page = list(set([f'{link.get_attribute("href")}' for link in find_links]))
            products_urls.extend(products_urls_on_page[:-12])

            print('[+] Ссылки на товары собраны!')
        except Exception as e:
            print(f'Error: {e}')

        time.sleep(2)
        next_page_button.click()

    products_urls_dict = {}

    for k, v in enumerate(products_urls):
        products_urls_dict.update({k: v})

    time.sleep(2)

    products_data = []

    for i in range(count_items):
        data = collect_product_info(driver=driver, url=products_urls[i], count_reviews=count_reviews)
        print(f'[+] Собраны данные товара id: {data.get("product_id")}')
        time.sleep(2)
        products_data.append(data)

    with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

    driver.close()
    driver.quit()


def main():
    item_name = input('Введите название товара: ')
    count_items = int(input('Введите количество товаров: '))
    count_reviews = int(input('Введите количество отзывов: '))
    print('[INFO] Сбор данных начался...')
    get_products_links(item_name=item_name, count_items=count_items, count_reviews=count_reviews)
    print('[INFO] Работа выполнена успешно!')


if __name__ == '__main__':
    main()