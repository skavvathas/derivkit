from derivkit import binomial_tree

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print(binomial_tree(S, K, T, r, sigma, n=500, option_type='call'))