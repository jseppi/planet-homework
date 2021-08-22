# Data Preparation

This file describes the steps and tools used for converting the homework assignment's data files into the desired formats.

## Prerequisites

1. Make sure you have [GDAL](https://gdal.org/) installed and its commands available on your system PATH. Version 3.1+ is recommended.

   On Mac OSX, you can use [homebrew](https://brew.sh/):

   ```sh
   brew install gdal
   ```

2. Install [`rio-cogeo`](https://cogeotiff.github.io/rio-cogeo/). We'll use this for creating the final COG.

   [`miniconda`](https://conda.io/en/latest/miniconda) is what I use to manage dependencies for this project, so the installation command is:

   ```sh
   conda install -c conda-forge rio-cogeo
   ```

3. Download the homework ZIP and extract its contents.

   Move the extracted `homework.tiff` and `homework.geojson` files into this project's `data/` directory.

   The commands described below and in the project `Makefile` assume the source data files are in that directory.

## Making the data

Run `make data`. This will prepare the data files and place the resultant files into `./app/assets/`, where the API application expects them.

If you need to change something with how the data are prepared, you can run `make clean` to delete final and intermediate files. Make adjustments to the process in the `Makefile`, then run `make data` again to run your adjusted commands.

## Notes

These are my notes on the data preparation steps for each file.

### GeoPackage from `homework.geojson`

To prepare the GeoPackage, I used `ogr`.

First I took a look at the provided file using `ogrinfo`:

```sh
ogrinfo ./data/homework.geojson
```

which showed that the file contains a single layer, `tl_2020_27_tract`.

Looking at this layer specifically,

```sh
ogrinfo ./data/homework.geojson tl_2020_27_tract
```

we see that the spatial reference system is "NAD83". This is confirmed when directly inspecting the `homework.geojson` in a text editor, where we can see it has a `crs` of `urn:ogc:def:crs:EPSG::4269`, which is NAD83.

The [current GeoJSON spec](https://datatracker.ietf.org/doc/html/rfc7946) status that GeoJSON should use WGS84, though the previous 2008 spec allowed for alternate reference systems. For better interoperability, I decided to reproject to WGS84 (`EPSG:4326`) when I converted the file to a GeoPackage.

Here's the command I used:

```sh
ogr2ogr -t_srs EPSG:4326 -f GPKG -nln tracts ./app/assets/homework.gpkg ./data/homework.geojson
```

The `-nln tracts` flag names the layer in the GeoPackage "tracts" as instructed in the homework assignment.

### Cloud Optimized GeoTIFF (COG) from `homework.tiff`

To prepare the COG, I first followed Rob Simmon's [_Gentle Introduction to GDAL_](https://medium.com/planet-stories/a-gentle-introduction-to-gdal-part-4-working-with-satellite-data-d3835b5e2971) to make the image more suitable for viewing. I'm not an imagery expert, and I know there are many more techniques for color correction, but I found this guide helpful for quickly producing an image that looked fairly okay.

First, I used `gdalinfo -mm ./data/homework.tiff` to get a sense of the source file.

Here's the part of the output I was most interested in:

```txt
Band 1 Block=256x256 Type=UInt16, ColorInterp=Blue
  Description = blue
    Computed Min/Max=19.000,6014.000
  NoData Value=0
  Overviews: 4656x3391, 1552x1131, 518x377
Band 2 Block=256x256 Type=UInt16, ColorInterp=Green
  Description = green
    Computed Min/Max=116.000,6813.000
  NoData Value=0
  Overviews: 4656x3391, 1552x1131, 518x377
Band 3 Block=256x256 Type=UInt16, ColorInterp=Red
  Description = red
    Computed Min/Max=56.000,7826.000
  NoData Value=0
  Overviews: 4656x3391, 1552x1131, 518x377
Band 4 Block=256x256 Type=UInt16, ColorInterp=Undefined
  Description = nir
    Computed Min/Max=252.000,8335.000
  NoData Value=0
  Overviews: 4656x3391, 1552x1131, 518x377
```

First, we see that there are 4 bands. The first three are blue, green, red, which are what we want for visualizing the image, in the order we want (according to the aforementioned article). The fourth is near infrared (nir), which we don't need so we can get rid of it. The `gdal_translate` flags `-b 1 -b 2 -b 3` will select the first three bands, and leave out the fourth.

Looking at the blue, green, red bands, we can get the total range of values across the three bands. The minimum is `19` and the maximum is `7826`. We'll stretch our image's values, across all three bands, so that they span the possible values of the UINT16 range (0 to 65535). The `gdal_translate` flag `-scale 19 7826 0 65535` will do this stretching. I also used the `-exponent 0.4` flag to do the scaling with a power function, instead of linear. After trying a few values here (Rob uses 0.5), I found `0.4` produced an image that I thought looked the best.

Here's the full `gdal_translate` command I used:

```sh
gdal_translate ./data/homework.tiff ./data/tmp/homework_scaled.tiff -b 1 -b 2 -b 3 -scale 19 7826 0 65535 -exponent 0.4 -co COMPRESS=DEFLATE -co PHOTOMETRIC=RGB
```

Now that I've got an image that visually looks pretty good, I am ready to create the Cloud Optimized GeoTIFF. I used `rio-cogeo` to do this since it includes a web-optimized profile (using the `--web-optimized`) flag.

Here's the `rio-cogeo` command, using the output file from the previous command:

```sh
rio cogeo create ./data/tmp/homework_scaled.tiff ./app/assets/homework_cog.tiff --web-optimized --add-mask --blocksize 256
```

![preview image](/preview.png)
