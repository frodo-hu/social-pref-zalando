// background.js

// Listen for messages from popup or content script
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type === "getPrefs") {
      chrome.storage.local.get(["prefs"], ({ prefs }) => {
        sendResponse({ prefs });
      });
      return true; // indicates async sendResponse
    }
  });