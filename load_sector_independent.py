import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'networking.settings')
django.setup()

import pandas as pd
from core.models import *  # Replace 'myapp' with your actual app name

def load_data(csv_file):
    data = pd.read_csv(csv_file)
    for index, row in data.iterrows():
        Sectors.objects.create(industry=row['industry'], name=row['name'], description=row['description'])

if __name__ == "__main__":
    csv_file_path = 'sector_data.csv'  # Update with your CSV file path
    load_data(csv_file_path)