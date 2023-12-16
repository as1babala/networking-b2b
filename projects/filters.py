import django_filters
from core.models import *

class ProjectFilter(django_filters.FilterSet):
    #project_category = django_filters.CharFilter(lookup_expr='icontains')
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    #created_month = django_filters.NumberFilter(field_name='created_on', lookup_expr='month')
    #created_month__gt = django_filters.NumberFilter(field_name='created_on', lookup_expr='month__gt')
    #created_month__lt = django_filters.NumberFilter(field_name='created_on', lookup_expr='month__lt')
    
    class Meta:
        model = Projects
        #fields = '__all__'
        fields = ['project_category', 'company_name', 'reviewed', 'approved', 'approved_by']