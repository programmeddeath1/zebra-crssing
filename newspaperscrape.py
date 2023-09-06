from newspaper import Article

url = "https://curlytales.com/indians-splurge-the-most-on-travel-home-upkeep-may-not-be-the-priority-says-report/"
article = Article(url)
article.download()
import pdb;pdb.set_trace()
# article.html
article.parse()
print(article.text)
print(article.title)
print(article.top_image)
print(article.keywords)
print(article.summary)

