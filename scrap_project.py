from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def scrape_user_projects(driver):
    """
    Navigate to the user's project page and collect all project links.
    Returns a list of dicts: [{'title': ..., 'url': ...}, ...]
    """
    try:
        project_page_driver = navigate_to_project_page(driver)
        if not project_page_driver:
            raise Exception("Project page navigation failed.")

        possible_keywords = ["project", "portfolio", "work", "my work"]
        project_links = []

        sections = driver.find_elements(By.XPATH, "//section|//div|//ul")
        for section in sections:
            text = section.text.lower()
            if any(keyword in text for keyword in possible_keywords):
                links = section.find_elements(By.TAG_NAME, "a")
                for link in links:
                    title = link.text.strip()
                    href = link.get_attribute("href")
                    if href and title:
                        project_links.append({"title": title, "url": href})

        if not project_links:
            raise Exception("No project links found on the project page.")

        print(f"Found {len(project_links)} project(s).")
        return True, project_links

    except Exception as e:
        print("Failed to scrape user projects:", str(e))
        return False, str(e)


def extract_project_details(driver, project_links):
    """
    Given a list of project_links (dicts with 'title' and 'url'), visit each URL
    and extract details such as description, skills, and tools used.
    Returns a list of dicts with project details.
    """
    details_list = []
    wait = WebDriverWait(driver, 10)

    for proj in project_links:
        title = proj.get('title')
        url = proj.get('url')
        print(f"Processing project: {title} @ {url}")
        try:
            driver.get(url)
            time.sleep(2)

            # Description
            try:
                desc_el = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//p[contains(@class, 'description') or //div[contains(@class, 'description')]]")))
                description = desc_el.text.strip()
            except Exception:
                description = ''

            # Skills
            skills = []
            try:
                skill_els = driver.find_elements(By.XPATH,
                    "//span[contains(@class, 'skill') or contains(@class, 'tag')]//a | //a[contains(@class, 'skill')]"
                )
                skills = [el.text.strip() for el in skill_els if el.text.strip()]
            except Exception:
                pass

            # Tools (assume elements labeled 'Tools used')
            tools = []
            try:
                tools_section = driver.find_element(By.XPATH,
                    "//*[contains(text(),'Tools used')]/following-sibling::*"
                )
                tool_els = tools_section.find_elements(By.TAG_NAME, 'li')
                tools = [li.text.strip() for li in tool_els]
            except Exception:
                pass

            details_list.append({
                'title': title,
                'url': url,
                'description': description,
                'skills': skills,
                'tools': tools
            })

        except Exception as e:
            print(f"Error extracting details for {url}: {e}")
            details_list.append({
                'title': title,
                'url': url,
                'error': str(e)
            })

    return details_list



def navigate_to_project_page(driver, project_url):
    try:
        driver.get(project_url)
        time.sleep(2)  # Optional: wait for page to load
        return driver
    except Exception as e:
        raise Exception(f"Failed to navigate to project page: {str(e)}")