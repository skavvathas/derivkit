from derivkit import black_scholes, delta, gamma, vega, binomial_tree, max_drawdown

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print(black_scholes(S, K, T, r, sigma, option_type='call'))
print(delta(S, K, T, r, sigma, option_type='call'))
print(gamma(S, K, T, r, sigma))
print(vega(S, K, T, r, sigma))
print(binomial_tree(S, K, T, r, sigma, n=500, option_type='call'))
print(max_drawdown([100, 120, 90, 110, 80, 130]))
