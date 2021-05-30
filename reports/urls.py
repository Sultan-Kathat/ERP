from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name='index'),
    path("skulabel-25x50", views.sku_label_25x50, name='sku25x50'),
]