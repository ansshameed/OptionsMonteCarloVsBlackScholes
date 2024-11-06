import numpy as np 

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

#Loop through simulations
for _ in range(num_simulations): 
    S = S0 #for each simulation reset S to initial asset price
    for _ in range(time_steps): #loop through steps in simulation to create price path of random price movements (GBM). Repeat until expiration date T, creating complete simulated price path for asset
        Z = np.random.normal() #Random variable from normal dist. (randomness)
        S = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z) 
        #Assign asset price for each time step in path
    #PAYOFF CALCULATION FOR EACH SIM
    call_payoffs.append(max(S - K, 0)) #call option payoff; Current - Strike. Want strike price to be lower to be ITM (below current price)
    put_payoffs.append(max(K - S, 0)) #put option payoff
    #calculates payoff for each simulation

#Calculate option price
call_option_price = np.exp(-r * T) * np.mean(call_payoffs) 
put_option_price = np.exp(-r * T) * np.mean(put_payoffs)

print("Estimated Call Option Price: ", call_option_price)
print("Estimated Put Option Price: ", put_option_price)