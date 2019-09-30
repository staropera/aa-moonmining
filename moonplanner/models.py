from django.db import models
from allianceauth.eveonline.models import EveCorporationInfo, EveCharacter
from evesde.models import EveSolarSystem, EveItem, EveType, EveTypeMaterial


class Moon(models.Model):
    moon = models.OneToOneField(
        EveItem,         
        on_delete=models.CASCADE,
        primary_key=True
    )
    solar_system = models.ForeignKey(
        EveSolarSystem,         
        on_delete=models.DO_NOTHING,        
        null=True, 
        default=None
    )
    income = models.BigIntegerField(
        null=True, 
        default=None
    )    
    
    def name(self):
        return str(self.moon.eveitemdenormalized.item_name)

    def __str__(self):
        return self.name()

    
    def calc_income_estimate(
        self, 
        total_volume, 
        reprocessing_yield, 
        moon_product = None):
        """returns newly calculated income estimate for a given volume in ISK
        
        Args:
            total_volume: total excepted ore volume for this moon
            reprocessing_yield: expected average yield for ore reprocessing
            moon_product(optional): restrict estimation to given moon product

        Returns:
            income estimate for moon or None if prices are missing
        
        """
        income = 0        
        if moon_product is None:
            moon_products = self.moonproduct_set.select_related('ore_type')
        else:
            moon_products = [moon_product]
        try:
            for product in moon_products:
                volume_per_unit = product.ore_type.volume
                volume = total_volume * product.amount
                units = volume / volume_per_unit      
                r_units = units / 100            
                for t in EveTypeMaterial.objects.filter(
                            type=product.ore_type
                        ).select_related('material_type__marketprice'):
                
                    income += (t.material_type.marketprice.average_price
                        * t.quantity
                        * r_units
                        * reprocessing_yield)
        except models.ObjectDoesNotExist:
            income = None

        return income

    class Meta:
        permissions = (
            ('access_moonplanner', 'Can access the moonplanner app'),
            ('research_moons', 'Can research all moons in the database'),
            ('upload_moon_scan', 'Can upload moon scans'),
        )


class MoonProduct(models.Model):
    moon = models.ForeignKey(
        Moon,        
        on_delete=models.CASCADE
    )
    ore_type = models.ForeignKey(
        EveType,         
        on_delete=models.DO_NOTHING,
        null=True, 
        default=None
    )
    amount = models.FloatField()

    def __str__(self):
        return "{} - {}".format(self.ore_type.type_name, self.amount)

    class Meta:
        unique_together = (('moon', 'ore_type'),)
        indexes = [
            models.Index(fields=['moon']),
        ]


class MiningCorporation(models.Model):
    corporation = models.OneToOneField(
        EveCorporationInfo, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    character = models.OneToOneField(
        EveCharacter, 
        on_delete=models.DO_NOTHING, 
        default=None, 
        null=True
    )
    # latest_notification = models.BigIntegerField(null=True, default=0)

    def __str__(self):
        return self.corporation.corporation_name

    @classmethod
    def get_esi_scopes(cls):
        return [
            'esi-industry.read_corporation_mining.v1', 
            'esi-universe.read_structures.v1',
            'esi-characters.read_notifications.v1',
            'esi-corporations.read_structures.v1'
        ]


class Refinery(models.Model):
    structure_id = models.BigIntegerField(primary_key=True)
    moon = models.OneToOneField(
        Moon, 
        on_delete=models.SET_DEFAULT,
        default=None, 
        null=True
    )
    name = models.CharField(max_length=150)    
    corporation = models.ForeignKey(
        MiningCorporation, 
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(EveType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Extraction(models.Model):
    refinery = models.ForeignKey(Refinery, on_delete=models.CASCADE)    
    arrival_time = models.DateTimeField()
    decay_time = models.DateTimeField()
            
    class Meta:
        unique_together = (('arrival_time', 'refinery'),)

    def __str__(self):
        return "{} - {}".format(self.refinery, self.arrival_time)


class ExtrationProduct(models.Model):
    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE)
    ore_type = models.ForeignKey(
        EveType,         
        on_delete=models.DO_NOTHING,
        null=True, 
        default=None
    )
    volume = models.FloatField()

    class Meta:
        unique_together = (('extraction', 'ore_type'),)

    def __str__(self):
        return "{} - {}".format(self.extraction, self.ore_type)


class MarketPrice(models.Model):
    type = models.OneToOneField(
        EveType, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    average_price = models.FloatField(null=True, default=None)
    adjusted_price = models.FloatField(null=True, default=None)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):        
        if not self.average_price is None:
            return "{} {:,.2f}".format(self.type.type_name, self.average_price)
        else:
            return "{} {}".format(self.type.type_name, self.average_price)