from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from news.models import *
# Register your models here.
class UserprofileAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff','dob','gender','phone','city','state','country','private','Profile_Image']

    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'password')
        }),
        ('Personal informations', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('dob','gender','phone','city','state','country','bio','profile','private')
        })
    )

    add_fieldsets = (
        ('Authentications', {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('dob','gender','phone','city','state','country','bio','profile','private')
        })
    )

    
    def Profile_Image(self,obj):
        profile = ''
        try:
            profile = f'<a href="{obj.profile.url}"><img style="width:50px;height:50px;border-radius:50%;" src="{obj.profile.url}" alt=""></a>'
        except:
            return "None"
            print(obj)
        return format_html(profile)
        
    def has_add_permission(self, request):
        return super().has_add_permission(request)



# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    model=News
    list_display = ['Channel','title','author',"Published",'Page']

    ordering= ['-pk']

    def Channel(self,obj):
        img = f"<div style='display:flex;align-items:center;justify-content:left;'> <img src='{obj.channel.icon}' width='40px' height='40px'/> <span style='margin-left:10px;'> {obj.channel.name}</span></div>"
        return format_html(img)
    
    def Page(self,obj):
        p = f"<a  style='background-color:white;color:black;border-radius:4px;padding:5px;cursor:pointer;' href='/news?q={obj.title}'>Read</a>"
        return format_html(p)


    def Published(self,obj):
        return obj.publishedAt



class ChannelsAdmin(admin.ModelAdmin):
    model = NewsSource
    list_display = ['Icon','domain','Page']

    def Icon(self,obj):
        img = f"<div style='display:flex;align-items:center;justify-content:left;'> <img src='{obj.icon}' width='40px' height='40px'/> <span style='margin-left:10px;'> {obj.name}</span></div>"
        return format_html(img)

    def Page(self,obj):
        p = f"<a  style='background-color:white;color:black;border-radius:4px;padding:5px;cursor:pointer;' clas='btn btn-info' href='/channels?name={obj.name}'>Continou to reading</a>"
        return format_html(p)


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ['id','user']

class PageAdmin(admin.ModelAdmin):
    list_display = ['url','User','view_count','likes']
    
    def User(self,obj):
        return [user for user in obj.user.all()]
class CommentAdmin(admin.ModelAdmin):
    list_display= ["page","user","content","created_at","parent"]

class PageViewAdmin(admin.ModelAdmin):
    list_display = ['page','ip_address','user','timestamp']

admin.site.register(News,NewsAdmin)
admin.site.register(NewsSource,ChannelsAdmin)
admin.site.register(Subscribers,SubscribersAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(User,UserprofileAdmin)
admin.site.register(PageView,PageViewAdmin)
