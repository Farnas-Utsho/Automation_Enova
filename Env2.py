from asyncio import timeout
from traceback import print_tb

from appium import webdriver
from appium.options.android import UiAutomator2Options  # Import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
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

# # # Click Login Button
# # try:
# #     wait = WebDriverWait(driver, 20)
# #     login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="LOGIN"]')))
# #     login_button.click()
# # except Exception as e:
# #     print("Login button not found:", e)
# #
# # # Input Email
# # try:
# #     wait = WebDriverWait(driver, 50)
# #     email = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[2]')))
# #     email.click()
# #     email.clear()
# #     email.send_keys('vaskar@nagorik.tech')
# # except Exception as e:
# #     print("Email field not found:", e)
# #
# # # Input Password
# # try:
# #     wait = WebDriverWait(driver, 50)
# #     password = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText')))
# #     password.click()
# #     password.clear()
# #     password.send_keys('A12345678')
# # except Exception as e:
# #     print("Password field not found:", e)
# #
# # # Show Password (Optional)
# # try:
# #     wait = WebDriverWait(driver, 20)
# #     show_password = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText/android.widget.ImageView[2]')))
# #     show_password.click()
# # except Exception as e:
# #     print("Show password button not found, skipping:", e)
# #
# # # Click Sign-in
# # try:
# #     wait = WebDriverWait(driver, 20)
# #     signin_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="SIGN IN"]')))
# #     signin_button.click()
# # except Exception as e:
# #     print("Sign-in button not found:", e)
# #
# #
# #
# # # #log in successful
#
#
# #Open the vpn list
#
# try:
#     wait = WebDriverWait(driver, 50)
#
#     # Find ANY server that is available
#     server = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')
#     ))
#
#     server.click()
#
#
# except Exception as e:
#     print("No server found:", e)
#
#
# ################ Check all the USA servers Under Shadowsocks Protocol ################
#
# 1. Click the USA dropdown to display the list of servers

try:
    wait = WebDriverWait(driver, 50)
    USA_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[contains(@content-desc, "USA")]')))  # Update XPath as needed
    USA_button.click()  # This should trigger the dropdown
    print("USA dropdown button clicked, dropdown should now open.")
except Exception as e:
    print('Failed to click USA button:', str(e))

#
#  # 2. Connect with  USA-1
# # try:
# #
# #     Connect_USA_1 = wait.until(EC.element_to_be_clickable(
# #         (By.XPATH, '//*[contains(@content-desc, "USA - 1")]')))  # Update XPath as needed
# #     Connect_USA_1.click()
# #     print("Selected to USA-1.")
# # except Exception as e:
# #     print('Unable to Select  USA-1:', str(e))
#
#
#  # 3. Connect with  USA-2
# # try:
# #
# #     Connect_USA_2 = wait.until(EC.element_to_be_clickable(
# #         (By.XPATH, '//*[contains(@content-desc, "USA - 2")]')))  # Update XPath as needed
# #     Connect_USA_2.click()
# #     print("Selected to USA-2.")
# # except Exception as e:
# #     print('Unable to Select  USA-2:', str(e))
#
#
# #3. Connect with  USA-5
# try:
#
#     Connect_USA_5 = wait.until(EC.element_to_be_clickable(
#         (By.XPATH, '//*[contains(@content-desc, "USA - 5")]')))  # Update XPath as needed
#     Connect_USA_5.click()
#     print("Selected to USA - 5.")
#     wait = WebDriverWait(driver, 50)
#     # Wait for the element and click on it
#     usa_5 = wait.until(EC.element_to_be_clickable(
#         (By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
#     usa_5.click()
#     press_ok = wait.until(EC.element_to_be_clickable((By.ID, '	android:id/button1')))
#     print('Connected with USA 5')
# except Exception as e:
#     print('Unable to Select  USA - 5:', str(e))
#
#
# #Connect with USA - 5
# # try:
# #     wait=WebDriverWait(driver,50)
# #     # Wait for the element and click on it
# #     usa_5 = wait.until(EC.element_to_be_clickable((By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
# #     usa_5.click()
# #     press_ok=wait.until(EC.element_to_be_clickable((By.ID,'	android:id/button1')))
# #     print('Connected with USA 5')
# # except Exception as e:
# #     print('Not Connected with USA 5', e)
#
#
#
#
#
#
#
#
#
#
#
#
#
# #Connect with Germany server
try:
    wait = WebDriverWait(driver, 50)

    # Locate and click Germany 3 server
    germany_server = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//android.view.View[@content-desc="Germany - 3"]')
    ))

    germany_server.click()
    print("Germany 3 is selected")
    wait = WebDriverWait(driver, 50)
    # Wait for the element and click on it



    germany_3 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
    germany_3.click()
    press_ok = wait.until(EC.element_to_be_clickable((By.ID, '	android:id/button1')))
    print('Connected with germany_3')


except Exception as e:
    print("Germany 3 not found or could not be connected:", e)


# #Connect with Singapore server
try:
   wait = WebDriverWait(driver, 50)


   # Locate and click Singapore server
   singapore_server = wait.until(EC.presence_of_element_located(
       (By.XPATH, '//*[contains(@content-desc, "Singapore")]')))

   singapore_server.click()
   print("Singapore server is selected")
   Singapore = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
   Singapore.click()







except Exception as e:
   print("Singapore server is not selected ", e)
#
#
# #Connect with Netherlands - 1
#
# try:
#    wait = WebDriverWait(driver, 50)
#
#
#    # Locate and click Netherlands 1 server
#    Netherlands_1_server = wait.until(EC.presence_of_element_located(
#        (By.XPATH, '//android.view.View[contains(@content-desc, "Netherlands")]')
#    ))
#
#
#    Netherlands_1_server.click()
#    print("Netherlands 1 server is selected")
#
#
#
#
# except Exception as e:
#    print(" Netherlands 1 is not selected ", e)
#
# #Connect with France server
# try:
#     wait = WebDriverWait(driver, 50)
#
#     # Locate and click France server
#     france_server = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//android.view.View[contains(@content-desc, "France")]')
#     ))
#
#     france_server.click()
#     print("France  server is selected")
#
#
# except Exception as e:
#     print("France server is not selected ", e)
#
#
# #Connect with Indonesia server
# try:
#     wait = WebDriverWait(driver, 50)
#
#     # Locate and click Germany 3 server
#     indonesia_server = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//android.view.View[@content-desc="Indonesia"]')
#     ))
#
#     indonesia_server.click()
#     print("Indonesia  is selected")
#
#
# except Exception as e:
#     print("Indonesia  not found ", e)
#
#
#
#
 #Connect with South korea server
try:
    wait = WebDriverWait(driver, 50)

    # Locate and click South Korea server
    southkorea_server = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//android.view.View[@content-desc="South Korea"]')
    ))

    southkorea_server.click()
    print("South Korea server is selected")


except Exception as e:
    print("South Korea server is not selected ", e)