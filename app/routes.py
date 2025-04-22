import os
from flask import render_template, request, jsonify, redirect, url_for
from threading import Thread
import time

def init_routes(app, model, scraper):
    # Store analyzed news
    analyzed_news = []
    last_fetch_time = None

    def background_news_fetcher():
        nonlocal analyzed_news, last_fetch_time
        while True:
            try:
                print("Fetching latest news...")
                news_items = scraper.get_google_news()
                current_batch = []
                
                for item in news_items:
                    prediction = model.predict(item['text'])
                    current_batch.append({
                        **item,
                        'prediction': prediction['prediction'],
                        'confidence': round(prediction['confidence'], 2),
                        'analyzed_at': time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                
                analyzed_news = sorted(current_batch, key=lambda x: x['confidence'], reverse=True)
                last_fetch_time = time.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Error in background fetcher: {e}")
            time.sleep(1800)  # 30 minutes

    # Start background thread
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        Thread(target=background_news_fetcher, daemon=True).start()

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze():
        if 'news_url' in request.form:
            article = scraper.scrape_from_url(request.form['news_url'])
            if article:
                result = model.predict(article['text'])
                return render_template('result.html',
                    prediction=result['prediction'],
                    confidence=round(result['confidence'], 2),
                    article=article)
        
        elif 'news_text' in request.form:
            result = model.predict(request.form['news_text'])
            return render_template('result.html',
                prediction=result['prediction'],
                confidence=round(result['confidence'], 2),
                article={'title': 'User Input', 'text': request.form['news_text']})
        
        return redirect(url_for('home'))

    @app.route('/api/predict', methods=['POST'])
    def api_predict():
        data = request.get_json()
        if 'text' in data:
            return jsonify(model.predict(data['text']))
        elif 'url' in data:
            article = scraper.scrape_from_url(data['url'])
            if article:
                result = model.predict(article['text'])
                return jsonify({
                    "prediction": result['prediction'],
                    "confidence": result['confidence'],
                    "article": article
                })
        return jsonify({"error": "Invalid request"}), 400