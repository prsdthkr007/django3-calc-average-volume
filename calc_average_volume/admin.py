from django.contrib import admin

# Register your models here.
from .models import AverageVolumeDaily
admin.site.register(AverageVolumeDaily)

from .models import bluechip
admin.site.register(bluechip)