from asyncio import timeout
from traceback import print_tb

from appium import webdriver
from appium.options.android import UiAutomator2Options  # Import options
import time

# Define desired capabilities using UiAutomator2Options
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "16"  # Change according to your device version
options.device_name = "emulator-5554"  # Use 'adb devices' to check the device name
options.app = "D:/EnovaVPN.apk"  # Provide the correct path to your APK file
options.app_package = "com.enovavpn.mobile"  # Replace with your app's package name
options.app_activity = "com.enovavpn.mobile.MainActivity"  # Replace with your app's main activity
options.automation_name = "UiAutomator2"
options.no_reset = True  # Set to False if you want a fresh install every time

# Connect to Appium Server
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)

# Wait for the app to load
time.sleep(5)

# # Click Login Button
# try:
#     wait = WebDriverWait(driver, 20)
#     login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="LOGIN"]')))
#     login_button.click()
# except Exception as e:
#     print("Login button not found:", e)
#
# # Input Email
# try:
#     wait = WebDriverWait(driver, 50)
#     email = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]')))
#     email.click()
#     email.clear()
#     email.send_keys('vaskar@nagorik.tech')
# except Exception as e:
#     print("Email field not found:", e)
#
# # Input Password
# try:
#     wait = WebDriverWait(driver, 50)
#     password = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText')))
#     password.click()
#     password.clear()
#     password.send_keys('A12345678')
# except Exception as e:
#     print("Password field not found:", e)

# # Show Password (Optional)
# try:
#     wait = WebDriverWait(driver, 20)
#     show_password = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText/android.widget.ImageView[2]')))
#     show_password.click()
# except Exception as e:
#     print("Show password button not found, skipping:", e)
#
# # Click Sign-in
# try:
#     wait = WebDriverWait(driver, 20)
#     signin_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="SIGN IN"]')))
#     signin_button.click()
# except Exception as e:
#     print("Sign-in button not found:", e)
#
#
#
# # #log in successful



from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def connect_and_disconnect_server(driver, server_name):
    try:
        wait = WebDriverWait(driver, 50)

        # Locate and click on the server name from the list
        server = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[contains(@content-desc, "{server_name}")]')))
        server.click()
        print(f"{server_name} server is selected")

        # Click on the connect button
        connect_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
        connect_button.click()
        print(f'{server_name} server is connected')

        # Wait for connection to establish
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]')))

    except Exception as e:
        print(f"{server_name} server is not selected", e)
        return

    try:
        # Click on the disconnect button
        disconnect_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')
        ))
        disconnect_button.click()

        disconnect_confirm = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')
        ))
        disconnect_confirm.click()
        print("Server disconnected")

        # Locate the element containing the IP address
        ip_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, ".")]')
        ))

        # Extract the IP address from content-desc
        content_desc = ip_element.get_attribute("content-desc")

        # Regular expression to match an IPv4 address
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        match = re.search(ip_pattern, content_desc)

        if match:
            print(f"Extracted IP Address for {server_name}: {match.group()}")
        else:
            print("No IP Address found in content-desc")

    except Exception as e:
        print("Server is not disconnected", e)


# Example usage:
server_list = ["Singapore", "France", "Indonesia", "South Korea"]

driver = None  # Initialize your Appium driver before running the function

for server in server_list:
    connect_and_disconnect_server(driver, server)

# Close the session
#driver.quit()
