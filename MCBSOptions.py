import numpy as np 
import matplotlib.pyplot as plt

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

#Calculate option price
call_option_price = np.exp(-r * T) * np.mean(call_payoffs) 
put_option_price = np.exp(-r * T) * np.mean(put_payoffs)

print("Estimated Call Option Price: ", call_option_price)
print("Estimated Put Option Price: ", put_option_price)

plt.figure(figsize=(12, 6)) 
for i in range(min(10, num_simulations)):
    #Plots i'th simulated asset price path. X-axis is time from 0 to expiration T, y-axis asset price. Lw = line width, alpha = transparency
    #np.linspace generates array of time_steps + 1, evenly spaced values between 0 and T, representing time points at which the asset is simulated
    plt.plot(np.linspace(0, T, time_steps + 1), simulated_paths[i], lw=0.8, alpha=0.7) 
plt.title('Simulated Asset Price Paths') 
plt.xlabel('Time to Expiration (Years)') 
plt.ylabel('Asset Price')
plt.grid(True)
plt.show()