import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import norm

#Parameters 
S0 = 100 # Initial asset price 
K = 105 # Strike price 
T = 1 # Time to expiration (1 year) 
r = 0.05 # Risk-free rate 
sigma = 0.2 # Volatility (asset price fluctuation)
num_simulations = 1000 #possible price paths
time_steps = 100 #Intervals in each simulation/paths. More steps = finer detail

#SIMULATE RANDOM PRICE PATHS
dt = T/time_steps #time to expiration/no. time steps (change in time or time step)
call_payoffs = [] #Difference between strike price and market value of asset at expiration 
put_payoffs = []

#Store simulated asset price paths for visualisation 
simulated_paths = []

#MONTE CARLO SIMULATION
#Loop through simulations
for _ in range(num_simulations): 
    S = S0 #for each simulation reset S to initial asset price
    path = [S] #Store asset price at each time step for path

    for _ in range(time_steps): #loop through steps in simulation to create price path of random price movements (GBM). Repeat until expiration date T, creating complete simulated price path for asset
        Z = np.random.normal() #Random variable from normal dist. (randomness)
        S = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z) 
        path.append(S) #Store asset price at each step
        #Assign asset price for each time step in path

    #Calculates payoff for each simulation
    call_payoffs.append(max(S - K, 0)) #call option payoff; Current - Strike. Want strike price to be lower to be ITM (below current price)
    put_payoffs.append(max(K - S, 0)) #put option payoff

    #append current path simulation to list of simulated paths
    simulated_paths.append(path)

#BLACK SCHOLES
def black_scholes_call(S0, K, T, r, sigma): 
    d1 = (np.log(S0/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T) 
    call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S0, K, T, r, sigma): 
    d1 = (np.log(S0/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T) 
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    return put_price

#Calculate option price
mc_call_price = np.exp(-r * T) * np.mean(call_payoffs) 
mc_put_price = np.exp(-r * T) * np.mean(put_payoffs)
bs_call_price = black_scholes_call(S0, K, T, r, sigma)
bs_put_price = black_scholes_put(S0, K, T, r, sigma)

print(f"Black-Scholes Call Option Price:  {bs_call_price:.2f}")
print(f"Black-Scholes Put Option Price:  {bs_put_price:.2f}")

print(f"Monte Carlo Call Option Price: {mc_call_price:.2f}")
print(f"Monte Carlo Put Option Price: {mc_put_price:.2f}")

#PLOTTING
plt.figure(figsize=(12, 6)) 
for i in range(num_simulations):
    #Plots i'th simulated asset price path. X-axis is time from 0 to expiration T, y-axis asset price. Lw = line width, alpha = transparency
    #np.linspace generates array of time_steps + 1, evenly spaced values between 0 and T, representing time points at which the asset is simulated
    plt.plot(np.linspace(0, T, time_steps + 1), simulated_paths[i], lw=0.8, alpha=0.7) 

# Title and labels
plt.title('Simulated Asset Price Paths') 
plt.xlabel('Time to Expiration (Years)') 
plt.ylabel('Asset Price')
plt.grid(True)

# Add bold line at strike price (K)
plt.axhline(y=K, color='red', linewidth=0.5, linestyle='--', label=f'Strike Price (K) = {K}')

# Add text label for K (strike price)
plt.text(T + 0.048, K, 'K', color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='right', fontweight='bold')

# Define table data with 'Constants' and 'Values'
constants_table_data = [
    ['S0 (Spot Price)', f'{S0}'],
    ['K (Strike Price)', f'{K}'],
    ['T (Time to Expiration)', f'{T}'],
    ['R (Risk-Free Rate)', f'{r}'],
    ['σ (Volatility)', f'{sigma}'],
    ['Simulations', f'{num_simulations}'],
    ['Time Steps', f'{time_steps}']
]

# Add the constants table to the plot window
constants_table = plt.table(
    cellText=constants_table_data,
    colLabels=['Constants', 'Values'],
    cellLoc='center',
    loc='upper left',  # Position it in the upper left corner
    colColours=['#f5f5f5']*2,
    cellColours=[['#f5f5f5']*2]*7,  # Adjust this to match the number of rows
    bbox=[1.03, 0.50, 0.35, 0.3]  # Adjust position: [x0, y0, width, height]
)

# Adjust font size for the constants table
constants_table.auto_set_font_size(False)
constants_table.set_fontsize(8)  # Set the font size for the constants table text

# Auto-adjust column widths for constants table
constants_table.auto_set_column_width([0, 1, 2])   # Auto-adjust column widths for a neat look

# Calculate the accuracy of Monte Carlo to Black-Scholes
call_accuracy = abs(mc_call_price - bs_call_price) / bs_call_price * 100  # Percentage error for call option
put_accuracy = abs(mc_put_price - bs_put_price) / bs_put_price * 100  # Percentage error for put option

# Table data
table_data = [
    ['Call Option Price', f'{bs_call_price:.2f}', f'{mc_call_price:.2f}'],
    ['Put Option Price', f'{bs_put_price:.2f}', f'{mc_put_price:.2f}']
]

# Define custom cell colors
cell_colours = [
    ['#90EE90', '#90EE90', '#90EE90'],  # Green for Call Option Price
    ['#FF6347', '#FF6347', '#FF6347']   # Red for Put Option Price
]

# Add the table to the plot window
table = plt.table(
    cellText=table_data,
    colLabels=['Option Type', 'Black-Scholes', 'Monte Carlo'],
    cellLoc='center',
    loc='upper right',
    colColours=['#f5f5f5']*3,
    cellColours=cell_colours,  # Apply custom cell colors
    bbox=[1.03, 0.25, 0.35, 0.2]  # Adjust position: [x0, y0, width, height]
)

# Adjust font size for the table
table.auto_set_font_size(False)
table.set_fontsize(8)  # Set the font size for the table text

# Adjust the table size
table.scale(0.8, 0.8)  # Make the table smaller, change the scale factors as needed

# Auto-adjust column widths
table.auto_set_column_width([0, 1, 2])  # Auto-adjust column widths for a neat look

# Adjust the layout again to make sure everything fits
plt.subplots_adjust(right=0.75)

# Calculate the accuracy of Monte Carlo to Black-Scholes
call_accuracy = abs(mc_call_price - bs_call_price) / bs_call_price * 100  # Percentage error for call option
put_accuracy = abs(mc_put_price - bs_put_price) / bs_put_price * 100  # Percentage error for put option

# Display the accuracy in a separate table below the main table
accuracy_table_data = [
    ['Call Option', f'{call_accuracy:.2f}%'],
    ['Put Option', f'{put_accuracy:.2f}%']
]

# Define custom cell colors for accuracy table
accuracy_cell_colours = [
    ['#90EE90', '#90EE90'],  # Green for Call Option Accuracy
    ['#FF6347', '#FF6347']   # Red for Put Option Accuracy
]

# Add the accuracy table to the plot window
accuracy_table = plt.table(
    cellText=accuracy_table_data,
    colLabels=['Option Type', 'Error'],
    cellLoc='center',
    loc='upper right',
    colColours=['#f5f5f5']*2,
    cellColours=accuracy_cell_colours,  # Apply custom cell colors
    bbox=[1.03, 0.05, 0.35, 0.15]  # Position of the accuracy table below the main table
)

# Adjust font size for the accuracy table
accuracy_table.auto_set_font_size(False)
accuracy_table.set_fontsize(8)

# Auto-adjust column widths
accuracy_table.auto_set_column_width([0, 1])

# Show plot
plt.show()
