from django.db import models
from django.conf import settings
from django.core.files import File
import urllib
import os


class Brand(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    def __unicode__(self):
        return self.name

#dress, jeans or jacket, etc
class ProductType(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    def __unicode__(self):
        return self.name
    

class BaseColor(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=False)
    level = models.PositiveSmallIntegerField(blank=True, null=True)
    
    unique_together = ("name", "level")
    
    def __unicode__(self):             
        return self.name + "" + str(self.level)
    
    def get_related_color_patterns(self):
        return self.colorpattern_set.all()
    
    def get_num_of_related_color_patterns(self):
        return self.colorpattern_set.count()


class ColorPattern(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique = True)
    slug = models.SlugField(max_length=32, blank=True, null=True)
    swatch_url = models.URLField(blank=True, null=True)
    swatch_file = models.ImageField(upload_to=settings.SWATCH_ROOT, blank=False)
    
    num_of_colors = models.IntegerField(blank=True, null=True)
    is_solid = models.BooleanField(blank=False, default=False)
    is_complex_pattern = models.BooleanField(blank=False, default=False)
    is_blackandwhite = models.BooleanField(blank=False, default=False)
    known_names = models.CharField(max_length=300, null=True)
    basecolors = models.ManyToManyField(BaseColor)
    
    def __unicode__(self):
        return "name of color palette: %s " % self.name
    
    
    def download_image(self, url):
        if self.swatch_url and not self.swatch_file:
            result = urllib.urlretrieve(self.swatch_url)
            self.swatch_file.save(
                os.path.basename(self.swatch_url),
                File(open(result[0]))
            )
        

    def save(self, *args, **kwargs):
        self.download_image(self.swatch_url)
        super(ColorPattern, self).save(*args, **kwargs)
        
    def add_basecolor(self, basecolor):
        self.basecolors.add(basecolor)
    
    def remove_basecolor(self, basecolor):
        self.basecolor.remove(basecolor)
    
    def get_related_color_families(self):
        return self.colorfamily_set
    
    def get_num_of_related_color_families(self):
        return self.colorfamily_set.count()
    
    def get_related_clothitems(self):
        return self.clothitem_set.all()
    
    def get_num_of_related_clothitems(self):
        return self.clothitem_set.count() 

class ColorFamily(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=False)
    colorpatterns = models.ManyToManyField('ColorPattern')
   
    def __unicode__(self):
        return "name of color family: %s" % self.name
    
    def add_colorpattern(self, colorpattern):
        self.colorpatterns.add(colorpattern)
    
    def remove_colorpattern(self, colorpattern):
        self.colorpatterns.remove(colorpattern)
        
    def get_related_clothitems(self):
        return self.clothitem_set.all()
    
    def get_num_of_related_clothitems(self):
        return self.clothitem_set.count() 
    

class ClothItem(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    path = models.URLField(blank=True, null=True)
    brand = models.ForeignKey('Brand')
    
    colorpatterns = models.ManyToManyField(ColorPattern)
    colorfamilies = models.ManyToManyField(ColorFamily)
    
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
    
    image_file = models.ImageField(upload_to=settings.MEDIA_ROOT)
    image_url = models.URLField(null=True, blank=True)
   
    
    regular_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    percent_off = models.PositiveIntegerField(default=0, blank=True, null=True)    
    
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    is_designer = models.BooleanField(default = False)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
        
    def __unicode__(self):
        return self.name
    
    def download_image(self, url):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                os.path.basename(self.image_url),
                File(open(result[0]))
            )
        

    def save(self, *args, **kwargs):
        self.download_image(self.image_url)
        super(ClothItem, self).save(*args, **kwargs)
        
    
    def add_colorpatterns(self, palette):
        self.colorpatterns.add(palette)
    
    def remove_colorpatterns(self, palette):
        self.colorpatterns.remove(palette)
    
    def add_colorfamilies(self, colorfamily):
        self.colorfamilies.add(colorfamily)
    
    def remove_colorfamilies(self, colorfamily):
        self.colorfamilies.remove(colorfamily)

    @property
    def get_num_palettes(self):
        return len(self.palettes)
    
    def get_all_colorpatterns(self):
        return self.palettes.all()
    
    def get_all_colorfamilies(self):
        return self.colorfamilies.all()
    
    
 # find colorpattern that this basecolor appears in.  

#basecolor.colorpattern_set.all()  # print all colorpatterns with this base color
#ColorPattern.objects.filter(basecolors__name="blue").distinct()

# find clothitem with this colorpattern with these basecolor   
#ClothItem.objects.filter(colorpatterns__name="blueyellowcolor")

# print all cloth items with this colorpattern
#colorpattern.clothitem_set.all()
