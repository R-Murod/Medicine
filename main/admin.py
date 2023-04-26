from django.contrib import admin
from main.models import *


# Register your models here.
class AdminModelSingle(admin.ModelAdmin):
    pass


admin.site.register(Category, AdminModelSingle)
admin.site.register(SubCategory, AdminModelSingle)
admin.site.register(Doctor, AdminModelSingle)
admin.site.register(History, AdminModelSingle)
admin.site.register(SiteUser, AdminModelSingle)
admin.site.register(Email, AdminModelSingle)
admin.site.register(CategoryQuestion, AdminModelSingle)
admin.site.register(Answer)
admin.site.register(QuesModel)
