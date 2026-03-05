from django.db import models
from django.db.models import TextField

from django.contrib.auth.models import User,auth

from django.db import models

class Room(models.Model):
    hostel_username_id =models.TextField(blank=True)
    room_number = models.TextField(blank=True)
    total_beds = models.TextField(blank=True)
    created_at = models.TextField(blank=True)

   # def __str__(self):
      #  return f"Room {self.room_number}"


class Bed(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="beds"
    )
    bed_number = models.CharField(max_length=10,blank="True")
    is_occupied = models.BooleanField(default=False,blank="True")
    hostel_username_id =models.TextField(blank=True)

   # def __str__(self):
    #    return f"{self.room.room_number} - Bed {self.bed_number}"

class Student_details(models.Model):
    hostel_username_id =models.TextField(blank=True)

    student_name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    address = models.TextField()

    student_phn_number = models.CharField(max_length=15)
    parent_phn_number = models.CharField(max_length=15)

    room_bed = models.CharField(max_length=20,blank=True)

    joined_date = models.DateField(blank=True)
    advance_amount = models.TextField(blank=True)
    total_fee = models.TextField(blank=True)

    
    #room_bed = models.ForeignKey(Bed,on_delete=models.SET_NULL,null=True,blank=True)





class student_payment(models.Model):
    hostel_username_id=models.TextField(blank=True)
    student_id = models.TextField(blank=True)
    amount_paid=models.TextField(blank=True)
    amountpaid_date=models.TextField(blank=True)
    nothing = models.TextField(blank=True)



class student_payment_add(models.Model):
    hostel_username_id=models.TextField(blank=True)
    student_id = models.TextField(blank=True)
    amount_paid=models.TextField(blank=True)
    amountpaid_date=models.TextField(blank=True)
    nothing = models.TextField(blank=True)

