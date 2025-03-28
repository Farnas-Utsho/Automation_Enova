from appium import webdriver
from appium.options.android import UiAutomator2Options  # Import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
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


def connect_disconnect_server(server_name):
    """
    This function will select the given server, connect to it,
    disconnect, and print the extracted IP address.
    It will also close any pop-up message after displaying the IP address.
        """
    #Open the server list
    try:
        wait = WebDriverWait(driver, 100)

        #Open the Server list
        server = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')
        ))

        server.click()
        print('Server list is opened')

    except Exception as e:
        print("Server list  is not Opened ", e)

    # 1. Click the USA dropdown to display the list of servers

    try:
        wait = WebDriverWait(driver, 50)
        USA_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[contains(@content-desc, "USA")]')))  # Update XPath as needed
        USA_button.click()  # This should trigger the dropdown
        print("USA dropdown button clicked, dropdown should now open.")
    except Exception as e:
        print('Failed to Open USA DropDown:', str(e))


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


    try:
        #Check the IP address in the browser
        #check_ip_in_browser(server_name)
        print("Checking the ip address")
        #check_ip_via_requests(server_name)
        #check_ip_via_adb(server_name)
        check_ip_via_app(server_name)
    except Exception as e :
        print ("Ip is not checked through browser")





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


def check_ip_via_app(server_name):
    """
    Opens the IP Info app, fetches the public IP address, and then closes the app.
    """
    app_package ="io.uax.myip"
    app_activity ="io.uax.myip.MainActivity"
    try:
        # Step 1: Launch the IP Info app using its package and activity name
        command = f"am start -n {app_package}/{app_activity}"
        driver.execute_script("mobile: shell", {"command": command})

        # Step 2: Wait for the IP address to be displayed in the TextView
        wait = WebDriverWait(driver, 20)  # Wait for up to 20 seconds
        ip_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.TextView[@resource-id="io.uax.myip:id/tvValue" and @text!=""]')
        ))

        # Step 3: Extract the IP address
        ip_address = ip_element.text.strip()
        print(f"Displayed IP Address for {server_name}: {ip_address}")

        # Step 4: Close the app (using the home button)
        driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
        print(f"App closed after fetching IP for {server_name}.")

    except Exception as e:
        print(f"Error while checking IP for {server_name}: {e}")


def check_ip_in_browser(server_name):
    """
    Opens Brave browser in the emulator, navigates to an IP-checking website,
    and extracts the displayed IP address.
    """
    try:
        # Open Brave browser using ADB shell command
        driver.execute_script("mobile: shell", {"command": "am start -n com.brave.browser/com.brave.browser.BrowserActivity"})
        time.sleep(5)

        # Enter the IP check website (e.g., myip.com)
        wait = WebDriverWait(driver, 100)
        url_bar = wait.until(EC.presence_of_element_located(
            (By.ID, 'com.brave.browser:id/url_bar')))  # Adjusting for Brave's URL bar ID
        url_bar.click()
        url_bar.send_keys("https://myip.com\n")
        time.sleep(10)

        # Extract the displayed IP address (using updated XPath)
        ip_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '(//android.widget.TextView[contains(@text, ".")])[1]')))  # Adjusted XPath to capture the IP

        displayed_ip = ip_element.text  # Get the extracted IP
        print(f"Displayed IP Address in Brave Browser for {server_name}: {displayed_ip}")

    except Exception as e:
        print(f"Error while checking IP in Brave browser for {server_name}: ", e)

    # Return to home screen before switching VPNs
    driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
    time.sleep(3)





# List of servers to connect to
servers = ["Singapore", "France", "Indonesia", "South Korea","Germany - 3","USA - 1","USA - 2","USA - 5"]

# Loop through the server list and call the function for each server
for server in servers:
    connect_disconnect_server(server)

# Quit the driver at the end
driver.quit()
