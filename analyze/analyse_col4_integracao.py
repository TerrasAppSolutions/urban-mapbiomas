import ee
ee.Initialize()

def get_area(asset_image, geometry, year, classe):
    image = ee.Image(asset_image).clip(geometry)

    image_area = ee.Image.pixelArea().divide(10000).clip(geometry)
    raw_data = image_area.mask(image.select('classification_' + str(year)).eq(classe)).reduceRegion(**{
    'reducer':ee.Reducer.sum(), 
    'geometry':geometry,
    'scale':30,
    'maxPixels':30000000
    } )

    return raw_data.get('area')


def get_stats_cobertura_mun(municipio_name, col=4, classe=24):
    if col == 4:
        years = range(1985, 2019)
        asset_image = 'projects/mapbiomas-workspace/COLECAO4/mapbiomas_collection40_integration_v1'
    elif col == 3:
        years = range(1985, 2018)
        asset_image = 'projects/mapbiomas-workspace/public/collection3_1/mapbiomas_collection31_integration_v1'
    elif col == 2:
        years = range(2000, 2017)
        asset_image = 'projects/mapbiomas-workspace/public/collection2_3/mapbiomas_collection23_integration_v1'
    
    municipios = ee.FeatureCollection('projects/mapbiomas-workspace/AUXILIAR/municipios-2016');
    municipio = ee.Feature(municipios.filterMetadata('NM_MUNICIP', 'equals', municipio_name).first())
    geometry = municipio.geometry()
    area_mun = geometry.area().divide(10000)
    
    info = []
    
    for year in years:

        area = get_area(asset_image,  geometry, year, classe)
        info.append(ee.Feature(None, {'year':year, 'area':area, 'name':municipio_name, 'area_mun':area_mun}))
        
    ftc = ee.FeatureCollection(info).getInfo()
    
    
    return [item['properties'] for item in ftc['features']]