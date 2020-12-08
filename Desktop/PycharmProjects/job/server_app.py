from flask import Flask, render_template, request
from connected_scrape import all_data


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input_dictionary = request.form
        title_filters = []
        requiremets_filters = []
        summary_filter = []
        any_filters = []
        for field in input_dictionary:
            if 'title' in field:
                title_filters.append(input_dictionary.get(field))
            elif 'requirement' in field:
                requiremets_filters.append(input_dictionary.get(field))
            elif 'summary' in field:
                summary_filter.append(input_dictionary.get(field))
            elif 'any' in field:
                any_filters.append(input_dictionary.get(field))




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
