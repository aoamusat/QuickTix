import uuid
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from quicktix.models import Ticket
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

# @method_decorator(csrf_exempt, name='post')
class TicketView(View):
    def post(self, request, payment_ref):
        if request.user.is_authenticated:
            ticket = Ticket.objects.create(
                ticket_id=uuid.uuid4(),
                origin=request.POST.get('origin'),
                destination = request.POST.get('destination'),
                ticket_class = request.POST.get('ticket_class'),
                departure_date = request.POST.get('departure_date'),
                cost = request.POST.get('cost'),
                id_type = request.POST.get('id_type'),
                id_number = request.POST.get('id_number'),
                email = request.user.email,
                next_of_kin = request.POST.get('next_of_kin'),
                next_of_kin_contact = request.POST.get('next_of_kin_contact'),
                payment_reference = payment_ref,
                user=request.user,
                payment_status = 'success'
            )
            ticket.save()
            response = {"message": "Ticker created successfully!"}
            return JsonResponse(response, status=201)
        else:
            return JsonResponse({
                'message': "Unauthorized!"
            }, status=401)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)