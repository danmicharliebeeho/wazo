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
from core.models import Brand, ProductType, BaseColor, ColorPattern, ClothItem, ColorFamily


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
             #   response = requests.get(full_photo_path)
                
                
                
                
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
                                     percent_off=percent_off, is_designer=True,  \
                                     image_url=full_photo_path)
                  
                if curr_clothitem != None:
                    for available_colors in item['AvailableColors']:
                        color_name = slugify(available_colors['ColorName'])
                        swatchImageUrl = available_colors['swatchImageUrl']
                         
                        #download the swatch image
                        full_swatch_path = "{0}{1}".format(swatchimg_base_url, swatchImageUrl)
                     #   fd_loc = "{0}/{1}.jpg".format(settings.SWATCH_ROOT, color_name)
                      #  urllib.urlretrieve(full_swatch_path, fd_loc)
                      
                        print settings.SWATCH_ROOT
                        colorpattern = None
                        try:
                            colorpattern = ColorPattern.objects.get(name = color_name)
                        except ColorPattern.DoesNotExist:
                            print "colorpattern does not exist"
                            colorpattern = ColorPattern.objects.create(name=color_name, swatch_url=full_swatch_path)
                            
                            # find base colors first
                        start_time = time.time()
                        detailed_color, color_group = fast_fuzzy.fast_fuzzy_palettes(colorpattern.swatch_file)
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
                            print bc
                        print BaseColor.objects.all()
                     
                        
                        #standard colors -> translates to family name
                        standardColors = available_colors['StandardColors']
                        colorfamilies = []
                        for item in standardColors:
                            name = item['StandardColor']
                            colorfamily = None
                            try:
                                colorfamily = ColorFamily.objects.get(name=name)
                            except ColorFamily.DoesNotExist:
                                print "colorfamily does not exist"
                                colorfamily = ColorFamily.objects.create(name=name)
                            if colorfamily != None:
                                colorfamilies.append(colorfamily)
                        
                         
                        
                        print ColorPattern.objects.all()
                        # add this colorpattern to its colorfamilies
                        for item in colorfamilies:
                            item.add_colorpattern(colorpattern)
                            # now assign colorgamily to current clothitem
                            curr_clothitem.add_colorfamilies(item)
                            
                        # add basecolors to this colorpattern
                        for item in basecolors:
                            colorpattern.add_basecolor(item)
                        
                        
                        # now assign colorpattern to current clothitem
                        curr_clothitem.add_colorpatterns(colorpattern)
                        curr_clothitem.save()
                    
                        basecolors = []
                        colorfamilies = []
             
                print '\n'
            except KeyError:
                pass
            break
        print agegroup_set
 
def main():
    
    ns = nordstrom_collector('nordstrom', 'http://www.nordstrom.com')
    url = 'http://shop.nordstrom.com/FashionSearch.axd?category=b2374331&contextualsortcategoryid=0&instoreavailability=false&page=2&pagesize=100&partial=0&shopperSegment=1-0-2%7C6M2%3ARS&sizeFinderId=2&type=category'
    print url
    ns.process_single_page(url, 2)
     
    # {u'PathAlias': u'xscape-beaded-two-piece-satin-ballgown', u'ParentProductTypeDisplayName': u'Dresses', u'OriginalMinimumPrice': 229.0, u'Title': u'Xscape Beaded Two-Piece Satin Ballgown', u'PickUpInStore': True, u'BrandLabelId': 4614, u'GenderName': u'Female', u'Highlight': None, u'IsAvailableInStoreLocally': False, u'New': False, u'AgeGroup': u'A', u'AverageRating': 0.0, u'Available': True, u'IsAvailableInStoreGlobally': False, u'PriceDisplay': {u'PercentOff': None, u'SalePrice': None, u'RegularPrice': u'$229.00'}, u'IsFCAvailable': False, u'MultipleColors': False, u'PercentOff': 0.0, u'BrandLabelName': u'XSCAPE', u'PhotoPath': u'/5/_10273685.jpg', u'ProductTypeDisplayName': u'Dress', u'NumberReviews': 0, u'Gender': u'F', u'IsOutfit': False, u'SpecialTreatmentTypes': 0, u'HighlightStyle': None, u'QuickViewEnabled': True, u'FreeShipping': False, u'SaleType': 0, u'CampaignTier': 0, u'MoreColors': False, u'PickUpInStoreEligible': False, u'MinimumPrice': 229.0, u'VideoMediumUrl': u'', u'ParentProductTypeId': u'1', u'IsDesigner': False, u'AgeGroupName': u'Adult', u'SpriteName': u'3_9997423', u'SkuStores': [], u'InfoDivStyleName': u'info default women adult', u'MultipleViews': True, u'SuppressMoreColorsFlag': 0, u'SuppressPrice': False, u'MaximumPrice': 229.0, u'StyleNumber': u'1021191', u'IsUMAPPED': False, u'IsBeauty': False, u'OriginalMaximumPrice': 229.0, u'AvailableColors': [{u'ColorName': u'WHITE/ CORAL', u'Selected': True, u'productImageUrl': u'/5/_10273685.jpg', u'StandardColors': [{u'StandardColor': u'pink'}], u'swatchImageUrl': u'/3/_9997423.jpg', u'SpriteIndex': 0}], u'CategoryTier': 0, u'MasterRank': 9999999.0, u'Id': 3923672, u'AltPhotoPath': u'/12/_10273672.jpg'}

if __name__ == '__main__':
    main()


