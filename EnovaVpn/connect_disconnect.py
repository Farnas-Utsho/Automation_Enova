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


def scroll_and_click(element_text):
    """ Scrolls down until an element with the given text is found and clicks it. """
    try:
        wait = WebDriverWait(driver, 50)
        scrollable_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{element_text}"));'
        )))
        scrollable_element.click()
    except Exception as e:
        print(f"❌ Failed to open {element_text} dropdown: {e}")


def connect_disconnect_server(server_name):
    """ Connects to a given VPN server, verifies the IP, and disconnects """
    global ip_address

    print(f"\n🚀 Attempting to connect to {server_name}...")

    try:
        wait = WebDriverWait(driver, 50)

        # Open the Server List
        server = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')))
        server.click()
        time.sleep(2)

        # Open the country dropdowns
        for country in ["USA", "Singapore", "Netherlands"]:
            scroll_and_click(country)

        # Select the specific server
        server_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{server_name}"));'
        )))
        server_element.click()
        print(f"✅ {server_name} selected.")

        # Click Connect button
        connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
        connect_button.click()
        time.sleep(5)

    except Exception as e:
        print(f"❌ {server_name} - Connection failed: {e}")
        return  # Skip this server and continue with the next one

    # Fetch IP Address from IP Info App
    try:
        ip_address = get_ip_from_app()
    except Exception as e:
        print(f"❌ {server_name} - Failed to fetch IP: {e}")

    # Switch back to Enova VPN
    try:
        driver.execute_script("mobile: shell", {"command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"})
        time.sleep(2)
    except Exception as e:
        print(f"❌ {server_name} - Failed to reopen Enova VPN: {e}")

    # Disconnect the VPN
    try:
        turn_on_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()
        disconnect_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
        time.sleep(3)
        print(f"🔌 {server_name} disconnected successfully.")
    except Exception as e:
        print(f"❌ {server_name} - Disconnection failed: {e}")

    # Validate IP
    try:
        ip_element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, ".")]')))
        content_desc = ip_element.get_attribute("content-desc")
        match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content_desc)

        if match:
            extracted_ip = match.group()
            print(f"Extracted IP Address for {server_name}: {extracted_ip}")
            if extracted_ip == ip_address:
                print("✅ IP Matched")
            else:
                print("❌ IP Does Not Match")
        else:
            print(f"No IP Address found for {server_name}")
    except Exception as e:
        print(f"⚠️ Error extracting IP for {server_name}: {e}")

    # Close the pop-up
    try:
        close_popup = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[1]')))
        close_popup.click()
        time.sleep(2)
        print(f"✅ Pop-up for {server_name} closed.")
    except Exception as e:
        print(f"⚠️ Failed to close pop-up for {server_name}: {e}")


def get_ip_from_app():
    """ Fetches the public IP using the IP Info App """
    app_package = "cz.webprovider.whatismyipaddress"
    app_activity = "cz.webprovider.whatismyipaddress.MainActivity"

    # Open IP Info App
    driver.execute_script("mobile: shell", {"command": f"am start -n {app_package}/{app_activity}"})
    time.sleep(5)

    try:
        refresh_button = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/refresh_info"))
        )
        refresh_button.click()
        time.sleep(5)

        ip_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/zobraz_ip"))
        )
        print("Ip from the My Ip app : ", ip_element.text.strip())
        return ip_element.text.strip()

    except TimeoutException:
        print("❌ IP fetch timed out.")
        return None

    except NoSuchElementException as e:
        print(f"❌ IP element not found: {e}")
        return None

    finally:
        driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
        print("📱 Returned to home screen.")








print("\n################################### IPsec Protocol ############################################")
servers = ["USA - 1", "USA - 2", "USA - 5", "USA - 6", "Germany - 1", "Germany - 2", "Germany - 6", "Germany - 7",
               "Germany - 8", "Singapore", "Singapore - 2", "Singapore - 7", "Netherlands - 1", "Netherlands - 3",
               "France", "Indonesia", "South Korea", "Canada", "Poland", "United Kingdom"]

# Loop through servers and attempt connections
for server in servers:
    connect_disconnect_server(server)


print("✅ VPN testing completed.")


