# fees/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Admin fee management
    path("", views.fee_list, name="fee_list"),
    path("add/", views.fee_create, name="fee_create"),
    path("<int:pk>/edit/", views.fee_update, name="fee_update"),
    path("<int:pk>/delete/", views.fee_delete, name="fee_delete"),

    # Student fee view
    path("my/", views.my_fee, name="my_fee"),
]
