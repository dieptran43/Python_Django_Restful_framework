from django.db import models

class Customer(models.Model):
    customer_name = models.CharField(max_length=256)
    city =models.CharField(max_length=256)
    state =models.CharField(max_length=256)
    address =models.CharField(max_length=256)

    def __str__(self):
        return "{}_{}".format(self.customer_name,self.id)

class Circuit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    circuit_id = models.CharField(max_length=256, unique=True)
    mep_id = models.CharField(max_length=256)
    cir_az = models.IntegerField()
    cir_za = models.IntegerField()

    def __str__(self):
        return self.circuit_id

    def add_site(self, site):
        if self.site_set.count() > 2:
            raise Exception("More than two ip for one circuit !")
        self.site_set.add(site)

class Site(models.Model):
    TYPE_CHOICES=(("A","A"),("Z","Z"))

    circuit =models.ForeignKey(Circuit, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=256)
    hw_version = models.CharField(max_length=256)
    ip_type = models.CharField(max_length=256, choices=TYPE_CHOICES)

    def __str__(self):
        return "circuitIp :{} siteIp :{}".format(self.circuit_fk,self.ip)
