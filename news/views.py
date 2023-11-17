from django.contrib.sessions.models import Session
from django.shortcuts import render,HttpResponse
from news.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json,requests
from django.shortcuts import render, redirect
from .models import Page
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
import time
# Create your views here.

def UploadNews(data):
    if data['status']=='ok':
        
        channels = [name.name for name in NewsSource.objects.all()]
        for news in data['articles']:
               
                if  news['source']['name'] not in channels:

                    newChannel = NewsSource.objects.create(name = news['source']['name'],domain=str(news['url']).replace("https://","").split("/")[0])
                    newChannel.save()

                newnews = News()
                newnews.author = news['author']
                newnews.title = news['title']
                newnews.url = news['url']
                newnews.description = news['description']
                newnews.urlToImage = news['urlToImage']
                newnews.content = news['content']
                newnews.channel = NewsSource.objects.filter(name=news['source']['name']).first()    
                newnews.save()
      
@csrf_exempt
def HomePage(request):
    if request.method=="POST":
        data  = request.POST

    
    channels = NewsSource.objects.all()
    news = News.objects.all().order_by('-publishedAt').distinct()

    return render(request,'home.html',{'news':news[:7],"channels":channels,'tnews':news[20:32],'topnews':news[7:19]})


# __________

def search_words_in_model(line):
    matching_objects = []   # List to store matching objects

    for obj in News.objects.all():
        line_words = line.split()  # Split the line into individual words

        object_words = [
            obj.title.lower().replace('-',' ').replace('_',' '),
            obj.description.lower().replace('-',' ').replace('_',' '),
            obj.content.lower().replace('-',' ').replace('_',' '),
            obj.author.lower().replace('-',' ').replace('_',' '),
        ] 
        matches = sum(word in word_list.split() for word in line_words for word_list in object_words) 

        if matches > 0:
            matching_objects.append((obj, matches))
            
        matching_objects.sort(key=lambda x: x[1], reverse=True)  # Sort the matching objects based on the match count


    return [match[0] for match in matching_objects if match[1]>0]  # Return the list of matching objects


def sort_results_by_created_date(matching_results,re=False):
    
    matching_results.sort(key=lambda x: x.publishedAt, reverse=re)  # Sort the matching objects based on the match count

    
    return matching_results

def getTranddingNews():
    trandding_news = []
    
    for tnews in News.objects.all().distinct():
        trad = PageView.objects.filter(page="/news?q="+tnews.title).count()
        trandding_news.append([tnews,trad])
    
    trandding_news.sort(key=lambda x: x[1],reverse=True)  # Sort the matching objects based on the match count

    return [n[0] for n in trandding_news][:10]
# ________________________________________________________________________________


def Chennels(request):
    name = request.GET.get('name')
    author =request.GET.get('au')
    sort =request.GET.get('or')
    page =request.GET.get('page')
    
    channels =[]
    channelNews = []
    page_title = "channels"
    scrap_time = 0
    page_nun = 1
    
    
    if page is not None:
        page_nun = page
   
    if name is not None:
        start_time = time.time()
        
        page_title = name
        channelNews = News.objects.filter(channel__name=name).order_by('-publishedAt')
        scrap_time = time.time()-start_time

    elif author is not None:
        page_title = author
        
        start_time = time.time()
        channelNews = News.objects.filter(author=author)
        scrap_time = time.time()-start_time
        
    else:
        start_time = time.time()
        channels = NewsSource.objects.all()
        scrap_time = time.time()-start_time
        
    results =len(channelNews)
    
    
                
    channelNews = Paginator(object_list=channelNews,per_page=24).page(page_nun)
  
    if sort is not None:
            if sort=='date':
                channelNews.object_list = sort_results_by_created_date(channelNews.object_list,re = False)
            else:
                channelNews.object_list = sort_results_by_created_date(channelNews.object_list,re=True)
            
    return render(request,'channels.html',{"channels":channels,'channelNews':channelNews,"channelname":page_title,'time':str(scrap_time)[:7],'results':results})
    

