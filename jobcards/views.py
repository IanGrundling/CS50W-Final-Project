from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from .models import User, Customer, Product, Jobcard, JobcardItem, JobcardId

# Create your views here.
def index(request):
        # Authenticated users view their inbox
    if request.user.is_authenticated:
        user = request.user
        jobcard = Jobcard.objects.filter(installer=user).order_by("-timestamp").all()

            # listing 10 posts at a time
        paginator = Paginator(jobcard, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "jobcards/index.html", {
            "jobcard":page_obj
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "jobcards/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "jobcards/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "jobcards/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "jobcards/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "jobcards/register.html")

@login_required
def register_customer(request):
    if request.method == "POST":
        name = request.POST["cust_name"]
        surname = request.POST["cust_surname"]
        number = request.POST["cust_number"]
        email = request.POST["cust_email"]

        # check is customer exist in database
        if Customer.objects.filter(cust_name=name, cust_surname=surname).exists():
            return render(request, "jobcards/register-customer.html", {
                "message": "Customer already exist"
            })

        new_customer = Customer(
            cust_name=name,
            cust_surname=surname,
            cust_number=number,
            cust_email=email
        )

        try:
            new_customer.save()
        except ValueError:
            return render(request, "jobcards/register-customer.html", {
                "message": "Please fill out all fields"
            })
        
        return HttpResponseRedirect(reverse("index"))

    return render(request, "jobcards/register-customer.html")

@login_required
def register_product(request):
    if request.method == "POST":
        manufacturer = request.POST["manufacturer"]
        model = request.POST["model"]
        price = request.POST["price"]

        # check if product exist in database
        if Product.objects.filter(manufacturer=manufacturer, model=model, price=price):
            return render(request, "jobcards/register-customer.html", {
                "message": "Product already exist"
            })

        new_product = Product(
            manufacturer=manufacturer,
            model=model,
            price=price
        )

        try:
            new_product.save()
        except ValueError:
            return render(request, "jobcards/register-customer.html", {
                "message": "Please fill out all fields"
            })
        
        return HttpResponseRedirect(reverse("index"))

    return render(request, "jobcards/register-product.html")

@login_required
def view_customers(request):
    customer = Customer.objects.all().order_by("-timestamp").all()

    # listing 10 posts at a time
    paginator = Paginator(customer, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "jobcards/view-customers.html",{
        "page_obj": page_obj
    })

@login_required
def view_products(request):
    product = Product.objects.all().order_by("-timestamp").all()

    # listing 10 posts at a time
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "jobcards/view-products.html",{
        "page_obj": page_obj
    })

@login_required
def edit_customer(request, id):
    if request.method == "POST":
        # getting json data
        edit_customer_data = json.loads(request.body)

        # getting product in model
        edit_customer = Customer.objects.get(pk=id)

        # updating and saving information
        edit_customer.cust_name = edit_customer_data["name"]
        edit_customer.cust_surname = edit_customer_data["surname"]
        edit_customer.cust_number = edit_customer_data["number"]
        edit_customer.cust_email = edit_customer_data["email"]
        edit_customer.save()

        # sending json response with updated information
        return JsonResponse({
            "message": "Change success", 
            "name": edit_customer_data["name"],
            "surname": edit_customer_data["surname"],
            "number": edit_customer_data["number"],
            "email": edit_customer_data["email"],
            })

@login_required
def edit_product(request, id):
    if request.method == "POST":
        # getting json data
        edit_product_data = json.loads(request.body)

        # getting product in model
        edit_product = Product.objects.get(pk=id)

        # updating and saving information
        edit_product.manufacturer = edit_product_data["manufacturer"]
        edit_product.model = edit_product_data["model"]
        edit_product.price = edit_product_data["price"]
        edit_product.save()

        # sending json response with updated information
        return JsonResponse({
            "message": "Change success", 
            "manufacturer": edit_product_data["manufacturer"],
            "model": edit_product_data["model"],
            "price": edit_product_data["price"]
            })

