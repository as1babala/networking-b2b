import django_filters
from core.models import *

class ProductDealsFilter(django_filters.FilterSet):
    #product_category = django_filters.CharFilter(lookup_expr='iexact')
    #city = django_filters.CharFilter(lookup_expr='icontains')
    #country = django_filters.CharFilter(lookup_expr='icontains')
    announcement_date_month = django_filters.NumberFilter(field_name='announcement_date', lookup_expr='month')
    announcement_date_start = django_filters.NumberFilter(field_name='announcement_date', lookup_expr='date__gt')
    announcement_date_end = django_filters.NumberFilter(field_name='announcement_date', lookup_expr='date__lt')
    
    class Meta:
        model = ProductDeals
        
        fields = ['product_category', 'city', 'country', 'announcement_date_start', 'announcement_date_end']
        
    