import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Values for mu and sigma
params = [
    (0, 1),   # mu=0, sigma=1
    (2, 1),   # mu=2, sigma=1
    (0, 0.5), # mu=0, sigma=0.5
    (2, 2)    # mu=2, sigma=2
]

x_values = np.linspace(-5, 5, 1000)

for mu, sigma in params:
    y = norm.pdf(x_values, mu, sigma)
    plt.plot(x_values, y, label=f"µ={mu}, σ={sigma}")

plt.title("Normal Distributions")
plt.xlabel("x")
plt.ylabel("Probability Density")
plt.legend()
plt.tight_layout()
plt.savefig("normal_plot.svg", format='svg')
plt.close()
