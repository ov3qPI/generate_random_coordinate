#!/usr/bin/env python3

import sys
import random
from lxml import etree
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import unary_union

def parse_kml(file_path):
    """
    Parses the KML file and extracts all polygon coordinates.
    Returns a list of Shapely Polygon objects.
    """
    with open(file_path, 'rb') as f:
        tree = etree.parse(f)

    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    polygons = []

    for placemark in tree.findall('.//kml:Placemark', namespaces=ns):
        for polygon in placemark.findall('.//kml:Polygon', namespaces=ns):
            outer_boundary = polygon.find('.//kml:outerBoundaryIs/kml:LinearRing/kml:coordinates', namespaces=ns)
            if outer_boundary is not None:
                coords_text = outer_boundary.text.strip()
                coords = []
                for coord in coords_text.split():
                    lon, lat, *rest = coord.split(',')
                    coords.append((float(lon), float(lat)))
                if len(coords) >= 3:
                    polygons.append(Polygon(coords))
    return polygons

def generate_random_point(union_polygon):
    """
    Generates a random point within the given union of polygons.
    """
    min_x, min_y, max_x, max_y = union_polygon.bounds
    while True:
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if union_polygon.contains(random_point):
            return random_point

def main():
    if len(sys.argv) != 2:
        print("Usage: {} /path/to/file.kml".format(sys.argv[0]))
        sys.exit(1)

    kml_file = sys.argv[1]
    try:
        polygons = parse_kml(kml_file)
    except Exception as e:
        print("Error parsing KML file:", e)
        sys.exit(1)

    if not polygons:
        print("No polygons found in the KML file.")
        sys.exit(1)

    # Combine all polygons into a single MultiPolygon or Polygon
    try:
        combined = unary_union(polygons)
    except Exception as e:
        print("Error combining polygons:", e)
        sys.exit(1)

    if combined.is_empty:
        print("Combined polygon is empty.")
        sys.exit(1)

    # Generate one random point within the combined polygons
    point = generate_random_point(combined)
    print("{:.6f}, {:.6f}".format(point.y, point.x))  # Latitude, Longitude

if __name__ == "__main__":
    main()
