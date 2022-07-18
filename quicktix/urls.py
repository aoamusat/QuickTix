from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.homepage),
    path("features/", view=views.features),
    path("login/", view=views.login),
    path("dashboard/", view=views.dashboard)
]
