from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.list, name="list"),
    path('create/', views.create, name="create"),
    path('<int:item_id>/update/', views.update, name="update"),
    path('<int:item_id>/delete/', views.delete, name="delete"),
    path('<int:item_id>/complete/', views.complete, name="complete"),
]
