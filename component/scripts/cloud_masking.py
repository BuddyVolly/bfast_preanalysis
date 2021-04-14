import ee
import math

ee.Initialize()

def cloud_mask_S2(image):
    
    CLD_PRB_THRESH = 30
    
    # Get s2cloudless image, subset the probability band.
    cld_prb = ee.Image(image.get('s2cloudless')).select('probability')
    
    # Condition s2cloudless by the probability threshold value.
    is_not_cloud = cld_prb.lt(CLD_PRB_THRESH).rename('clouds')

    return image.updateMask(is_not_cloud)

def cloud_mask_S2_SR(image):
    
    CLD_PRB_THRESH = 30
    NIR_DRK_THRESH = 0.15
    CLD_PRJ_DIST = 1
    BUFFER = 50

    # Get s2cloudless image, subset the probability band.
    cld_prb = ee.Image(image.get('s2cloudless')).select('probability')
    
    # Condition s2cloudless by the probability threshold value.
    is_cloud = cld_prb.gt(CLD_PRB_THRESH).rename('clouds')
    
    # Identify water pixels from the SCL band.
    not_water = image.select('SCL').neq(6)

    # Identify dark NIR pixels that are not water (potential cloud shadow pixels).
    SR_BAND_SCALE = 1e4
    dark_pixels = image.select('B8').lt(NIR_DRK_THRESH*SR_BAND_SCALE).multiply(not_water).rename('dark_pixels')

    # Determine the direction to project cloud shadow from clouds (assumes UTM projection).
    shadow_azimuth = ee.Number(90).subtract(ee.Number(image.get('MEAN_SOLAR_AZIMUTH_ANGLE')));

    # Project shadows from clouds for the distance specified by the CLD_PRJ_DIST input.
    cld_proj = (is_cloud.directionalDistanceTransform(shadow_azimuth, CLD_PRJ_DIST*10)
        .reproject(**{'crs': image.select(0).projection(), 'scale': 100})
        .select('distance')
        .mask()
        .rename('cloud_transform'))

    # Identify the intersection of dark pixels with cloud shadow projection.
    shadows = cld_proj.multiply(dark_pixels).rename('shadows')
    
    # Combine cloud and shadow mask, set cloud and shadow as value 1, else 0.
    is_cld_shdw = is_cloud.add(shadows).gt(0)

    # Remove small cloud-shadow patches and dilate remaining pixels by BUFFER input.
    # 20 m scale is for speed, and assumes clouds don't require 10 m precision.
    is_cld_shdw = (is_cld_shdw.focal_min(2).focal_max(BUFFER*2/20)
        .reproject(**{'crs': image.select([0]).projection(), 'scale': 20})
        .rename('cloudmask'))
    
    #return image.addBands(is_cld_shdw)
    return image.updateMask(is_cld_shdw.unmask(0).neq(1))


def cloudMaskLsatSR(image):
    
    # Select the QA band.
    qa = image.select('pixel_qa')
    
    # Get the internal_cloud_algorithm_flag bit.
    cloud_mask = bitwiseExtract(qa, 5).eq(0)
    shadow_mask = bitwiseExtract(qa, 3).eq(0)
    
    # Return an image masking out cloudy areas.
    return image.updateMask(cloud_mask).updateMask(shadow_mask)


def cloudMaskLsatTOA(image):
    
    # Select the QA band.
    qa = image.select('BQA');
    
    # Get the internal_cloud_algorithm_flag bit.
    cloud_mask = bitwiseExtract(qa, 4)
    shadow_mask = bitwiseExtract(qa, 7, 8)
    
    # Return an image masking out cloudy areas.
    return image.updateMask(cloud_mask).updateMask(shadow_mask)


def bitwiseExtract(value, fromBit, toBit=None):
    if not toBit:
        toBit = fromBit
    maskSize = ee.Number(1).add(toBit).subtract(fromBit)
    mask = ee.Number(1).leftShift(maskSize).subtract(1)
    return value.rightShift(fromBit).bitwiseAnd(mask)