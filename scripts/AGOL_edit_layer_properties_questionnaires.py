from arcgis.gis import GIS
from arcgis.features import FeatureLayer

import country_converter as coco
converter = coco.CountryConverter()

images_urls = {'COL': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data',
              'COD' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data',
              'LBR' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data',
              'MLI' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data',
              'NER' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data',
              'SLE' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data',
              'SOM' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data',
              'ZWE' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/05e7911eae664161b5a2aeb6ce7808d5/data'}

def main():
    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer
    search_results = gis.content.search(query="title: COL Household Questionnaire - Round1")
    reference_iso3 = 'COL'
    
    #getting parent feature layer properties
    parent_feature_layer = search_results[0]
    parent_description = parent_feature_layer.description
    parent_license_info = parent_feature_layer.licenseInfo
    parent_snippet = parent_feature_layer.snippet
    parent_credits = parent_feature_layer.accessInformation

    #searching all country layer views (by tag)
    search_results = gis.content.search(query="tags: Questionnaire round 1")

    #looping through each layer for editing properties based on parent ones.
    for layer_view in search_results:
        layer_view_title = layer_view.title
        print(layer_view_title)
        # getting country ISO3 from title
        layer_view_iso3 = layer_view_title[:3]
        if layer_view_iso3 != reference_iso3:
            # use CountryConverter module for converting ISO3 to official country name
            layer_view_standard_name = converter.convert(names=[layer_view_iso3], src='ISO3', to='name_official') #also 'short_name'
            # edit layer snippet, inserting country name
            layer_view_snippet = parent_snippet.replace('Republic of Colombia', layer_view_standard_name)
            # applying all country properties to layer view
            layer_view.update(item_properties={'accessInformation': parent_credits, 'snippet' : layer_view_snippet, 'description' : parent_description, 'licenseInfo' : parent_license_info}, thumbnail=images_urls[layer_view_iso3])
        else:
            pass

if __name__ == "__main__":
    main()