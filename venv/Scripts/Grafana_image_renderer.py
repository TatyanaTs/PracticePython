import urllib.request, json


def is_visible(driver, locator, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False


def getPanelImage(url):
    xpath = '//*[@id="reactRoot"]/div/main/div[3]/div[1]/section/div[2]/div/div[1]/div/div[1]/div/div/div[4]'
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.get(url)
    try:
        is_visible(driver, xpath)
    except:
        driver.quit()

    driver.get_screenshot_as_file(f'out{panel}.png')
    driver.quit()


def dologin(baseurl):
    driver.get(f'{baseurl}/login')
    driver.maximize_window()
    driver.find_element(By.NAME, "user").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.CSS_SELECTOR, ".css-1daj7gy-button > .css-1mhnkuh").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".css-8waqwc-button > .css-1mhnkuh").click()


if __name__ == "__main__":
    baseurl = "http://localhost:3000"
    driver = webdriver.Chrome(executable_path="C:/Program Files/JetBrains/PyCharm Community Edition 2020.3.3/plugins/chromedriver")
    dologin(baseurl)
with urllib.request.urlopen("http://localhost:3000/d/FVt3H34Vk/telegraf-and-influx-windows-host-overview?editview=dashboard_json&orgId=1&refresh=1m") as url:
    data = json.load(url)
    print(data)