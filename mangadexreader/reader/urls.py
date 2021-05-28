from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manga_list', views.manga_list, name="manga_list"),
    path('manga/<str:manga_id>/<int:offset>', views.manga, name="manga"),
    path('chapter/<str:chapter_id>/<int:page>', views.chapter, name="chapter")
]