import django_filters
from core.models import *

class EnterprisesFilter(django_filters.FilterSet):
    industry = django_filters.CharFilter(lookup_expr='icontains')
    sector = django_filters.CharFilter(lookup_expr='icontains')
    company_type = django_filters.CharFilter(lookup_expr='icontains')
    company_country = django_filters.CharFilter(lookup_expr='icontains')
    company_city = django_filters.CharFilter(lookup_expr='icontains')
    #created_month = django_filters.NumberFilter(field_name='created_on', lookup_expr='month')
    #created_month__gt = django_filters.NumberFilter(field_name='created_on', lookup_expr='month__gt')
    #created_month__lt = django_filters.NumberFilter(field_name='created_on', lookup_expr='month__lt')
    
    class Meta:
        model = Enterprises
        #fields = '__all__'
        fields = ['industry', 'sector', 'company_type', 'company_country', 'company_city']