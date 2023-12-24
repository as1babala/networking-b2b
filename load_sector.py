import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'networking.settings')
django.setup()
import csv
import pandas as pd
from core.models import *  # Replace 'myapp' with your actual app name
from django.db.utils import IntegrityError
import django

django.setup()

def load_sectors_from_csv(csv_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader
        
        for row in reader:
            industry_name = row['industry']
            sector_name = row['name']
            sector_description = row['description']
            
            # Fetch the industry by name
            industry, industry_created = Industry.objects.get_or_create(
                name=industry_name,
                defaults={'description': 'A default description if new industry'}  # Add a default or fetch from somewhere if needed
            )
            
            # Create a new Sector instance
            sector, sector_created = Sectors.objects.get_or_create(
                name=sector_name,
                defaults={
                    'industry': industry,
                    'description': sector_description
                }
            )
            
            if sector_created:
                print(f'Sector "{sector_name}" created for industry "{industry_name}".')
            else:
                # If sector already exists, you might want to update it or just skip.
                print(f'Sector "{sector_name}" already exists for industry "{industry_name}".')

if __name__ == '__main__':
    # Path to your CSV file
    csv_file_path = 'sector_data.csv'
    
    # Call the function to load data
    load_sectors_from_csv(csv_file_path)