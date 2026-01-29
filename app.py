from flask import Flask, render_template, request, redirect, url_for
from deep_translator import GoogleTranslator
from quotes_data import quotes  # your existing quotes_data.py

app = Flask(__name__)

@app.route('/')
def home():
    categories = list(quotes.keys())
    return render_template('home.html', categories=categories)

@app.route('/quote/<category>')
def show_quote(category):
    if category not in quotes:
        return f"No quotes found for category: {category}"

    index = int(request.args.get('index', 0))
    lang = request.args.get('lang', 'en')

    category_quotes = quotes[category]
    total = len(category_quotes)
    quote_obj = category_quotes[index % total]

    quote_text = quote_obj['text']
    author = quote_obj['author']

    # Translate if language is not English
    if lang != 'en':
        try:
            quote_text = GoogleTranslator(source='en', target=lang).translate(quote_text)
            author = GoogleTranslator(source='en', target=lang).translate(author)
        except Exception as e:
            quote_text = f"Translation Error: {e}"

    return render_template('quote.html',
                           category=category,
                           quote=quote_text,
                           author=author,
                           index=index,
                           total=total,
                           lang=lang)

@app.route('/next/<category>/<int:index>')
def next_quote(category, index):
    lang = request.args.get('lang', 'en')
    return redirect(url_for('show_quote', category=category, index=index+1, lang=lang))

@app.route('/prev/<category>/<int:index>')
def prev_quote(category, index):
    lang = request.args.get('lang', 'en')
    return redirect(url_for('show_quote', category=category, index=index-1, lang=lang))

if __name__ == '__main__':
    app.run(debug=True)
