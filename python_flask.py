from flask import Flask, request
import numpy as np
from scipy.stats import norm

app = Flask(__name__)

@app.route('/', methods=['POST'])
def euro_option_price():
    s = float(request.form['s'])
    k = float(request.form['k'])
    t = float(request.form['t'])
    r = float(request.form['r'])
    d = float(request.form['d'])
    sigma = float(request.form['sigma'])
    option_type = request.form['option_type']
    
    d1 = (np.log(s / k) + (r - d + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    if option_type == 'call':
        option_price = s * np.exp(-d * t) * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
    else:
        option_price = k * np.exp(-r * t) * norm.cdf(-d2) - s * np.exp(-d * t) * norm.cdf(-d1)
    
    return str(option_price)

if __name__ == '__main__':
    app.run()
