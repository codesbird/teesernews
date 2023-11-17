from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,Group,Permission


# Create your models here.
class User(AbstractUser):
    gender = models.CharField(max_length=10,default='male',choices=[('male','male'),('female','female'),('other','other')])
    dob = models.DateField(null=True,blank=True)
    phone = models.CharField(max_length=15,default='',blank=True)
    city = models.CharField(max_length=50,default='',blank=True)
    state = models.CharField(max_length=50,default='',blank=True)
    country = models.CharField(max_length=50,default='',blank=True)
    bio = models.TextField(blank=True)
    private = models.BooleanField(default=False)
    profile = models.ImageField(upload_to='profile_images', blank=True,null=True)

    groups = models.ManyToManyField(Group, related_name='users',blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='users',blank=True)


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||



class NewsSource(models.Model):
    name = models.CharField(max_length=150)
    domain = models.CharField(max_length=1000,default='')
    icon = models.URLField(max_length=1000,default='')

    
    def __str__(self):
        return self.name


class News(models.Model):
    author = models.CharField(max_length=100, default="",blank=True,null=True)
    title = models.CharField(max_length=250, default="",blank=True,null=True)
    description = models.TextField(default="",blank=True,null=True)
    url = models.URLField(max_length=1000, default="",blank=True,null=True)
    urlToImage = models.URLField(max_length=1000, default="",blank=True,null=True)
    publishedAt = models.DateTimeField(null=True,blank=True)
    content = models.TextField(default="",blank=True,null=True)
    type = models.CharField(max_length=70,choices=[('tranding',"tranding"),('related','related',),('featured','featured')])
    channel = models.ForeignKey(NewsSource,related_name='channel',null=True,blank=True,on_delete=models.CASCADE,default='')
    
class Subscribers(models.Model):
    user = models.EmailField()
   
class Page(models.Model):
    url = models.CharField(max_length=255, unique=True)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL,default=' ')
    def __str__(self):
        return self.url

class Comment(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.page}"


class PageView(models.Model):
    page = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# from django.contrib.auth.models import User
# from django.db import models
# from django.utils.text import slugify
# from textblob import TextBlob
# from gensim.summarization import summarize
# from gensim import keywords

# class Category(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Tag(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class News(models.Model):
#     title = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True, max_length=100, editable=False)
#     content = models.TextField()
#     summary = models.TextField(blank=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     tags = models.ManyToManyField(Tag)
#     image = models.ImageField(upload_to='news_images/', null=True, blank=True)
#     pub_date = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     sentiment = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     view_count = models.PositiveIntegerField(default=0)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         if not self.sentiment:
#             self.sentiment = self.analyze_sentiment()
#         if not self.summary:
#             self.summary = self.generate_summary()
#         super(News, self).save(*args, **kwargs)

#     def analyze_sentiment(self):
#         blob = TextBlob(self.content)
#         sentiment = blob.sentiment.polarity
#         return round(sentiment, 2)

#     def generate_summary(self):
#         return summarize(self.content, word_count=50)

#     def extract_keywords(self):
#         return keywords.extract_keywords(self.content)

#     def get_related_articles(self):
#         keywords = self.extract_keywords()
#         related_articles = News.objects.filter(tags__name__in=keywords).exclude(id=self.id).distinct()[:5]
#         return related_articles

#     @classmethod
#     def get_trending_articles(cls, limit=5):
#         trending_articles = cls.objects.order_by('-view_count')[:limit]
#         return trending_articles

#     def __str__(self):
#         return self.title
