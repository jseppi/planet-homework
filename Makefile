.PHONY: start
start: data
	uvicorn app:server

.PHONY: start-dev
start-dev: data
	uvicorn app:server --reload

.PHONY: format
format:
	isort .
	black .

.PHONY: test
test:
	black --check .
	flake8 .
	pytest --cov

data: ./app/assets/homework.gpkg ./app/assets/homework_cog.tiff 

./app/assets/homework.gpkg:
	ogr2ogr -t_srs EPSG:4326 -f GPKG -nln tracts ./app/assets/homework.gpkg ./data/homework.geojson

./app/assets/homework_cog.tiff:
	mkdir -p ./data/tmp
	gdal_translate ./data/homework.tiff ./data/tmp/homework_scaled.tiff -b 1 -b 2 -b 3 -scale 19 7826 0 65535 -exponent 0.4 -co COMPRESS=DEFLATE -co PHOTOMETRIC=RGB
	rio cogeo create ./data/tmp/homework_scaled.tiff ./app/assets/homework_cog.tiff --web-optimized --add-mask --blocksize 256

.PHONY: clean
clean:
	rm -rf ./data/tmp
	rm -rf ./app/assets/homework_cog.tiff
	rm -rf ./app/assets/homework.gpkg
