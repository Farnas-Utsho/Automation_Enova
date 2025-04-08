import re
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Connect local device with desired capabilities using UiAutomator2Options
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "12                                                                                                                              "  # Set your actual Android version
options.device_name = "10ECBH02JJ000D2"  # Use your real device ID from `adb devices`
options.app = "D:/EnovaVPN.apk"  # Ensure the correct path to the APK
options.app_package = "com.enovavpn.mobile"  # Replace with your actual app's package name
options.app_activity = "com.enovavpn.mobile.MainActivity"  # Replace with the correct main activity
options.automation_name = "UiAutomator2"
options.no_reset = True  # Set to False if you want a fresh install every time
options.new_command_timeout = 300  # Prevent session timeout
options.auto_grant_permissions = True  # Auto-grant required permissions

# Optional: Ensure Appium detects the correct activity
options.ensure_webviews_have_pages = True
options.dont_stop_app_on_reset = True  # Keeps the app running when reconnecting

# Connect to Appium Server
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)

# Wait for the app to load
time.sleep(5)

def switch_protocol( location_x, location_y):
    # Click on settings
    global select_vpn_protocol
    print("Switch protocol page")

    try:
        wait = WebDriverWait(driver, 50)
        click_settings = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.Button[contains(@content-desc, "Settings")]')
        ))
        click_settings.click()
    except Exception as e:
        print("Settings Icon not found")
        return False

    # Click on vpn settings
    try:
        wait = WebDriverWait(driver, 50)
        click_vpn_settings = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.ImageView[@content-desc="VPN settings"]')
        ))
        click_vpn_settings.click()
    except Exception as e:
        print("VPN Settings Icon not found")
        driver.back()  # Go back if VPN settings not found
        return False

    # Click on Vpn Protocol
    try:
        wait = WebDriverWait(driver, 50)
        click_vpn_protocol = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "VPN protocol")]')
        ))
        click_vpn_protocol.click()
    except Exception as e:
        print("VPN Protocol not found")

    # Select vpn protocol
    try:
        driver.execute_script('mobile: shell', {
            'command': 'input',
            'args': ['tap',622, 1114]
        })
        time.sleep(2)  # Wait for protocol to switch

        # Navigate back to main screen
    except Exception as e:
        print(f"Error selecting protocol: {str(e)}")

    # Close the pop-up
    try:
        wait = WebDriverWait(driver, 50)
        click_close = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.ImageView')
        ))
        click_close.click()
    except Exception as e:
        print("Close button not found")


    #Click on the Back Navigation
    try:
        driver.execute_script('mobile: shell', {
            'command': 'input',
            'args': ['tap', 64, 118]
        })
        time.sleep(2)  # Wait for protocol to switch

        # Navigate back to main screen
    except Exception as e:
        print(f"Error selecting protocol: {str(e)}")

    # Click on the home icon
    try:
        wait = WebDriverWait(driver, 50)
        click_close = wait.until(EC.presence_of_element_located(
            (By.ACCESSIBILITY_ID, "Home\nTab 1 of 4")  # Correct usage of ACCESSIBILITY_ID
        ))
        click_close.click()
    except Exception as e:
        print(f"Home button not found: {e}")  # Correct exception printing


switch_protocol(622, 1114)