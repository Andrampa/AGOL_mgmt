from arcgis.gis import GIS
from arcgis.features import FeatureLayer

images_urls = {'% of hh reporting sales change': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/7b829f23388b48ac9d68099449c723af/data',
              '% of hh reporting income change' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/d170149360334a3782a3bf9f26c5fbaa/data',
              '% of hh reporting needs of assistance' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/f024196552774fd9853e3cfe4870507a/data',
              '% of hh reporting drop in crop production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/875fcb7167eb44f1aabe0f5d7cc96866/data',
              '% of hh reporting herd size change' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/854eda862011440c88b64fe002efe6fa/data',
               '% of hh reporting shocks directly or indirectly related to COVID-19': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/eb96f9e5026d45868f3ff938b63021aa/data'}

tables_urls = {'% of hh reporting shocks directly or indirectly related to COVID-19': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/9d44fdf00fde4213950e8da771163ea7/data',
              '% of hh reporting herd size change' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/db6576af73174f6db30b6d6b4702537d/data',
              '% of hh reporting sales change' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/f767b5c05c694ae4b891d87016c611b4/data',
              '% of hh reporting drop in crop production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/5d16cc7cc65d4245b58cb0cf07f1d129/data',
              '% of hh reporting income change' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/d4969616de2348e388164b0a7909d352/data',
              '% of hh reporting needs of assistance' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/5e469c58765c460290ca45c93b329f53/data'}

def main():
    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer
    search_results = gis.content.search(query="title: Aggregated Household data - % of hh reporting shocks directly or indirectly related to COVID-19")
    
    #getting parent feature layer properties
    parent_feature_layer = search_results[0] # il primo item puo essere la tabella di field description se ha lo stesso nome
    parent_description = parent_feature_layer.description
    parent_license_info = parent_feature_layer.licenseInfo
    parent_title = parent_feature_layer.title
    parent_thematic_area = parent_title.split("Thematic")[0].strip()
    parent_snippet = parent_feature_layer.snippet
    parent_credits = parent_feature_layer.accessInformation
    # parent_categories = parent_feature_layer.categories
    # parent_table = parent_feature_layer.tables[0]


    #searching all country layer views (by tag)
    search_results = gis.content.search(query="tags: Dashboard layer round 1")
    list_of_countries = "Afghanistan, Colombia, DRC, Liberia, Mali, Niger, Sierra Leone, Somalia, Yemen and Zimbabwe"
    #looping through each layer for editing properties based on parent ones.
    for layer_view in search_results:
        layer_view_title = layer_view.title
        print(layer_view_title)
        # getting country ISO3 from title
        layer_view_indicator = layer_view_title.split("ggregated Household data - ")[1].strip() #split("ggregated Household data - ")[1].strip() or split("% of hh")[0].strip()
        # edit layer snippet, inserting country name
        #layer_view_snippet = parent_snippet.replace('Thematic area subset: Livestock Production', "Thematic area subset: %s" % layer_view_indicator)

        layer_view_snippet = "This layer contains aggregated data collected by interviewing households in COUNTRIES. " \
                             "Data is provided on Admin 1 level. See full description for information on indicators and survey dates."
        layer_view_snippet = layer_view_snippet.replace('COUNTRIES', list_of_countries)
        layer_view_description = parent_description
        layer_view_description = layer_view_description.replace('https://hqfao.maps.arcgis.com/sharing/rest/content/items/0dcf97b3db524790a6a176998f1a1796/data', tables_urls[layer_view_indicator])
        layer_view_description = layer_view_description.split("Admin1 level, from")[0]
        layer_view_description += "Admin1 level, from <b>%s</b>. Indicator: <b>%s</b>" % (list_of_countries, layer_view_indicator)
        layer_view_description = layer_view_description.replace("% of hh", "Percentage of households")
        # applying all country properties to layer view
        #print (layer_view_snippet)
        print(layer_view_indicator)
        print(layer_view_description)
        print(images_urls[layer_view_indicator])
        layer_view.update(item_properties={'accessInformation': parent_credits, 'snippet' : layer_view_snippet, 'description' : layer_view_description, 'licenseInfo' : parent_license_info}, thumbnail=images_urls[layer_view_indicator])
        #layer_view.update(item_properties={'accessInformation': parent_credits,'description': layer_view_description, 'licenseInfo': parent_license_info},thumbnail=images_urls[layer_view_indicator])


if __name__ == "__main__":
    main()