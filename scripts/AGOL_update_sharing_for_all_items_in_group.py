from arcgis.gis import GIS
from arcgis.features import FeatureLayer

import country_converter as coco
converter = coco.CountryConverter()

def main():
    #connecting to AGOL
    gis = GIS('home')
    data_in_emergencies_content_group = gis.groups.search('title:Data in Emergencies Content', max_groups=1)
    old_hub_content_group = gis.groups.search('title:COVID - 19 Trends and Statistics Content', max_groups=1)
    old_hub_content_group_content = old_hub_content_group[0].content()

    for content in old_hub_content_group_content:
        print("%s, Current access: %s" % (content, content.access))
        print("Sharing content to new hub group")
        content.share(groups=data_in_emergencies_content_group)

if __name__ == "__main__":
    main()