import time
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import re

# # Define desired capabilities using UiAutomator2Options
# options = UiAutomator2Options()
# options.platform_name = "Android"
# options.platform_version = "16"  # Change according to your device version
# options.device_name = "emulator-5554"  # Use 'adb devices' to check the device name
# options.app = "D:/EnovaVPN.apk"  # Provide the correct path to your APK file
# options.app_package = "com.enovavpn.mobile"  # Replace with your app's package name
# options.app_activity = "com.enovavpn.mobile.MainActivity"  # Replace with your app's main activity
# options.automation_name = "UiAutomator2"
# options.no_reset = True  # Set to False if you want a fresh install every time


#Connect local device with desired capabilities using UiAutomator2Options


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







def connect_disconnect_server(server_name):
    """
    This function will select the given server, connect to it,
    disconnect, and print the extracted IP address.
    It will also close any pop-up message after displaying the IP address.
    """
    # Open the server list
    try:
        wait = WebDriverWait(driver, 100)
        # Open the Server list
        server = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')
        ))
        server.click()
        print('Server list is opened')
    except Exception as e:
        print("Server list is not Opened ", e)

   # Open the USA dropdown to display the list of servers
    try:
        wait = WebDriverWait(driver, 50)
        USA_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[contains(@content-desc, "USA")]')))  # Update XPath as needed
        USA_button.click()  # This should trigger the dropdown
        print("USA dropdown button clicked, dropdown should now open.")
    except Exception as e:
        print('Failed to Open USA DropDown:', str(e))

    #Scroll for the server list
    try:
        # Scroll to the server by name
        server_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{server_name}"));'
        )
        server_element.click()
        print(f"✅ {server_name} server selected successfully!")
    except Exception as e:
        print(f"❌ Could not find or select {server_name}: {e}")

    try:
        wait = WebDriverWait(driver, 50)
        # Locate and click on the server by name (server_name)
        server_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[contains(@content-desc, "{server_name}")]')))

        server_element.click()
        print(f"{server_name} server is selected")

        # Wait and click on the "Disconnected" button to connect
        connect_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
        connect_button.click()

        print(f'{server_name} server is connected')
    except Exception as e:
        print(f"{server_name} server is not selected or connected", e)

    # Check the IP address in the app
    try:
        print("Checking the ip address using IP Info app")
       # check_ip_in_browser(server_name)

    except Exception as e:
        print("IP is not checked through the app", e)

    # Disconnect the server
    try:
        wait = WebDriverWait(driver, 50)

        # Click on the "Connected" button to disconnect
        turn_on_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()

        # Click "Disconnect" button
        disconnect_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
        print(f"{server_name} server disconnected")

        # Locate the element containing the IP address
        ip_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, ".")]')))

        # Extract the IP address from content-desc
        content_desc = ip_element.get_attribute("content-desc")

        # Regular expression to match an IPv4 address
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        match = re.search(ip_pattern, content_desc)

        if match:
            print(f"Extracted IP Address for {server_name}: {match.group()}")
        else:
            print(f"No IP Address found for {server_name}")
    except Exception as e:
        print(f"Error while disconnecting or extracting IP for {server_name}: ", e)

    # Close the pop-up message if it appears
    try:
        wait = WebDriverWait(driver, 50)
        # Locate and click on the close button for the pop-up
        close_popup = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[2]/android.widget.ImageView[1]')
        ))
        close_popup.click()
        print(f"Pop-up for {server_name} closed")
    except Exception as e:
        print(f"Failed to close pop-up for {server_name}: ", e)




# def check_ip_in_browser(server_name):
#     """
#     Opens Brave browser in the emulator, navigates to an IP-checking website,
#     extracts the displayed IP address, then reopens Enova VPN.
#     """
#     try:
#         # Open Brave browser using ADB shell command
#         print("Opening Brave browser...")
#         driver.execute_script("mobile: shell", {
#             "command": "am start -n com.brave.browser/org.chromium.chrome.browser.ChromeTabbedActivity"
#         })
#         time.sleep(5)
#
#         # Wait for the URL bar and enter the IP-check website
#         wait = WebDriverWait(driver, 50)
#         url_bar = wait.until(EC.presence_of_element_located(
#             (By.ID, 'com.brave.browser:id/url_bar')  # Ensure this is the correct ID
#         ))
#         url_bar.click()
#         url_bar.send_keys("https://www.myip.com\n")
#         # Explicitly press Enter/Go button
#         driver.execute_script("mobile: performEditorAction", {"action": "search"})
#         time.sleep(10)  # Wait for the page to load
#
#
#         # Extract the displayed IP address using the provided XPath
#         ip_element = wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//span[@id='ip']")
#         ))
#
#         displayed_ip = ip_element.text.strip()  # Get the extracted IP
#         print(f"✅ Displayed IP Address in Brave Browser for {server_name}: {displayed_ip}")
#
#     except Exception as e:
#         print(f"❌ Error while checking IP in Brave browser for {server_name}: {e}")
#         displayed_ip = None  # Ensure function doesn't break on failure
#
#     finally:
#         # Return to home screen before switching VPNs
#         print("Closing Brave and reopening Enova VPN...")
#         driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
#         time.sleep(3)
#
#         # Reopen Enova VPN
#         reopen_enova_vpn()
#
#     return displayed_ip


# def reopen_enova_vpn():
#     """
#     Reopens the Enova VPN application to continue execution.
#     """
#     try:
#         app_package = "com.enovavpn.mobile"
#         app_activity = "com.enovavpn.mobile.MainActivity"
#
#         print("Reopening Enova VPN...")
#         command = f"am start -n {app_package}/{app_activity}"
#         driver.execute_script("mobile: shell", {"command": command})
#
#         time.sleep(8)  # Give time for the app to launch
#         print("✅ Enova VPN app reopened successfully.")
#
#     except Exception as e:
#         print("❌ Failed to reopen Enova VPN:", e)


# List of servers to connect to
servers = [ "France", "Singapore","Indonesia", "South Korea", "Germany - 3", "USA - 1", "USA - 2", "USA - 5"]

# Loop through the server list and call the function for each server
for server in servers:
    connect_disconnect_server(server)

# Quit the driver at the end
driver.quit()
