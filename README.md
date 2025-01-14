Generates one random coordinate from a set of polygons in a .kml

This script generates a random coordinate point within the boundaries of polygons defined in a KML file. The script parses the KML file, extracts polygon data, and produces a point that lies within the polygons.

## Requirements

- Python 3
- Required Python libraries:
  - `lxml`
  - `shapely`

You can install the required libraries by running the following command:

```sh
pip install lxml shapely
```

## Notes
- Ensure that the KML file structure adheres to the expected format, specifically with `<Placemark>` and `<Polygon>` tags.
