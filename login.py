from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.chrome.service import Service
from tools.captcha_solver import handle_captcha

def find_input_by_keywords(driver, keywords, wait, input_type='input'):
    # Try to find an input field matching common attributes or placeholder text
    xpath_parts = []
    for key in keywords:
        xpath_parts.append(f"contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{key}')")
        xpath_parts.append(f"contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{key}')")
        xpath_parts.append(f"contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{key}')")
        xpath_parts.append(f"contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{key}')")
    xpath = f"//{input_type}[{' or '.join(xpath_parts)}]"

    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

def login_freelancer(driver,url, username, password, security_answer=''):
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)

        # Email or Username input
        try:
            email_input = find_input_by_keywords(driver, ['email', 'user', 'login', 'username'], wait)
            email_input.clear()
            email_input.send_keys(username)
        except  Exception as e:
            raise Exception(f"Login error: {str(e)}")

        # Next button if any
        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'next')]")
            next_btn.click()
            time.sleep(2)
        except  :
             pass

        # Password input
        try:
            password_input = find_input_by_keywords(driver, ['password', 'pass'], wait)
            password_input.clear()
            password_input.send_keys(password)
            
        except:
             pass

        # Login button or press Enter
        try:
            login_btn = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login') or contains(@type, 'submit')]")
            login_btn.click()
        except:
            password_input.send_keys(Keys.RETURN)

        time.sleep(3)

        # Optional Security Question
        try:
            security_input = find_input_by_keywords(driver, ['security', 'answer'], wait)
            if security_answer:
                security_input.send_keys(security_answer)
                try:
                    submit_btn = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')]")
                    submit_btn.click()
                except:
                    security_input.send_keys(Keys.RETURN)
        except:
            pass
        
        # try to press login button
        if re.search(r'login|signin', driver.current_url, re.IGNORECASE):
            try: 
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Next')]"))
                )
                next_button.click()
                time.sleep(5)
                
                # Detect if still on login page
                # current_url = driver.current_url
                # if re.search(r'login|signin', current_url, re.IGNORECASE):
                #     # Check if any CAPTCHA detected
                if re.search(r'captcha|recaptcha|verify you are human', driver.page_source.lower()):
                        try:
                            captcha_solved, msg = handle_captcha(driver)
                            if not captcha_solved:
                                return False, msg
                        except Exception as e:
                            raise Exception(f"Login error: {str(e)}")

                        # After CAPTCHA is solved, click 'Login' or 'Next' button
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Next')]"))
                        )
                        next_button.click()
                        time.sleep(5)
                    

            except Exception as e:
                raise Exception(f"Login error: {str(e)}")

        else:
            return True, "Login successful based on URL change."
        

        # Check if home page is loaded
        # Smarter check to confirm login success across various platforms
        try:
            # Wait for login fields to disappear (if still there, login likely failed)
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'user') or contains(@name, 'email') or contains(@name, 'login')]"))
            )
        except Exception as e:
            raise Exception(f"Login error: {str(e)}")

        # Optionally check for presence of post-login indicators
        try:
            post_login_indicators = [
                "//a[contains(@href, 'profile')]",
                "//a[contains(@href, 'dashboard')]",
                "//img[contains(@src, 'avatar') or contains(@class, 'avatar')]",
                "//div[contains(@class, 'user-menu') or contains(@class, 'profile')]"
            ]
            for xpath in post_login_indicators:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    return True, "Login successful. Post-login element detected."
        except:
            pass

        # Fallback: check URL change
        if not re.search(r'login|signin', driver.current_url, re.IGNORECASE):
            return True, "Login successful based on URL change."

        return False, "Login might have failed. No reliable post-login indicator found."

    except Exception as e:
        raise Exception(f"Login error: {str(e)}")
