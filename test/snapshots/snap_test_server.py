# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "TestGetTractTile.test_get_tract_tile 1"
] = '{"type": "FeatureCollection", "features": [{"id": "75", "type": "Feature", "properties": {"ALAND": 74775280, "AWATER": 3224613, "COUNTYFP": "139", "FUNCSTAT": "S", "GEOID": "27139081001", "INTPTLAT": "+44.6668232", "INTPTLON": "-093.4500515", "MTFCC": "G5020", "NAME": "810.01", "NAMELSAD": "Census Tract 810.01", "STATEFP": "27", "TRACTCE": "081001"}, "geometry": {"type": "Polygon", "coordinates": [[[-93.4716796875, 44.676465648659644], [-93.4716796875, 44.68427737181224], [-93.460693359375, 44.68427737181224], [-93.460693359375, 44.676465648659644], [-93.4716796875, 44.676465648659644]]]}}]}'
