from django.contrib import admin
from django.db.models import Count
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip_type', 'created_by', 'total_price', 'status')
    list_filter = ('trip_type', 'status')
    search_fields = ('trip_type', 'status')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            num_bookings=Count('status', distinct=True)
        )
        return queryset

    def get_bookings_by_status(self, obj):
        return obj.num_bookings
    get_bookings_by_status.short_description = 'Number of Bookings'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        chart_data = self.get_booking_status_data()
        response.context_data['chart_data'] = chart_data
        return response

    def get_booking_status_data(self):
        queryset = self.get_queryset(None)
        booking_status_data = queryset.values('status').annotate(count=Count('id'))
        chart_data = {
            'labels': [],
            'data': [],
        }
        for data in booking_status_data:
            chart_data['labels'].append(data['status'])
            chart_data['data'].append(data['count'])
        return chart_data

admin.site.register(Booking, BookingAdmin)
