if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)