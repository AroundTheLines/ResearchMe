from django.contrib import admin

from .models import Resume, RunningTotal, KeyWord

class ResumeAdmin(admin.ModelAdmin):
    
    list_display = ('__str__', 'sub_date')

admin.site.register(Resume, ResumeAdmin)
admin.site.register(RunningTotal)
admin.site.register(KeyWord)