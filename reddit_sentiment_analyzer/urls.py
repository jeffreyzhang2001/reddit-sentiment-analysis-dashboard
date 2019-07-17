from django.urls import path
from reddit_sentiment_analyzer import views

urlpatterns = [
    path('', views.index, name="index")
]