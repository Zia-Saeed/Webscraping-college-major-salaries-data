from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import csv

if __name__ == '__main__':
    service = Service(executable_path="chromedriver.exe")
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    wb = webdriver.Chrome(service=service, options=option)
    wb.get(url="https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors")
    time.sleep(5)
    table = wb.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/article/div[2]/table/thead/tr")
    data_heading = table.find_elements(By.TAG_NAME, "th")
    heading = []
    for text in data_heading:
        if text.text == "":
            continue
        heading.append(text.text)
    with open("salaries_by_college_major.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(heading)
    file.close()

    def records_scraping():
        df = pd.read_csv("salaries_by_college_major.csv")
        time.sleep(3)
        table_body = wb.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/article/div[2]/table/tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            first_row_data = row.find_elements(By.CLASS_NAME, "data-table__value")
            row_list = []
            for txt in first_row_data:
                if txt.text == "":
                    continue
                row_list.append(txt.text)
            new_row = pd.DataFrame([row_list], columns=df.columns)
            df = df._append(new_row, ignore_index=True)
            df.to_csv("salaries_by_college_major.csv", index=False)

    while True:
        time.sleep(10)
        records_scraping()
        next_button = wb.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/article/div[3]/a[7]")
        if next_button:
            next_button.click()
            time.sleep(10)

        else:
            wb.close()
            break