# Planet Tile Server Homework

This repo contains my solution to the homework prompt in `homework.md`.

## Setup

### Dependencies

This project uses [`miniconda`](https://conda.io/en/latest/miniconda) for dependency management and installation. Follow its [installation instructions](https://docs.conda.io/projects/conda/en/4.6.0/user-guide/install/macos.html) to get it installed on your system.

Create a new environment and install project dependencies:

```sh
conda create -n planet-homework python=3.8
conda install -n planet-homework -c conda-forge --file requirements.txt
conda activate planet-homework
```

For local development, you'll also want to install dev packages:

```sh
conda install -n planet-homework -c conda-forge --file requirements-dev.txt
```

### Data preparation

The app expects prepared data files to exist in the `./app/assets/` directory.

See [DATA.md](./DATA.md) for more detailed notes on how the data are prepared.

For a shortcut, follow these steps:

1. Download the homework ZIP and extract its contents.

   Move the extracted `homework.tiff` and `homework.geojson` files into this project's `data/` directory.

2. Run `make data`

## Usage

After Setup is complete, you can start a server at `http://127.0.0.1:8000` with

```sh
make start
```

### API endpoints

#### GET `/imagery/{z}/{x}/{y}.png`

✅ Required

Returns a 256x256 Web-Mercator PNG tile from the COG generated in the data preparation section, for the tile extent specified by the z, x, and y in the request path.

For requests that are out of bounds of the COG data, returns a blank (transparent) PNG.

This route relies primarily on [`rio-tiler`](https://cogeotiff.github.io/rio-tiler/) for extracting the requested tile image from the imagery COG.

#### GET `/tracts/{z}/{x}/{y}.json`

✅ Required

Returns GeoJSON of clipped features from the `tracts` table of the GeoPackage generated in the data preparation section, for the tile extent specified by the z, x, and y in the request path.

For requests that are out of bounds of the `tracts` layer, returns an empty GeoJSON FeatureCollection.

This route relies primarily on [`geopandas`](https://geopandas.org/) for extracting features and clipping them to the bounds of the requested tile.

#### GET `/`

🍬 Bonus

Returns an HTML page that includes a [Leaflet](https://leafletjs.com/) web map. The map has a base layer from Mapbox, and a tile layer that uses the `/imagery/{z}/{x}/{y}.png` endpoint to fetch image tiles.

Clicking the map will load the `/tracts/{z}/{x}/{y}.json` JSON for the tile at the clicked location and current map zoom level.

#### GET `/imagery/preview.png`

🍬 Bonus

Returns a single preview PNG image of the prepared COG file.

## Development

Once Setup is complete, you are ready to start development.

### Dev server

First make sure your conda environment is activated:

```sh
conda activate planet-homework
```

Then start a local auto-reloading server at `http://127.0.0.1:8000`:

```sh
make start-dev
```

The server will reload whenever changes are made to source files.

### Tests

This project uses the [`pytest`](https://docs.pytest.org/en/6.2.x/) framework for tests. Coverage is enforced with `pytest-cov`.

Formatting and linting is done with [`black`](https://black.readthedocs.io/en/stable/) and [`flake8`](https://flake8.pycqa.org/en/latest/).

Run all linters and tests:

```sh
make test
```
