from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Flight, Location, Stepover
from datetime import timedelta

class LocationAdmin(admin.ModelAdmin):
    list_display = ['airport_name', 'country']
    search_fields = ['airport_name', 'country']

admin.site.register(Location, LocationAdmin)

class DurationWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={'placeholder': 'Days'}),
            forms.NumberInput(attrs={'placeholder': 'Hours'}),
            forms.NumberInput(attrs={'placeholder': 'Minutes'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.days, value.seconds // 3600, (value.seconds // 60) % 60]
        return [None, None, None]

class DurationFormField(forms.MultiValueField):
    widget = DurationWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
            forms.IntegerField(),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return timedelta(days=data_list[0], hours=data_list[1], minutes=data_list[2])
        return None

class StepoverForm(forms.ModelForm):
    duration = DurationFormField(required=False)

    class Meta:
        model = Stepover
        fields = '__all__'

class StepoverInline(admin.TabularInline):
    model = Stepover
    form = StepoverForm
    extra = 1

class FlightForm(forms.ModelForm):
    num_tickets = forms.IntegerField(label=_('Number of Available Tickets'), required=True)

    class Meta:
        model = Flight
        fields = '__all__'

class FlightAdmin(admin.ModelAdmin):
    inlines = [StepoverInline]
    autocomplete_fields = ['departure_location', 'arrival_location'] 
    list_display = ['departure_location', 'arrival_location', 'departure_datetime', 'return_datetime', 'base_price', 'checked_bag_price']
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
admin.site.register(Stepover, StepoverAdmin)
