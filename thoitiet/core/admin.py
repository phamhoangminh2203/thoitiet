from django.contrib import admin
from .models import (
    Province, District, Ward, Location, Station, TideMeasurement, User, Policy
)

admin.site.register(Province)
admin.site.register(District)
admin.site.register(Ward)
admin.site.register(Location)
admin.site.register(Station)
admin.site.register(TideMeasurement)
admin.site.register(User)

admin.site.register(Policy)