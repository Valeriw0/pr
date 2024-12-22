import time
from bs4 import BeautifulSoup


def collect_product_reviews(driver, url, max_count_reviews=10):
    driver.switch_to.new_window('tab')
    time.sleep(3)
    driver.get(url=url)
    time.sleep(3)

    reviews_data = []

    page_sources = str(driver.page_source)
    soup = BeautifulSoup(page_sources, 'lxml')

    try:
        reviews_list = soup.find('ul', class_='comments__list').find_all('li', class_='comments__item')

        i = 1
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(reviews_list) < max_count_reviews:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(3)

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            page_sources = str(driver.page_source)
            soup = BeautifulSoup(page_sources, 'lxml')
            reviews_list = soup.find('ul', class_='comments__list').find_all('li', class_='comments__item')
            last_height = new_height
            i += 1

        reviews_count = 0

        for review in reviews_list:
            if reviews_count == max_count_reviews:
                break
            author = review.find('p', class_='feedback__header').text
            date = review.find('div', class_='feedback__date').text
            content = review.find('div', class_='feedback__content').text.strip()

            stars = None
            span_tag = review.find('span', class_='feedback__rating')
            if span_tag:
                count_stars = int(span_tag['class'][2].replace('star', ''))
                stars = '⭐' * count_stars

            review_data = (
                {
                    'author_review': author,
                    'review_stars': stars,
                    'date_review': date,
                    'review_content': content,
                }
            )
            reviews_data.append(review_data)
            reviews_count += 1

    except:
        reviews_data = 'Отзывов нет'

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return reviews_data
