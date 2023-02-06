from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register_customer", views.register_customer, name="register_customer"),
    path("register_product", views.register_product, name="register_product"),
    path("view_customers", views.view_customers, name="view_customers"),
    path("view_products", views.view_products, name="view_products"),
    path("edit_customer/<int:id>", views.edit_customer, name="edit_customer"),
    path("edit_product/<int:id>", views.edit_product, name="edit_product"),
    path("current_jobcard", views.current_jobcard, name="current_jobcard"),
    path("select_customer", views.select_customer, name="select_customer"),
    path("update_jobcard", views.update_jobcard, name="update_jobcard"),
    path("submit_jobcard", views.submit_jobcard, name="submit_jobcard"),
    path("view_jobcard/<int:id>", views.view_jobcard, name="view_jobcard"),
    path("search_jobcard", views.search_jobcard, name="search_jobcard"),
    path("search_product", views.search_product, name="search_product"),
    path("search_customer", views.search_customer, name="search_customer")
]