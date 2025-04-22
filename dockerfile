FROM python:3.9-slim


RUN apt-get update && \
    apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 \
    lxml==4.9.3 && \
    pip install --no-cache-dir --default-timeout=1000 \
    -r requirements.txt

RUN python -c "import nltk; \
    nltk.download('stopwords'); \
    nltk.download('wordnet'); \
    nltk.download('punkt'); \
    nltk.download('punkt_tab')"

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "120", "app:app"]