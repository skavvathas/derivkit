from derivkit import vanna, vomma, charm, veta, vera
from derivkit import delta, vega

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print('Vanna:', vanna(S, K, T, r, sigma))
print('Vomma:', vomma(S, K, T, r, sigma))
print('Charm:', charm(S, K, T, r, sigma))
print('Veta :', veta(S, K, T, r, sigma))
print('Vera :', vera(S, K, T, r, sigma))

# Sanity check: compare the analytic second-order Greeks against finite-difference
# approximations of the relevant first-order Greeks.
h = 1e-4

# Vanna = d(Vega)/dS
vanna_fd = (vega(S + h, K, T, r, sigma) - vega(S - h, K, T, r, sigma)) / (2 * h)
# Vomma = d(Vega)/dsigma
vomma_fd = (vega(S, K, T, r, sigma + h) - vega(S, K, T, r, sigma - h)) / (2 * h)
# Charm = d(Delta)/dt = -d(Delta)/dT
charm_fd = -(delta(S, K, T + h, r, sigma) - delta(S, K, T - h, r, sigma)) / (2 * h)
# Veta = d(Vega)/dt = -d(Vega)/dT
veta_fd = -(vega(S, K, T + h, r, sigma) - vega(S, K, T - h, r, sigma)) / (2 * h)
# Vera = d(Vega)/dr
vera_fd = (vega(S, K, T, r + h, sigma) - vega(S, K, T, r - h, sigma)) / (2 * h)

assert abs(vanna(S, K, T, r, sigma) - vanna_fd) < 1e-4, 'vanna mismatch'
assert abs(vomma(S, K, T, r, sigma) - vomma_fd) < 1e-3, 'vomma mismatch'
assert abs(charm(S, K, T, r, sigma) - charm_fd) < 1e-4, 'charm mismatch'
assert abs(veta(S, K, T, r, sigma) - veta_fd) < 1e-3, 'veta mismatch'
assert abs(vera(S, K, T, r, sigma) - vera_fd) < 1e-3, 'vera mismatch'

print('All second-order Greeks match finite-difference checks.')
