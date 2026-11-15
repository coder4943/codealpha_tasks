from django.contrib import admin

from .models import Application, Candidate, Employer, Job

admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(Candidate)
admin.site.register(Application)