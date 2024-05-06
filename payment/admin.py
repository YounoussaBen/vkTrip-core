from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking_id', 'user', 'total_price', 'payment_status', 'timestamp')
    list_filter = ('payment_status', 'timestamp')
    search_fields = ('booking_id__id', 'user__email', 'payment_status')
    readonly_fields = ('id', 'booking_id', 'user', 'total_price', 'payment_status', 'timestamp', 'payment_intent_id', 'payment_method_id', 'card_token')

# Register the Payment model with its admin class
admin.site.register(Payment, PaymentAdmin)