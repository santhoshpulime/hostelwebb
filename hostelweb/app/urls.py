from django.urls import path
from . import views
import random
from  django.contrib import admin
urlpatterns = [
path('admin/', admin.site.urls),

		path('',views.home,name="home"),
		path('loginpage',views.loginpage,name="loginpage"),

	path('signup_page',views.signup_page,name="signup_page"),

	path('add_room_beds',views.add_room_beds,name="add_room_beds"),
	path('add_student',views.add_student,name="add_student"),
	path('delete_room/<int:id>/',views.delete_room,name="delete_room"),
	path('edit_room/<int:id>/',views.edit_room,name="edit_room"),
	path('studentspage',views.studentspage,name="studentspage"),
	path('delete_student/<int:id>/',views.delete_student,name="delete_student"),
	path('amount_paid/<int:id>/',views.amount_paid,name="amount_paid"),
	path('edit_show_paidamount/<int:id>/',views.edit_show_paidamount,name="edit_show_paidamount"),
  	path('logout/', views.user_logout, name='logout'),
  	  	path('accounts/', views.accounts, name='accounts'),

]
