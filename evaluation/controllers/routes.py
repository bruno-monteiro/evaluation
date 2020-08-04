from evaluation import app
from flask import render_template, request
from evaluation.controllers.aux import create_buttons, get_result_data, open_news_file

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    d = request.form.to_dict()
    return render_template('result.html', request=d)

@app.route("/analisar", methods=['POST','GET'])
def analisar():

    # Get a random news
    news = open_news_file()

    # Toponym list from 'results_geonames'
    tp_list = get_result_data(news)

    # News with buttons and and a list of tp_buttons
    (text, buttons_list) = create_buttons(news, tp_list)

    # Split the title, subtitle and text
    (news['titulo'], news['subtitulo'], news['texto']) = text.split("||")
    
    # Break the text into paragraphs
    paragraphs = news['texto'].split('\n\n')

    return render_template('analisar.html', title=news['titulo'], subtitle=news['subtitulo'], paragraphs=paragraphs, tp_list=buttons_list)
