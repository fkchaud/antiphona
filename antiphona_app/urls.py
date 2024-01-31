"""This is where the URLs get routed to Views"""

from django.urls import path

from antiphona_app import views


url_patterns = [
    path('missae/', None, name='missae-index'),
]
