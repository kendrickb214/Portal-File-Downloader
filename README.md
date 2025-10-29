# Portal File Downloader

This project contains a Chrome extension that triggers a Python API (using Playwright) to automate website logins and file downloads.

---

## 🧩 Project Structure

```
/api/        → Python Flask API that runs Playwright  
/extension/  → Google Chrome extension frontend
```

---

## 🚀 How to Run the Full Project

### 1. Start the API

1. Navigate to your `/api/` folder in the terminal.

2. Install dependencies:

   ```bash
   poetry install
   ```

   *(This will install Flask, Flask-CORS, and Playwright.)*

3. Install Playwright browsers (one-time setup):

   ```bash
   poetry run playwright install
   ```

4. Run the API:

   ```bash
   poetry run python main.py
   ```

5. You should see a message indicating the server is running:

   ```
   Server running at http://127.0.0.1:8000
   ```

   or

   ```
   Server running at http://localhost:8000
   ```

---

### 2. Use the Chrome Extension

1. Open Chrome and navigate to:

   ```
   chrome://extensions
   ```

2. Enable **Developer mode** (toggle in the top right).

3. Click **Load unpacked** and select your `/extension/` folder.

4. Click the extension icon in your Chrome toolbar.

5. Click **“Start Download.”**

Your extension will now call the running Python API, and you should see the status message update!
