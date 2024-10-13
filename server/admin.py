from django.contrib import admin
from .models import Record,ErrorLog,Site,LocalRecord,LocalErrorLog,LocalSite
# Register your models here.

admin.site.register(Site)
admin.site.register(Record)
admin.site.register(ErrorLog)


admin.site.register(LocalSite)
admin.site.register(LocalRecord)
admin.site.register(LocalErrorLog)