import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import os

nltk.download('stopwords')
nltk.download('wordnet')

class FakeNewsModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
        self.model = PassiveAggressiveClassifier(max_iter=50)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
        tokens = nltk.word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)
    
    def load_data(self, true_path, fake_path):
        true_news = pd.read_csv(true_path)
        true_news['label'] = 1
        fake_news = pd.read_csv(fake_path)
        fake_news['label'] = 0
        
        data = pd.concat([true_news, fake_news], axis=0)
        data = data.sample(frac=1).reset_index(drop=True)
        data['text'] = data['text'].apply(self.preprocess_text)
        return data['text'], data['label']
    
    def train(self, true_path, fake_path, save_path='models/'):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            
        X, y = self.load_data(true_path, fake_path)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        self.model.fit(X_train_vec, y_train)
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.2f}")
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        joblib.dump(self.model, os.path.join(save_path, 'fake_news_model.pkl'))
        joblib.dump(self.vectorizer, os.path.join(save_path, 'tfidf_vectorizer.pkl'))
        return accuracy
    
    def load_model(self, model_path='models/fake_news_model.pkl', 
                  vectorizer_path='models/tfidf_vectorizer.pkl'):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
    
    def predict(self, text):
        processed_text = self.preprocess_text(text)
        text_vec = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(text_vec)[0]
        proba = self.model._predict_proba_lr(text_vec)[0]
        
        if prediction == 1:
            return {"prediction": "True", "confidence": proba[1]*100}
        else:
            return {"prediction": "Fake", "confidence": proba[0]*100}