from django.contrib import admin
from test_app.models import JobSeeker


# Register your models here.
models = [JobSeeker]
admin.site.register(models)