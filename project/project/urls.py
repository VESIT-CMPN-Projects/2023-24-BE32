from django.contrib import admin
from django.urls import path
from dashboard.views import exitpoll_view, news_list, social, index_view, aboutus
from dashboard.views import history_search, state_data, feedback, tweets, predict

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index_view, name='index'),
    path('exitpoll/', exitpoll_view, name='exitpoll'),
    path('index/', index_view, name='index'),
    path('predict/', predict, name='predict'),
    path('news/', news_list, name='news'),
    path('social/', social, name='social'),
    path('tweets/', tweets, name='tweets'),
    path('history/', history_search, name='history_election'), 
    path('history/', history_search, name='search_history'),
    path('state/',state_data, name='state'),
    path('aboutus/',aboutus, name='aboutus'),
    path('feedback/',feedback, name='feedback')
]
