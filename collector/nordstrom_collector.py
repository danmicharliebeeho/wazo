import urllib
import urllib2
import os
import json
from sets import Set
from decimal import Decimal
from PIL import Image 
from slugify import slugify
import time
import requests

from django.conf import settings
from django.core.files.base import ContentFile

from palettes import get_palette, get_dominant_color
from imageprocess import fast_fuzzy, kmeans, findROI
from core.models import Brand, ProductType, BaseColor, ColorPattern, ClothItem

class Collector(object):
    urls_to_visit = {}
    urls_visited = {}
    store_name = ''
    store_url = ''
    
    def __init__(self, store_name, store_url):
        self.store_name = store_name
        self.store_url = store_url
    
    def collect_urls(self):
        pass
    
class nordstrom_collector(Collector):
    
    
    
    def process_single_page(self, url, page_id):
        response = urllib2.urlopen(url)
        data = json.load(response)
        count = -1
        prod_base_url = "http://shop.nordstrom.com/s"
        mediumimg_base_url = "http://g.nordstromimage.com/imagegallery/store/product/Medium"
        swatchimg_base_url = "http://g.nordstromimage.com/imagegallery/store/product/SwatchSmall"
        agegroup_set = Set([])
        for item in data['Fashions']:
            try:
                count = count + 1
                #print count
                item_name = item['Title']
                
                brand = item['BrandLabelName']
                curr_brand = Brand.objects.get_or_create(name=brand)
                
                product_type = item['ProductTypeDisplayName']
                curr_prod_type = ProductType.objects.get_or_create(name=product_type)
                
                is_designer_str = item['IsDesigner']
                is_designer=False
                if is_designer == "true":
                    is_designer=True
                #print brand
                regular_price = item['PriceDisplay']['RegularPrice']
                regular_price = Decimal(regular_price.strip("$"))
                
                sale_price = item['PriceDisplay']['SalePrice']
                sale_price = Decimal(sale_price.strip("$"))
                
                percent_off = item['PriceDisplay']['PercentOff']
                percent_off = int(percent_off.strip("%"))
                
                photo_path = item['PhotoPath']
                full_photo_path = "{0}/{1}".format(mediumimg_base_url, photo_path)
                response = requests.get(full_photo_path)
                
                
                alt_photo_path = item['AltPhotoPath']
                full_alt_photo_path = "{0}/{1}".format(mediumimg_base_url, alt_photo_path)
                
                 
                 
                
                gender =item['Gender']
                
                agegroup = item['AgeGroup']
                path_alias = item['PathAlias']
                product_id = item['Id']
                # make full URL of this product
                full_prod_url = "{0}/{1}/{2}".format(prod_base_url, path_alias, product_id )
               
               # find a ClothItem with the same url, the name of the item could be duplicate, ex: red shirt
               curr_clothitem = None
               try:
                   curr_clothitem = ClothItem.objects.get(path=full_prod_url)
               except ClothItem.DoesNotExist:
                   curr_clothitem = ClothItem.objects.create(name=item_name, path=full_prod_url, brand=curr_brand, \
                                     gender=gender, agegroup=agegroup, regular_price=regular_price, sale_price=sale_price,\
                                     percent_off=percent_off, is_designer=True, photo_path=ContentFile(response.content), \
                                     photo_url=full_photo_path)
                  
               if curr_clothitem != None:
                    for available_colors in item['AvailableColors']:
                          print available_colors['ColorName']
                        color_name = slugify(available_colors['ColorName'])
                     
                         swatchImageUrl = available_colors['swatchImageUrl']
                         full_swatch_path = "{0}{1}".format(swatchimg_base_url, swatchImageUrl)
                         print full_swatch_path
                        
                         fd_loc = "{0}/{1}.jpg".format(settings.SWATCH_ROOT, color_name)
                         urllib.urlretrieve(full_swatch_path, fd_loc)
                         
                         # find base colors first
                         start_time = time.time()
                         found_colors = fast_fuzzy.fast_fuzzy_palettes(fd_loc)
                         print("fast-fuzzy:--- %s seconds ---" % (time.time() - start_time))
                         
                         basecolors = []
                         for c in found_colors:
                             bc = BaseColor.objects.get(name=c)
                             basecolors.append(bc)
                         
                         # is_solid_color
                        is_solid, is_complex_pattern, is_blackandwhite = analyze_colors(basecolors)
                        # maybe only top 3, 4?
                        try:
                             colorpattern = ColorPattern.objects.get(basecolors__in=basecolors)
                        except ColorPattern.DoesNotExist:
                             colorpattern = ColorPattern.objects.create(name = color_name, num_of_colors = len(basecolors), \
                                             is_solid = is_solid, is_complex_pattern = is_complex_pattern, \
                                             is_blackandwhite = is_blackandwhite)
                             for b in basecolors:
                                  colorpattern.append(b)
                         # if this colorn pattern doesn't exist
                         
                         curr_clothitem.append(colorpattern)
                         
                    
                    #start_time = time.time()
                    #with get_palette(filename=fd_loc, color_count=3) as palette:
                    #    print palette
                    #print("color-thief:--- %s seconds ---" % (time.time() - start_time))
                    
                    # get dominant colors by kmeans
                    #start_time = time.time()
                    #kmeans.colorz(fd_loc)
                    #print("kmeans: --- %s seconds ---" % (time.time() - start_time))
                    
                    # get dominant colors by fast fuzzy
                     
                     
                    num_standard_colors = len(available_colors['StandardColors'])
                    
                    
                    
                    #if num_standard_colors > 1:
                    #    print "num of standard colors: %d" % len(available_colors['StandardColors'])
                        #for curr in available_colors['StandardColors']:
                        #    print curr
                
                  #  for curr in available_colors['StandardColors']:
                   #     print curr
                print '\n'
            except KeyError:
                pass
        print agegroup_set
 
def main():
    
    ns = nordstrom_collector('nordstrom', 'http://www.nordstrom.com')
    url = 'http://shop.nordstrom.com/FashionSearch.axd?category=b2374331&contextualsortcategoryid=0&instoreavailability=false&page=2&pagesize=100&partial=0&shopperSegment=1-0-2%7C6M2%3ARS&sizeFinderId=2&type=category'
    print url
    ns.process_single_page(url, 2)
     
    
if __name__ == '__main__':
    main()
