import requests
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# HEADSPIN CONFIGURATION
# ============================================================

HS_API_SERVER = "https://api-dev.headspin.io"

# IMPORTANT:
# Replace this with your newly rotated HeadSpin token.
TOKEN = "191cd7d19e0e4034992ac4dabf14d573"

DEVICE_ID = "17081HFDD2699Y"

HEADSPIN_WEBDRIVER_URL = (
    "https://dev-us-sny-9.headspin.io:7028/"
    "v0/e70f41cd904c4a3998fde1d73a13c947/wd/hub"
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_PACKAGE = "com.example.firecatalog"

APP_ACTIVITY = "com.example.firecatalog.MainActivity"


# ============================================================
# LOCK DEVICE
# ============================================================

def lock_device(
    token: str,
    device_id: str,
    *,
    automation: bool = False,
    api_server: str = HS_API_SERVER
) -> requests.Response:

    api_url = f"{api_server}/v0/devices/lock"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "device_id": device_id
    }

    params = {}

    if automation:
        params["automation"] = True

    response = requests.post(
        api_url,
        headers=headers,
        json=data,
        params=params
    )

    return response


# ============================================================
# START CAPTURE SESSION
# ============================================================

def start_capture_session(
    token: str,
    device_id: str,
    *,
    api_server: str = HS_API_SERVER
) -> requests.Response:

    api_url = f"{api_server}/v0/sessions"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "session_type": "capture",
        "allow_replace": True,
        "device_id": device_id,
        "network_capture": False,
        "capture_network": False
    }

    response = requests.post(
        api_url,
        headers=headers,
        json=data
    )

    return response


# ============================================================
# STOP CAPTURE SESSION
# ============================================================

def stop_capture_session(
    token: str,
    session_id: str,
    *,
    api_server: str = HS_API_SERVER
) -> requests.Response:

    api_url = f"{api_server}/v0/sessions/{session_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "active": False
    }

    response = requests.patch(
        api_url,
        headers=headers,
        json=data
    )

    return response


# ============================================================
# UNLOCK DEVICE
# ============================================================

def unlock_device(
    token: str,
    device_id: str,
    *,
    api_server: str = HS_API_SERVER
) -> requests.Response:

    api_url = f"{api_server}/v0/devices/unlock"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "device_id": device_id
    }

    response = requests.post(
        api_url,
        headers=headers,
        json=data
    )

    return response


# ============================================================
# APPIUM AUTOMATION
# ============================================================

