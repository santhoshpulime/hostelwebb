from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User,auth
from django.http import JsonResponse,HttpResponse
import random
from django.contrib.auth import logout

import datetime
from django.contrib import messages
from .models import student_payment_add

from .models import Room,Bed,Student_details,student_payment,student_payment_add
from datetime import date
def home(request):

    if not request.user.is_authenticated:
        return redirect('loginpage')
  
    return render(request,'home.html')


###login page
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        userdata = auth.authenticate(username=username,password=password)
        if userdata is not None:
            auth.login(request,userdata)
            return redirect('/')
        else:
            messages.info(request,'username and password does not match')
            return redirect('loginpage')
    return render(request,'loginpage.html')


##signup page
def signup_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        
        password = request.POST['password']
        if User.objects.filter(username=username):
            messages.info(request,'username already exists')
            print('already exists')
            return redirect('signup_page')

        else:
            

            usersave = User.objects.create_user(username=username,password=password)
            usersave.save()
            print(username,password)
            return redirect('loginpage')
    return render(request,'signup.html')





def add_room_beds(request):
    if request.method == 'POST':
        room_number = request.POST.get("room_number")
        total_beds = int(request.POST.get("total_beds"))
        ##create room

        room= Room.objects.create(
            room_number=room_number,
            total_beds=total_beds,
            hostel_username_id=request.user.id)

        #create beds automatically
        for i in range(1,total_beds+1):

            Bed.objects.create(
                room=room,
                bed_number=f"B{i}",
                hostel_username_id=request.user.id)
        return redirect("add_room_beds")



    ##getting rooms and beds to show
    room_show = Room.objects.filter(hostel_username_id=request.user.id)
    bed_show  = Bed.objects.filter(hostel_username_id=request.user.id)
    return render(request,'addroom.html',{
        'room_show':room_show,
        'bed_show':bed_show,
        })


#########delete room
def delete_room(request,id):
    room_delete = get_object_or_404(Bed,id=id) 
    room_delete.delete()
    return redirect("add_room_beds")





def add_student(request):
    bed_show  = Bed.objects.filter(hostel_username_id=request.user.id)


    if request.method == "POST":

        student_name = request.POST.get("sudent_name")
        parent_name = request.POST.get("parent_name")
        address = request.POST.get("address")
        student_phn_number = request.POST.get("student_phn_number")
        parent_phn_number = request.POST.get("parent_phn_number")
        room_bed = request.POST.get("student_room_id")
        adv_amount = request.POST.get("advance_amount")
        fee = request.POST.get("total_fee")
        if room_bed:
            bedroom=get_object_or_404(Bed,id=room_bed)
            Student_details.objects.create(
                    student_name=student_name,
                    parent_name=parent_name,
                    address=address,
                    student_phn_number=student_phn_number,
                    parent_phn_number=parent_phn_number,
                    room_bed=bedroom.room.room_number+"-"+bedroom.bed_number,
                    joined_date=date.today(),
                    advance_amount=adv_amount,
                    total_fee=fee,
                    hostel_username_id=request.user.id

        )
            bedroom.is_occupied=True
            bedroom.save()
        else:
            bedroom = None
            Student_details.objects.create(
                    student_name=student_name,
                    parent_name=parent_name,
                    address=address,
                    student_phn_number=student_phn_number,
                    parent_phn_number=parent_phn_number,
                    joined_date=date.today(),
                    advance_amount=adv_amount,
                    total_fee=fee,
                    hostel_username_id=request.user.id

                    )
      

        return redirect("add_student") 

    return render(request, "add_student.html",{'bed_show':bed_show})


##edit room

def edit_room(request, id):
    room = get_object_or_404(Room, id=id)

    if request.method == "POST":
        room.room_number = request.POST.get("room_number")
        room.total_beds = request.POST.get("total_beds")
        room.save()
        return redirect("home")   # change to your page

    return render(request, "edit_room.html", {"room": room})






##########students page
def studentspage(request):
    student_details= Student_details.objects.filter(hostel_username_id=request.user.id)
    students_paid_amount=student_payment_add.objects.filter(hostel_username_id=request.user.id)
    
    return render(request,'studentspage.html',{'student_details':student_details,'students_paid_amount':students_paid_amount})


######delete student
def delete_student(request,id):
    student_delete= get_object_or_404(Student_details,id=id)
    student_delete.delete()
    return redirect("studentspage")


#####amount paid
def amount_paid(request,id):
    if request.method == 'POST':
        hostel_username_id=request.user.id
        student_id = request.POST.get('student_id')
        amount_paid = request.POST.get('amount')
        amountpaid_date = date.today()
        student_payment_add.objects.create(
            hostel_username_id=hostel_username_id,
            student_id=student_id,
            amount_paid=amount_paid,
            amountpaid_date=amountpaid_date
            ).save()
        print("data saved")
    return redirect("studentspage")


####show paid amount
def edit_show_paidamount(request, id):
    bed_show  = Bed.objects.filter(hostel_username_id=request.user.id)

    student = Student_details.objects.get(id=id)
    if request.method == "POST":
        student.student_name = request.POST.get("student_name")
        student.parent_name = request.POST.get("parent_name")
        student.student_phn_number = request.POST.get("student_phn_number")
        student.parent_phn_number = request.POST.get("parent_phn_number")
        student.address = request.POST.get("address")
        room_bed_stu = request.POST.get("room_bed")
        student.advance_amount = request.POST.get("stu_adv")
        student.total_fee = request.POST.get("total_fee")
        if room_bed_stu.isdigit():
            
            bedroom=get_object_or_404(Bed,id=room_bed_stu)
            student.room_bed=bedroom.room.room_number+"-"+bedroom.bed_number

            student.save()
            bedroom.is_occupied=True
            bedroom.save()
        else:
            student.room_bed=room_bed_stu
            student.save()

        return redirect('edit_show_paidamount', id=student.id)
    payment_history = student_payment_add.objects.filter(student_id=id)
    student_advance = Student_details.objects.filter(id=id)
    total_paid = 0
    for i in payment_history:
        total_paid += int(i.amount_paid)
    stu_adv = student.advance_amount
    if stu_adv =="":
        stu_adv=0
        total_fee_paid = int(total_paid)+int(stu_adv)

    else:

        total_fee_paid = int(total_paid)+int(stu_adv)
    student_total_fee = student.total_fee
    if student_total_fee == '':
        student_total_fee=0
        remaning_amount=int(student_total_fee)-int(total_fee_paid)

    else:
        remaning_amount=int(student_total_fee)-int(total_fee_paid)


    return render(request, 'edit_show_paidamount.html', {
        'student': student,
        'payment_history': payment_history,
        'total_paid': total_paid,
        'bed_show':bed_show,
        'total_fee_paid':total_fee_paid,
        'remaning_amount':remaning_amount
    })





def user_logout(request):
    logout(request)
    return redirect('loginpage')  # redirect to login page



####accounts
def accounts(request):
    payments=student_payment_add.objects.filter(hostel_username_id=request.user.id)
    total = 0
    for i in payments:
        try:

            total+=int(i.amount_paid)
        except:
            pass
    advance_payments = Student_details.objects.filter(hostel_username_id=request.user.id)
    adv_total = 0
    for a in advance_payments:
        try:
            adv_total+=int(a.advance_amount)
        except:
            pass 

    return render(request,'accounts.html',{
        'payments':payments,
        'total':total,
        'advance_payments':advance_payments,
        'adv_total':adv_total,
        'grandtotal':total+adv_total,
        })

