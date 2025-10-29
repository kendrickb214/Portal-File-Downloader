import asyncio
import os
from playwright.async_api import async_playwright, expect

# --- Credentials for the public test website ---
LOGIN_URL = "https://the-internet.herokuapp.com/login"
DOWNLOADS_URL = "https://the-internet.herokuapp.com/download"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
FILE_TO_DOWNLOAD = "some-file.txt"
DOWNLOAD_PATH = os.path.join(os.getcwd(), "my_downloaded_file.txt")


async def main():
    """
    Main function to run the automation task.
    """
    async with async_playwright() as p:
        browser = None
        try:
            print("Launching browser...")
            # We launch in non-headless mode (headless=False) and add a
            # slow_mo so you can see what's happening.
            browser = await p.chromium.launch(headless=False, slow_mo=500)
            
            page = await browser.new_page()
            
            # --- 1. LOGIN ---
            print(f"Navigating to login page: {LOGIN_URL}")
            await page.goto(LOGIN_URL)
            
            print("Filling in login form...")
            # Use 'get_by_label' for form fields, it's very reliable.
            await page.get_by_label("Username").fill(USERNAME)
            await page.get_by_label("Password").fill(PASSWORD)
            
            # Use 'get_by_role' for buttons.
            await page.get_by_role("button", name="Login").click()
            
            # --- 2. VERIFY LOGIN ---
            print("Verifying login success...")
            # We wait for the success message to appear.
            # 'expect' will wait automatically for a few seconds.
            success_message = page.get_by_text("You logged into a secure area!")
            await expect(success_message).to_be_visible()
            print("Login successful!")
            
            # --- 3. NAVIGATE TO DOWNLOAD ---
            print(f"Navigating to download page: {DOWNLOADS_URL}")
            await page.goto(DOWNLOADS_URL)
            
            # --- 4. DOWNLOAD FILE ---
            print(f"Waiting to download file: {FILE_TO_DOWNLOAD}...")
            
            # This is the key:
            # 1. Start a "listener" for the download event.
            # 2. Perform the action that triggers the download.
            async with page.expect_download() as download_info:
                # Click the link for the file we want
                await page.get_by_text(FILE_TO_DOWNLOAD).click()
            
            # Wait for the download_info to be populated
            download = await download_info.value
            
            # Save the file to our desired path
            await download.save_as(DOWNLOAD_PATH)
            
            print("-" * 30)
            print(f"Successfully downloaded file!")
            print(f"Saved to: {DOWNLOAD_PATH}")
            print("-" * 30)

        except Exception as e:
            print(f"An error occurred: {e}")
            
        finally:
            if browser:
                print("Closing browser.")
                await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
