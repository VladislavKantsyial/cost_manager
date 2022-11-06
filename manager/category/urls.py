from django.urls import path
from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
]
