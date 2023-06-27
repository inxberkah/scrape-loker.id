import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import telegram
import asyncio
#Author Berkah@code:~

driver = webdriver.Chrome()

url = 'https://www.loker.id/cari-lowongan-kerja?q=sales&lokasi=jakarta&category=0&pendidikan=0'

driver.get(url)

elements = driver.find_elements(By.CSS_SELECTOR, 'a[title="Lihat detail lowongan"]')

if elements:
    with open('links.txt', 'w') as file:
        for element in elements:
            href = element.get_attribute('href')
            file.write(href + '\n')
    print("Link telah disimpan dalam file links.txt")
else:
    print("Elemen tidak ditemukan dengan selector yang diberikan.")

with open('links.txt', 'r') as file:
    links = file.read().splitlines()

bot_token = 'INPUT_TOKEN'
chat_id = 'INPUT_CHAT_ID'
bot = telegram.Bot(token=bot_token)

for link in links:
    driver.get(link)
    print("Judul Halaman:", driver.title)
    print("URL Link:", link)
    print()

    try:
        page_source = driver.page_source

        print("# INFORMASI LOWONGAN KERJA #")
        job_title = re.search(r"'jobTitle':\s*'(.+?)'", page_source).group(1)
        job_date = re.search(r"'jobDate':\s*'(.+?)'", page_source).group(1)
        job_category = re.search(r"'jobCat':\s*'(.+?)'", page_source).group(1)
        job_location = re.search(r"'jobLoc':\s*'(.+?)'", page_source).group(1)
        job_salary = re.search(r"'jobSal':\s*'(.+?)'", page_source).group(1)
        job_type = re.search(r"'jobType':\s*'(.+?)'", page_source).group(1)
        job_level = re.search(r"'jobLevel':\s*'(.+?)'", page_source).group(1)
        job_education = re.search(r"'jobEdu':\s*'(.+?)'", page_source).group(1)

        print("Job Title:", job_title)
        print("Job Date:", job_date)
        print("Job Category:", job_category)
        print("Job Location:", job_location)
        print("Job Salary:", job_salary)
        print("Job Type:", job_type)
        print("Job Level:", job_level)
        print("Job Education:", job_education)
        print()

        message = f"Judul Halaman: {driver.title}\n" \
                  f"URL Link: {link}\n" \
                  f"Job Title: {job_title}\n" \
                  f"Job Date: {job_date}\n" \
                  f"Job Category: {job_category}\n" \
                  f"Job Location: {job_location}\n" \
                  f"Job Salary: {job_salary}\n" \
                  f"Job Type: {job_type}\n" \
                  f"Job Level: {job_level}\n" \
                  f"Job Education: {job_education}\n"

        async def send_message():
            await bot.send_message(chat_id=chat_id, text=message)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_message())

    except:
        print("Gagal mengambil data dari halaman ini.")

    time.sleep(random.uniform(3, 5))

driver.quit()
