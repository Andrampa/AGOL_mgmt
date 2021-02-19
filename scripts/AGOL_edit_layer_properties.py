from arcgis.gis import GIS
import country_converter as coco
converter = coco.CountryConverter()

def main():
    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer
    search_results = gis.content.search(query="title: Raw Household Data, owner: boneill_hqfao", item_type="Feature *",
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

    #getting detailed table properties (field properties - field Description and Visible missing)
    parent_table_dict = {}
    for f in parent_table_properties.fields:
        field_name = f['name']
        actualType = f['actualType']
        type = f['type']
        alias = f['alias']
        print(field_name,actualType,type,alias)
        parent_table_dict[field_name] = [actualType, type, alias]

    #searching all country layer views (by tag)
    search_results = gis.content.search(query="tags: Country view round 1, owner: boneill_hqfao", item_type="Feature *",
                                    max_items=150)

    #looping through each layer for editing properties based on parent ones.
    for layer_view in search_results:
        layer_view_title = layer_view.title
        print(layer_view_title)
        # getting country ISO3 from title
        layer_view_iso3 = layer_view_title[:3]
        # use CountryConverter module for converting ISO3 to official country name
        layer_view_standard_name = converter.convert(names=[layer_view_iso3], src='ISO3', to='name_official') #also 'short_name'
        # edit layer snippet, inserting country name
        layer_view_snippet = parent_snippet.replace('8 food-insecure countries', layer_view_standard_name)
        # edit layer description, inserting country name
        cut_description_after = "<b>household </b>interviews from "
        layer_view_description = parent_description[:parent_description.index(cut_description_after) + len(cut_description_after)] + layer_view_standard_name
        # applying all country properties to layer view
        layer_view.update(item_properties={'accessInformation': parent_credits, 'snippet' : layer_view_snippet, 'description' : layer_view_description, 'licenseInfo' : parent_license_info})


if __name__ == "__main__":
    main()