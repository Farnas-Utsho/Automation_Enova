

from asyncio import timeout
from traceback import print_tb

from appium import webdriver
from appium.options.android import UiAutomator2Options  # Import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import re
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

#Connect with Singapore server
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

   print('Singapore server is connected')


except Exception as e:
   print("Singapore server is not selected ", e)



#Disconnect the server
try:
   #Clicking on the turn on button
   wait = WebDriverWait(driver, 50)

   turn_on = wait.until(EC.presence_of_element_located(
      (By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')
   ))
   turn_on.click()

   #click Disconnect
   disconnect = wait.until(EC.presence_of_element_located(
      (By.XPATH,'//android.view.View[@content-desc="DISCONNECT"]')

   ))
   disconnect.click()
   print("Server disconnected")

   # Locate the element containing the IP address
   ip=wait.until(EC.presence_of_element_located(
      (By.XPATH, '//android.view.View[contains(@content-desc, ".")]')
   ))


   # Extract the IP address from content-desc
   content_desc = ip.get_attribute("content-desc")

   # Regular expression to match an IPv4 address
   ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
   match = re.search(ip_pattern, content_desc)

   if match:
      print("Extracted IP Address:", match.group())  # This prints the dynamic IP
   else:
      print("No IP Address found in content-desc")





except Exception as L:
   print("Server is not disconnected",e)





#
# try:
#    wait = WebDriverWait(driver, 100)
#
#    server = wait.until(EC.presence_of_element_located(
#       (By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')
#    ))
#
#    server.click()
#    print('Server list is opened')
#    time.sleep(50)
#
# except Exception as e:
#    print("Server list  is not selected ", e)
#
#
# # #Connect with the Netherlands - 1
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
#    time.sleep(10)
#
#    # Switch to Netherlands Server
#    switch = wait.until(EC.presence_of_element_located(
#       (By.XPATH, '//android.view.View[@content-desc="Switch"]')
#    ))
#    switch.click()
#
#
#
#
# except Exception as e:
#    print(" Netherlands 1 is not selected ", e)



