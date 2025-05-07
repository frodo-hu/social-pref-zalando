# rules_engine/engine.py

from typing import List, Dict
from preferences.model import PreferenceModel

def generate_layout_rules(
    user_embeddings: List[List[float]],
    catalog_embeddings: Dict[str, List[float]],
    top_n: int = 5
) -> Dict:
    """
    Given user and catalog embeddings, select top-N catalog items most similar
    to the user's preference vectors and pick a color theme.
    """
    # 1. Fit a quick KMeans on user_embeddings
    model = PreferenceModel(n_clusters=3)
    model.fit(user_embeddings)

    # 2. Compute similarity between each catalog item and user's cluster centers
    import numpy as np
    centers = model._kmeans.cluster_centers_
    scores = {}
    for prod_id, emb in catalog_embeddings.items():
        emb = np.array(emb)
        # cosine similarity to each center
        sims = np.dot(centers, emb) / (np.linalg.norm(centers, axis=1) * np.linalg.norm(emb))
        scores[prod_id] = sims.max()  # best-match cluster

    # 3. Pick top-N products by score
    top_products = sorted(scores, key=scores.get, reverse=True)[:top_n]

    # 4. Derive a theme color (stub: pick red/green)
    theme = {"primary": "#FF4500", "secondary": "#32CD32"}

    return {
        "highlightProducts": top_products,
        "themeColors": theme
    }