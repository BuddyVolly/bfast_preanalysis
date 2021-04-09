import time

import numpy as np
import pandas as pd
import ee
import ipyvuetify as v
from matplotlib import pyplot as plt

from component.message import ms
from component import parameter as pm

from .helpers import *
from .cloud_masking import *

ee.Initialize()

def analysis(aoi, start, end, l8, l7, l5, l4, t2, s2_toa, output):
    
    coll = None
    
    if l8:

        # create collection (with masking) and add NDVI 
        coll = create_collection(
            ee.ImageCollection("LANDSAT/LC08/C01/T1_SR"), t2, start, end, aoi
        ).map(addNDVIL8)

    if l7:

        # create collection (with masking) and add NDVI 
        l7_coll = create_collection(
            ee.ImageCollection("LANDSAT/LC08/C01/T1_SR"), t2, start, end, aoi
        ).map(addNDVILsat)
        
        # merge collection
        coll = coll.merge(l7_coll) if coll else l7_coll
            
        
    if l5:

        # create collection (with masking) and add NDVI 
        l5_coll = create_collection(
            ee.ImageCollection("LANDSAT/LC08/C01/T1_SR"), t2, start, end, aoi
        ).map(addNDVILsat)
        
        # merge collection
        coll = coll.merge(l5_coll) if coll else l5_coll
        
                
    if l4:

        # create collection (with masking) and add NDVI 
        l4_coll = create_collection(
            ee.ImageCollection("LANDSAT/LC08/C01/T1_SR"), t2, start, end, aoi
        ).map(addNDVILsat)
        
        # merge collection
        coll = coll.merge(l4_coll) if coll else l4_coll

    #if s2_sr:
#
    #    s2_sr_cld_col_eval = get_s2_sr_cld_col(aoi, start, end)
    #    s2_sr_coll = (
    #        s2_sr_cld_col_eval
    #            .map(add_cld_shdw_mask)
    #            .map(addDate)
    #    )
#
    #    
    #    dummy_coll = dummy_coll.merge(s2_sr_coll)
    #    dummy_coll = dummy_coll.filter(ee.Filter.gt('system:time', 1)) 
#
    if s2_toa:

        s2_coll = (
            ee.ImageCollection("COPERNICUS/S2")
                .filterBounds(aoi)
                .filterDate(start, end)
                .map(cloudMaskS2)
                .map(addNDVIS2)
        )
        
        # merge collection
        coll = coll.merge(s2_coll) if coll else s2_coll
        
 
     # let the user know that you managed to do something
    output.add_live_msg(ms.process.end_computation, 'success')
    
    return coll