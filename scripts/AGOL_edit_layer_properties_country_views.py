from arcgis.gis import GIS
from arcgis.features import FeatureLayer

import country_converter as coco
converter = coco.CountryConverter()

images_urls = {'AFG': 'https://cloud.githubusercontent.com/assets/7389593/20107607/1d2c3844-a5a7-11e6-9ec0-9e389033ccd8.jpg',
               'COL': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/9734c572ab5c4dc09b1c12887c42c633/data',
              'COD' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/70dd8165fdbf4833b81794a8cbba0bae/data',
              'LBR' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/eb7329eca6e64b29a0d8b90416e4557a/data',
              'MLI' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/f07376174a884649881d5d0dec047812/data',
              'NER' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/cb1b47c711be40d2b14bc81cbb268c13/data',
              'SLE' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/482e512295de4f98aeb7349dd841a798/data',
              'SOM' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/da1233e24726490dbfd8335284b1f928/data',
              'YEM' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/ae3d8ae9628a41cf9a93dab7fdb4f12c/data',
               'ZWE': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/defb0b94744142d0b364a6150c6eedda/data'
               }

def main():
    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer
    search_results = gis.content.search(query="title: Raw Household Data", item_type="Feature *",
                                    max_items=150)
    
    #getting parent feature layer properties
    parent_feature_layer = search_results[0]
    parent_description = parent_feature_layer.description
    parent_license_info = parent_feature_layer.licenseInfo
    parent_title = parent_feature_layer.title
    parent_snippet = parent_feature_layer.snippet
    parent_credits = parent_feature_layer.accessInformation
    parent_categories = parent_feature_layer.categories
    parent_table = parent_feature_layer.tables[0]
    parent_table_properties = parent_table.properties


    #searching all country layer views (by tag)
    search_results = gis.content.search(query="tags: Country view", item_type="Feature *",
                                    max_items=150)

    #looping through each layer for editing properties based on parent ones.
    for layer_view in search_results:
        layer_view_title = layer_view.title
        print(layer_view_title)
        # getting country ISO3 from title
        layer_view_standard_name = layer_view_title.split("-")[0].strip()
        # use CountryConverter module for converting ISO3 to official country name
        country_coverter_src = 'short_name'
        if layer_view_standard_name in ['Democratic Republic of the Congo']:
            country_coverter_src = 'name_official'
        layer_view_iso3 = converter.convert(names=[layer_view_standard_name], src=country_coverter_src, to='ISO3') #also 'short_name' name_official ISO3
        if layer_view_iso3 == 'not found':
            print("country name not found")
        # edit layer snippet, inserting country name
        layer_view_snippet = "This table contains original data collected by interviewing households in COUNTRY, " \
                              "mainly through Computer-Assisted Telephone Interviews (CATI). See full description for information on survey dates"
        layer_view_snippet = layer_view_snippet.replace('COUNTRY', layer_view_standard_name)
        # edit layer description, inserting country name
        cut_description_after = "<b>household </b>interviews from "
        layer_view_description = parent_description[:parent_description.index(cut_description_after) + len(cut_description_after)] + layer_view_standard_name
        # applying all country properties to layer view
        layer_view.update(item_properties={'accessInformation': parent_credits, 'snippet' : layer_view_snippet, 'description' : layer_view_description, 'licenseInfo' : parent_license_info}, thumbnail=images_urls[layer_view_iso3])


if __name__ == "__main__":
    main()