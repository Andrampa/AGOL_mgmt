from arcgis.gis import GIS
from arcgis.features import FeatureLayer

images_urls = {'Value Chains and Market': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/7b829f23388b48ac9d68099449c723af/data',
              'Food Security and Livelihoods' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/d170149360334a3782a3bf9f26c5fbaa/data',
              'Needs' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/f024196552774fd9853e3cfe4870507a/data',
              'Crop Production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/875fcb7167eb44f1aabe0f5d7cc96866/data',
              'Livestock Production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/854eda862011440c88b64fe002efe6fa/data'}

tables_urls = {'Value Chains and Market': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/8bf2b852e265479f8bbec36115c80063/data',
              'Food Security and Livelihoods' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/278e1717b3814f5f8fc205061f169664/data',
              'Needs' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/0dcf97b3db524790a6a176998f1a1796/data',
              'Crop Production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/38d7afbaa4bc477b9c29700938337ea8/data',
              'Livestock Production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/56f31694268c4ca2804e1e23eb11115f/data'}

def main():
    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer
    search_results = gis.content.search(query="title: Livestock Production Thematic Area - Cleaned and weighted household data")
    
    #getting parent feature layer properties
    parent_feature_layer = search_results[0]
    parent_description = parent_feature_layer.description
    parent_license_info = parent_feature_layer.licenseInfo
    parent_title = parent_feature_layer.title
    parent_thematic_area = parent_title.split("Thematic")[0].strip()
    parent_snippet = parent_feature_layer.snippet
    parent_credits = parent_feature_layer.accessInformation
    parent_categories = parent_feature_layer.categories
    parent_table = parent_feature_layer.tables[0]



    #searching all country layer views (by tag)
    search_results = gis.content.search(query="tags: Thematic view round 1")

    #looping through each layer for editing properties based on parent ones.
    for layer_view in search_results:
        layer_view_title = layer_view.title
        print(layer_view_title)
        # getting country ISO3 from title
        layer_view_thematic_area = layer_view_title.split("Thematic")[0].strip()
        # edit layer snippet, inserting country name
        list_of_countries = "Afghanistan, Colombia, DRC, Liberia, Mali, Niger, Sierra Leone, Somalia, Yemen and Zimbabwe"
        layer_view_snippet = "This table contains original data collected by interviewing households in COUNTRIES. Thematic area subset: THEMATIC_AREA. " \
                             "See full description for information on survey dates"
        layer_view_snippet = layer_view_snippet.replace('THEMATIC_AREA', layer_view_thematic_area)
        layer_view_snippet = layer_view_snippet.replace('COUNTRIES', list_of_countries)
        layer_view_description = parent_description.split("referring to <b>")[0]
        layer_view_description += "referring to <b>%s</b> from <b>%s</b>" % (layer_view_thematic_area, list_of_countries)
        layer_view_description = layer_view_description.replace('https://hqfao.maps.arcgis.com/sharing/rest/content/items/56f31694268c4ca2804e1e23eb11115f/data', tables_urls[layer_view_thematic_area])
        # applying all country properties to layer view
        print(layer_view_thematic_area)
        print (layer_view_snippet)
        print(layer_view_description)
        print(images_urls[layer_view_thematic_area])
        layer_view.update(item_properties={'accessInformation': parent_credits, 'snippet' : layer_view_snippet, 'description' : layer_view_description, 'licenseInfo' : parent_license_info}, thumbnail=images_urls[layer_view_thematic_area])


if __name__ == "__main__":
    main()