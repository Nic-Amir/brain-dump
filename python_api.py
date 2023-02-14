from flask import Flask, request
import numpy as np
from scipy.stats import norm

app = Flask(__name__)

@app.route('/bs_eu_option')
def bs_eu_option():
    St = float(request.args.get('St'))
    K = float(request.args.get('K'))
    sigma = float(request.args.get('sigma'))
    delta_t = float(request.args.get('delta_t'))
    r = float(request.args.get('r'))
    d = float(request.args.get('d'))
    option_type = request.args.get('option_type')
    
    d_1 = (np.log(St/K)+(r-d+((sigma**2)/2))*(delta_t))/(sigma*np.sqrt(delta_t))
    d_2 = d_1 - (sigma*np.sqrt(delta_t))
    
    if option_type == "call":
        return str(norm.cdf(d_1) * St - norm.cdf(d_2) * K * np.exp(-r * delta_t))
    elif option_type == "put":
        return str(norm.cdf(-d_2) * K * np.exp(-r * delta_t) -norm.cdf(-d_1) * St)
    else:
        return "Option type is invalid, please check"

@app.route('/bs_binary_option')
def bs_binary_option():
    St = float(request.args.get('St'))
    K = float(request.args.get('K'))
    sigma = float(request.args.get('sigma'))
    delta_t = float(request.args.get('delta_t'))
    r = float(request.args.get('r'))
    d = float(request.args.get('d'))
    option_type = request.args.get('option_type')
    
    d_1 = (np.log(St/K)+(r-d+((sigma**2)/2))*(delta_t))/(sigma*np.sqrt(delta_t))
    d_2 = d_1 - (sigma*np.sqrt(delta_t))
    
    if option_type == "call":
        return str(norm.cdf(d_2) * np.exp(-r * delta_t))
    elif option_type == "put":
        return str(norm.cdf(-d_2) * np.exp(-r * delta_t))
    else:
        return "Option type is invalid, please check"

@app.route('/mc_pricer')
def mc_pricer():
    St = float(request.args.get('St'))
    K = float(request.args.get('K'))
    sigma = float(request.args.get('sigma'))
    delta_t = float(request.args.get('delta_t'))
    r = float(request.args.get('r'))
    d = float(request.args.get('d'))
    n_sample = int(request.args.get('n_sample'))
    option_type = request.args.get('option_type')
    
    dt = 1/(365*86400)
    n_steps = int(delta_t/dt)-1
    S0 = St
    payoff = 0
    for i in range(n_sample):
        z = np.random.normal(0,1, n_steps)
        S = S0*np.exp(np.cumsum((r-d - sigma**2/2)*dt + sigma*np.sqrt(dt)*z))
        if option_type == "call":
            payoff += max(S[-1] - K, 0)
        elif option_type == "put":
            payoff += max(K - S[-1], 0)
        else:
            return "Supported option types: 'call', 'put'"
    return str(payoff/n_sample * np.exp(-r*delta_t))

@app.route('/eu_tree')
def eu_tree():
    S0 = float(request.args.get('S0'))
    K = float(request.args.get('K'))
    r = float(request.args.get('r'))
    T = float(request.args.get('T'))
    N = int(request.args.get('N'))
    sigma = float(request.args.get('sigma'))
    option_type = request.args.get('type')
    
    dt = T/N
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))
    p = (np.exp(r * dt) - d) / (u-d)
    S = np.zeros(N+1)
    discount = np.exp(-r * dt)
    
    for i in range(N+1):
        S[i] = S0 * u ** (N-i) * d ** i
        
    payoff = np.zeros(N+1)
    
    for i in range(N+1):
        if option_type == "call":
            payoff[i] = max(S[i] - K, 0)
        elif option_type == "put":
            payoff[i] = max(K - S[i], 0)
        else:
            return "Invalid option type"
            
    for j in np.arange(N-1, -1, -1):
        for i in range(j+1):
            payoff[i] = discount * (p * payoff[i] + (1-p) * payoff[i+1])
            
    return str(payoff[0])

@app.route('/american_tree')
def american_tree():
    S0 = float(request.args.get('S0'))
    K = float(request.args.get('K'))
    r = float(request.args.get('r'))
    T = float(request.args.get('T'))
    N = int(request.args.get('N'))
    sigma = float(request.args.get('sigma'))
    option_type = request.args.get('type')
    
    dt = T/N
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))
    p = (np.exp(r * dt) - d) / (u-d)
    S = np.zeros(N+1)
    discount = np.exp(-r * dt)
    
    for i in range(N+1):
        S[i] = S0 * u ** (N-i) * d ** i
        
    payoff = np.zeros(N+1)
    
    for i in range(N+1):
        if option_type == "call":
            payoff[i] = max(S[i] - K, 0)
        elif option_type == "put":
            payoff[i] = max(K - S[i], 0)
        else:
            return "Invalid option type"
            
    for j in np.arange(N-1, -1, -1):
        for i in range(j+1):
            payoff[i] = discount * (p * payoff[i] + (1-p) * payoff[i+1])
            S = S0 * u ** (j-1) * d ** i
            if option_type == "call":
                payoff[i] = np.maximum(payoff[i], S-K)
            if option_type == "put":
                payoff[i] = np.maximum(payoff[i], K-S)
    return str(payoff[0])

if __name__ == '__main__':
    app.run()