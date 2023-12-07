import csv
from core.models import Industry, Sectors

def load_industries():
    with open('industry.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Industry.objects.get_or_create(name=row['name', 'description'])
            
'''
def load_sectors():
    with open('sectors.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            industry = Industry.objects.get(id=row['industry_id'])
            Sectors.objects.get_or_create(name=row['name'], industry=industry)
'''
if __name__ == "__main__":
    load_industries()
    #load_sectors()