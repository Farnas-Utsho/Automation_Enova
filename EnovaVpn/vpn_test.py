import re
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Connect local device with desired capabilities using UiAutomator2Options
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "12"  # Set your actual Android version
options.device_name = "10ECBH02JJ000D2"  # Use your real device ID from `adb devices`
options.app = "D:/EnovaVPN.apk"  # Ensure the correct path to the APK
options.app_package = "com.enovavpn.mobile"  # Replace with your actual app's package name
options.app_activity = "com.enovavpn.mobile.MainActivity"  # Replace with the correct main activity
options.automation_name = "UiAutomator2"
options.no_reset = True  # Set to False if you want a fresh install every time
options.new_command_timeout = 300  # Prevent session timeout
options.auto_grant_permissions = True  # Auto-grant required permissions

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)

def switch_protocol():
    # Your existing switch_protocol code
    pass

def connect_disconnect_server(server_name):
    """ Connects to a given VPN server, verifies the IP, and disconnects """
    global ip_address
    print(f"\n🚀 Attempting to connect to {server_name}...")

    try:
        wait = WebDriverWait(driver, 50)
        # Open the Server List
        server = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')))
        server.click()
        time.sleep(2)

        # Open the country dropdowns
        for country in ["USA", "Singapore", "Netherlands", "Germany"]:
            scroll_and_click(country)

        # Select the specific server
        server_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{server_name}"));'
        )))
        server_element.click()
        print(f"✅ {server_name} selected.")

        # Click Connect button
        connect_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
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
        return  # Skip this server and continue with the next one

    # Switch back to Enova VPN
    try:
        driver.execute_script("mobile: shell",
                              {"command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"})
        time.sleep(2)
    except Exception as e:
        print(f"❌ {server_name} - Failed to reopen Enova VPN: {e}")
        return  # Skip this server and continue with the next one

    # Disconnect the VPN
    try:
        turn_on_button = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()
        disconnect_button = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
        time.sleep(3)
        print(f"🔌 {server_name} disconnected successfully.")
    except Exception as e:
        print(f"❌ {server_name} - Disconnection failed: {e}")
        return  # Skip this server and continue with the next one

    # Validate IP
    try:
        ip_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, ".")]')))
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
        return  # Skip this server and continue with the next one

    # Close the pop-up
    try:
        close_popup = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[1]')))
        close_popup.click()
        time.sleep(2)
        print(f"✅ Pop-up for {server_name} closed.")
    except Exception as e:
        print(f"⚠️ Failed to close pop-up for {server_name}: {e}")

def wireguard():
    print("Running WireGuard test")
    switch_protocol()
    print("################################### Wireguard Protocol ############################################")

    # List of servers
    servers = [
        "France", "Indonesia", "South Korea", "Brazil", "Canada", "Poland", "United Kingdom", "Germany - 1",
        "USA - 1", "USA - 6", "USA - 5", "Singapore", "Singapore - 7", "Netherlands - 3", "Netherlands - 1"
    ]

    # Loop through the server list and call the function for each server
    for server in servers:
        connect_disconnect_server(server)  # Call connect_disconnect_server inside the loop
