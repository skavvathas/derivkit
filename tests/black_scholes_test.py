from derivkit import black_scholes, delta, gamma, vega, binomial_tree, max_drawdown

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print('Black-Scholes Price:', black_scholes(S, K, T, r, sigma, option_type='call'))
print('d1:', d1(S, K, T, r, sigma))
print('d2:', d2(S, K, T, r, sigma))
