from django.urls import path
from .views import (
    CourseListView, CourseDetailView, UserProductListView,
     )

app_name = "content"

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("myproducts/", UserProductListView.as_view(), name="user-products"),
    path("<slug>/", CourseDetailView.as_view(), name="course-detail"),
    
]
