"""This is where models are registered for the admin site"""

from django.contrib import admin
from antiphona_app.models import (
    Anno,
    Antiphona,
    Antiphona_Missa,
    AntiphonaType,
    Documentum,
    Missa,
    MissaType,
    MissaType_AntiphonaType,
    Suggestion,
)


# Register your models here.
admin.site.register(Anno)
admin.site.register(Antiphona)
admin.site.register(Antiphona_Missa)
admin.site.register(AntiphonaType)
admin.site.register(Documentum)
admin.site.register(Missa)
admin.site.register(MissaType)
admin.site.register(MissaType_AntiphonaType)
admin.site.register(Suggestion)
