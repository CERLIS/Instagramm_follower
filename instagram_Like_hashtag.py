
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from data import username, password, hashtag
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import time
import random

class InstagrmBot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('/home/ser/PycharmProjects/pythonProject/venv/local/bin/Instagramm_bot/chromedriver/chromedriver') # загружаем драйвер хрома укажите папку где он сохранен. ссылка для скачивания https://chromedriver.storage.googleapis.com/index.html
# метод для закрытия браузера
    def close_browser(self):
        self.browser.close()
        self.browser.quit()
 # метод логина
    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')  # заходим на сайт инстаграмм
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element(By.NAME, "username") #поиск поля имя пользователя
        username_input.clear() # очистка поля
        username_input.send_keys(username) # ввод имени


        time.sleep(2)

        password_input = browser.find_element(By.NAME, 'password') #поиск поля пассворд
        password_input.clear() # очистка поля
        password_input.send_keys(password) # ввод пароля

        password_input.send_keys(Keys.ENTER)
        time.sleep(5)
        browser.minimize_window()
    # метод ставит лайки по hashtag
    def like_photo_by_hastag(self, hashtag):

        browser = self.browser
        print(len(hashtag))
        while input('Продолжить ставить лайки? Если да введите y').lower() == 'y': #проверка на готовность к лайканью. или если хватит лайков на сегодня предлагает остановиться
                posts_urls = []
                for i in random.sample(hashtag, len(hashtag)): # выбираем все #тега случайным образом и набираем ссылки. Если заменить len на число будет определенное количесвто тегов выбрано.

                    browser.get(f'https://www.instagram.com/explore/tags/{i}/')

                    time.sleep(random.randrange(3, 5))

                    for _ in range(1, 3): #выбираем нужное количество скролов для каждой страницы
                        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);') #скролим страницу сверху вниз команда для java
                        time.sleep(random.randrange(3, 5))

                    hrefs = browser.find_elements(By.TAG_NAME, 'a') # вытаскиваем со страницы ссылки для дальнешего лайканья


                    posts_urls.extend([item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]) # фильтруем нужные ссылки в которых есть р.
                print(posts_urls)
                with open(r'input.txt', 'a', encoding='utf-8') as output:
                    print('"', str(datetime.now()), ':', file=output) #сохранияем дату внесения posts_ url в файл найденого по определе
                    print(posts_urls, file=output) #сохраниние posts_url в файл
                n = len(posts_urls)
                print(n)
                random.shuffle(posts_urls)

                for url in posts_urls:
                    with open(r'output.txt', 'r+', encoding='utf-8') as file:
                        click_url = [i.strip() for i in file.readlines()]
                    n -= 1
                    print(f"осталось постов на обработек: {n}")

                    if url not in click_url:
                        try:

                            self.put_exacrly_like(url) #лайк по прямой ссылке с провекой на отсутствие страницы, если не заработает то комменты с других убераем, а этот коментим
                            time.sleep(random.randrange(3, 5))

                            with open(r'output.txt', 'a', encoding='utf-8') as output:
                                print('"', str(datetime.now()), ':', file=output) #сохранияем дату внесения url в файл
                                print(url, file=output) #Gсохраниние url в файл
                                print(f'{url} добавлен в output.txt')

                            time.sleep(random.randrange(77, 85))
                        except Exception as es:
                            print(f'like do not make {url}')

    # проверяем по xpath существует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # ставил лайе на пост по прямой ссылке
    def put_exacrly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)
        # проверка на то что пост из инстаграмм исчез
        wrong_userpage = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/h2"

        if self.xpath_exists(wrong_userpage):
            print('Такого поста нет')

        else:
            print('Post yes')
            time.sleep(2)
            like_button = browser.find_element(By.CSS_SELECTOR, 'section:first-child span button').click() #помог парень не знаю как работает https://www.endtest.io/blog/a-practical-guide-for-finding-elements-with-selenium
            time.sleep(2)
            print(f'like put {userpost} done')


my_bot = InstagrmBot(username, password)
my_bot.login()
# my_bot.put_exacrly_like('https://www.instagram.com/p/CouDTQsdfatfghiuG/') #лайк по прямой ссылке с провекой на отсутствие страницы
my_bot.like_photo_by_hastag(hashtag) #лайкает как во втором занятии, по циклу но не проверяет ошибки из списка hastagov

