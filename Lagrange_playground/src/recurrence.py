from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist


def flatten_history(history: np.ndarray) -> np.ndarray:                    # Flatten_history takes a time-stack of fields and  
    t = history.shape[0]                                                   # flattens each frame into one long vector-> (73, 160, 160) -> (73, 25600)
    return history.reshape(t, -1)                                          # 73 times stemps and 25,600 values per time steps.
                                                                           # so each row is now one full system state
                                                                           # tradeoff: it preserves time as rows but collapses the spatial structure


                                                                           # This compares every time-state to every other time-state
def recurrence_matrix(history: np.ndarray, epsilon: float = 0.12, metric: str = "euclidean", normalize: bool=True): #epsilon is a distance threshold that decides when 'the state recurs'
    X = flatten_history(history)                                           # we normal all distances by the max distance and we flatten to a 2D state matrix
    D = cdist(X, X, metric=metric)                                         # D is the distance matrix and R the recurrence matrix- we compute pairwaise- b/w X and X rows
    if normalize:                                                          # And here we turn the distance matrix in a 0 to 1 scale and prevent dividing by 0
        D = D / (D.max() + 1e-12)                                          # Building the recurrence boolean matrix: True= close enough, False= too far
    R = (D <= epsilon).astype(float)                                       # R becomes a numeric matrix of recurrence contacts. A rolodex, if you will. 
    return R, D                                                            # Couple gotchas:epsilon- 12% of observed distance is not raw Euclidean dist 
                                                                           # and D = cdist can be expensive but for the current model it'll do just fine. 

def recurrence_density(R: np.ndarray) -> float:                            # We want to know how much of the time-state grid is recurrent... if mostly 0s: low, else 1s: high
    return float(R.mean())                                                 # input is the recurrence matrix, func computes the avg val of all entries in R 
                                                                           # because R contains only 0.0 and 1.0, the mean is the proportion of 1s
                                                                           # super gotcha- the diagonal is always recurrent bc every state is distance 0 from itself. also, stay tuned...

def lag_profile(R: np.ndarray) -> np.ndarray:                              # How recurrent is the whole matrix? 
    n = R.shape[0]                                                         # We create a profile empty output vector of len(n) and fill it with zeros
    lags = np.arange(n)                                                    # And no.diag extracts a diagonal from matrix R and averags that diagonal 
    profile = np.zeros(n)                                                  # Then stores that average at index k and returns the lag profile
    for k in lags:                                                         # so each lag k profile[0] = self recurrence, profile[1] = recurrence one step apart,
        profile[k] = np.mean(np.diag(R, k=k))                              # profile[2] = recurrence two steps apart
    return profile                                                         