def run_appium_test():

    driver = None

    try:

        # ====================================================
        # CONFIGURE APPIUM
        # ====================================================

        print()
        print("----------------------------------------")
        print("Configuring Appium...")
        print("----------------------------------------")

        options = UiAutomator2Options()

        options.platform_name = "Android"

        options.automation_name = "UiAutomator2"

        options.device_name = "Chromecast"

        options.udid = DEVICE_ID

        options.app_package = APP_PACKAGE

        options.app_activity = APP_ACTIVITY

        options.intent_action = "android.intent.action.MAIN"
        options.intent_category = "android.intent.category.LEANBACK_LAUNCHER"

        options.no_reset = True

        # Do not automatically launch the application.
        options.auto_launch = True

        options.new_command_timeout = 300

        # ====================================================
        # CONNECT TO HEADSPIN WEBDRIVER
        # ====================================================

        print()
        print("----------------------------------------")
        print("Connecting to HeadSpin WebDriver...")
        print("----------------------------------------")

        driver = webdriver.Remote(
            command_executor=HEADSPIN_WEBDRIVER_URL,
            options=options
        )

        print()
        print("Connected to HeadSpin device.")
        print("Appium session started.")

        # ====================================================
        # PRINT SESSION ID
        # ====================================================

        print()
        print("----------------------------------------")
        print("Appium Session Information")
        print("----------------------------------------")

        print(
            f"Appium Session ID: {driver.session_id}"
        )

        if not driver.session_id:

            raise Exception(
                "Appium session ID is empty."
            )

        # ====================================================
        # LAUNCH APPLICATION
        # ====================================================

        print()
        print("----------------------------------------")
        print("Launching FireCatalog application...")
        print("----------------------------------------")

        print(
            f"Package: {APP_PACKAGE}"
        )

        print(
            f"Activity: {APP_ACTIVITY}"
        )

        # FireCatalog is an Android TV application.
        # It uses LEANBACK_LAUNCHER.
        #
        # Therefore explicitly start the activity
        # instead of using activate_app().



        print()
        print(
            "FireCatalog application launched successfully."
        )

        # ====================================================
        # WAIT FOR APPLICATION
        # ====================================================

        print()
        print(
            "Waiting for FireCatalog application "
            "to load..."
        )

        time.sleep(3)

        # ====================================================
        # CHECK SESSION
        # ====================================================

        print()
        print("----------------------------------------")
        print("Checking Appium session...")
        print("----------------------------------------")

        print(
            f"Current Appium Session ID: "
            f"{driver.session_id}"
        )

        # ====================================================
        # WAIT FOR APPLICATION ELEMENTS
        # ====================================================

        wait = WebDriverWait(
            driver,
            20
        )

        # ====================================================
        # VERIFY TITLE
        # ====================================================

        print()
        print("Verifying application title...")

        title_xpath = (
            '//android.widget.TextView'
            '[@resource-id="com.example.firecatalog:id/title_text"]'
        )

        title_element = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    title_xpath
                )
            )
        )

        title = title_element.text

        print()
        print(
            f"Title: {title}"
        )

        print(
            "PASS: Title is displayed."
        )

        # ====================================================
        # CLICK KITCHEN
        # ====================================================

        print()
        print("Clicking Kitchen...")

        kitchen_xpath = (
            '//android.widget.TextView'
            '[@resource-id="com.example.firecatalog:id/row_header" '
            'and @text="Kitchen"]'
        )

        kitchen = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    kitchen_xpath
                )
            )
        )

        kitchen.click()

        print(
            "Kitchen clicked successfully."
        )

        # ====================================================
        # CLICK HOME
        # ====================================================

        print()
        print("Clicking Home...")

        home_xpath = (
            '//android.widget.TextView'
            '[@resource-id="com.example.firecatalog:id/row_header" '
            'and @text="Home"]'
        )

        home = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    home_xpath
                )
            )
        )

        home.click()

        print(
            "Home clicked successfully."
        )

        # ====================================================
        # TEST PASSED
        # ====================================================

        print()
        print("========================================")
        print("APPIUM TEST PASSED")
        print("========================================")

        return True

    except Exception as e:

        # ====================================================
        # TEST FAILED
        # ====================================================

        print()
        print("========================================")
        print("APPIUM TEST FAILED")
        print("========================================")

        print(
            f"Error: {e}"
        )

        # ====================================================
        # SAVE FAILURE SCREENSHOT
        # ====================================================

        if driver:

            try:

                print()
                print(
                    "Attempting to save failure screenshot..."
                )

                driver.save_screenshot(
                    "firecatalog_failure.png"
                )

                print(
                    "Failure screenshot saved: "
                    "firecatalog_failure.png"
                )

            except Exception as screenshot_error:

                print(
                    "Could not save screenshot: "
                    f"{screenshot_error}"
                )

        return False

    finally:

        # ====================================================
        # CLOSE APPIUM SESSION
        # ====================================================

        if driver:

            try:

                print()
                print(
                    "Closing Appium session..."
                )

                driver.quit()

                print(
                    "Appium session closed."
                )

            except Exception as e:

                print(
                    "Error while closing "
                    f"Appium session: {e}"
                )


# ============================================================
# MAIN EXECUTION FLOW
# ============================================================

