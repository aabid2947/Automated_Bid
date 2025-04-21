from login import login_freelancer
from scrap_project import scrape_user_projects
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service


def setup_driver():
    try:
        service = Service()  # Uses Selenium Manager
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 20)
        return driver
    except Exception as e:
        print("Error setting up WebDriver:", e)
        traceback.print_exc()
        raise Exception(f"Error setting up WebDriver: {str(e)}")


def main(url, username, password, security_answer):
    # url = "https://www.freelancer.com/login"
    # username = "your_username_here"
    # password = "your_password_here"
    # security_answer = "your_security_answer_here"

    driver = setup_driver()
    if not driver:
        print("Driver setup failed. Exiting...")
        return

    try:
        success, result = login_freelancer(driver, url, username, password, security_answer)
        if not success:
            print(f"Login failed: {result}")
            return

        print("Login successful. Navigating to scrape projects...")

        success, projects = scrape_user_projects(driver)
        if success:
            print("Scraped projects:")
            for project in projects:
                print("-", project)
        else:
            print("Failed to scrape projects:", projects)

    except Exception as e:
        print("An error occurred during main execution:", e)
        traceback.print_exc()
        raise Exception(f"Login error: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
