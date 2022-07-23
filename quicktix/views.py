from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
from django.contrib import messages


User = get_user_model()


# Create your views here.
def homepage(request):
    return render(request, "quicktix/index.html")

def features(request):
   return render(request, "quicktix/features.html")

def logout_user(request):
    logout(request)
    return redirect("/")


class DashboardIndexView(LoginRequiredMixin, View):
    template_name = "quicktix/dashboard.html"
    login_url = "/login"
    redirect_field_name = "next"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class LoginView(View):
    intended = None

    def get(self, request):
        self.intended = (
            request.GET.get("next")
            if request.GET.get("next") is not None
            else "/dashboard"
        )
        if request.user.is_authenticated:
            return redirect(self.intended)
        return render(request, "quicktix/login.html")

    def post(self, request):
        self.intended = (
            request.GET.get("next")
            if request.GET.get("next") is not None
            else "/dashboard"
        )
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.intended)
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("%s" % ("/login"))

class RegisterView(View):
    model = User
    template_name = "quicktix/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/dashboard")
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form = form.clean()
            try:
                user = User.objects.create_user(
                    form.get("email"),
                    form.get("phone"),
                    form.get("first_name"),
                    form.get("last_name"),
                    form.get("password")
                )
            except IntegrityError as e:
                messages.error(request, "Email Already Exists!")
                return redirect(reverse("QuickTix:user.register"))
            try:
                user.save()
                login(request, user)
                return redirect(reverse("QuickTix:user.dashboard"))
            except Exception as e:
                messages.error(request, e)
                return redirect(reverse("QuickTix:user.register"))
        else:
            messages.error(request, form.errors)
            return redirect(reverse("QuickTix:user.register"))