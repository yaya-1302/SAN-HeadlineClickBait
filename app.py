from flask import Flask, render_template, request
import json
from src import controller
# flask read views in "templates" folder
# flask read asset in "static" folder


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('/views/dashboard.html')


@app.route('/accordions')
def to_accordions():
    return render_template('/views/accordions.html')


@app.route('/gallery')
def to_gallery():
    return render_template('/views/gallery.html')


@app.route('/formcontrol')
def to_form():
    return render_template('/views/basic_elements.html')

# code started here


@app.route('/demo')
def demo_page():
    return render_template('/views/demo.html')

@app.route('/identify', methods=['GET'])
def san_headline_identification():
    judul = request.args.get('title')
    pengolahan = request.args.get('model')

    is_cb = is_clickbait(judul, pengolahan)
    return json.dumps(
        {
            'judul': judul,
            'is_clickbait': is_cb
        }
    ), 200, {'ContentType': 'application/json'}


def is_clickbait(judul, model):
    return controller.identify_text(judul, model)


app.run(debug=True)
