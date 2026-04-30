from __future__ import annotations

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import eigh

def delay_embedding(series: np.ndarray, dim: int = 3, tau: int = 2) -> np.ndarray:      # This is for a 1D time series the delay embedding  constructs points
    series = np.asarray(series, dtype=float)                                            # whose coordinates are lagged versions of the same series
    n = len(series) - (dim -1) * tau                                                    # computes how many complete lagged vectors one can make without running off the end
    if n <= 0:                                                                          # τ (tau)-> the delay interval b/w coordinates
        raise ValueError("series too short for requested embedding")                    # tau is carrying the job of 'time separation' by answering:
                                                                                        # when I step from one coordinate to the next, how many time steps do I skip?
    return np.column_stack([                                                            # here we're building the delayed columns and staking them side by side
        series[i:i + n]                                                                 # output shape = rows-> # of valid embedded points
        for i in range(0, dim * tau, tau)                                               # and columns-> embedding dimension
    ])

def classical_mds(X: np.ndarray, n_components: int = 3)-> np.ndarray:                   # The Geometry Engine: takes a matrix of observations and says:
    D = squareform(pdist(X, metric="euclidean"))                                        # this computes a pairwise distance matrix between all rows of X
    n = D.shape[0]                                                                      # here we are just calling for the first value of the shape tuple which gives us the legth of the axis
                                                                                        # And so just like a license plate that reads: Golf 'Are'- 
    J = np.eye(n) - np.ones((n, n)) /n                                                  # we have the, 'Eye'-dentity Matrix and we take our Jungian
    B = -0.5 * J @ (D ** 2) @ J                                                         # matrix of the mind and mult by the matrix of experience. transposed
                                                                                        # This in PCA in a different outfit- from pairwise distances first 
    vals, vecs = eigh(B)                                                                # then we make magic with eigendecomposition, keeping the principle directions,
    idx = np.argsort(vals)[::-1]                                                        # and then she's off to the low-dimensional ball
    vals = vals[idx][:n_components]                                                     # taking the matrix of e-vectors, we scale it column-wise
    vecs = vecs[:, idx][:, :n_components]                                               # by the sqrt of each eigenvalue
    vals = np.clip(vals, 0, None)                                                       # clip negatives and set them to zero so we don't break anyting
    return vecs * np.sqrt(vals)                                                         # and then ship it

def state_space_from_history(history: np.ndarray, n_components: int = 3)->np.ndarray:   # We reshape 'history' such that we take the first dimension
    X = history.reshape(history.shape[0], -1)                                           # and flatten everything else into one long diemnsion
    return classical_mds(X, n_components=n_components)                                  # so (t, r, c) -> (t, rc) - The universe of being has to invest in the 
                                                                                        # universe of becoming to be more than it was.
