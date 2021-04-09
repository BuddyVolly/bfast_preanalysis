import ee
import math

ee.Initialize()

def cloudMaskS2(image):
    
    qa = image.select('QA60');
  
    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = math.pow(2, 10);
    cirrusBitMask = math.pow(2, 11);
  
    # Both flags should be set to zero, indicating clear conditions.
    mask = (qa.bitwiseAnd(cloudBitMask).eq(0).And(
             qa.bitwiseAnd(cirrusBitMask).eq(0)))

    # Return the masked and scaled data.
    return image.updateMask(mask).divide(10000).copyProperties(image, ["system:time_start"])

def cloudMaskLsat(image):
    qa = image.select('pixel_qa');
    # If the cloud bit (5) is set and the cloud confidence (7) is high
    # or the cloud shadow bit is set (3), then it's a bad pixel.
    cloud = (
        qa.bitwiseAnd(1<<5)
        .And(qa.bitwiseAnd(1<<7))
        .Or(qa.bitwiseAnd(1<<3))
    )
    
    # Remove edge pixels that don't occur in all bands
    mask2 = image.mask().reduce(ee.Reducer.min());
    return image.updateMask(cloud.Not()).updateMask(mask2).copyProperties(image, ["system:time_start"]);