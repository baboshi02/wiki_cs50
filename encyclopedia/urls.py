from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry,name="entry"),
    path("search/",views.search,name="search"),
    path("new_page/",views.new_page,name="new_page"),
    path("new_page/create_new_page/",views.create_new_page,name="create_new_page"), 
    path("edit/",views.edit,name="edit"),
    path("save_edit/",views.save_edit,name="save_edit")
]
