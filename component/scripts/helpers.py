import ee
ee.Initialize()
from .cloud_masking import cloudMaskLsat


EPOCH = ee.Date('1970-01-01')

def add_date(image):
    mask = image.mask().reduce(ee.Reducer.min())
    days = image.date().difference(EPOCH, 'day')
    return (
        ee.Image.constant(days).int()
          .clip(image.geometry())
          .updateMask(mask)
          .copyProperties(image, ["system:time_start"])
    )

def addNDVIL8(image): 
    return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('NDVI'))

def addNDVILsat(image): 
    return image.addBands(image.normalizedDifference(['B4', 'B3']).rename('NDVI'))

def addNDVIS2(image): 
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('NDVI'))

def create_collection(collection, t2, start, end, aoi):
    coll = (
        collection
            .filterBounds(aoi)
            .filterDate(start, end)
    )


    if t2:
        coll_name = coll.get('system:id').getInfo()
        coll_t2 = coll_name[:-5] + 'T2_SR'

        coll = coll.merge(
            ee.ImageCollection(coll_t2)
                .filterBounds(aoi)
                .filterDate(start, end)
        )

    return coll.map(cloudMaskLsat)