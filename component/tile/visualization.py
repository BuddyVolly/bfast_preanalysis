### TILE SHOWING THE RESULTS

from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm
import ipyvuetify as v

from component.message import ms
from component.scripts import * 
from component import parameter as pm

# create an empty result tile that will be filled with displayable plot, map, links, text
class VisualizationTile(sw.Tile):
    
    def __init__(self, aoi_io, io, **kwargs):
        
        # gather the io
        self.aoi_io = aoi_io
        self.io = io
        
        # create an output alert 
        self.output = sw.Alert()
       
        # add the widgets 
        self.m = sm.SepalMap()
        
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "visualization_widget", # the id will be used to make the Tile appear and disapear
            title  = ms.visualization.title, # the Title will be displayed on the top of the tile
            inputs = [self.m],
            output = self.output
        )
        
        
    def _on_change(self, change):
        
        coll = self.io.dataset
        start = self.io.start
        end = self.io.end
        aoi = self.aoi_io.get_aoi_ee()
        
        if self.io.measure == 'pixel_count':
            reducer = ee.Reducer.count()
            coll = coll.select('B3')
            viz = pm.visParamCount

        elif self.io.measure == 'ndvi_median':
            reducer = ee.Reducer.median()
            coll = coll.select('NDVI')
            viz = pm.visParamNDVIMean
            
        elif self.io.measure == 'ndvi_stdDev':
            reducer = ee.Reducer.median()
            coll = coll.select('NDVI')
            viz = pm.visParamNDVIStdDev
            
        list_of_images = {}
        
        if self.io.annual:

            end, end_y = ee.Date(end).getInfo()['value'], 0
            while end > end_y:
                
                # advance year and just get the year part so we make sure to get the 1st of Jan
                advance_start = ee.Date(start).advance(1, 'year').format('Y')

                # get last day of current year
                end_y = ee.Date(advance_start).advance(-1, 'day').getInfo()['value']

                # catch last iterartion and set to actual end date
                if end_y > end:
                    end_y = end


                # create collection and fill list
                list_of_images[start] = (
                    coll
                        .filterDate(start, end_y)
                        .reduce(reducer).rename(self.io.measure)
                        .clip(aoi)
                )

                # reset start ot new start of the year
                start = ee.Date(advance_start).format('Y-MM-dd').getInfo()

        else:
            list_of_images['total'] = (
                coll
                    .filterDate(start, end)
                    .reduce(reducer).rename(self.io.measure)
                    .clip(aoi)
            )

        # Display the map
        display_result(
            self.aoi_io.get_aoi_ee(),
            list_of_images,
            self.m, 
            viz,
            self.io.measure,
            self.io.annual
        )
        
        
