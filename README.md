Distinctiveness and Complexity
- This app allows users to register customers and products, then add the products and a single customer to a jobcard.

- Upon submission the jobcard will be created and you will be able to access jobcards that are created in the index view if the user who created the jobcard is logged in.

- There are multiple javascript functions calling to the back end sending and receiving data, updating the user interface as the data is received.

Some examples of the functions mentioned above is for instance, when a user is in the 'view_jobcard' directory, user is able to select a customer in a drop down option. The selections of that dropdown list is customers in the database, selecting a customer sends information to the backend and saving the new customer selected and updating the innerHTML content so that the user can immediately see changes, the page does not need to be reloaded.

Other functions like this is changing the quantities of items in the jobcard when adding and removing items, sending data to the backend and updating quantities and calculating totals accourding to what is currently in the job cards.

The JobcardItem models is a child model for jobcards, we can have a lot of jobcarditems in a single jobcard.

This project has 6 models in the models.py folder 
-User
-Customer
-Product
-Jobcard (with properties to calculate items in jobcard and total value of items in jobcard.)
-JobcardItem (with properties to calculate item totals.)
-JobcardID

Getting started
1. Download the distribution code from https://github.com/me50/IanGrundling/blob/web50/projects/2020/x/capston and unzip it.
2. In your terminal, cd into the IanGrundling-web50-projects-2020-x-capstone directory.
3. Run python manage.py makemigrations jobcards to make migrations for the jobcards app.
4. Run python manage.py migrate to apply migrations to your database.
5. Run python manage.py createsuperuser, enter desired details for super user
6. Run python manage.py runserver
7. Go to http://127.0.0.1:8000/admin and login the superuser
8. Go to Jobcards ids and add a jobcard id, set the number to 1 and save.
9. Go to http://127.0.0.1:8000/ and explore the rest of the app.

Understanding
In the distribution code is a Django project called finalproject with a app called jobcards.

Open jobcards/urls.py, where the URL configuration for this app is defined. Here is all of the urls for this app, index, login, logout, register and various other urls that will be explained later.

Open jobcards/views.py, here is all the views for the project.
1. index - if the user is logged in the index page with the jobacrads the user created will render, else the user will be promted to sign in, or create a account.

2. login_view - if the user is registered they can enter their user name and password and login, if the user is not logged in they can click on 'Don't have a account, register here' to register.

3. logout_view - when the user is logged in, they will see at the top right corner 'logout' if the user click on logout they will be logged out and redirected to the login page.

4. register - user will be able to give a user name, email and password for their account, once the user filled out the fields, user can click on 'register' to register, user will be logged in and redirected to the index view. If the user already have a account they can click on 'Already have a account? Log in here.'

5. register_customer - if a user click on 'Register a Customer' when signed in the user will be able to input details for a customer and register a customer on the database.

6. register_product - if a user click on 'Register a Product' when signed in the user will be able to input details for a product and register a customer on the database.

7. view_customers - if a user click on 'View Customers' the user will be able to see all customers registered in the database, in this view the user will be able to search the customers by name and edit the customers.

8. view_products - if a user click on 'View Products' the user will be able to see all products registered in the database, in this view the user will be able to search the products by name and edit the products and add products to jobcard.

9. edit_customer - this view receives a json object getting the users inputs from the modal form, gets the customer in the database and update the information then sends a json response.

9. edit_product - this view receives a json object getting the users inputs from the modal form, gets the product in the database and update the information then sends a json response.

10. current_jobcard - if the user click on 'View current jobcard' the user can see the current jobcard, if the user added product to the jobcard the products will be displayed in a table under products. The user will be able to change the quantity of items in the jobcard by clicking '+' or '-'. If the user click on '-' and there is only one item, the item will be removed from the jobcard.

11. update_jobcard - handles the add and remove product functionality.

12. select_customer - in the 'View current jobcard' page user is able to select a cutomer from a dropdown list, when the user select a customer the customers information will be displayed if the customer is registered.

13. submit_jobcard - gets all of the information from database and json objects from the front end. get the specific jobcard user is working on and save all the information.

14. view_jobcard - when a user click on the blue text of the jobcard on the index page, user will be able to see all information of that jobcard.

15. search_jobcard - user can search for jobcards by customer name in the search field in the index view.

16. search_product - user can seerch for products by manufacturer in the search field in the view products view.

17. search_customer - user can seerch for customer by manufacturer in the search field in the view customer view.


open jobcards/models.py, here is 6 models for this app, User, Customer, Product, Jobcard, JobcardItem, JobcardId
- User, storing all the users.
- Customer, model for all the customer information.
- Product, model for all the product information.
- Jobcard, model for jobcards, has 2 foreignkey fields, installer(user), customer(customer). This model also have 2 properties, get_item_total and get_jobcard_items to do calculations for the total value of items in jobcard and total number of items.
- JobcardItem, used as a child of jobcard, Items are stored in this model and connecet to jobcard with a foreignkey. This model has one property get_total this returns the a total value, quantity multiplied by the value of the item to get the total value.
- JobcardId when submitting a jobcard this value gets incremented to create a unique Id for all of the jobcards that are created.