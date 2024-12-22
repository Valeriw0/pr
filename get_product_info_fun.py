import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from get_product_reviews_fun import collect_product_reviews


def collect_product_info(driver, url, count_reviews):

    driver.switch_to.new_window('tab')
    time.sleep(3)
    driver.get(url=url)
    time.sleep(3)

    # product_id
    product_id = driver.find_element(By.ID, 'productNmId').text

    page_source = str(driver.page_source)
    soup = BeautifulSoup(page_source, 'lxml')

    # product_name
    product_name = soup.find('h1', class_='product-page__title').text

    # product_rate
    product_rate = soup.find('span', class_='product-review__rating').text
    product_num_ratings = soup.find('span', class_='product-review__count-review').text.replace(' ', '').split(' ')
    product_num_ratings = ''.join(product_num_ratings).split('о')[0]

    rub = '₽'
    wb_card_price = None
    price = 0
    try:
        prices = soup.find('span', class_='price-block__price').text.split(' ')
        prices = ''.join(prices).replace(' ', '')
        if prices.count(rub) == 2:
            prs = prices.split(rub)
            price = prs[0] + rub
            wb_card_price = prs[1] + rub
        else:
            price = prices
    except Exception as e:
        print(f"Error: {e}")

    old_price = soup.find('del', class_='price-block__old-price').text.split(' ')
    old_price = ''.join(old_price).replace(' ', '')

    find_review_url = driver.find_element(By.CLASS_NAME, 'product-review')
    review_url = find_review_url.get_attribute("href")

    reviews = collect_product_reviews(driver, review_url, count_reviews)

    product_data = (
        {
            'product_url': url,
            'product_id': product_id,
            'product_name': product_name,
            'product_wb_card_price': wb_card_price,
            'product_price': price,
            'product_old_price': old_price,
            'product_rate': product_rate,
            'product_number_of_ratings': product_num_ratings,
            'product_reviews': reviews
        }
    )

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return product_data
