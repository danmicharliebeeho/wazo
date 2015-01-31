from django.db import models
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

#dress, jeans or jacket, etc
class ProductType(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)


class BaseColor(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    level = models.PositiveSmallIntegerField(blank=True, null=True)
    
    
class ColorPattern(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique = True)
    family_name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    slug = models.SlugField(max_langth=32, blank=True, null=True)
    swatch = models.ImageField(upload_to=settings.SWATCH_ROOT, blank=False)
    
    num_of_colors = models.IntegerField(blank=True, null=True)
    is_solid = models.BooleanField(blank=False, default=False)
    is_complex_pattern = models.BooleanField(blank=False, default=False)
    is_blackandwhite = models.BooleanField(blank=False, default=False)
    known_names = models.CharField(max_length=300, null=True)
    basecolors = models.ManyToManyField(BaseColor)
    
    def append(self, basecolor):
        self.basecolors.add(basecolor)
    
    def remove(self, basecolor):
        self.basecolor.remove(basecolor)

    def __unicode__(self):
        return u"name of color palette: %s " % self.name
    
    @property
    def swatch_url(self):
        return self.swatch.url


    
class ClothItem(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    path = models.URLField(blank=True, null=True)
    brand = models.ForeignKey('Brand')
    
    palettes = models.ManyToManyField(ColorPattern)
    
    has_multiple_colors = models.BooleanField(default=False)
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    AGEGROUP_CHOICES = (
        ('E', 'Teen'),
        ('A', 'Adult'),
    )
    agegroup = models.CharField(max_length=1, choices=AGEGROUP_CHOICES)
    
    photo_path=models.ImageField(upload_to=settings.MEDIA_PATH)
    photo_url = models.URLField(null=True, blank=True)
   
    
    regular_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    percent_off = models.PositiveIntegerField()    
    
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    is_designer = models.BooleanField(default = False)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimefield(auto_now=True)
    
    def append(self, color):
        self.palettes.add(color)
    
    def remove(self, color):
        self.palettes.remove(color)
    
    @property
    def get_num_palettes(self):
        return len(self.palettes)
    
 # find colorpattern that this basecolor appears in.  

#basecolor.colorpattern_set.all()  # print all colorpatterns with this base color
#ColorPattern.objects.filter(basecolors__name="blue").distinct()

# find clothitem with this colorpattern with these basecolor   
#ClothItem.objects.filter(colorpatterns__name="blueyellowcolor")

# print all cloth items with this colorpattern
#colorpattern.clothitem_set.all()
