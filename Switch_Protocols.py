
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
options.platform_version = "14"  # Set your actual Android version
options.device_name = "RZCTA02JRZP"  # Use your real device ID from `adb devices`
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


def switch_protocol():
     #click on settings
     global select_vpn_protocol
     try:
         wait = WebDriverWait(driver, 50)
         click_settings=wait.until(EC.presence_of_element_located(
             (By.XPATH,'//android.widget.Button[contains(@content-desc, "Settings")]')
         ))
         click_settings.click()
     except Exception as e:
         print("Settings Icon not found")


     #Click on vpn settings
     try:
         wait = WebDriverWait(driver, 50)
         click_vpn_settings = wait.until(EC.presence_of_element_located(
             (By.XPATH, '//android.widget.ImageView[@content-desc="VPN settings"]')
         ))
         click_vpn_settings.click()
     except Exception as e:
         print("VPN Settings Icon not found")

         # Click on Vpn Protocol
     try:
         wait = WebDriverWait(driver, 50)
         click_vpn_protocol = wait.until(EC.presence_of_element_located(
             (By.XPATH, '//android.view.View[contains(@content-desc, "VPN protocol")]')
         ))
         click_vpn_protocol.click()

     except Exception as e:
         print("VPN Protocol  not found")

    #Select vpn protocol
     # try:
     #     wait = WebDriverWait(driver, 10)
     #     select_vpn_protocol = wait.until(EC.element_to_be_clickable(
     #         (AppiumBy.ANDROID_UIAUTOMATOR,
     #          'new UiSelector().descriptionContains("WireGuard")')
     #     ))
     #
     #     select_vpn_protocol.click()
     #     print("Element found")
     # except Exception as e:
     #     print("VPN Protocol is not selected:", e)
     # Alternative pure-W3C version
     try:
         wait = WebDriverWait(driver, 20)  # Increased wait time

         # Step 1: Locate the protocol container using bounds information
         protocol_container = wait.until(EC.presence_of_element_located(
             (AppiumBy.ANDROID_UIAUTOMATOR,
              'new UiSelector().descriptionContains("WireGuard")')
         ))

         # Step 2: Get precise coordinates from bounds [77,1779][1003,2088]
         x_center = 77 + (1003 - 77) // 2  # Horizontal center
         y_center = 1779 + (2088 - 1779) // 2  # Vertical center

         # Step 3: Calculate tap position (right side of element)
         tap_x = x_center + 400  # Adjust based on your screen resolution
         tap_y = y_center

         # Step 4: Use W3C pointer input for precise tapping
         actions = ActionChains(driver)
         actions.w3c_actions = ActionBuilder(driver,
                                             mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
         actions.w3c_actions.pointer_action.move_to_location(tap_x, tap_y)
         actions.w3c_actions.pointer_action.click()
         actions.w3c_actions.perform()

         # Verification
         try:
             wait.until(lambda d: protocol_container.get_attribute("checked") == "true")
             print("WireGuard protocol successfully enabled")
         except:
             print("Warning: Couldn't verify protocol activation")

     except Exception as e:
         print(f"Protocol selection failed: {str(e)}")
         # Alternative method using direct Appium commands
         try:
             driver.execute_script('mobile: click', {
                 'x': 900,  # Right side of switch area
                 'y': 1930,  # Vertical center
                 'duration': 100
             })
             print("Used direct coordinate click as fallback")
         except Exception as fallback_e:
             print(f"All methods failed: {str(fallback_e)}")
             driver.save_screenshot("protocol_selection_failed.png")

switch_protocol()
driver.close()




