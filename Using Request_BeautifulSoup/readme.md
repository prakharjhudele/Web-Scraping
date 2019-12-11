Using Selenium comes in handy when scraping dynamic web pages, that is when the page is loaded with javascripts and we need sufficient user interaction to show the required data. However, there are simple pages where data is readily available on load. These are called static web pages. I have attached a scraping example which downloads data from news paper archive of Indian economic newspaper daily The Hindu Business Line.

Key Highlights-
1) Use the start and End date range to get data for the period. This selection generates a dynamic URL's based on the date range.


2). The script also fetches the link of all the available articles.


3). Each link is fetched to get the data.Fields available after scraping
'news_headline', 'news_article', 'news_category','news_author', 'news_date'


4).The data is downloaded as a CSV created from dataframe.  
