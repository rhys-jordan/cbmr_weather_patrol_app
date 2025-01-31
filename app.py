from flask import *

app = Flask(__name__, static_url_path = '/static')

@app.route('/')
def home() :
    return render_template('home.html')

@app.route('/<n>')
def n(n) :
    return render_template('n.html', n=n)

@app.route('/isPrime/<n>')
def isPrime(n) :
    primeness = True
    count = 0;
            
    for i in range(1,int(n)+1) :
        if (int(n) % i == 0) : 
            count += 1
    
    if count > 2 :
        primeness = False

    return render_template('isPrime.html', n=n, primeness=primeness)

app.run()