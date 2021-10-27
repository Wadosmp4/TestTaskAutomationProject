import csv
import time
import config as con
from selenium import webdriver
from selenium.webdriver.common.by import By


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def parse_departments(driver):
    deps = driver.find_elements(By.CSS_SELECTOR, value=con.DEPARTMENT_SELECTOR)
    deps_data = []
    for dep in deps:
        dep_name = dep.find_element(By.CSS_SELECTOR, con.DEPARTMENT_NAME_SELECTOR).text
        dep_spending = dep.find_element(By.CSS_SELECTOR, con.DEPARTMENT_SPENDING_SELECTOR).text

        row = (dep_name, dep_spending)
        deps_data.append(row)

    return deps_data


def process_departments(deps_data):
    with open(con.EXCEL_DEPS_FILENAME, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        headers = ['Name', 'Spending']
        csv_writer.writerow(headers)
        for dep in deps_data:
            csv_writer.writerow(dep)


def process_investments(driver, investments):
    with open(con.EXCEL_INVESTS_FILENAME, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        headers = ['UUI', 'Burea', 'Investment title', 'Total FY2021 Spending($M)', 'Type', 'CIO Rating', '# of Projects']
        csv_writer.writerow(headers)

        for investment in investments:
            try:
                driver.execute_script("window.open('{}');".format(investment[-1]))
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(5)
                download_url = driver.find_element(By.XPATH, con.DOWNLOAD_URL_XPATH)
                download_url.click()
                time.sleep(5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception:
                print('Url not available')
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            finally:
                csv_writer.writerow(investment[:-1])


def process_table(page_investments):
    result = []
    investments = page_investments.find_elements(By.CSS_SELECTOR, con.TR_SELECTOR)

    for investment in investments:
        processed_investment = investment.find_elements(By.CSS_SELECTOR, con.TD_SELECTOR)

        try:
            investment_to_text = [col.text for col in processed_investment]
        except Exception:
            return None

        try:
            investment_url = (processed_investment[0].find_element(By.CSS_SELECTOR, 'a:nth-child(1)')
                              .get_attribute('href'))
        except Exception:
            investment_url = 'No url'

        investment_to_text.append(investment_url)
        result.append(investment_to_text)

    return result


def parse_investments(driver):
    while True:
        try:
            num_of_pages = int(driver.find_element(By.CSS_SELECTOR, con.NUM_OF_PAGES_SELECTOR).text)
            break
        except Exception:
            time.sleep(1)

    all_investments = []
    investments = process_table(driver.find_element(By.CSS_SELECTOR, con.INVESTMENT_SELECTOR))
    all_investments += investments

    next_button = driver.find_element(By.XPATH, con.NEXT_BUTTON_XPATH)
    next_button.click()

    for _ in range(num_of_pages - 1):
        while True:
            if ((investments_check := process_table(driver.find_element(By.CSS_SELECTOR, con.INVESTMENT_SELECTOR)))
                    is not None and investments_check != investments):

                investments = investments_check
                all_investments += investments

                next_button = driver.find_element(By.XPATH, con.NEXT_BUTTON_XPATH)
                next_button.click()
                break
            time.sleep(1)

    return all_investments


if __name__ == '__main__':
    # Creating driver
    driver = webdriver.Firefox(options=con.fp)
    driver.get(con.BASE_URL)

    # Find all departments
    dive_in_button = driver.find_element(By.XPATH, value=con.DIVE_IN_XPATH)
    dive_in_button.click()

    scroll_to_bottom(driver)
    time.sleep(5)

    # Write departments to excel
    deps = parse_departments(driver)
    process_departments(deps)

    # Find searched department
    test_dep = driver.find_elements(By.XPATH, f'//*[contains(text(), "{con.TEST_DEPARTMENT_NAME}")]')[2]
    test_dep.click()
    scroll_to_bottom(driver)

    # Download pdf files and write investments to excel
    investments = parse_investments(driver)
    process_investments(driver, investments)

    driver.close()
