# Stochastic Options Pricing Engine
Understanding options pricing by comparing results between the Monte Carlo Simulation and Black Scholes. 


- Dynamic functionality to adjust options parameters (e.g. volatility, no. simulations, time steps etc.) to change options price. 
- GUI to see comparability between Monte Carlo and Black Scholes options pricing by visualising graphs. 
- Visualisation of random walks of asset prices using Geometric Brownian Motion.

### Features 
- **Monte Carlo Simulation**:
  - Simulates asset price paths using **Geometric Brownian Motion**
  - Calculates **call and put option prices** based on simulated paths
- **Black-Scholes Model**:
  - Calculates theoretical call and put option prices using Black-Scholes formula
  - Provides benchmark for comparison with Monte Carlo results
- **Dynamic Parameter Adjustment**: Interactive Sliders 
  - ```S0```: Spot Price
  - ```K```: Strike Price
  - ```T```: Time to Expiration
  - ```σ```: Volatility
  - ```Number of Simulations```
  - ```Time Steps```
- **Error Analysis**:
  - Compares Monte Carlo prices with Black-Scholes prices
  - Displays absolute percentage errors for call and put options
- **Visualisations**:
  - Plots up to 50 simulates asset price paths
  - Highlights the strike price as a reference line
- **Interactive UI**:
  - Includes sliders for real-time parameter updates
  - An 'Apply' button recalculates prices and updates plots
 
### How to Use 
1. ```python3 MCBSOptions.py```
2. Adjust the sliders to set the desired parameters
3. Click 'Apply' to update simulations and pricing
4. View updated Monte Carlo and Black-Scholes prices, along with percentage errors

### Dependencies
- ```numpy```
- ```matplotlib```
- ```scipy```

## Screenshot: 

![Screenshot 2024-12-25 at 22 53 18](https://github.com/user-attachments/assets/045dc887-7a95-4196-8303-f7900b3e5a70)


