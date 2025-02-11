from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forum')
def about():
    return render_template('forum.html')

@app.route('/autobus')
def contact():
    return render_template('autobus.html')

if __name__ == '__main__':
    app.run(debug=True)