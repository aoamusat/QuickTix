from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.homepage),
    path("features/", view=views.features),
    path("login/", view=views.LoginView.as_view()),
    path("logout/", view=views.logout_user),
    path("dashboard/", view=views.DashboardIndexView.as_view())
]
