from django.db import models

# Create your models here.

class County(models.Model):
    
    county_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    population_density = models.FloatField()
    capital = models.CharField(max_length=255)
 
    def __str__(self):
        return self.name
  
class Commodity(models.Model):
    commodity_id = models.IntegerField()
    name = models.CharField(max_length=255)
       
    def __str__(self):
        return self.name
    
class Productions(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    year= models.IntegerField()
    quantity_per_area=models.FloatField()
    
    
class CommodityPrices(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    unit_price = models.IntegerField()
    date = models.DateField()

class Climate(models.Model):
    date = models.DateField()
    rainfall=models.FloatField()
    temperature=models.FloatField()
    
class FertilizerImports(models.Model):
    year = models.IntegerField()
    quantity=models.FloatField()
    
class SecurityAndStability(models.Model):
    year = models.IntegerField(null=True)
    index = models.FloatField()  

class AgricultureSpending(models.Model):
    year = models.IntegerField()
    totalexpenditure = models.FloatField()
    agriculturespending = models.FloatField()
