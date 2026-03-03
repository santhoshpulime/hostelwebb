from django.contrib import admin

from .models import Room, Bed,Student_details,student_payment_add

admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(Student_details)
admin.site.register(student_payment_add)
