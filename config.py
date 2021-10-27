import os
from selenium.webdriver.firefox.options import Options

# URLS
BASE_URL = r'https://itdashboard.gov/'

# SELECTORS
DIVE_IN_XPATH = '/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/a'
DEPARTMENT_SELECTOR = 'div.col-sm-4.text-center.noUnderline'
DEPARTMENT_NAME_SELECTOR = 'span.h4.w200'
DEPARTMENT_SPENDING_SELECTOR = 'span.h1.w900'
TEST_DEPARTMENT_NAME = 'Department of the Interior'
INVESTMENT_SELECTOR = '#investments-table-object > tbody:nth-child(2)'
TR_SELECTOR = 'tr:nth-child(n)'
TD_SELECTOR = 'td:nth-child(n)'
NUM_OF_PAGES_SELECTOR = 'a.paginate_button:nth-last-child(1)'
NEXT_BUTTON_XPATH = '//*[@id="investments-table-object_next"]'
DOWNLOAD_URL_XPATH = '/html/body/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[6]/a'

# Export filenames
EXCEL_DEPS_FILENAME = r'Agencies.xls'
EXCEL_INVESTS_FILENAME = f'{TEST_DEPARTMENT_NAME}_investments.xls'

# Config for webdriver
mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
fp = Options()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir",
                  os.path.join(os.getcwd(),
                               f"{TEST_DEPARTMENT_NAME.replace(' ', '_')}_PDF_files"))
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
fp.set_preference("pdfjs.disabled", True)
