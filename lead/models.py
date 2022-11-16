from django.db import models
from core.models import BaseModel

class Country(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20,primary_key=True)
    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length =20,primary_key=True)
    country = models.ForeignKey(Country,blank=True,null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length =20,primary_key=True)
    state = models.ForeignKey(State,blank=True,null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Lead(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10,blank=True,null=True)
    country = models.CharField(max_length=20,blank=True,null=True)
    state = models.CharField(max_length=20,blank=True,null=True)
    city = models.CharField(max_length=20,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    message = models.TextField(null=True,blank=True)
    company = models.CharField(max_length=60,blank=True,null=True)
    LEAD_TYPE_CHOICES = (
        ('buyer','Buyer'),
        ('seller','Seller'),
        ('parts','Parts'),
        ('services','Services'),
        ('contact','Contact'),
        ('others','Others')
    )
    lead_type = models.CharField(max_length=10,choices=LEAD_TYPE_CHOICES,default="others",db_index=True)


    # Buyer
    URGENCY_CHOICES = (
        ('now','Immediate'),
        ('1to3','1-3 Months'),
        ('3to6','3-6 Months'),
        ('6to12','6-12 Months'),
        ('12to24','12-24 Months'),
        ('noidea','Dont know yet'),
        ('others','Others'),
    )
    buyer_urgency = models.CharField(max_length=10,choices=URGENCY_CHOICES,default="others",help_text="When do you need the Equipment?")
    buyer_manufacturer_details = models.CharField(max_length=500,blank=True,null=True,help_text="Manufacturer Details")
    buyer_model_details = models.CharField(max_length=500,blank=True,null=True,help_text="Model Details")
    buyer_studies_needed = models.TextField(blank=True,null=True,help_text="What types of studies do you need a system to perform?")

    FACILITY_CHOICES = (
        ('clinic','Clinic'),
        ('hospital','Hospital'),
        ('dia_center','Diagnostic Center'),
        ('others','Others'),
    )
    buyer_facility = models.CharField(max_length=15,choices=FACILITY_CHOICES,help_text="Facility",default="others")
    buyer_budget = models.CharField(max_length=20,null=True,blank=True)

    #Seller
    SELLER_TYPE_CHOICES = (
        ('clinic','Clinic'),
        ('hospital','Hospital'),
        ('eqd','Equipment Dealer'),
        ('fin_ins','Financial Institution'),
        ('ser_com','Service Company'),
        ('OEM','OEM'),
        ('part_supp','Parts Supplier'),
        ('others','Others')
    )
    seller_type = models.CharField(max_length=20,choices=SELLER_TYPE_CHOICES,default="others",help_text="Which of these best describes you?")
    seller_modality = models.CharField(max_length=20,blank=True,null=True)
    seller_manufacturer_details = models.CharField(max_length=500,null=True,blank=True)
    seller_model_details = models.CharField(max_length=500,null=True,blank=True)
    seller_manufacture_date = models.CharField(max_length=15,null=True,blank=True,help_text="Date of Manufacture")
    seller_reason_for_sale=models.TextField(blank=True,null=True,help_text="Describe Your Imaging Project and Reason for Sale")
    SELLER_PROJECT_TIMING = (
        ('now','Immediate'),
        ('1to3','1-3 Months'),
        ('3to6','3-6 Months'),
        ('6to12','6-12 Months'),
        ('12to24','12-24 Months'),
        ('noidea','Dont know yet'),
        ('others','Others'),
    )
    project_timing = models.CharField(max_length=10,choices=SELLER_PROJECT_TIMING,default="others",help_text="Project Timing")
    IS_FUNCTIONAL_CHOICES = (
        ('yes','Yes'),
        ('no','No'),
        ('ins','Installed'),
        ('others','Others'),
    )
    is_functional = models.CharField(max_length=8,choices=IS_FUNCTIONAL_CHOICES,default="others",help_text="Functional")

    #Parts
    part_name = models.CharField(max_length=100,null=True,blank=True)
    part_number = models.CharField(max_length=100,null=True,blank=True)
    PART_URGENCY_CHOICES = (
        ('now','Immediate'),
        ('1to3','1-3 Months'),
        ('3to6','3-6 Months'),
        ('6to12','6-12 Months'),
        ('12to24','12-24 Months'),
        ('noidea','Dont know yet'),
        ('others','Others'),
    )
    part_urgency = models.CharField(max_length=10,choices=PART_URGENCY_CHOICES,default="others",help_text="When do you need the Part?")
    BOOLEAN_CHOICES=(
        ('y','Yes'),
        ('n','No'),
        ('o','Others')
    )
    part_exchange_available = models.CharField(max_length=2,default="O",choices=BOOLEAN_CHOICES)
    part_description = models.TextField(null=True,blank=True)

    #Services
    PACK_CHOICES = (
        ('G','GOLD'),
        ('S','SILVER'),
        ('B','BRONZE'),
        ('O','OTHER')
    )
    services_pack = models.CharField(max_length=2,choices=PACK_CHOICES,default='O')

    def __str__(self):
        return self.name

    @classmethod
    def get_choices(cls):
        return {
            'default':{
                'lead_type':cls.LEAD_TYPE_CHOICES,
                'country':list(Country.objects.values('name','slug',value=models.F('name'))),
                'states':list(State.objects.values('name','slug',value=models.F('name'))),
                'cities':list(City.objects.values('name','slug',value=models.F('name'))),
            },
            'buyer':{
                'urgency':cls.URGENCY_CHOICES,
                'facility':cls.FACILITY_CHOICES,
            },
            'seller':{
                'seller_type':cls.SELLER_TYPE_CHOICES,
                'project_timing':cls.SELLER_PROJECT_TIMING,
                'is_functional':cls.IS_FUNCTIONAL_CHOICES,
            },
            'parts':{
                'urgency':cls.PART_URGENCY_CHOICES,
                'exchange_available':cls.BOOLEAN_CHOICES,
            },
            'services':{
                'pack':cls.PACK_CHOICES
            }
        }