"""
http://shop.nordstrom.com/FashionSearch.axd?category=b2374331&contextualsortcategoryid=0&instoreavailability=false&page=2&pagesize=100&partial=0&shopperSegment=1-0-2%7C6M2%3ARS&sizeFinderId=2&type=category
{u'PathAlias': u'june-hudson-floral-print-high-low-wrap-dress', u'ParentProductTypeDisplayName': u'Dresses', u'OriginalMinimumPrice': 78.0, u'Title': u'June & Hudson Floral Print High/Low Wrap Dress', u'PickUpInStore': True, u'BrandLabelId': 8989, u'GenderName': u'Female', u'Highlight': u'NEW!', u'IsAvailableInStoreLocally': False, u'New': True, u'AgeGroup': u'A', u'AverageRating': 4.1, u'Available': True, u'IsAvailableInStoreGlobally': False, u'PriceDisplay': {u'PercentOff': None, u'SalePrice': None, u'RegularPrice': u'$78.00'}, u'IsFCAvailable': False, u'MultipleColors': False, u'PercentOff': 0.0, u'BrandLabelName': u'June & Hudson', u'PhotoPath': u'/18/_10174178.jpg', u'ProductTypeDisplayName': u'Dress', u'NumberReviews': 17, u'Gender': u'F', u'IsOutfit': False, u'SpecialTreatmentTypes': 0, u'HighlightStyle': u'highlight new', u'QuickViewEnabled': True, u'FreeShipping': False, u'SaleType': 0, u'CampaignTier': 0, u'MoreColors': False, u'PickUpInStoreEligible': False, u'MinimumPrice': 78.0, u'VideoMediumUrl': u'/10/_10295950.mp4', u'ParentProductTypeId': u'1', u'IsDesigner': False, u'AgeGroupName': u'Adult', u'SpriteName': u'12_10142232', u'SkuStores': [], u'InfoDivStyleName': u'info new women adult', u'MultipleViews': True, u'SuppressMoreColorsFlag': 0, u'SuppressPrice': False, u'MaximumPrice': 78.0, u'StyleNumber': u'862406', u'IsUMAPPED': False, u'IsBeauty': False, u'OriginalMaximumPrice': 78.0, u'AvailableColors': [{u'ColorName': u'CREAM', u'Selected': True, u'productImageUrl': u'/18/_10174178.jpg', u'StandardColors': [{u'StandardColor': u'offwhite'}], u'swatchImageUrl': u'/12/_10142232.jpg', u'SpriteIndex': 0}], u'CategoryTier': 0, u'MasterRank': 9999999.0, u'Id': 3800814, u'AltPhotoPath': u'/2/_10333662.jpg'}
June & Hudson
/Users/Jamie_Park1/wazo/wazo/swatch
Counter({'yellow20': 2, 'yellow-red15': 2, 'yellow-red13': 2, 'magenta-blue22': 1, 'red17': 1, 'gray1': 1, 'yellow17': 1, 'yellow16': 1, 'yellow21': 1, 'red-magenta20': 1, 'white0': 1, 'red-magenta18': 1, 'yellow15': 1, 'blue-cyan18': 1, 'yellow13': 1, 'yellow-red11': 1, 'gray0': 1, 'cyan22': 1})
Counter({'yellow': 33.33, 'yellow-red': 23.81, 'gray': 9.52, 'red-magenta': 9.52, 'magenta-blue': 4.76, 'cyan': 4.76, 'blue-cyan': 4.76, 'white': 4.76, 'red': 4.76})
fast-fuzzy:--- 0.0260028839111 seconds ---
Counter({'yellow20': 2, 'yellow-red15': 2, 'yellow-red13': 2, 'magenta-blue22': 1, 'red17': 1, 'gray1': 1, 'yellow17': 1, 'yellow16': 1, 'yellow21': 1, 'red-magenta20': 1, 'white0': 1, 'red-magenta18': 1, 'yellow15': 1, 'blue-cyan18': 1, 'yellow13': 1, 'yellow-red11': 1, 'gray0': 1, 'cyan22': 1})
('magenta-blue', '22')
magenta-blue22
('red', '17')
red17
('gray', '1')
gray1
('yellow', '17')
yellow17
('yellow', '16')
yellow16
('yellow', '20')
yellow20
('yellow', '21')
yellow21
('red-magenta', '20')
red-magenta20
('white', '0')
white0
('red-magenta', '18')
red-magenta18
('yellow', '15')
yellow15
('blue-cyan', '18')
blue-cyan18
('yellow', '13')
yellow13
('yellow-red', '11')
yellow-red11
('gray', '0')
gray0
('cyan', '22')
cyan22
('yellow-red', '15')
yellow-red15
('yellow-red', '13')
yellow-red13
[<BaseColor: magenta-blue22>, <BaseColor: red17>, <BaseColor: gray1>, <BaseColor: yellow17>, <BaseColor: yellow16>, <BaseColor: yellow20>, <BaseColor: yellow21>, <BaseColor: red-magenta20>, <BaseColor: white0>, <BaseColor: red-magenta18>, <BaseColor: yellow15>, <BaseColor: blue-cyan18>, <BaseColor: yellow13>, <BaseColor: yellow-red11>, <BaseColor: gray0>, <BaseColor: cyan22>, <BaseColor: yellow-red15>, <BaseColor: yellow-red13>]
colorfamily does not exist
[<ColorPattern: name of color palette: cream >]


Set([])
"""