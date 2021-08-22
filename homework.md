# Take home code test

## Data preparation

There are two attached files that require conversion to a different format.
Document how you converted the files.

 1. `homework.geojson` is a GeoJSON file of Census Tracts. Convert it to a GeoPackage with the table named `tracts`.
 2. `homework.tiff` is a sample TIFF. Convert it to a COG.

## Serving data

Write a REST service using Python or Go that can serve the converted files as tiled data.

The service should provide the following endpoints:

  1. `GET /imagery/<z>/<x>/<y>.png`
    Returns a 256x256 Web-Mercator PNG tile from the COG generated in the data preparation section.
    For requests that are out of bound, return a blank PNG.
  2. `GET /tracts/<z>/<x>/<y>.json`
    Returns clipped features from the `tracts` table in the GeoPackage generated in the data preparation section.
    The bounds are defined by the Web-Mercator Grid and the tile specified by z, x, and y in
    the request.

## Implementation notes

  1. Any design decision not specified herein are open. Completed projects will be evaluated on completeness and cleanliness.
  2. The final project should be shared as a public Git repo. It should include the following:
    * A `README.md` file with enough instructions for setting up and running the project.
    * A `DATA.md` file which documents how the homework files were converted.
    * All of the code and support files for the REST service.
  3. This project is intended to take less than 8 hours. Do not get hung up on scaling or persistence issues. Bonus points for adding comments in the code that recognizes where those problems could occur.
