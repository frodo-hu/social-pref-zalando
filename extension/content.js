// extension/content.js

console.log("🛠️ content.js has loaded on", location.href);

(async () => {
  chrome.runtime.sendMessage({ type: "getPrefs" }, ({ prefs }) => {
    if (!prefs) return;

    const { highlightProducts, themeColors } = prefs;

    // 1) Recolor the nav bar (and footer, if you like)
    document.querySelector(".z-nav")?.style.setProperty("background-color", themeColors.primary);
    document.querySelector("footer")?.style.setProperty("background-color", themeColors.secondary);

    // 2) Find the product‐tile container
    const grid =
      document.querySelector(".cat-tiles-root") ||
      document.querySelector("[data-testid='product-grid']") ||
      document.querySelector("main");

    if (!grid) {
      console.log("No product grid found on this page.");
      return;
    }

    // 3) Grab all the <article> cards
    const cards = Array.from(grid.querySelectorAll("article"));
    console.log(`Found ${cards.length} cards; highlighting:`, highlightProducts);

    // 4) For each keyword, find & promote the first matching card
    highlightProducts.forEach(name => {
      const terms = name.toLowerCase().split(/\s+/);
      const match = cards.find(card => {
        const text = card.innerText.toLowerCase();
        return terms.every(t => text.includes(t));
      });

      if (match) {
        grid.prepend(match);
        console.log(`Promoted card matching “${name}”`);
      } else {
        console.log(`No card matched “${name}”`);
      }
    });
  });
})();