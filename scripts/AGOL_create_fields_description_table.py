from arcgis.gis import GIS
import pandas as pd
from pandas import ExcelWriter
import ast

def main():

    #connecting to AGOL
    gis = GIS('home')

    #searching the parent feature layer

    search_results = gis.content.search(query="tags: master table")

    for feature_layer in search_results:
        feature_layer_title = feature_layer.title
        output_table_name = "%s - Fields descriptions" % feature_layer_title

        #getting parent feature layer properties
        table = feature_layer.tables[0] #either layers[0] or tables[0]
        table_properties = table.properties

        #getting detailed table properties )
        field_properties_list = []
        for f in table_properties.fields:
            field_name = f['name']
            try:
                actualType = f['actualType']
            except:
                actualType = f['type']
            alias = f['alias']
            if "description" in f:
                description = f["description"]
                # description info is provided in a string representation of a dictionary, and we need to convert it
                description = ast.literal_eval(description)['value']
            else:
                description = ""
            print(field_name, actualType, alias, description)
            field_properties = [field_name, actualType, alias, description]
            field_properties_list.append(field_properties)

        df = pd.DataFrame.from_records(field_properties_list, columns=['Field name', 'Field type', 'Field alias', 'Field description'])

        writer = ExcelWriter(output_table_name + '.xlsx')
        df.to_excel(writer, 'table_properties')
        writer.save()


if __name__ == "__main__":
    main()