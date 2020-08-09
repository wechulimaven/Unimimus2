from django.contrib import admin
from accounts.models import *
# Register your models here.



@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ["student_name","index_number_year","school","student_name","joined_date","gender"]
    link_display = ["adm_no"]
    list_filter = ['gender', 'joined_date', 'school']

admin.site.register(UserRUCA1)
admin.site.register(UserRUCF1)
admin.site.register(UserRUCF2)
admin.site.register(UserRUM)
admin.site.register(Referees)
