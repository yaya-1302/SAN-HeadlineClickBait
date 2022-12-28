from flask import Flask, render_template, request
import json
from src import controller
# flask read views in "templates" folder
# flask read asset in "static" folder


app = Flask(__name__)


@app.route('/dashboard')
def index():
    return render_template('/views/dashboard.html')


@app.route('/accordions')
def to_accordions():
    return render_template('/views/accordions.html')


@app.route('/gallery')
def to_gallery():
    return render_template('/views/gallery.html')

# code started here

@app.route('/eval_training')
def to_form():
    return render_template('/views/eval_training.html')

@app.route('/eval')
def eval_page():
    return render_template('/views/eval.html')

@app.route('/')
def demo_page():
    return render_template('/views/demo.html')

@app.route('/identify', methods=['GET'])
def san_headline_identification():
    judul = request.args.get('title').strip()
    word_judul, len_judul = controller.text_length(judul)
    if word_judul > 3 and len_judul < 250 :
        clean_txt = controller.clean(judul)
        is_cb, acc = controller.identify_text(judul)
        return json.dumps(
            {
                'judul': clean_txt,
                'is_clickbait': is_cb,
                'accuracy' : acc
            }
        ), 200, {'ContentType': 'application/json'}
    else :
        return 500

app.run(debug=True)
