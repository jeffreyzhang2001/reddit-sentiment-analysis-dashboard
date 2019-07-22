from django.urls import path
from reddit_sentiment_analyzer import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('analyze_sentiment/', views.analyze_sentiment, name="analyze_sentiment")
]