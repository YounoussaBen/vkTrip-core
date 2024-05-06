from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Flight, Location, Stopover, Airline, Ticket
from datetime import timedelta


admin.site.register(Ticket)

class LocationAdmin(admin.ModelAdmin):
    list_display = ['airport_name', 'country']
    search_fields = ['airport_name', 'country']

admin.site.register(Location, LocationAdmin)

class AirlineAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']
    search_fields = ['name', 'logo']

admin.site.register(Airline, AirlineAdmin)

class StepoverForm(forms.ModelForm):
    class Meta:
        model = Stopover
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['duration'].initial = '00:00:00'
class StepoverInline(admin.TabularInline):
    model = Stopover
    form = StepoverForm
    extra = 1

class FlightForm(forms.ModelForm):
    num_tickets = forms.IntegerField(label=_('Number of Available Tickets'), required=True)
    airline = forms.ModelChoiceField(queryset=Airline.objects.all(), label=_('Airline Name'))

    class Meta:
        model = Flight
        fields = '__all__'

class FlightAdmin(admin.ModelAdmin):
    inlines = [StepoverInline]
    autocomplete_fields = ['departure_location', 'arrival_location'] 
    list_display = ['airline', 'departure_location', 'arrival_location', 'departure_datetime', 'flight_duration', 'passenger_type', 'flight_class', 'base_price', 'checked_bag_price', 'available_tickets']
    form = FlightForm

    def save_model(self, request, obj, form, change):
        obj.save()
        num_tickets = form.cleaned_data.get('num_tickets')
        for _ in range(num_tickets):
            obj.tickets.create()

class StepoverAdmin(admin.ModelAdmin):
    autocomplete_fields = ['location']
    search_fields = ['location__airport_name', 'location__country']

admin.site.register(Flight, FlightAdmin)
admin.site.register(Stopover, StepoverAdmin)
