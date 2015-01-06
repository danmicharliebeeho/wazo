import time
from PIL import Image
import math
from collections import Counter


def get_rgb_delta(rgb_a, rgb_b):
    delta_r = abs(rgb_a[0]-rgb_b[0])
    delta_g = abs(rgb_a[1]-rgb_b[1])
    delta_b = abs(rgb_a[2]-rgb_b[2])
    delta_sum = delta_r + delta_g + delta_b
    return delta_sum

def rgb_to_xyz(R, G, B):
    '''
    Convert from RGB to XYZ.
    '''
    var_R = ( R / 255.)
    var_G = ( G / 255.)
    var_B = ( B / 255.)

    if var_R > 0.04045:
        var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_R /= 12.92

    if var_G > 0.04045:
        var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_G /= 12.92
    if var_B > 0.04045:
        var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_B /= 12.92

    var_R *= 100
    var_G *= 100
    var_B *= 100

    #Observer. = 2 deg, Illuminant = D65
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    return X,Y,Z

ref_X =  95.047
ref_Y = 100.000
ref_Z = 108.883

def xyz_to_cielab(X, Y, Z):
    '''
    Convert from XYZ to CIE-L*a*b*
    '''
    var_X = X / ref_X
    var_Y = Y / ref_Y
    var_Z = Z / ref_Z

    if var_X > 0.008856:
        var_X **= ( 1./3. )
    else:
        var_X = ( 7.787 * var_X ) + ( 16. / 116. )
    if var_Y > 0.008856:
        var_Y **= ( 1./3. )
    else:
        var_Y = ( 7.787 * var_Y ) + ( 16. / 116. )
    if var_Z > 0.008856:
        var_Z **= ( 1./3. )
    else:
        var_Z = ( 7.787 * var_Z ) + ( 16. / 116. )

    CIE_L = ( 116 * var_Y ) - 16.
    CIE_a = 500. * ( var_X - var_Y )
    CIE_b = 200. * ( var_Y - var_Z )

    return CIE_L, CIE_a, CIE_b

def rgb_to_cielab(R, G, B):
    '''
    Convert from RGB to CIE-L*a*b*.
    '''
    X,Y,Z = rgb_to_xyz(R,G,B)
    return xyz_to_cielab(X,Y,Z)

def get_distance(a, b):
    return math.pow(a-b, 2)

def get_lab_delta(rgb_a, rgb_b):
    (a_L, a_A, a_B) = rgb_to_cielab(rgb_a[0], rgb_a[1], rgb_a[2])
    (b_L, b_A, b_B) = rgb_to_cielab(rgb_b[0], rgb_b[1], rgb_b[2])
    
    delta = get_distance(a_L, b_L) + get_distance(a_A, b_A) + get_distance(a_B, b_B);
    return math.sqrt(delta);


def convert_rgb_hsv(rgb):
    r, g, b = rgb
    r = float(r) / 255.0
    g = float(g) / 255.0
    b = float(b) / 255.0
    
    Cmax = max(r,g,b)
    Cmin = min(r,g,b)
    delta = float(Cmax) - float(Cmin)
     
    # Hue Calculation
    
    if delta == 0:
        hue = 0
    else:
        if Cmax == r:
            hue = (((g-b) / delta) % 6) * 60.0
        elif Cmax == g:
            hue = (((b-r) / delta) + 2.0) * 60.0
        elif Cmax == b:
            hue = (((r-g) / delta) + 4.0) * 60.0
        
    # Saturation Calculation
    saturation = 0
    if delta != 0:
        saturation = delta / float(Cmax)
    
    # Value Calculation
    value = Cmax
    return hue, saturation, value
 
 
def assign_color_group(color, start_index, value):
    return color + str(start_index) if value > 0.8 else \
        color + str(start_index+1) if value < 0.8 and value > 0.6 else \
        color + str(start_index+2) if value < 0.6 and  value > 0.4 else \
        color + str(start_index+3) if value < 0.6  and value > 0.2 else \
        color + str(start_index+4) if value < 0.2  and value > 0.125 else \
        "black0"

def get_color_group(color,saturation, value):   
    return assign_color_group(color, 0, value) if saturation == 1 else \
                assign_color_group(color, 5, value) if saturation < 1 and saturation > 0.75 else \
                assign_color_group(color, 10, value) if saturation < 0.75 and saturation > 0.5 else \
                assign_color_group(color, 15, value)  if saturation < 0.5 and saturation > 0.25 else \
                assign_color_group(color, 20, value)

def round_to_nearest_thirty(hue):
    mod = hue % 30
    if mod < 15:
        return hue - mod
    else:
        return hue + mod

def get_color_family(hue, saturation, value):
    # Round to nearest 30s
    group_name = ""
    if value < 0.125:  # it's close to black
        group_name = "black0"

    if saturation == 0 or saturation < 0.125:
        if value == 1:
            group_name = "white0"
        if value < 1:
            group_name = assign_color_group("gray", 0, value)
    else:
        group_name = get_color_group("red", saturation, value) if hue == 0 else \
                    get_color_group("yellow-red", saturation, value) if hue == 30 else \
                    get_color_group("yellow", saturation, value) if hue == 60 else \
                    get_color_group("green-yellow", saturation, value) if hue == 90 else \
                    get_color_group("green", saturation, value) if hue == 120 else \
                    get_color_group("cyan-green", saturation, value) if hue == 150 else \
                    get_color_group("cyan", saturation, value) if hue == 180 else \
                    get_color_group("blue-cyan", saturation, value) if hue == 210 else \
                    get_color_group("blue", saturation, value) if hue == 240 else \
                    get_color_group("magenta-blue", saturation, value) if hue == 270 else \
                    get_color_group("magenta", saturation, value) if hue == 300 else \
                    get_color_group("red-magenta", saturation, value)
    
    return group_name


 
def fast_fuzzy_palettes(filename):
    im = Image.open(filename)
    hue_targets = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    color_groups = []
    pixels = list(im.getdata())
    data = Counter(pixels)
    for i in range(0, 10):
        new_data = Counter()
        image_data = data.most_common()
    
        if len(image_data) <= i:
            break
        curr_rgb, curr_count = image_data[i]
        for item in image_data:
            to_rgb = item[0]
            to_count = int(item[1])
            delta_sum = get_lab_delta(curr_rgb, to_rgb)
             
            if curr_rgb != to_rgb:
                if delta_sum < 20:
                    new_data[curr_rgb]= int(curr_count) + int(to_count)
                    curr_count = new_data[curr_rgb]
                else:
                    new_data[to_rgb] =  int(to_count)

        data=new_data
 
    for item in data.keys():
        curr_hue, saturation, value = convert_rgb_hsv((item[0],item[1], item[2]))
         
        normalized_hue = min(hue_targets, key=lambda x:abs(x-curr_hue))

        curr_color_family =  get_color_family(normalized_hue, saturation, value)
        color_groups.append(curr_color_family)
    
    detailed_color_group = Counter(color_groups)
    # strip out the trailing digits to get unique color families
    groups = [i.rstrip('1234567890.') for i in color_groups]
    color_group =  Counter(groups)
    
    # get composition percentage of each color in
    
     
    total_sum = float(sum(color_group.values()))
    for item in color_group:
        new_item = float(color_group[item]) / total_sum * 100.0
        color_group[item] = round(new_item, 2)
    
    
    print detailed_color_group
    print color_group
     
    return detailed_color_group, color_group 

 
  

