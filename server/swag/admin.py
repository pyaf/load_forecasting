from django.contrib import admin

# Register your models here.
from .forms import CSVForm
from .models import CSV

class CSVAdmin(admin.ModelAdmin):
    list_display = ["__str__","timestamp","load_value","date"]
    form = CSVForm
    # class Meta:
    #     model = SignUp

admin.site.register(CSV,CSVAdmin)
