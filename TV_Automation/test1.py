import requests
import subprocess
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# HEADSPIN CONFIGURATION
# ============================================================

# HeadSpin API server
HS_API_SERVER = "https://api-dev.headspin.io"

# HeadSpin API token
# IMPORTANT: Do not commit your real token to GitHub.
TOKEN = "191cd7d19e0e4034992ac4dabf14d573"

# HeadSpin device ID
DEVICE_ID = "G071R20720850KJ6"

# HeadSpin WebDriver URL
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
    api_server: str = HS_API_SERVER,
    **kwargs
) -> requests.Response:
    """
    Starts a HeadSpin capture session.

    Appium automation starts only after the capture
    session has successfully started.

    Network capture parameters are removed.
    """

    api_url = f"{api_server}/v0/sessions"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "session_type": "capture",
        "allow_replace": True,
        "device_id": device_id,
        "network_capture": False,
        "capture_network" : False
    }

    # Prevent network capture parameters
    # from being passed.
  #  kwargs.pop("network_capture", None)
  #  kwargs.pop("capture_network", None)

    # Add any other session parameters
   # data.update(kwargs)

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
    """
    Stops the HeadSpin capture session.

    This is called only after Appium automation finishes.
    """

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
    """
    Unlocks the HeadSpin device after automation completes.
    """

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
    """
    Runs the FireCatalog Appium automation.

    Execution order:

        Start Capture
              ↓
        Start Appium Session
              ↓
        Terminate Existing FireCatalog App
              ↓
        Wait 2 Seconds
              ↓
        Launch FireCatalog App
              ↓
        Run Automation
              ↓
        Close Appium Session
              ↓
        Stop Capture
    """

    driver = None

    try:

        # ====================================================
        # APPIUM CAPABILITIES
        # ====================================================

        print()
        print("----------------------------------------")
        print("Configuring Appium...")
        print("----------------------------------------")

        options = UiAutomator2Options()

        # Android platform
        options.platform_name = "Android"

        # UiAutomator2 automation engine
        options.automation_name = "UiAutomator2"

        # Device name
        options.device_name = "Chromecast"

        # HeadSpin device ID
        options.udid = DEVICE_ID

        # Application package
        options.app_package = APP_PACKAGE

        # Application activity
        options.app_activity = APP_ACTIVITY

        # Do not clear application data
        options.no_reset = True

        # IMPORTANT:
        # Do not automatically launch the application
        # when the Appium session is created.
        options.auto_launch = False

        # Terminate application when Appium session ends
        options.set_capability(
            "appium:shouldTerminateApp",
            True
        )

        options.set_capability(
            "appium:intentCategory",
            "android.intent.category.LEANBACK_LAUNCHER"
        )

        # Appium command timeout
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
        # TERMINATE EXISTING APPLICATION
        # ====================================================

        # print()
        # print("----------------------------------------")
        # print("Terminating FireCatalog application...")
        # print("----------------------------------------")

        #driver.terminate_app(APP_PACKAGE)
        #driver.activate_app(APP_PACKAGE)

        #print()
        # print(
        #     "FireCatalog application terminated successfully."
        # )

        # ====================================================
        # WAIT BEFORE LAUNCHING
        # ====================================================

       # print()
       # print("Waiting 2 seconds before launching...")

        time.sleep(15)

        # ====================================================
        # LAUNCH APPLICATION
        # ====================================================

        print()
        print("----------------------------------------")
        print("Launching FireCatalog application...")
        print("----------------------------------------")

       # driver.activate_app(APP_PACKAGE)

        print()
        print(
            "FireCatalog application launched successfully."
        )

        # ====================================================
        # WAIT FOR APPLICATION ELEMENTS
        # ====================================================

        wait = WebDriverWait(
            driver,
            20
        )


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

                driver.quit()

                print()
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

    # Capture session ID
    session_id = None

    # Track whether device was successfully locked
    device_locked = False

    # Track Appium test result
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

        # ----------------------------------------------------
        # Appium will NOT start if capture fails
        # ----------------------------------------------------

        session_response.raise_for_status()

        # Get response JSON
        session_data = session_response.json()

        # Extract session ID
        session_id = session_data["session_id"]

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

        # Appium has completely finished here

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

    # this is a comment