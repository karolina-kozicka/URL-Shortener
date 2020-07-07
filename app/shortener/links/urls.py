from django.urls import path

from . import views

app_name = 'links'
urlpatterns = [
    path('', views.LinksListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.LinksDetailView.as_view(), name='detail'),
    path('add/', views.LinksAddView.as_view(), name='add'),
    path('edit/<int:pk>/', views.LinksEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.LinksDeleteView.as_view(), name='delete'),
]