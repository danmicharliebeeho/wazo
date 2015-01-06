from PIL import Image, ImageFilter
from collections import namedtuple
from math import sqrt
import random
import time
import colorsys

Point = namedtuple('Point', ('color', 'n','ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))
color_code_table = {
                'Black':(0, 0, 0),
                'White':(255, 255, 255),
                'Red':(255, 0, 0),
                'Lime':(0, 255, 0),
                'Blue':(0, 0, 255),
                'Yellow':(255, 255, 0),
                'Cyan/Aqua':(0, 255, 255),
                'Magenta/Fuchsia':(255, 0, 255),
                'Silver':(192, 192, 192),
                'Gray':(128, 128, 128),
                'Maroon':(128, 0, 0),
                'Olive':(128, 128, 0),
                'Green':(0, 128, 0),
                'Purple':(128, 0, 128),
                'Teal':(0, 128, 128),
                'Navy':(0, 0, 128),
                'maroon':(128, 0, 0),
                'darkred':(139, 0, 0),
                'brown':(165, 42, 42),
                'firebrick':(178, 34, 34),
                'crimson':(220, 20, 60),
                'red':(255, 0, 0),
                'tomato':(255, 99, 71),
                'coral':(255, 127, 80),
                'indianred':(205, 92, 92),
                'lightcoral':(240, 128, 128),
                'darksalmon':(233, 150, 122),
                'salmon':(250, 128, 114),
                'lightsalmon':(255, 160, 122),
                'orangered':(255, 69, 0),
                'darkorange':(255, 140, 0),
                'orange':(255, 165, 0),
                'gold':(255, 215, 0),
                'darkgoldenrod':(184, 134, 11),
                'goldenrod':(218, 165, 32),
                'palegoldenrod':(238, 232, 170),
                'darkkhaki':(189, 183, 107),
                'khaki':(240, 230, 140),
                'olive':(128, 128, 0),
                'yellow':(255, 255, 0),
                'yellowgreen':(154, 205, 50),
                'darkolivegreen':(85, 107, 47),
                'olivedrab':(107, 142, 35),
                'lawngreen':(124, 252, 0),
                'chartreuse':(127, 255, 0),
                'greenyellow':(173, 255, 47),
                'darkgreen':(0, 100, 0),
                'green':(0, 128, 0),
                'forestgreen':(34, 139, 34),
                'lime':(0, 255, 0),
                'limegreen':(50, 205, 50),
                'lightgreen':(144, 238, 144),
                'palegreen':(152, 251, 152),
                'darkseagreen':(143, 188, 143),
                'mediumspringgreen':(0, 250, 154),
                'springgreen':(0, 255, 127),
                'seagreen':(46, 139, 87),
                'mediumaquamarine':(102, 205, 170),
                'mediumseagreen':(60, 179, 113),
                'lightseagreen':(32, 178, 170),
                'darkslategray':(47, 79, 79),
                'teal':(0, 128, 128),
                'darkcyan':(0, 139, 139),
                'aqua':(0, 255, 255),
                'cyan':(0, 255, 255),
                'lightcyan':(224, 255, 255),
                'darkturquoise':(0, 206, 209),
                'turquoise':(64, 224, 208),
                'mediumturquoise':(72, 209, 204),
                'paleturquoise':(175, 238, 238),
                'aquamarine':(127, 255, 212),
                'powderblue':(176, 224, 230),
                'cadetblue':(95, 158, 160),
                'steelblue':(70, 130, 180),
                'cornflowerblue':(100, 149, 237),
                'deepskyblue':(0, 191, 255),
                'dodgerblue':(30, 144, 255),
                'lightblue':(173, 216, 230),
                'skyblue':(135, 206, 235),
                'lightskyblue':(135, 206, 250),
                'midnightblue':(25, 25, 112),
                'navy':(0, 0, 128),
                'darkblue':(0, 0, 139),
                'mediumblue':(0, 0, 205),
                'blue':(0, 0, 255),
                'royalblue':(65, 105, 225),
                'blueviolet':(138, 43, 226),
                'indigo':(75, 0, 130),
                'darkslateblue':(72, 61, 139),
                'slateblue':(106, 90, 205),
                'mediumslateblue':(123, 104, 238),
                'mediumpurple':(147, 112, 219),
                'darkmagenta':(139, 0, 139),
                'darkviolet':(148, 0, 211),
                'darkorchid':(153, 50, 204),
                'mediumorchid':(186, 85, 211),
                'purple':(128, 0, 128),
                'thistle':(216, 191, 216),
                'plum':(221, 160, 221),
                'violet':(238, 130, 238),
                'magenta/fuchsia':(255, 0, 255),
                'orchid':(218, 112, 214),
                'mediumvioletred':(199, 21, 133),
                'palevioletred':(219, 112, 147),
                'deeppink':(255, 20, 147),
                'hotpink':(255, 105, 180),
                'lightpink':(255, 182, 193),
                'pink':(255, 192, 203),
                'antiquewhite':(250, 235, 215),
                'beige':(245, 245, 220),
                'bisque':(255, 228, 196),
                'blanchedalmond':(255, 235, 205),
                'wheat':(245, 222, 179),
                'cornsilk':(255, 248, 220),
                'lemonchiffon':(255, 250, 205),
                'lightgoldenrodyellow':(250, 250, 210),
                'lightyellow':(255, 255, 224),
                'saddlebrown':(139, 69, 19),
                'sienna':(160, 82, 45),
                'chocolate':(210, 105, 30),
                'peru':(205, 133, 63),
                'sandybrown':(244, 164, 96),
                'burlywood':(222, 184, 135),
                'tan':(210, 180, 140),
                'rosybrown':(188, 143, 143),
                'moccasin':(255, 228, 181),
                'navajowhite':(255, 222, 173),
                'peachpuff':(255, 218, 185),
                'mistyrose':(255, 228, 225),
                'lavenderblush':(255, 240, 245),
                'linen':(250, 240, 230),
                'oldlace':(253, 245, 230),
                'papayawhip':(255, 239, 213),
                'seashell':(255, 245, 238),
                'mintcream':(245, 255, 250),
                'slategray':(112, 128, 144),
                'lightslategray':(119, 136, 153),
                'lightsteelblue':(176, 196, 222),
                'lavender':(230, 230, 250),
                'floralwhite':(255, 250, 240),
                'aliceblue':(240, 248, 255),
                'ghostwhite':(248, 248, 255),
                'honeydew':(240, 255, 240),
                'ivory':(255, 255, 240),
                'azure':(240, 255, 255),
                'snow':(255, 250, 250),
                'black':(0, 0, 0),
                'dimgray/dimgrey':(105, 105, 105),
                'gray/grey':(128, 128, 128),
                'darkgray/darkgrey':(169, 169, 169),
                'silver':(192, 192, 192),
                'lightgray/lightgrey':(211, 211, 211),
                'gainsboro':(220, 220, 220),
                'whitesmoke':(245, 245, 245),
                'white':(255, 255, 255),
              }



def distance(left,right):
    return sum((l-r)**2 for l, r in zip(left, right))**0.5

def euclidean_distance(rgb1, rgb2):
    color1 = colorsys.rgb_to_hsv(rgb1[0], rgb1[1], rgb1[2])
    color2 = colorsys.rgb_to_hsv(rgb2[0], rgb2[1], rgb2[2])
    avghue = (color1[0] + color2[0])/2
    distance = abs(color1[0]-avghue)
    return distance

class NearestColorKey(object):
    def __init__(self, goal):
        self.goal = goal
    def __call__(self, item):
        return distance(self.goal, item[1])

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w*h):
        points.append(Point(color, 3, count))
    return points


def construct_points(img):
    points = []
    
    points_dict = {}
    w,h = img.size
    last_visited_color_name = None
    last_visited_color_rgb = None
    last_visited_color_dist = 0.0
    max_diff = 0
    for rgb in list(img.getdata()):
            if last_visited_color_rgb != None:
                curr_dist = distance(last_visited_color_rgb, rgb)
                diff = abs(round(curr_dist) - last_visited_color_dist)
                if diff <= 40.0:
                    points_dict[last_visited_color_name]['count'] +=1
                    continue
                
            closest_color = min(color_code_table.items(), key=NearestColorKey(rgb))
            closest_color_name = closest_color[0]
            closest_color_rgb =closest_color[1]
          
            if closest_color_name in points_dict:
                points_dict[closest_color_name]['count'] +=1
                
                if last_visited_color_name == closest_color_name:
                    print "diff:{0}".format(diff)
                    if diff > max_diff:
                        max_diff = diff
            else:
                points_dict[closest_color_name] = {}
                points_dict[closest_color_name]['rgb'] = closest_color_rgb
                points_dict[closest_color_name]['count'] = 1
            last_visited_color_name = closest_color_name
            last_visited_color_rgb = closest_color_rgb
            last_visited_color_dist = round(distance(closest_color_rgb, rgb))
    print "max_diff:{0}".format(max_diff)            
    print "color dictionary"
    print points_dict
    print "length: {0}".format(len(points_dict))
 

 

def euclidean(p1, p2):
#    return sqrt(sum([
#                    (p1.color[i] - p2.color[i]) ** 2 for i in range(p1.n)
#        ]))
    return sum([
                (p1.color[i] - p2.color[i]) ** 2 for i in range(p1.n)
        ])

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.color[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]
    
    while True:
        plists = [[] for i in range(k)]
        
        for p in points:
            smallest_distance = float('Inf')
            idx = None
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            if idx is not None:
                plists[idx].append(p)
        
        diff = 0
        
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))
        
        if diff < min_diff:
            break
    return clusters


rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb)) 

 
def colorz(filename, n=5):
    img = Image.open(filename)
   # img.thumbnail((200,200))
    
    # edges
   # img = img.filter(ImageFilter.FIND_EDGES)
 #   img = img.filter(ImageFilter.BLUR)
   # im1.show()
    
    w,h = img.size
    
    # get background color
    px = img.load()
    background_color =  min(color_code_table.items(), key=NearestColorKey((px[1,1])))
    print "background color name:{0}".format(background_color[0])
    # divide up the picture 
    
    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.color) for c in clusters]
#     i = 0
#     for c in clusters:
#         print 'cluster: %d' % int(i)
#         print 'cluster size %d' % len(c.points)
#         for coord in c.center.color:
#             print int(coord)
# #        print int(c.center.n)
# #        print int(c.center.ct)
#         i = i + 1
#     print rgbs
    for item in rgbs:
        closest_color = min(color_code_table.items(), key=NearestColorKey(item))
        closest_color_name = closest_color[0]
        closest_color_rgb =closest_color[1]
        #print closest_color_name
     
    # construct what? 
    construct_points(img)
    return map(rtoh, rgbs)


    
# rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))
# result = colorz("/Users/Jamie_Park1/Documents/workspace/roloc/data/swatch/00000002.jpg")
# print result
# # ['#f7f6f6', '#ddbe8d', '#a02644']
# elapsed = time.clock()
# elapsed = elapsed - start
# print "Time spent is {0}".format(elapsed)
 