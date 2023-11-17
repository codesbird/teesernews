# my news api key: 5b1e3a14331746dbb9cd3431707755f6
from django.urls import path
from news import views
urlpatterns=[
    path('',views.HomePage,name="homepage"),
    path('channels',views.Chennels,name='channels'),
    path('search',views.Search,name='search'),
    path('signup',views.Userauth,name='signup'),
    path('login',views.Signin,name='login'),
    path('subscribe',views.Subscriber,name='subscribe'),
    path('modal',views.LoadModal,name='modal'),
    path('news',views.ScrapNews,name='news'),
    path('likes',views.LikeUnlike,name='likes'),
    path('comments',views.Comments,name='likes'),

    path('contact',views.Contactus.as_view(),name='contact'),
    path('aboutus',views.TemplateView.as_view(template_name='about.html'), name='contact')
]

