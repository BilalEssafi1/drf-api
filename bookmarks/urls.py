from django.urls import path
from bookmarks import views

urlpatterns = [
    path('folders/', views.BookmarkFolderList.as_view()),
    path('folders/<int:pk>/', views.BookmarkFolderDetail.as_view()),
    path('bookmarks/', views.BookmarkList.as_view()),
    path('bookmarks/<int:pk>/', views.BookmarkDetail.as_view()),
]