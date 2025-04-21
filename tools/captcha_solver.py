from selenium.webdriver.common.by import By
import time
from PIL import Image
from io import BytesIO
import pytesseract
import cv2
import numpy as np
import os

# Set tesseract cmd to your bundled executable
pytesseract.pytesseract.tesseract_cmd = os.path.abspath("tools_dependencies/tesseract/tesseract.exe")

# Set environment variable for tessdata
os.environ["TESSDATA_PREFIX"] = os.path.abspath("tools_dependencies/tesseract/tessdata")

def handle_captcha(driver):
    try:
        # Loop until the CAPTCHA is solved or the home page is reached
        while True:
            print("Checking for CAPTCHA...")
            if "captcha" in driver.page_source.lower():
                # Check for click-based CAPTCHA first
                captcha_solved = handle_click_captcha(driver)
                if captcha_solved:
                    print("Click-based CAPTCHA solved.")
                    time.sleep(3)  # Allow time for page to load
                    continue  # Recheck the page for any further CAPTCHA or steps

                # If click CAPTCHA is not found, handle image-based CAPTCHA
                captcha_solved = handle_image_captcha(driver)
                if captcha_solved:
                    print("Image CAPTCHA solved.")
                    time.sleep(3)  # Allow time for page to load
                    continue  # Recheck the page for any further CAPTCHA or steps

            # If no CAPTCHA found or home page is detected, break the loop
            if "home" in driver.page_source.lower() or "dashboard" in driver.page_source.lower():
                return True, "Captcha solved, home page detected."

            # If we cannot detect home page or CAPTCHA is still present after attempts
            time.sleep(5)
            break

        return False, "Captcha handling failed or home page not detected."

    except Exception as e:
        print(f"Captcha handling error: {str(e)}")
        return False, "Captcha handling failed."

def handle_click_captcha(driver):
    try:
        # Check for iframe (common for CAPTCHAs like reCAPTCHA, hCaptcha)
        iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha') or contains(@src, 'hcaptcha') or contains(@src, 'turnstile')]")
        driver.switch_to.frame(iframe)

        # Try to click the CAPTCHA checkbox
        checkbox = driver.find_element(By.XPATH, "//div[@id='recaptcha-anchor' or @id='checkbox' or contains(@class, 'recaptcha-checkbox')]")
        checkbox.click()
        print("Clicked CAPTCHA checkbox.")

        # Switch back to main page
        driver.switch_to.default_content()

        # Wait for the CAPTCHA challenge to pass
        time.sleep(5)

        # Check if CAPTCHA is still present
        if "captcha" in driver.page_source.lower():
            print("Click-based CAPTCHA failed or wasn't solved.")
            return False

        return True

    except Exception as e:
        print(f"Click CAPTCHA failed: {str(e)}")
        return False

def handle_image_captcha(driver):
    try:
        # Find the CAPTCHA image
        captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha')]")
        location = captcha_img.location
        size = captcha_img.size

        # Take full-page screenshot
        screenshot = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot))

        # Crop to CAPTCHA location
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        captcha_image = img.crop((left, top, right, bottom))

        # Enhance image for better OCR (optional)
        captcha_image_cv = cv2.cvtColor(np.array(captcha_image), cv2.COLOR_RGB2BGR)
        captcha_image_cv = cv2.cvtColor(captcha_image_cv, cv2.COLOR_BGR2GRAY)
        captcha_image_cv = cv2.threshold(captcha_image_cv, 150, 255, cv2.THRESH_BINARY)[1]

        # OCR to extract text
        captcha_text = pytesseract.image_to_string(captcha_image_cv, config='--psm 8').strip()
        print("Detected CAPTCHA text:", captcha_text)

        # Enter CAPTCHA
        captcha_input = driver.find_element(By.XPATH, "//input[contains(@name, 'captcha')]")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)

        return True

    except Exception as e:
        print(f"Image CAPTCHA handling failed: {str(e)}")
        return False
