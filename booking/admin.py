from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip_type', 'created_by', 'total_price', 'status')
    list_filter = ('trip_type', 'status')
    search_fields = ('trip_type', 'status')

admin.site.register(Booking, BookingAdmin)
