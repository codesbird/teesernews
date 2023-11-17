import time,json
from news.models import *
import requests
from bs4 import BeautifulSoup

class PageViewsMiddleware:
    latestNews = []
    trandingNews = []
    singleNews = {}
    url = 'https://www.ndtv.com/latest#pfrom=home-ndtv_mainnavgation'
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        # upload = threading.Thread(target=self.uploadNews,args=['NDTV News'])
        # upload.start()
        pass


   
    # """""""""""""""""" NDTV Latest news """""""""""""""""""""
    def latestNewsNDTV(self):
        self.url = 'https://www.ndtv.com/latest#pfrom=home-ndtv_mainnavgation'
        
        try:
            
            page = requests.get(self.url)
            soup = BeautifulSoup(str(page.content), "html.parser")

            latest = soup.find('div',{'class':'lisingNews'}).find_all('div',{'class':'news_Itm'})
            for i,news in enumerate(latest):
                latest_news = BeautifulSoup(str(news), "html.parser")

                if news !=" ":
                    try:
                        self.latestNews.append(latest_news.find('a').get('href'))
                    except Exception as r:
                        # print(r,i)
                        pass
            
            return self.latestNews
        except requests.exceptions.ConnectionError as r:
            print(":No internet connection check it first: ",r)
            return []
    
    def trandingNewsNDTV(self):
        try:
            
            page = requests.get(self.url)
            soup = BeautifulSoup(str(page.content), "html.parser")
            tranding = soup.find("ul",{'class':'s-ls_ul s-ls_br'}).find_all('li')
            
            print(len(tranding))
            for i,trand in enumerate(tranding):
                tranding_news=  BeautifulSoup(str(trand), "html.parser")
                n = {
                    
                "image": tranding_news.find('img').get('data-src'),
                "title": tranding_news.find('img').get('alt'),
                "url": tranding_news.find('div').find('a').get('href'),
                }
            
                self.trandingNews[str(i)] = n
                
            return json.dumps(self.trandingNews)
        
        except requests.exceptions.ConnectionError as r:
            print("No internet connecion check connection first: ",r)
            return []
    
    def singleNewsNDTV(self,url):
        # url = 'https://www.ndtv.com/india-news/sameer-wankhede-citing-shah-rukh-khan-chats-as-certificate-of-integrity-cbi-4056277#News_Trending'
        try:
            page = requests.get(url)
            soup = BeautifulSoup(str(page.content), "html.parser")
            
            news = soup.find("div",{'id':'ins_storybody'})
            # return news
            if news == None:
                return json.dumps({})
        
        
            try:
                    image = news.find('img')
                    video = news.find('iframe')
                                
                    if image is not None:
                        media =  image.get('src')
                    
                    if video is not None:
                        media = video.get('src')
                    
                    
                    try:
                        dateTime = soup.find('span',{'itemprop':'dateModified'}).get('content')
                        author = soup.find('span',{"itemprop":"author"}).text
                        desc = soup.find('h2',{'class':'sp-descp'}).text
                        headline= soup.find('h1',{"itemprop":"headline"}).text
                        self.singleNews["media"] = media
                        self.singleNews["author"] = author
                        self.singleNews["dateTime"] = dateTime
                        self.singleNews["desc"] = desc
                        self.singleNews["headline"] = headline
                        textStr = ''
                        for p in news.find_all('p'):
                            textStr+=str(p)
                        self.singleNews["text"] = textStr
                    
                    except Exception as p:
                        # print(p)
                        pass
                    return json.dumps(self.singleNews)

            except Exception as r:
                return json.dumps({"r":r})
            
        except requests.exceptions.ConnectionError as r:
            print(":No internet connection check it first: ",r)
            return []
        
    def timeFormat(self,time:str):
        from datetime import datetime
        
        time = time.split('+')[0]
        date = [int(d) for d in time.replace("-"," ").replace("T"," ").replace("Z","").replace(":"," ").split(" ")]
        return datetime(year=date[0],month=date[1],day=date[2],hour=date[3],minute=date[4],second=date[5])

    def uploadNews(self,channel):
        channel = NewsSource.objects.filter(name=channel).first()
        if channel is not None:
            for latest in self.latestNewsNDTV():
                news = json.loads(self.singleNewsNDTV(latest))
                print(news)
                
                if len(news)>0:
                    print('exists news : ',news["headline"],)
                    if News.objects.filter(title=news["headline"]).count()==0:
                        
                        ndtv   = News()
                        print("The author is : ",news['author'])
                        ndtv.author = news['author']
                        ndtv.title= news["headline"]
                        ndtv.description = news["desc"]
                        ndtv.url = latest
                        ndtv.urlToImage = news["media"]
                        ndtv.publishedAt = self.timeFormat(str(news["dateTime"]))
                        ndtv.content = news["text"]
                        ndtv.type = 'latests' #if 'News_Trending' in url else 'latests'
                        ndtv.channel = channel
                        ndtv.save()
                    else:
                        # print("The news is already uploaded")
                        pass
                else:
                    # print("No news find")
                    pass
        else:
            print("The channel is not available | upload a channel before pushing news")

if __name__ == '__main__':
    while True:
        # your_task_function()
        print("I am News and I am ")
        time.sleep(60)  # Interval in seconds