def Search(request):    
    query =request.GET.get('query').lower()
    sort =request.GET.get('or')
    page =request.GET.get('page')
    page_nun = 1
    results = 0
    
    
    if page is not None:
        page_nun = page
   
    start_time = time.time()
    searNews = search_words_in_model(query)
    
    
    
    total_time = time.time()-start_time
    results = len(searNews)
    searNews = Paginator(object_list=searNews,per_page=24).get_page(page_nun)
    
    if sort is not None:
        
        if sort=='date':
            searNews.object_list = sort_results_by_created_date(searNews.object_list,re = False)
        else:
            searNews.object_list = sort_results_by_created_date(searNews.object_list,re=True)
       
   
    
    
    return render(request,'channels.html',{"channels":[],'channelNews':searNews,'time':str(total_time)[:4],'results':results,"channelname":str(query).capitalize()})

def Userauth(request):
    
    if request.user.is_authenticated:
        return redirect('/profile/')
    
    if request.method == 'POST':
            
        try:
                
            form = UserCreationForm(request.POST)
            form.is_valid()
        
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('homepage')
            
        except Exception as r:
            pass
    else:
        form = UserCreationForm()
            
    
        
    
    return render(request, 'signup.html', {'form': form})


def Signin(request):
    
    if request.user.is_authenticated:
        return redirect('/profile/')

    if request.method == 'POST':
        form = AuthenticationForm(request.POST,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if(user is not None):
                
                login(request, user)
                return redirect('homepage')
        
                    
    else:
        form = AuthenticationForm()
       
    return render(request, 'login.html', {'form': form})

def Logout(request):
    if request.user.is_authenticated:
        user = request.user.username
        logout(request)
        return render(request,'logout.html',{'user':user})
    return redirect('login')

from django.views.decorators.csrf import csrf_exempt


def convert_to_string(number):
    if number >= 1000000000:  # Billion
        return str(number // 1000000000) + "B"
    elif number >= 1000000:  # Million
        return str(number // 1000000) + "M"
    elif number >= 1000:     # Thousand
        return str(number // 1000) + "K"
    else:
        return str(number)


@csrf_exempt
def Subscriber(request):
    
    if request.method=="POST":
        sub = request.POST.get('email')
        emails  = [email.user for email in Subscribers.objects.all()]
        confirm = False
        if sub not in emails:
            confirm = True
            Subscribers.objects.update_or_create(user = sub)
            
        subs = Subscribers.objects.all().count()
        representation = convert_to_string(subs)
        return HttpResponse(json.dumps({'status':confirm,'subs':representation}))
    else:
        subs = Subscribers.objects.all().count()
        representation = convert_to_string(subs)
        return HttpResponse(json.dumps({'subs':representation}))
    
@csrf_exempt
def LoadModal(request):
    data = {}
    item = request.POST.get('item')
    news = News.objects.filter(title=item).first()
    data["author"] = news.author
    data["title"] = news.title
    data["description"] = news.description
    data["url"] = news.url
    data["urlToImage"] = news.urlToImage
    data["publishedAt"] = news.publishedAt.strftime("%Y-%m-%dT%H:%m:%S")
    data["content"] = str(news.content)[:250]
    data["channel"] = str(news.channel)
    
    return HttpResponse(json.dumps({'data':data}))

@login_required
def LikeUnlike(request):
    if request.method == 'POST':
        
        page_id = request.POST.get('page_id')
        action = request.POST.get('like')
        page_url = request.POST.get('url')

        page = Page.objects.get(id=page_id)
        
        page.url = page_url
        if request.user not in page.user.all():
            page.likes = page.likes + 1
            page.user.add(request.user)
            page.save()
            status = 'liked'
        else:
            page.likes = page.likes - 1
            page.user.remove(request.user)
            page.save()
            status = 'unliked'
        
        return HttpResponse(json.dumps({'status':status,'likes':convert_to_string(page.likes)}))
           
# @login_required
def ScrapNews(request):
    title = request.GET.get('q')
    page_url = "/news?q="+title
    
    news = []
    news = News.objects.all()
    
    current_news= ''
    content = ''
    pages  ={}
    for n in news:
        if title.lower() in n.title.lower():
            current_news = n
            content = current_news.content
            
    previous = News.objects.filter(pk = current_news.pk-1)
    next =     News.objects.filter(pk = current_news.pk+1)

    pages['has_previous'] = True if previous.count()>0 else False
    pages['has_next'] = True if next.count()>0 else False
    pages['previous'] = previous.first()
    pages['next'] = next.first()

    
    page = Page.objects.filter(url=page_url).first()
    is_liked = False
    comments = []
    if page is not None:
        is_liked = True if request.user in  page.user.all() else False
        view_count = page.view_count
        likes = page.likes
        page_id = page.id
        
        order = request.GET.get('order')
    
        if order is not None and order=='date':
            order = 'created_at'
        else:
            order = '-created_at'
                
        
        comments = page.comments.filter(parent=None).order_by(order)  # Fetch top-level comments only
                
    else:
        p = Page.objects.create(likes=0,view_count=0,url=page_url)
        view_count = p.view_count
        likes = p.likes
        page_id = p.pk
    
    
    
    related_news = search_words_in_model(line=current_news.title[:100])
   
    some_others =  News.objects.order_by('?')[:10]
    trandding_news = getTranddingNews()

    
    page = request.path+"?q="+current_news.title
    ip_address = request.META['REMOTE_ADDR']
    user = request.user

    page_views = PageView.objects.filter(page = page).count()
    
    if not user.is_anonymous:
        PageView.objects.update_or_create(page=page, ip_address=ip_address, user=user)

    return render(request,'news.html',{'news':current_news,'content':content,'trandingnews':trandding_news,'relatednews':related_news,'someother':some_others,'pages':pages,'view_count': page_views, 'likes': likes, 'page_id': page_id,'is_liked':is_liked,'comments':comments})

@login_required
def Comments(request):
    if request.method == 'POST':
        
        page_id = request.POST.get('page_id')
        action = request.POST.get('action')
        
        
        
        page = Page.objects.get(id=page_id)
        
        if action == 'comment':
                user = request.user  # Assuming you have implemented user authentication
                content = request.POST.get('comment_content')
                comment = Comment.objects.create(page=page, user=user, content=content)
                comment.save()
                # return redirect(request.path)  # Redirect to refresh the page

        elif action == 'reply':
            comment_id = request.POST.get('comment_id')
            parent_comment = Comment.objects.get(id=comment_id)
            user = request.user  # Assuming you have implemented user authentication
            content = request.POST.get('reply_content')
            reply = Comment.objects.create(page=parent_comment.page, user=user, content=content, parent=parent_comment)
            reply.save()
        elif action == 'delete':
            comment_id = request.POST.get('comment_id')
            parent_comment = Comment.objects.filter(id=comment_id)
            parent_comment.delete()
        
        elif action=='upcomment':
            comment_id = request.POST.get('comment_id')
            parent_comment = Comment.objects.get(id=comment_id)
            content = request.POST.get('comment_content')
            parent_comment.content = content
            parent_comment.save()
            
        elif action=='upreplay':
            comment_id = request.POST.get('comment_id')
            
            parent_comment = Comment.objects.get(id=comment_id)
            user = request.user  # Assuming you have implemented user authentication
            content = request.POST.get('reply_content')
            reply = Comment.objects.filter(page=parent_comment.page, user=user,parent=parent_comment).update(content=content)
            # reply.save()
            
            
            
        
        return redirect(page.url)
    
    return redirect('homepage')

def LatestNews(request):
    start_time = time.time()
    order = request.GET.get('or')

    searNews = News.objects.all().order_by('-publishedAt')
    total_time = time.time()-start_time

    if order is not None:
        if order=='-date':
            searNews = searNews.order_by('-publishedAt')
        else:
            searNews = searNews.order_by('publishedAt')
    
    return render(request,'channels.html',{"channels":[],'channelNews':searNews[:21],'time':str(total_time)[:7],'results':searNews.count()})

 
class Contactus(TemplateView):
    template_name = 'contact.html'
    