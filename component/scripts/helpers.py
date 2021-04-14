import ee
ee.Initialize()
from .cloud_masking import cloudMaskLsatTOA, cloudMaskLsatSR 

def addNDVIL8(image): 
    return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('NDVI'))

def addNDVILsat(image): 
    return image.addBands(image.normalizedDifference(['B4', 'B3']).rename('NDVI'))

def addNDVIS2(image): 
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('NDVI'))

def create_collection(collection, t2, start, end, aoi, sr):
    
    coll = (
        collection
            .filterBounds(aoi)
            .filterDate(start, end)
    )


    if t2:
        coll_name = coll.get('system:id').getInfo()
        
        coll_t2 = coll_name.replace("/T1_", "/T2_")

        coll = coll.merge(
            ee.ImageCollection(coll_t2)
                .filterBounds(aoi)
                .filterDate(start, end)
        )

    if sr:
        return coll.map(cloudMaskLsatSR)
    else:
        return coll.map(cloudMaskLsatTOA)