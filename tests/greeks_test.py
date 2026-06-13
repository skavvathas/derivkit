from derivkit import delta, gamma, vega, theta, rho

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print(delta(S, K, T, r, sigma, option_type='call'))
print(gamma(S, K, T, r, sigma))
print(vega(S, K, T, r, sigma))
print(theta(S, K, T, r, sigma, option_type='call'))
print(rho(S, K, T, r, sigma, option_type='call'))