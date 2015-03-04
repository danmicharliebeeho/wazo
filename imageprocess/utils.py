from __builtin__ import True


def analyze_colors(foundcolors):
    is_solid, is_complex_pattern, is_blackandwhite = (False,) * 3
    
    colornames = list(set( [x[0] for x in foundcolors]))
     
    if len(colornames) == 1:
        is_solid = True
    else:
        is_complex_pattern = True
    
    if "black" in colornames and ("white" in colornames or "gray" in colornames):
        is_blackandwhite = True
        
    return is_solid, is_complex_pattern, is_blackandwhite