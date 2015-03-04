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
import re
from django.conf import settings
from django.core.files.base import ContentFile

from palettes import get_palette, get_dominant_color
from imageprocess import fast_fuzzy, kmeans, findROI, utils
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
                print item
                brand = item['BrandLabelName']
                print brand
                curr_brand, created = Brand.objects.get_or_create(name=brand)
                
                product_type = item['ProductTypeDisplayName']
                curr_prod_type, created = ProductType.objects.get_or_create(name=product_type)
                
                is_designer_str = item['IsDesigner']

                #print brand
                regular_price = item['PriceDisplay']['RegularPrice']
                
                regular_price = Decimal(regular_price.split("$")[-1])
                
                sale_price = item['PriceDisplay']['SalePrice']
                if sale_price != None:
                    sale_price = Decimal(sale_price.split("$")[-1])
                
                percent_off = item['PriceDisplay']['PercentOff']
                if percent_off != None:
                    percent_off = int(percent_off.split("%")[0])
                
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
                        
                        # standard color
                        standarcoors = available_colors['StandardColors']
                        for item in standarcoors:
                            print item['StandardColor']
                        
                      
                        color_name = slugify(available_colors['ColorName'])
                        print "olor name:", color_name
                        swatchImageUrl = available_colors['swatchImageUrl']
                        full_swatch_path = "{0}{1}".format(swatchimg_base_url, swatchImageUrl)
                        print full_swatch_path
                        
                        fd_loc = "{0}/{1}.jpg".format(settings.SWATCH_ROOT, color_name)
                        urllib.urlretrieve(full_swatch_path, fd_loc)
                         
                        # find base colors first
                        start_time = time.time()
                        detailed_color, color_group = fast_fuzzy.fast_fuzzy_palettes(fd_loc)
                        print("fast-fuzzy:--- %s seconds ---" % (time.time() - start_time))
                        print detailed_color
                        split_txt_digits_regex = re.compile("([a-zA-Z\-]+)([0-9]+)")
                        found_colors = [split_txt_digits_regex.match(color).groups() for color in detailed_color]
                        
                        # is_solid_color
                        is_solid, is_complex_pattern, is_blackandwhite = utils.analyze_colors(found_colors)
                        basecolors = []
                        for c in found_colors:
                            print c
                            color_name = c[0]
                            color_level = c[1]
                            bc = None
                            try:
                                bc = BaseColor.objects.get(name=color_name, level=color_level)
                            except BaseColor.DoesNotExist:
                                bc = BaseColor.objects.create(name=color_name, level=color_level)
                            if bc != None:
                                basecolors.append(bc)  
                        
                        print BaseColor.objects.all()
                     
                         
                        
                        print "current color name:", color_name
                        print ColorPattern.objects.all()
                        for c in ColorPattern.objects.all():
                            print "colorpatern:", c.name
                            print "family name:", c.family_name
                        # maybe only top 3, 4?
                        try:
                            colorpattern = ColorPattern.objects.get(basecolors__in=basecolors)
                        except ColorPattern.DoesNotExist:
                            print "colorpattern doesn't exist"
                            colorpattern = ColorPattern.objects.create(name = color_name, num_of_colors = len(basecolors), \
                                             is_solid = is_solid, is_complex_pattern = is_complex_pattern, \
                                             is_blackandwhite = is_blackandwhite)
                            for b in basecolors:
                                colorpattern.append(b)
 
                        curr_clothitem.append(colorpattern)
                        curr_clothitem.save()
                    
              
 
            
                print '\n'
            except KeyError:
                pass
        print agegroup_set
 
def main():
    
    ns = nordstrom_collector('nordstrom', 'http://www.nordstrom.com')
    url = 'http://shop.nordstrom.com/FashionSearch.axd?category=b2374331&contextualsortcategoryid=0&instoreavailability=false&page=2&pagesize=100&partial=0&shopperSegment=1-0-2%7C6M2%3ARS&sizeFinderId=2&type=category'
    print url
    ns.process_single_page(url, 2)
     
    # {u'PathAlias': u'xscape-beaded-two-piece-satin-ballgown', u'ParentProductTypeDisplayName': u'Dresses', u'OriginalMinimumPrice': 229.0, u'Title': u'Xscape Beaded Two-Piece Satin Ballgown', u'PickUpInStore': True, u'BrandLabelId': 4614, u'GenderName': u'Female', u'Highlight': None, u'IsAvailableInStoreLocally': False, u'New': False, u'AgeGroup': u'A', u'AverageRating': 0.0, u'Available': True, u'IsAvailableInStoreGlobally': False, u'PriceDisplay': {u'PercentOff': None, u'SalePrice': None, u'RegularPrice': u'$229.00'}, u'IsFCAvailable': False, u'MultipleColors': False, u'PercentOff': 0.0, u'BrandLabelName': u'XSCAPE', u'PhotoPath': u'/5/_10273685.jpg', u'ProductTypeDisplayName': u'Dress', u'NumberReviews': 0, u'Gender': u'F', u'IsOutfit': False, u'SpecialTreatmentTypes': 0, u'HighlightStyle': None, u'QuickViewEnabled': True, u'FreeShipping': False, u'SaleType': 0, u'CampaignTier': 0, u'MoreColors': False, u'PickUpInStoreEligible': False, u'MinimumPrice': 229.0, u'VideoMediumUrl': u'', u'ParentProductTypeId': u'1', u'IsDesigner': False, u'AgeGroupName': u'Adult', u'SpriteName': u'3_9997423', u'SkuStores': [], u'InfoDivStyleName': u'info default women adult', u'MultipleViews': True, u'SuppressMoreColorsFlag': 0, u'SuppressPrice': False, u'MaximumPrice': 229.0, u'StyleNumber': u'1021191', u'IsUMAPPED': False, u'IsBeauty': False, u'OriginalMaximumPrice': 229.0, u'AvailableColors': [{u'ColorName': u'WHITE/ CORAL', u'Selected': True, u'productImageUrl': u'/5/_10273685.jpg', u'StandardColors': [{u'StandardColor': u'pink'}], u'swatchImageUrl': u'/3/_9997423.jpg', u'SpriteIndex': 0}], u'CategoryTier': 0, u'MasterRank': 9999999.0, u'Id': 3923672, u'AltPhotoPath': u'/12/_10273672.jpg'}

if __name__ == '__main__':
    main()
