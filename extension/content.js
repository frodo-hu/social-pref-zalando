// extension/content.js
(async () => {
    const resp = await fetch("http://127.0.0.1:8000/preferences/");
    const { highlightProducts, themeColors } = await resp.json();
  
    console.log("Layout rules:", highlightProducts, themeColors);
  
    // 1) Change header/footer colors
    document.querySelector("header")?.style.setProperty("background-color", themeColors.primary);
    document.querySelector("footer")?.style.setProperty("background-color", themeColors.secondary);
  
    // 2) Bring highlighted products to front
    const grid = document.querySelector(".catalog--grid");
    if (grid) {
      const items = Array.from(grid.children);
      highlightProducts.forEach(id => {
        const card = items.find(c => c.dataset.productId === id);
        if (card) {
          grid.prepend(card);
        }
      });
    }
  })();