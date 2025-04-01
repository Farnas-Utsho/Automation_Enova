import re
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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


def scroll_and_click(element_text):
    """ Scrolls down until an element with given text is found and clicks it. """
    try:
        wait = WebDriverWait(driver, 100)

        # Scroll to element
        scrollable_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{element_text}"));'
        )))

        scrollable_element.click()
        #print(f"✅ {element_text} dropdown opened successfully!")

    except Exception as e:
        print(f"❌ Failed to open {element_text} dropdown: {e}")


def connect_disconnect_server(server_name):



    # Open the server list
    global ip_address
    try:
        wait = WebDriverWait(driver, 100)
        # Open the Server list
        server = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')
        ))
        server.click()
        #print('Server list is opened')
    except Exception as e:
        print("Server list is not Opened ", e)




    #Opening all the server lists
    try:
        # Scroll and open other country dropdowns
        countries = ["USA", "Singapore", "Netherlands"]
        for country in countries:
            scroll_and_click(country)


    except Exception as e:
        print("Failed to open the Server Drop Down")




        # Scroll for the server list
    try:
        wait = WebDriverWait(driver, 50)  # Wait up to 50 seconds for the element

        # Scroll and wait until the server element is present
        server_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{server_name}"));'
        )))

        # Click the server element
        server_element.click()
        print(f"{server_name} server selected successfully!")

    except Exception as e:
        print(f"❌ Could not find or select {server_name}: {e}")


    # Connect the server
    try:
        wait = WebDriverWait(driver, 50)
        # Locate and click on the server by name (server_name)
        server_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[contains(@content-desc, "{server_name}")]')))

        server_element.click()
        #print(f"{server_name} server is selected")

        # click on the "Disconnected" button to connect
        connect_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
        connect_button.click()
        time.sleep(5)
        #print(f'{server_name} server is connected')
    except Exception as e:
        print(f"{server_name} server is not selected or connected", e)

    try:
        """
        Opens the IP Info app, refreshes to get the public IP address, then switches back to Enova VPN to change server.
        """
        app_package = "cz.webprovider.whatismyipaddress"
        app_activity = "cz.webprovider.whatismyipaddress.MainActivity"
        refresh_button_id = "cz.webprovider.whatismyipaddress:id/refresh_info"
        ip_display_id = "cz.webprovider.whatismyipaddress:id/zobraz_ip"

        # Force close the IP Info app
        print("Closing IP Info app before reopening...")
        driver.execute_script("mobile: shell", {"command": f"am force-stop {app_package}"})
        time.sleep(3)  # Wait for the app to fully close

        # Launch the IP Info app
        print(f"Opening IP Info app to check IP for {server_name}...")
        driver.execute_script("mobile: shell", {"command": f"am start -n {app_package}/{app_activity}"})
        time.sleep(5)  # Give time for the app to open

        # Wait for the refresh button to appear and click it
        try:
            refresh_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, refresh_button_id))
            )
            print("Clicking refresh button to update IP...")
            refresh_button.click()
        except TimeoutException:
            print(f"❌ {server_name} - Refresh button not found. Skipping IP fetch.")
            return
        except NoSuchElementException as e:
            print(f"❌ {server_name} - Refresh button element not found. Error: {str(e)}")
            return

        # Wait for the IP to refresh (give extra time to ensure the IP is updated)
        time.sleep(5)  # Waiting a few seconds after the refresh button click

        # Wait for the new IP to appear
        try:
            ip_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, ip_display_id))
            )
            print("IP from the Application:")
            ip_address = ip_element.text.strip()
            print(f"Displayed IP Address for {server_name}: {ip_address}")

            if not ip_address:
                print(f"⚠️ Warning: No IP Address found for {server_name}. Checking page source...")
                print(driver.page_source)  # Debugging step
        except TimeoutException:
            print(f"❌ {server_name} - IP element not found. Skipping IP fetch.")
            return
        except NoSuchElementException as e:
            print(f"❌ {server_name} - IP element not found. Error: {str(e)}")
            return

        # Close the IP Info app and return to the home screen
        try:
            driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
            print(f"App closed after fetching IP for {server_name}.")
        except Exception as e:
            print(f"❌ {server_name} - Failed to return to home screen. Error: {str(e)}")

    except Exception as e:
        print(f"❌ {server_name} - Failed to fetch IP from the Application.")
        print(f"Error details: {str(e)}")



    #Reopen the Enova VPN

    try:

        enova_vpn_package = "com.enovavpn.mobile"
        enova_vpn_activity = "com.enovavpn.mobile.MainActivity"
        print("Switching back to Enova VPN to change server...")
        driver.execute_script("mobile: shell", {"command": f"am start -n {enova_vpn_package}/{enova_vpn_activity}"})
        time.sleep(10)  # Give time for the Enova VPN app to load

    except Exception as e :
        print("Failed to reopen the Enova VPN")
    # Disconnect the server
    try:
        wait = WebDriverWait(driver, 50)

        # Click on the "Connected" button to disconnect
        turn_on_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()
        time.sleep(3)
    except Exception as e :
        print("Failed to Click on Connected button",e)


    # Click "Disconnect" button in the pop-up
    try:
        wait = WebDriverWait(driver, 60)

        disconnect_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
    except Exception as e :
        print(f"{server_name} server disconnected")




    # Locate the element containing the IP address
    try :
        wait = WebDriverWait(driver, 50)

        ip_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, ".")]')))

        # Extract the IP address from content-desc
        content_desc = ip_element.get_attribute("content-desc")

        # Regular expression to match an IPv4 address
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        match = re.search(ip_pattern, content_desc)


        if match:
            print(f"Extracted IP Address for {server_name}: {match.group()}")
            if match.group() == ip_address:
                print("✅ Ip Matched")
            else:
                print("❌ Ip Does not Matched")

        else:
            print(f"No IP Address found for {server_name}")
    except Exception as e:
        print(f"Error while extracting IP for {server_name}: ", e)

    # Close the pop-up message
    try:

        wait = WebDriverWait(driver, 120)
        # Locate and click on the close button for the pop-up
        close_popup = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[2]/android.widget.ImageView[1]')
        ))
        close_popup.click()
        time.sleep(5)

        print(f"Pop-up for {server_name} closed")
    except Exception as e:
        print(f"Failed to close pop-up for {server_name}: ", e)




# List of servers to connect to

print("Checking the Wireguard Protocol")
servers = [ "France", "Indonesia", "South Korea","Brazil","Canada","Poland","United Kingdom",
                                                    "USA - 1", "USA - 6", "USA - 5","Singapore","Singapore - 7","Netherlands - 3","Netherlands - 1"]
#servers = [ "France", "Indonesia", "South Korea","Brazil","Canada","Poland","United Kingdom","Germany - 1","Germany - 2" ,"Germany - 6","Germany - 7","Germany - 8"
                                                    #,"USA - 1", "USA - 6", "USA - 5","Singapore","Singapore - 7","Netherlands - 3","Netherlands - 1"]
# Loop through the server list and call the function for each server
for server in servers:
    connect_disconnect_server(server)



# Quit the driver
driver.quit()