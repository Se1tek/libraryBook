from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/register/', views.event_register, name='event_register'),
    path('events/<int:pk>/unregister/', views.event_unregister, name='event_unregister'),
    path('events/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('api/search/', views.search_api, name='search_api'),
    path('my-events/', views.my_events, name='my_events'),
]
