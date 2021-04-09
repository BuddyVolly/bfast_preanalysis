import ee
import ipyvuetify as v

from component.message import ms
from component import parameter as pm


ee.Initialize()

def display_result(ee_aoi, dataset, m, vis, measure, annual):
    """
    Display the results on the map 
    
    Args:
        ee_aoi: (ee.Geometry): the geometry of the aoi
        dataset (ee.Image): the image the display
        m (sw.SepalMap): the map used for the display
        db (bool): either to use the db scale or not
        
    Return:
        (sw.SepalMap): the map with the different layers added
    """
    
    if measure == 'pixel_count' and annual:
        _max = 20 if annual else 100
        vis.update(max=_max)
        
    # AOI borders in blue 
    empty   = ee.Image().byte()
    outline = empty.paint(featureCollection = ee_aoi, color = 1, width = 3)
   
    # Zoom to AOI
    m.zoom_ee_object(ee_aoi.geometry())
    
    for year in sorted(dataset.keys()):
        label = year[:4] if annual else 'total'
        m.addLayer(dataset[year], vis, f'{measure} {label}')
    
    m.add_colorbar(colors=vis['palette'], vmin=vis['min'], vmax=vis['max'], layer_name="Colorbar")
    
    return