@login_required
def current_jobcard(request):
    # getting installer to get current open jobcard
    installer = request.user
    customer = Customer.objects.all()
    jobcard, created = Jobcard.objects.get_or_create(installer=installer, complete=False)
    items = jobcard.jobcarditem_set.all()

    # passing information to be displayed on view
    return render(request, "jobcards/current-jobcard.html",{
        "items": items,
        "jobcard": jobcard,
        "customer": customer
    })

@login_required
def update_jobcard(request):
    # getting json data
    add_product_data = json.loads(request.body)
    product_id = add_product_data["id"]
    action = add_product_data["action"]

    # getting jobcard
    installer = request.user
    product = Product.objects.get(id=product_id)
    jobcard, created = Jobcard.objects.get_or_create(installer=installer, complete=False)
    jobcard_item, created = JobcardItem.objects.get_or_create(jobcard=jobcard, product=product)

    # conditional check for add and remove items on jobcard
    if action == 'add':
        jobcard_item.quantity = (jobcard_item.quantity + 1)
    elif action == 'remove':
        jobcard_item.quantity = (jobcard_item.quantity - 1)

    jobcard_item.save()

    if jobcard_item.quantity <= 0:
        jobcard_item.delete()

    # passing information to be displayed on view
    return JsonResponse({
        "message":"Updated jobcard",
        "id": product_id,
        "action": action,
        "product_qty": jobcard_item.quantity,
        "item_price": jobcard_item.get_total,
        "total_price": jobcard.get_item_total,
        "total_items": jobcard.get_jobcard_items
        })

@login_required
def select_customer(request):
    # getting user to get open jobcard
    installer = request.user

    # getting json data
    customer_name_data = json.loads(request.body)
    cust_name = customer_name_data["name"]

    # getting customer information
    customer_obj = Customer.objects.get(cust_name=cust_name)

    # getting jobcard
    jobcard, created = Jobcard.objects.get_or_create(installer=installer, complete=False)

    # saving customer selected
    jobcard.customer = customer_obj
    jobcard.save()

    # passing information to be displayed on view
    return JsonResponse({
        "name": customer_obj.cust_name, 
        "surname": customer_obj.cust_surname,
        "number": customer_obj.cust_number,
        "email": customer_obj.cust_email
    })

@login_required
def submit_jobcard(request):
    if request.method == "POST":
        # getting user to get open jobcard
        installer = request.user

        # getting json data
        description_data = json.loads(request.body)
        description = description_data["description"]

        # creating jobcard
        jobcard, created = Jobcard.objects.get_or_create(installer=installer, complete=False)
        jobcard.description = description
        jobcard.complete = True
        jobcard_id = JobcardId.objects.get()
        jobcard_id.jc_id = ( jobcard_id.jc_id + 1 )
        jobcard_id.save()
        jobcard.jobcard_id = jobcard_id.jc_id

        jobcard.save()
        return JsonResponse({
            "description":description,
            "message": "Jobcard was created"
        })

@login_required
def view_jobcard(request, id):
    # getting jobcard
    jobcard = Jobcard.objects.get(pk=id)

    # getting jobcard items
    jobcard_item = JobcardItem.objects.filter(jobcard=id)
    return render(request, "jobcards/view-jobcard.html", {
        "jobcard": jobcard,
        "jobcard_item": jobcard_item
    })

@login_required
def search_jobcard(request):
    if request.method == "POST":
        searched = request.POST["searched"].capitalize()
        customer = Customer.objects.get(cust_name=searched)
        customer_id = customer.id
        jobcard = Jobcard.objects.filter(customer=customer_id)
        return render(request, "jobcards/search-jobcard.html", {
            "searched": searched,
            "customer": customer,
            "jobcard": jobcard
        })

@login_required
def search_product(request):
    if request.method == "POST":
        searched = request.POST["searched"].capitalize()
        product = Product.objects.filter(manufacturer=searched)
        # listing 10 posts at a time
        paginator = Paginator(product, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "jobcards/search-products.html", {
            "page_obj": page_obj,
            "searched": searched
        })

@login_required
def search_customer(request):
    if request.method == "POST":
        searched = request.POST["searched"].capitalize()
        customer = Customer.objects.filter(cust_name=searched)
        # listing 10 posts at a time
        paginator = Paginator(customer, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "jobcards/search-customer.html", {
            "page_obj": page_obj,
            "searched": searched
        })