from greeks import delta_call, gamma, vega

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print(delta_call(S, K, T, r, sigma))
print(gamma(S, K, T, r, sigma))
print(vega(S, K, T, r, sigma))