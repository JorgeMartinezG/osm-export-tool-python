import osm_export_tool
import osm_export_tool.tabular as tabular
import osm_export_tool.nontabular as nontabular
from osm_export_tool.mapping import Mapping
from osm_export_tool.geometry import load_geometry
from osm_export_tool.sources import Overpass, File

GEOJSON = """{
	"type": "Polygon",
    "coordinates": [
    	[
            [-155.077815, 19.722514],
            [-155.087643, 19.722514],
            [-155.087643, 19.715929],
            [-155.077815, 19.715929],
            [-155.077815, 19.722514]
		]
	]
}"""

geom = load_geometry(GEOJSON)
tempdir = 'tmp'
source = Overpass('http://overpass.hotosm.org',geom,'overpass.osm.pbf',tempdir=tempdir)

with open('../osm_export_tool/mappings/default.yml','r') as f:
	mapping_txt = f.read()
mapping = Mapping(mapping_txt)

shp = tabular.Shapefile("tmp/blah",mapping)
gpkg = tabular.Geopackage("tmp/blah",mapping)
kml = tabular.Kml("tmp/blah",mapping)
tabular_outputs = [shp,gpkg,kml]

h = tabular.Handler(tabular_outputs,mapping)

h.apply_file(source.path(), locations=True, idx='sparse_file_array')

for output in tabular_outputs:
	output.finalize()

nontabular.Osmand(source.path(),'tools/OsmAndMapCreator-main',tempdir=tempdir).run()
nontabular.Garmin(source.path(),'tools/splitter-r583/splitter.jar','tools/mkgmap-r3890/mkgmap.jar',tempdir=tempdir).run()