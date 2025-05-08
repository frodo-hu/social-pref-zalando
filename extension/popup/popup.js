// extension/popup/popup.js

const connectBtn = document.getElementById("connect");
const refreshBtn = document.getElementById("refresh");

// Step 1: Hit backend to store sandbox token in DB
connectBtn.addEventListener("click", async () => {
  try {
    const resp = await fetch("http://127.0.0.1:8000/users/auth/pinterest");
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const { message } = await resp.json();
    alert(message);  // e.g. "Using sandbox Pinterest token."
    refreshBtn.disabled = false;
  } catch (err) {
    alert("Failed to connect Pinterest: " + err.message);
  }
});

// Step 2: Fetch /preferences and store layout rules
refreshBtn.addEventListener("click", async () => {
  try {
    const resp = await fetch("http://127.0.0.1:8000/preferences/");
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const prefs = await resp.json();
    await chrome.storage.local.set({ prefs });
    alert("Preferences updated!");
  } catch (err) {
    alert("Failed to fetch preferences: " + err.message);
  }
});

// On load, enable Refresh only if prefs exist
chrome.storage.local.get("prefs", ({ prefs }) => {
  refreshBtn.disabled = !prefs;
});