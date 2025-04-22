from newspaper import Article
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

class NewsScraper:
    def __init__(self):
        pass
    
    def scrape_from_url(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return {
                "title": article.title,
                "text": article.text,
                "authors": article.authors,
                "publish_date": str(article.publish_date),
                "top_image": article.top_image,
                "url": url
            }
        except Exception as e:
            print(f"Error scraping article: {e}")
            return None
    
    def search_news(self, query, num_results=5):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            search_url = f"https://www.google.com/search?q={query}&tbm=nws"
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for item in soup.select('.dbsr')[:num_results]:
                title = item.select_one('.nDgy9d').text
                link = item.a['href']
                source = item.select_one('.XTjFC.WF4CUc').text
                date = item.select_one('.WG9SHc span').text
                
                parsed_url = urlparse(link)
                query_params = parse_qs(parsed_url.query)
                actual_url = query_params.get('url', [link])[0]
                
                results.append({
                    "title": title,
                    "url": actual_url,
                    "source": source,
                    "date": date
                })
            return results
        except Exception as e:
            print(f"Error searching news: {e}")
            return []