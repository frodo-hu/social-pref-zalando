# preferences/model.py

from sklearn.cluster import KMeans
import numpy as np

class PreferenceModel:
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self._kmeans = KMeans(n_clusters=n_clusters)

    def fit(self, embeddings: list[list[float]]):
        """
        Fit KMeans on a list of embeddings.
        """
        X = np.array(embeddings)
        self._kmeans.fit(X)

    def predict(self, embeddings: list[list[float]]) -> list[int]:
        """
        Assign each embedding to a cluster.
        """
        X = np.array(embeddings)
        return self._kmeans.predict(X)

    def top_clusters(self, embeddings: list[list[float]], top_n: int = 3) -> list[int]:
        """
        Return the most frequent clusters among embeddings.
        """
        labels = self.predict(embeddings)
        # count frequency
        counts = np.bincount(labels, minlength=self.n_clusters)
        # get top indices
        return list(np.argsort(counts)[-top_n:][::-1])