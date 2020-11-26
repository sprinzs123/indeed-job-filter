from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print('is it working')
        return render_template('home.html')
    else:
        return render_template('home.html')


@app.route('/results')
def result():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)
