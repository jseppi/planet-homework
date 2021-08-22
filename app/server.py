from os import path

import geopandas
import mercantile
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, Response
from rio_tiler.io import COGReader
from rio_tiler.models import ImageData
from rio_tiler.utils import linear_rescale, render
from shapely.geometry import box


def asset_path(filename: str):
    """
    Returns a path to a file in the assets directory
    """
    parent_dir_path = path.dirname(path.realpath(__file__))
    return f"{parent_dir_path}/assets/{filename}"


def renderPNG(img: ImageData):
    """
    Render the given ImageData to a PNG

    rio-tiler v2.1.0 has a bug where alpha values for uint16 PNGs masks
    are not scaled: https://github.com/cogeotiff/rio-tiler/issues/406
    This has been fixed in v2.1.1, but that version of rio-tiler is
    not currently available on conda-forge.
    """
    # This rescale fixes the issue
    # (taken from https://github.com/cogeotiff/rio-tiler/pull/407):
    mask = linear_rescale(img.mask, (0, 255), (0, 65535)).astype("uint16")
    return render(img.data, mask)


BLANK_TILE = open(asset_path("blank.png"), "rb").read()
TRACTS_GDF = geopandas.read_file(asset_path("homework.gpkg"), layer="tracts")
COG_PATH = asset_path("homework_cog.tiff")

server = FastAPI()


@server.get("/")
async def get_index():
    """
    Returns an HTML index page with a Leaflet map for visualizing data from tile routes.
    """
    return FileResponse(asset_path("index.html"))


@server.get(r"/imagery/preview.png")
async def get_imagery_preview():
    """
    Returns a PNG preview of the COG generated in the data preparation section.
    """
    with COGReader(COG_PATH) as cog:
        img = cog.preview()

    png = renderPNG(img)
    return Response(png, media_type="image/png")


@server.get(r"/imagery/{z}/{x}/{y}.png")
async def get_imagery_tile(z: int, x: int, y: int):
    """
    Returns a 256x256 Web-Mercator PNG tile from the COG generated
    in the data preparation section.
    For requests that are out of bounds, returns a blank (transparent) PNG.
    """
    with COGReader(COG_PATH) as cog:
        # Check if tile is within bounds of cog. Return blank PNG if not.
        if not cog.tile_exists(tile_z=z, tile_x=x, tile_y=y):
            return Response(BLANK_TILE, media_type="image/png")

        img = cog.tile(tile_z=z, tile_x=x, tile_y=y)
        png = renderPNG(img)
        return Response(png, media_type="image/png")


@server.get(r"/tracts/{z}/{x}/{y}.json")
async def get_tract_tile(z: int, x: int, y: int):
    """
    Returns clipped features from the `tracts `table of the GeoPackage generated
    in the data preparation section.
    The bounds are defined by the Web-Mercator Grid and the tile specified
    by z, x, and y in the request.
    For requests that are out of bounds, returns an empty GeoJSON FeatureCollection.
    """
    tile_bounds = mercantile.bounds(x, y, z)
    tile_box = box(*tile_bounds)

    tracts_box = box(*TRACTS_GDF.total_bounds)

    if not tile_box.intersects(tracts_box):
        # We can return early with an empty FeatureCollection
        return JSONResponse({"type": "FeatureCollection", "features": []})

    clipped = geopandas.clip(TRACTS_GDF, tile_box)
    return Response(clipped.to_json(), media_type="application/json")
