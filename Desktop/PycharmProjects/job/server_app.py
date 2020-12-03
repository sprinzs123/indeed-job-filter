from flask import Flask, render_template, request
from connected_scrape import dummy_items


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print('is it working')
        title = request.form
        for field in title:
            print(title.get(field))
        # print(title.get("title-0"))
        return render_template('home.html')
    else:
        return render_template('home.html')


@app.route('/results')
def result():
    all_items = dummy_items
    # all_items = {'title': 'title', "item": 'item'}
    # all_items = [1, 2, 3]
    return render_template('results.html', items=all_items)


if __name__ == '__main__':
    app.run(debug=True)
