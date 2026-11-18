from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(KeeperVersionChoice)
class KeeperVersionChoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(KeeperRotateDay)
class KKeeperRotateDaysAdmin(admin.ModelAdmin):
    pass

@admin.register(KeeperRotateSetting)
class KeeperRotateSettingAdmin(admin.ModelAdmin):
    pass

@admin.register(KeeperDisplaySetting)
class KeeperDisplaySettingAdmin(admin.ModelAdmin):
    pass

@admin.register(KeeperObjectBasedType)
class KeeperObjectBasedTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(KeeperObject)
class KeeperObjectAdmin(admin.ModelAdmin):
    pass
