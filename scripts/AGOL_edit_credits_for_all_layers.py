from arcgis.gis import GIS
from arcgis.features import FeatureLayer

import country_converter as coco
converter = coco.CountryConverter()

def main():
    #connecting to AGOL
    gis = GIS('home')
    tags_list = ["Country view round 1","Thematic view round 1","Country report round 1","Country findings presentations round 1","Dashboard round 1",
                 "Table properties round 1","Country report round 2","Country findings presentations round 2"]
    creative_commons_string = '<a rel="license" href="https://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>'
    for tag  in tags_list:
        #searching all country layer views (by tag)
        search_results = gis.content.search(query="tags: %s" % tag)

        #looping through each layer for editing properties based on parent ones.
        for layer_view in search_results:
            layer_view_title = layer_view.title
            print(layer_view_title)
            layer_view.update(item_properties={'licenseInfo': creative_commons_string})


if __name__ == "__main__":
    main()