def main():

    session_id = None

    device_locked = False

    test_passed = False

    try:

        # ====================================================
        # STEP 1: LOCK DEVICE
        # ====================================================

        print()
        print("========================================")
        print("STEP 1: LOCK DEVICE")
        print("========================================")

        lock_response = lock_device(
            TOKEN,
            DEVICE_ID,
            automation=True
        )

        print(
            f"Lock response: "
            f"{lock_response.status_code}"
        )

        lock_response.raise_for_status()

        device_locked = True

        print()
        print(
            "Device locked successfully."
        )

        # ====================================================
        # STEP 2: START CAPTURE SESSION
        # ====================================================

        print()
        print("========================================")
        print("STEP 2: START CAPTURE SESSION")
        print("========================================")

        session_response = start_capture_session(
            TOKEN,
            DEVICE_ID
        )

        print(
            f"Capture response: "
            f"{session_response.status_code}"
        )

        session_response.raise_for_status()

        # ====================================================
        # GET SESSION ID
        # ====================================================

        session_data = session_response.json()

        session_id = session_data.get(
            "session_id"
        )

        if not session_id:

            raise Exception(
                "Capture session started but "
                "no session_id was returned."
            )

        print()
        print(
            "Capture session started successfully."
        )

        print(
            f"Session ID: {session_id}"
        )

        # ====================================================
        # STEP 3: RUN APPIUM AUTOMATION
        # ====================================================

        print()
        print("========================================")
        print("STEP 3: RUN APPIUM AUTOMATION")
        print("========================================")

        print()
        print(
            "Capture session is active."
        )

        print(
            "Starting Appium automation..."
        )

        test_passed = run_appium_test()

        # ====================================================
        # CHECK TEST RESULT
        # ====================================================

        if test_passed:

            print()
            print(
                "Appium automation completed "
                "successfully."
            )

        else:

            print()
            print(
                "Appium automation completed "
                "with failures."
            )

    except Exception as e:

        # ====================================================
        # AUTOMATION FLOW ERROR
        # ====================================================

        print()
        print("========================================")
        print("AUTOMATION FLOW FAILED")
        print("========================================")

        print(
            f"Error: {e}"
        )

    finally:

        # ====================================================
        # STEP 4: STOP CAPTURE SESSION
        # ====================================================

        if session_id:

            print()
            print("========================================")
            print("STEP 4: STOP CAPTURE SESSION")
            print("========================================")

            try:

                stop_response = stop_capture_session(
                    TOKEN,
                    session_id
                )

                print(
                    f"Stop session response: "
                    f"{stop_response.status_code}"
                )

                stop_response.raise_for_status()

                print()
                print(
                    "Capture session stopped successfully."
                )

            except Exception as e:

                print(
                    "Failed to stop capture session: "
                    f"{e}"
                )

        else:

            print()
            print(
                "No capture session ID available."
            )

            print(
                "Skipping capture session stop."
            )

        # ====================================================
        # STEP 5: UNLOCK DEVICE
        # ====================================================

        if device_locked:

            print()
            print("========================================")
            print("STEP 5: UNLOCK DEVICE")
            print("========================================")

            try:

                unlock_response = unlock_device(
                    TOKEN,
                    DEVICE_ID
                )

                print(
                    f"Unlock response: "
                    f"{unlock_response.status_code}"
                )

                unlock_response.raise_for_status()

                print()
                print(
                    "Device unlocked successfully."
                )

            except Exception as e:

                print(
                    "Failed to unlock device: "
                    f"{e}"
                )

        else:

            print()
            print(
                "Device was not locked."
            )

            print(
                "Skipping device unlock."
            )

        # ====================================================
        # FINAL RESULT
        # ====================================================

        print()
        print("========================================")
        print("HEADSPIN AUTOMATION FLOW COMPLETED")
        print("========================================")

        if test_passed:

            print(
                "Final Result: PASS"
            )

        else:

            print(
                "Final Result: FAIL"
            )


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()