import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# --- Credentials for the public test website ---
# This is what I'm using for now to test the code until I get the real information
LOGIN_URL = "https://the-internet.herokuapp.com/login"
DOWNLOADS_URL = "https://the-internet.herokuapp.com/download"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
FILE_TO_DOWNLOAD = "some-file.txt"
# Save the file inside this API's directory
DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloaded_file.txt")

# --- Flask App Setup ---
app = Flask(__name__)

# It allows requests from any origin.
CORS(app)

# We use the SYNC version of Playwright, which is better for Flask.
def run_automation_task():
    """
    Runs the full login and download automation task.
    Returns True on success, False on failure.
    """
    with sync_playwright() as p:
        browser = None
        try:
            print("API: Launching browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 1. LOGIN
            print("API: Navigating to login page...")
            page.goto(LOGIN_URL)
            
            print("API: Filling in login form...")
            page.get_by_label("Username").fill(USERNAME)
            page.get_by_label("Password").fill(PASSWORD)
            page.get_by_role("button", name="Login").click()
            
            # 2. VERIFY LOGIN
            print("API: Verifying login success...")
            # Wait for the success message to appear (default 5-second timeout)
            success_message = page.get_by_text("You logged into a secure area!")
            success_message.wait_for(state="visible")
            print("API: Login successful!")
            
            # 3. NAVIGATE TO DOWNLOAD
            print("API: Navigating to download page...")
            page.goto(DOWNLOADS_URL)
            
            # 4. DOWNLOAD FILE
            print("API: Waiting to download file...")
            
            # Start a listener for the download event AND trigger the click
            with page.expect_download() as download_info:
                page.get_by_text(FILE_TO_DOWNLOAD).click()
            
            download = download_info.value
            
            # Save the file
            download.save_as(DOWNLOAD_PATH)
            
            print(f"API: Successfully downloaded file to {DOWNLOAD_PATH}")
            return True

        except PlaywrightError as e:
            print(f"API Error: An error occurred during automation: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"API Error: A general error occurred: {e}", file=sys.stderr)
            return False
        finally:
            if browser:
                print("API: Closing browser.")
                browser.close()

@app.route("/download", methods=["POST"])
def trigger_download():
    """
    This is the endpoint your Chrome extension will call.
    """
    print("API: /download endpoint called")
    
    try:
        success = run_automation_task()
        
        if success:
            # This JSON response is sent back to popup.js
            return jsonify({
                "message": "Download successful!",
                "file_path": DOWNLOAD_PATH
            }), 200
        else:
            return jsonify({
                "message": "Automation failed. Check API logs."
            }), 500
            
    except Exception as e:
        print(f"API Error: Failed to run task: {e}", file=sys.stderr)
        return jsonify({
            "message": "An internal server error occurred."
        }), 500

# --- Run the App ---
if __name__ == "__main__":
    # Runs the Flask server on http://localhost:8000
    # The extension (popup.js) is configured to call this exact address.
    app.run(host="0.0.0.0", port=8000, debug=True)
