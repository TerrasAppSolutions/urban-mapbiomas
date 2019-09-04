import ee
ee.Initialize()

def get_area(asset_imc, geometry, year):
    image = ee.Image( asset_imc + '/' + str(year)).clip(geometry)

    image_area = ee.Image.pixelArea().divide(10000).clip(geometry)
    raw_data = image_area.mask(image.select('classification_' + str(year)).eq(24)).reduceRegion(**{
    'reducer':ee.Reducer.sum(), 
    'geometry':geometry,
    'scale':30
    } )

    return raw_data.get('area')


def get_stats_cobertura_mun(municipio_name, col=4):
    if col == 4:
        years = range(1985, 2019)
        asset_imc = 'projects/mapbiomas-workspace/TRANSVERSAIS/INFRAURBANA4-FT'
    elif col == 3:
        years = range(1985, 2018)
        asset_imc = 'projects/mapbiomas-workspace/TRANSVERSAIS/INFRAURBANA3-FT-FINAL'
    
    municipios = ee.FeatureCollection('projects/mapbiomas-workspace/AUXILIAR/municipios-2016');
    municipio = ee.Feature(municipios.filterMetadata('NM_MUNICIP', 'equals', municipio_name).first())
    geometry = municipio.geometry()
    area_mun = geometry.area().divide(10000)
    
    info = []
    
    for year in years:

        area = get_area(asset_imc,  geometry, year)
        info.append(ee.Feature(None, {'year':year, 'area':area, 'name':municipio_name, 'area_mun':area_mun}))
        
    ftc = ee.FeatureCollection(info).getInfo()
    
    
    return [item['properties'] for item in ftc['features']]