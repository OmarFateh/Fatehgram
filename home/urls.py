from django.urls import path

from .views import feed_view    

urlpatterns = [
    # feed
    path('', feed_view, name='feed'),
]