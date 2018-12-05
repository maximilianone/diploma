import numpy as np
m, n = 3, 4
N = 100  # num samples

rng = np.random.RandomState(42)

W = rng.randn(m, n)
X = rng.randn(n, N)
Z_clean = W.dot(X)

Z = Z_clean + rng.randn(*Z_clean.shape) * .001

W_est = np.linalg.pinv(X.T).dot(Z.T).T

from numpy.testing import assert_array_almost_equal
assert_array_almost_equal(W, W_est, decimal=3)