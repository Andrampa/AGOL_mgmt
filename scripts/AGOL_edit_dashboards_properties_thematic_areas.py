from arcgis.gis import GIS
from arcgis.features import FeatureLayer

images_urls = {'Value Chains & Markets': 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/c24935d268dd4b16a2066a5e8d56e960/data',
              'FSL Outcomes' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/a1ecbf7fcb2442f8be1ce328739e3aab/data',
              'Needs' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/ebf0cc360320411b83f0b1008c25f9cc/data',
              'Crop Production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/dc58ce4bbfed40528479ba02a0575b9c/data',
              'Livestock Production' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/e71a7fe9fb73497398a2e21c08f401b0/data',
              'Summary' : 'https://hqfao.maps.arcgis.com/sharing/rest/content/items/01f3ce873b80484b8cd442614f0926e7/data'}

def main():
    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer
    search_results = gis.content.search(query="title: Livestock Production Dashboard - Household survey - Round 1")
    
    #getting parent feature layer properties
    parent_feature_layer = search_results[0]
    parent_description = parent_feature_layer.description
    parent_license_info = parent_feature_layer.licenseInfo
    parent_title = parent_feature_layer.title
    parent_thematic_area = parent_title.split("Dashboard")[0].strip()
    parent_snippet = parent_feature_layer.snippet
    parent_credits = parent_feature_layer.accessInformation


    #searching all country layer views (by tag)
    search_results = gis.content.search(query="tags: Dashboard round 1")

    #looping through each layer for editing properties based on parent ones.
    for dashboard in search_results:
        dashboard_title = dashboard.title
        print(dashboard_title)
        # getting country ISO3 from title
        dashboard_thematic_area = dashboard_title.split("Dashboard")[0].strip()
        # edit layer snippet, inserting country name
        dashboard_snippet = parent_snippet.replace('Thematic area subset: Livestock Production', "Thematic area subset: %s" % dashboard_thematic_area)
        dashboard_description = parent_description.replace('referring to\xa0<b>Livestock Production', "referring to<b> %s" % dashboard_thematic_area)
        # applying all country properties to layer view
        print (dashboard_snippet)
        print(dashboard_thematic_area)
        print(dashboard_description)
        print(images_urls[dashboard_thematic_area])
        dashboard.update(item_properties={'accessInformation': parent_credits, 'snippet' : dashboard_snippet, 'description' : dashboard_description, 'licenseInfo' : parent_license_info}, thumbnail=images_urls[dashboard_thematic_area])


if __name__ == "__main__":
    main()