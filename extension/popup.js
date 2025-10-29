// This is the URL where your Python API will be running.
// You MUST update this when you deploy to production.
const API_URL = "http://localhost:8000/download";

// Wait for the popup's HTML content to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  
  // Get references to the button and the status message element
  const downloadButton = document.getElementById("downloadButton");
  const statusMessage = document.getElementById("statusMessage");

  // Add a click listener to the button
  downloadButton.addEventListener("click", () => {
    
    // 1. Give immediate feedback to the user
    statusMessage.textContent = "Connecting to API...";
    statusMessage.style.color = "#555";
    downloadButton.disabled = true; // Disable the button

    // 2. Call the Python API using the fetch() function
    fetch(API_URL, { method: "POST" })
      .then(response => {
        // Check if the server responded successfully
        if (!response.ok) {
          // If the server response was an error (e.g., 500)
          throw new Error(`API Error: ${response.statusText}`);
        }
        return response.json(); // Parse the JSON response from the server
      })
      .then(data => {
        // 3. Show a success message from the API
        // We assume the API sends back: {"message": "Download successful!"}
        console.log("Success:", data);
        statusMessage.textContent = data.message || "Success!";
        statusMessage.style.color = "green";
      })
      .catch(error => {
        // 4. Show an error message if the fetch failed
        console.error("Error:", error);
        statusMessage.textContent = "Error: Could not connect to API.";
        statusMessage.style.color = "red";
      })
      .finally(() => {
        // 5. Re-enable the button whether it succeeded or failed
        downloadButton.disabled = false;
      });
  });
});
