import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def chrome_browser(request):
    option = Options()
    option.headless = False
    browser = webdriver.Chrome(chrome_options=option)
    yield browser
    browser.close()
