import urllib2
import json

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
        for item in data['Fashions']:
            try:
                count = count + 1
                print count
                brand = item['BrandLabelName']
                print brand
                regular_price = item['PriceDisplay']['RegularPrice']
                sale_price = item['PriceDisplay']['SalePrice']
                percent_off = item['PriceDisplay']['PercentOff']
                
                path_alias = item['PathAlias']
                photo_path = item['PhotoPath']
                alt_photo_path = item['AltPhotoPath']
                
                has_multiple_colors = item['MultipleColors']
                gender =item['Gender']
                agegroup_name = item['AgeGroupName']
                product_type = item['ProductTypeDisplayName']
                item_name = item['Title']
                print item_name
                
                for available_colors in item['AvailableColors']:
                    for curr in available_colors['StandardColors']:
                        print curr
                print '\n'
            except KeyError:
                pass
 
def main():
    
    ns = nordstrom_collector('nordstrom', 'http://www.nordstrom.com')
    url = 'http://shop.nordstrom.com/FashionSearch.axd?category=b2374331&contextualsortcategoryid=0&instoreavailability=false&page=2&pagesize=100&partial=0&shopperSegment=1-0-2%7C6M2%3ARS&sizeFinderId=2&type=category'
    ns.process_single_page(url, 2)
    
if __name__ == '__main__':
    main()
