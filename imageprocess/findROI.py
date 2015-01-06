
from collections import defaultdict
from PIL import Image, ImageDraw


def connected_components(edges):
    """
    Given a graph represented by edges (i.e. pairs of nodes), generate its
    connected components as sets of nodes.

    Time complexity is linear with respect to the number of edges.
    """
    neighbors = defaultdict(set)
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    seen = set()
    def component(node, neighbors=neighbors, seen=seen, see=seen.add):
        unseen = set([node])
        next_unseen = unseen.pop
        while unseen:
            node = next_unseen()
            see(node)
            unseen |= neighbors[node] - seen
            yield node
    return (set(component(node)) for node in neighbors if node not in seen)


def matching_pixels(image, test):
    """
    Generate all pixel coordinates where pixel satisfies test.
    """
    width, height = image.size
    pixels = image.load()
    for x in xrange(width):
        for y in xrange(height):
            if test(pixels[x, y]):
                yield x, y


def make_edges(coordinates):
    """
    Generate all pairs of neighboring pixel coordinates.
    """
    coordinates = set(coordinates)
    for x, y in coordinates:
        if (x - 1, y - 1) in coordinates:
            yield (x, y), (x - 1, y - 1)
        if (x, y - 1) in coordinates:
            yield (x, y), (x, y - 1)
        if (x + 1, y - 1) in coordinates:
            yield (x, y), (x + 1, y - 1)
        if (x - 1, y) in coordinates:
            yield (x, y), (x - 1, y)
        yield (x, y), (x, y)


def boundingbox(coordinates):
    """
    Return the bounding box of all coordinates.
    """
    xs, ys = zip(*coordinates)
    return min(xs), min(ys), max(xs), max(ys)


def disjoint_areas(image, test):
    """
    Return the bounding boxes of all non-consecutive areas
    who's pixels satisfy test.
    """
    for each in connected_components(make_edges(matching_pixels(image, test))):
        yield boundingbox(each)


def is_black_enough(pixel):
    r, g, b = pixel
    
    #return r ==247 and g==246 and b== 246
    return True
#    return r < 10 and g < 10 and b < 10
    

if __name__ == '__main__':

    image = Image.open('/Users/Jamie_Park1/Documents/workspace/roloc/data/sweater.jpg')
    
    width, height = image.size   # Get dimensions
    print width, height
    new_width, new_height= (45,27)
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

  
    
    draw = ImageDraw.Draw(image)
   # draw.rectangle([width/2,height/2,5,40], outline=(255,0,0))
    draw.rectangle(((width/2-22,height/2-13),(width/2 + 30, height/2 + 30)), fill="black", outline = "blue")
    image.show()
