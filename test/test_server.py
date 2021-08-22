import io
import json
import os

from fastapi.testclient import TestClient
from PIL import Image

from app import server

client = TestClient(server)


def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_get_imagery_preview():
    response = client.get("/imagery/preview.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    image = Image.open(io.BytesIO(response.content))
    assert image.width == 1024
    assert image.height == 774


class TestGetImageryTile:
    dir = os.path.dirname(os.path.realpath(__file__))
    blank_fixture = open(f"{dir}/../app/assets/blank.png", "rb").read()

    def test_get_imagery_tile(self, snapshot):
        response = client.get("/imagery/15/7876/11828.png")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert response.content != self.blank_fixture
        image = Image.open(io.BytesIO(response.content))
        assert image.width == 256
        assert image.height == 256

    def test_get_blank_imagery_tile(self):
        response = client.get("/imagery/10/50/100.png")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert response.content == self.blank_fixture
        image = Image.open(io.BytesIO(response.content))
        assert image.width == 256
        assert image.height == 256


class TestGetTractTile:
    def test_get_tract_tile(self, snapshot):
        response = client.get("/tracts/15/7876/11828.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        snapshot.assert_match(response.text)
        gj = json.loads(response.text)
        assert gj["type"] == "FeatureCollection"

    def test_get_empty_tract_tile(self):
        response = client.get("/tracts/10/50/100.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert json.loads(response.text) == {
            "type": "FeatureCollection",
            "features": [],
        }
