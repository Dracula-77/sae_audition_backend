
from django.urls import path
from AuditionForm import views

urlpatterns = [
    path("", views.frontpage, name='frontpage'),
    path("api/auditionform/", views.AuditionDataView.as_view(), name='Auditiondataview'),
    path("api/register/", views.RegisterUserView.as_view(), name='RegisterUserView'),
    path("api/login/", views.LoginUserView.as_view(), name='LoginUserView'),
    path("api/search/", views.SearchView.as_view(), name='SearchView'),
    path("api/delete/<int:pk>/", views.DeleteObjectView.as_view(), name='DeleteObjectView'),
    # path("api/checkroll/", views.SearchView.as_view(), name='SearchView'),
]
