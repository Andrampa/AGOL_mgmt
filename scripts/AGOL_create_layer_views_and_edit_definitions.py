## this script is based on the example provided here:
# https://support.esri.com/en/technical-article/000020083
# but it gets an error message in line 18: KeyError: 'spatialReference'

from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

def main():
    layer_name = "Raw Household Data"
    # connecting to AGOL
    gis = GIS('home')

    # searching the parent feature layer
    search_results = gis.content.search(query="title: " + layer_name, item_type="Feature *")[0]
    source_flc = FeatureLayerCollection.fromitem(search_results)

    #create a new layer view
    new_view = source_flc.manager.create_view(name="view_test")

    #seearch the new layer view
    view_search = gis.content.search("view_test")[0]
    view_flc = FeatureLayerCollection.fromitem(view_search)
    service_layer = view_flc.layers[0]

    #apply a query to the layer view
    update_dict = {"viewDefinitionQuery" : "admin0_3isocode is 'SLE'"}
    service_layer.manager.update_definition(update_dict)



if __name__ == "__main__":
    main()