import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.widgets import Slider, Button

# Initial parameter values
S0_init = 100
K_init = 105
T_init = 1
r = 0.05
sigma_init = 0.2
num_simulations_init = 5000
time_steps_init = 100

def calculate_option_prices(S0, K, T, sigma, num_simulations, time_steps):
    dt = T / time_steps
    call_payoffs = []
    put_payoffs = []
    simulated_paths = []

    # Monte Carlo simulation
    for _ in range(int(num_simulations)):
        S = S0
        path = [S]
        for _ in range(int(time_steps)):
            Z = np.random.normal()
            S = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)
            path.append(S)
        call_payoffs.append(max(S - K, 0))
        put_payoffs.append(max(K - S, 0))
        simulated_paths.append(path)

    mc_call_price = np.exp(-r * T) * np.mean(call_payoffs)
    mc_put_price = np.exp(-r * T) * np.mean(put_payoffs)
    bs_call_price = black_scholes_call(S0, K, T, r, sigma)
    bs_put_price = black_scholes_put(S0, K, T, r, sigma)

    return mc_call_price, mc_put_price, bs_call_price, bs_put_price, simulated_paths

# Black-Scholes formulas
def black_scholes_call(S0, K, T, r, sigma):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def black_scholes_put(S0, K, T, r, sigma):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

# Update function to recalculate and display results
def update_prices(event=None):
    S0 = s_S0.val
    K = s_K.val
    T = s_T.val
    sigma = s_sigma.val
    num_simulations = s_num_simulations.val
    time_steps = s_time_steps.val

    # Recalculate option prices
    mc_call, mc_put, bs_call, bs_put, simulated_paths = calculate_option_prices(S0, K, T, sigma, num_simulations, time_steps)

    # Clear and plot new paths
    ax.clear()
    for path in simulated_paths[:50]:
        ax.plot(np.linspace(0, T, int(time_steps) + 1), path, lw=0.8, alpha=0.5)

    ax.axhline(y=K, color='red', linewidth=0.5, linestyle='--', label=f'Strike Price (K) = {K}')
    ax.set_title('Simulated Asset Price Paths')
    ax.set_xlabel('Time to Expiration (Years)')
    ax.set_ylabel('Asset Price')
    ax.legend()
    ax.grid(True)

    # Calculate errors
    call_error = mc_call - bs_call
    put_error = mc_put - bs_put

    # Update text box with prices and error
    text_box.set_text(f"Black-Scholes Call Price: {bs_call:.2f}\n"
                      f"Black-Scholes Put Price: {bs_put:.2f}\n"
                      f"Monte Carlo Call Price: {mc_call:.2f} (Error: {call_error:.2f})\n"
                      f"Monte Carlo Put Price: {mc_put:.2f} (Error: {put_error:.2f})")

# Initial plot setup
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.05, bottom=0.45)

# Sliders for each parameter
ax_S0 = plt.axes([0.1, 0.3, 0.65, 0.03])
ax_K = plt.axes([0.1, 0.25, 0.65, 0.03])
ax_T = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_sigma = plt.axes([0.1, 0.15, 0.65, 0.03])
ax_num_simulations = plt.axes([0.1, 0.1, 0.65, 0.03])
ax_time_steps = plt.axes([0.1, 0.05, 0.65, 0.03])

# Slider creation
s_S0 = Slider(ax_S0, 'S0 (Spot Price)', 50, 150, valinit=S0_init)
s_K = Slider(ax_K, 'K (Strike Price)', 50, 150, valinit=K_init)
s_T = Slider(ax_T, 'T (Time)', 0.5, 3.0, valinit=T_init)
s_sigma = Slider(ax_sigma, 'Volatility (σ)', 0.1, 0.5, valinit=sigma_init)
s_num_simulations = Slider(ax_num_simulations, 'Num Simulations', 100, 10000, valinit=num_simulations_init, valstep=100)
s_time_steps = Slider(ax_time_steps, 'Time Steps', 10, 500, valinit=time_steps_init, valstep=10)

# Apply button for recalculating option prices
apply_ax = plt.axes([0.8, 0.02, 0.1, 0.04])
apply_button = Button(apply_ax, 'Apply', color='lightblue', hovercolor='lightgreen')
apply_button.on_clicked(update_prices)

# Display initial option prices and error
mc_call, mc_put, bs_call, bs_put, simulated_paths = calculate_option_prices(S0_init, K_init, T_init, sigma_init, num_simulations_init, time_steps_init)
for path in simulated_paths[:50]:
    ax.plot(np.linspace(0, T_init, time_steps_init + 1), path, lw=0.8, alpha=0.5)

text_box = plt.text(0.85, 0.5, '', transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
update_prices()  # Now this runs after sliders are defined

plt.show()


