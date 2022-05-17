from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from demo.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.
from demo.models import Product, Cart


def catalog(request):
    return render(request, template_name="demo/catalog.html")


def about(request):
    return render(request, template_name="demo/about.html")


def where(request):
    return render(request, template_name="demo/where.html")


def product(request, product_pk):
    product_obj = Product.objects.get(pk=product_pk)
    return render(request, template_name="demo/product.html", context={'product': product_obj})


def catalog(request):
    products = Product.objects.all()
    return render(request, template_name="demo/catalog.html", context={'products': products})


@login_required
def cart(request):
    cart_items = Cart.get_by_user(user=request.user).items.all()
    return render(request, template_name="demo/cart.html", context={'cart': cart_items})


@login_required
def cart_add(request, product_pk):
    cart = Cart.get_by_user(user=request.user)
    item = cart.add_item(product_pk=product_pk)
    return JsonResponse({
        'item': {
            'label': item.product.label,
            'count': item.count,
            'price': item.price
        }
    })


@login_required
def cart_del(request, product_pk):
    cart = Cart.get_by_user(user=request.user)
    item = cart.del_item(product_pk=product_pk)
    if not item:
        return JsonResponse({
            'item': None
        })
    else:
        return JsonResponse({
            'item': {
                'label': item.product.label,
                'count': item.count,
                'price': item.price
            }
        })


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
