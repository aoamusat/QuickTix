from django.urls import path

from . import views

app_name = "QuickTix"

urlpatterns = [
    path("", view=views.homepage),
    path("features/", view=views.features),
    path("login/", view=views.LoginView.as_view(), name='user.login'),
    path("register/", view=views.RegisterView.as_view(), name='user.register'),
    path("logout/", view=views.logout_user, name='user.logout'),
    path("dashboard/", view=views.DashboardIndexView.as_view(), name='user.dashboard'),
]