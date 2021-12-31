from django.urls import path
from . import views

urlpatterns = [
    path('terrain/', views.terrain, name='projects-terrain'),
    path('cluster/', views.cluster, name='projects-cluster'),
    path('thesis/', views.thesis, name='projects-thesis'),
    path('fpgann/', views.fpgann, name='projects-fpgann'),
    path('stock/', views.stock, name='projects-stock'),
    path('price/', views.price, name='price'),
    path('terrainapp/', views.terrainapp, name='terrainapp'),
]