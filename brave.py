import time
import re
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Appium Desired Capabilities
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "14"  # Your actual Android version
options.device_name = "RZCTA02JRZP"  # Your real device ID
options.app = "D:/EnovaVPN.apk"  # APK path
options.app_package = "com.enovavpn.mobile"
options.app_activity = "com.enovavpn.mobile.MainActivity"
options.automation_name = "UiAutomator2"
options.no_reset = True
options.new_command_timeout = 300
options.auto_grant_permissions = True
options.ensure_webviews_have_pages = True
options.dont_stop_app_on_reset = True

# Connect to Appium Server
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
time.sleep(5)  # Wait for app to load


def scroll_and_click(element_text):
    """ Scrolls down until an element with given text is found and clicks it. """
    try:
        scrollable_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{element_text}"));'
        )
        scrollable_element.click()
        print(f"✅ {element_text} dropdown opened successfully!")
    except Exception as e:
        print(f"❌ Failed to open {element_text} dropdown:", e)


def connect_disconnect_server(server_name):
    """ Automates the process of connecting, checking IP, and disconnecting from a VPN server. """

    # Open the server list
    try:
        wait = WebDriverWait(driver, 100)
        server_list = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')
        ))
        server_list.click()
        print("✅ Server list opened")
    except Exception as e:
        print("❌ Server list not opened:", e)

    # Scroll and open other country dropdowns
    countries = ["USA","Germany", "Singapore", "Netherlands"]
    for country in countries:
        scroll_and_click(country)



    try:
     # Scroll to the server by name
            server_element = driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{server_name}"));'
            )
            server_element.click()
            #print(f"✅ {server_name} server selected successfully!")
    except Exception as e:
            print(f"❌ Could not find or select {server_name}: {e}")



    # Connect the server
    try:
        wait = WebDriverWait(driver, 50)
        server_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[contains(@content-desc, "{server_name}")]')))
        server_element.click()

        # Click the "Disconnected" button to connect
        connect_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
        connect_button.click()

        print(f"✅ {server_name} server connected")
    except Exception as e:
        print(f"❌ {server_name} server not connected:", e)

    # Check IP Address
    try:
        app_package = "cz.webprovider.whatismyipaddress"
        app_activity = "cz.webprovider.whatismyipaddress.MainActivity"
        refresh_button_id = "cz.webprovider.whatismyipaddress:id/refresh_info"
        ip_display_id = "cz.webprovider.whatismyipaddress:id/zobraz_ip"

        # Open IP Info app
        driver.execute_script("mobile: shell", {"command": f"am start -n {app_package}/{app_activity}"})
        time.sleep(3)

        # Refresh IP
        refresh_button = driver.find_element(AppiumBy.ID, refresh_button_id)
        for _ in range(3):  # Tap refresh multiple times
            refresh_button.click()
            time.sleep(1)

        # Get displayed IP
        wait = WebDriverWait(driver, 30)
        ip_element = wait.until(EC.presence_of_element_located((AppiumBy.ID, ip_display_id)))
        ip_address = ip_element.text.strip()

        print(f"🌍 IP Address for {server_name}: {ip_address}")

        # Close the IP Info app
        driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
    except Exception as e:
        print("❌ Failed to fetch IP:", e)

    # Reopen Enova VPN
    try:
        enova_vpn_package = "com.enovavpn.mobile"
        enova_vpn_activity = "com.enovavpn.mobile.MainActivity"
        driver.execute_script("mobile: shell", {"command": f"am start -n {enova_vpn_package}/{enova_vpn_activity}"})
        time.sleep(8)
        print("✅ Switched back to Enova VPN")
    except Exception as e:
        print("❌ Failed to reopen Enova VPN:", e)

    # Disconnect from server
    try:
        wait = WebDriverWait(driver, 50)
        disconnect_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        disconnect_button.click()

        confirm_disconnect = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        confirm_disconnect.click()

        print(f"🔌 {server_name} disconnected")

        # Extract and display IP after disconnecting
        ip_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, ".")]')))
        content_desc = ip_element.get_attribute("content-desc")

        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        match = re.search(ip_pattern, content_desc)
        if match:
            print(f"🔄 Extracted IP Address after disconnecting: {match.group()}")
        else:
            print("⚠️ No IP Address found after disconnecting")
    except Exception as e:
        print(f"❌ Error while disconnecting from {server_name}:", e)

    # Handle any pop-ups
    try:
        wait = WebDriverWait(driver, 50)
        close_popup = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//android.widget.FrameLayout/android.widget.FrameLayout/android.view.View[2]/android.widget.ImageView[1]')))
        close_popup.click()
        print(f"✅ Closed pop-up for {server_name}")
    except Exception as e:
        print(f"❌ No pop-up to close for {server_name}:", e)


# List of servers to test
print("🌐 Checking WireGuard Protocol")
servers = [
    "France", "Indonesia", "South Korea", "Brazil", "Canada",
    "Poland", "United Kingdom", "Germany - 1", "Germany - 2", "Germany - 6",
    "Germany - 7", "Germany - 8", "USA - 1", "USA - 6", "USA - 5",
    "Singapore", "Singapore - 7", "Netherlands - 3", "Netherlands - 1"
]

# Loop through servers
for server in servers:
    connect_disconnect_server(server)

# Quit the driver
driver.quit()
