from django.db import models

# Create your models here.
# import datetime
class CSV(models.Model):
    timestamp = models.TimeField()
    load_value = models.FloatField()
    date = models.DateField()
    # statecode = models.CharField(max_length=2)
    # statename = models.CharField(max_length=32)
    # date = models.DateField('27-08-2017')


    def __str__(self):
        return "yes"


# class SignUp(models.Model):
#     email = models.EmailField()
#     full_name = models.CharField(max_length = 120,blank=True,null=True)
#     timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated = models.DateTimeField(auto_now_add=False,auto_now=True)
#     mob_no = models.CharField(max_length = 12)
#
#
#
#     def __str__(self):
#         return self.email
