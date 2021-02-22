from arcgis.gis import GIS
import pandas as pd
from pandas import ExcelWriter
import ast

def main():

    layer_name = "Raw Household Data"
    output_table_name = "Country data table properties (COVID monitoring system Round 1)"
    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer
    search_results = gis.content.search(query="title: " + layer_name, item_type="Feature *",
                                    max_items=150)
    
    #getting parent feature layer properties
    parent_feature_layer = search_results[0]
    parent_table = parent_feature_layer.tables[0]
    parent_table_properties = parent_table.properties

    #getting detailed table properties )
    field_properties_list = []
    for f in parent_table_properties.fields:
        field_name = f['name']
        actualType = f['actualType']
        alias = f['alias']
        if "description" in f:
            description = f["description"]
            description = ast.literal_eval(description)['value'] # for some reasons, description info is provided in a string representation of a dictionary, and we need to convert it
        else:
            description = ""
        print(field_name, actualType, alias, description)
        field_properties = [field_name, actualType, alias, description]
        field_properties_list.append(field_properties)

    df = pd.DataFrame.from_records(field_properties_list, columns=['Field name','Field type', 'Field alias','Field description'])

    writer = ExcelWriter(output_table_name + '.xlsx')
    df.to_excel(writer, 'table_properties')
    writer.save()


if __name__ == "__main__":
    main()