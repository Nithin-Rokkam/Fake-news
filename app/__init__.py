import os
import secrets
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration
    # app.config['SECRET_KEY'] = os.environ.get('ec58b3d0de26af5678dc3fa569d52fd292438360b1eefa25986b0734382ae79a', secrets.token_hex(32))
    from .models import FakeNewsModel
    from .scraper import NewsScraper
    
    model = FakeNewsModel()
    scraper = NewsScraper()
    
    # Load or train model
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    model_path = os.path.join(model_dir, 'fake_news_model.pkl')
    vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        model.load_model(model_path, vectorizer_path)
    else:
        print("Training new model...")
        true_path = os.path.join('data', 'true.csv')
        fake_path = os.path.join('data', 'fake.csv')
        model.train(true_path, fake_path, save_path=model_dir)
    
    # Register routes
    from .routes import init_routes
    init_routes(app, model, scraper)
    
    return app
app = create_app()