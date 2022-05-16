from django.shortcuts import render
from django.views.generic import FormView
from demo.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.
from demo.models import Product


def catalog(request):
    return render(request, template_name="demo/catalog.html")


def about(request):
    return render(request, template_name="demo/about.html")


def where(request):
    return render(request, template_name="demo/where.html")


def catalog(request):
    products = Product.objects.all()
    return render(request, template_name="demo/catalog.html", context={'products': products})


class LoginView(LoginView):
    success_url = "/login/"

    template_name = "registration/login.html"

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)

class register(FormView):

    form_class = UserCreationForm

    success_url = "/login/"

    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(register, self).form_valid(form)

    def form_invalid(self, form):
        return super(register, self).form_invalid(form)
