from django.db import models


class BaseColor(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    
 
# basecolors are children of this
class ColorPattern(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    slug = models.SlugField(max_langth=32, blank=True, null=True)
    basecolors = models.ManyToManyField('BaseColor')
    
    def append(self, basecolor):
        self.basecolors.add(basecolor)
    
    def remove(self, basecolor):
        self.basecolors.remove(basecolor)
    
    @property
    def get_num_basecolors(self):
        return len(self.basecolors)

    
class ClothItem(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    
    colorpatterns = models.ManyToManyField(ColorPattern)
    image=models.ImageField(upload_to=upload_path)
    image_url = models.URLField(null=True, blank=True)
    field = models.DecimalField(max_digits=8, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if self.image_url:
            import urllib, os
            from urlparse import urlparse
            file_save_dir = self.upload_path
            filename = urlparse(self.image_url).path.split('/')[-1]
            urllib.urlretrieve(self.image_url, os.path.join(file_save_dir, filename))
            self.image = os.path.join(file_save_dir, filename)
            self.image_url = ''
        super(tweet_photos, self).save()
 
 # find colorpattern that this basecolor appears in.  

#basecolor.colorpattern_set.all()  # print all colorpatterns with this base color
#ColorPattern.objects.filter(basecolors__name="blue").distinct()

# find clothitem with this colorpattern with these basecolor   
#ClothItem.objects.filter(colorpatterns__name="blueyellowcolor")

# print all cloth items with this colorpattern
#colorpattern.clothitem_set.all()