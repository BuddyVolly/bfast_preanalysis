### TILE SHOWING THE RESULTS

from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm
import ipyvuetify as v

from component.message import ms
from component.scripts import * 
from component import parameter as pm

# create an empty result tile that will be filled with displayable plot, map, links, text
class SelectionTile(sw.Tile):
    
    def __init__(self, aoi_io, io, viz_tile, **kwargs):
        
        # gather the io
        self.aoi_io = aoi_io
        self.io = io
        self.viz_tile = viz_tile
        
        # create an output alert 
        self.output = sw.Alert()
        
        # 
        self.start = sw.Markdown(pm.end)
        self.start_picker = sw.DatePicker(label='Start date')
        
        self.end = sw.Markdown(pm.end)
        self.end_picker = sw.DatePicker(label='End date')
        
        self.select = sw.Markdown(pm.select)
        self.l8 = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.l8,
                v_model = False
            )

        self.l7 = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.l7,
                v_model = False
            )

        self.l5 = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.l5,
                v_model = False
            )

        self.l4 = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.l4,
                v_model = False
            )

        self.t2 = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.t2,
                v_model = False
            )

        
        self.s2_toa = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.s2_toa,
                v_model = False
            )

        self.s2_sr = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.s2_sr,
                v_model = False
            )
        
        self.stats = sw.Markdown(pm.stats)
        self.measure = v.Select(
            label   = ms.selection.measure,
            v_model = None,
            items = pm.measures     
        )
        
        self.annual = v.Switch(
                class_  = "ml-5",
                label   = ms.selection.annual,
                v_model = False
            )
        
        # create the output alert 
        # this component will be used to display information to the end user when you lanch the process
        # it's hidden by default 
        # it also has the embeded `bind` method that link mutable variable to component v_model
        # bind return self so it can be chained to bind everything in one statement. 
        # args are (widget, io, io_attribute_name)
        self.output = sw.Alert() \
            .bind(self.start_picker, self.io, 'start')  \
            .bind(self.end_picker, self.io, 'end')  \
            .bind(self.l8, self.io, 'l8') \
            .bind(self.l7, self.io, 'l7') \
            .bind(self.l5, self.io, 'l5') \
            .bind(self.l4, self.io, 'l4') \
            .bind(self.t2, self.io, 't2') \
            .bind(self.s2_toa, self.io, 's2_toa') \
            .bind(self.measure, self.io, 'measure') \
            .bind(self.annual, self.io, 'annual')
            #.bind(self.s2_sr, self.io, 's2_sr') \
            
        # to launch the process you'll need a btn 
        # here it is as a special sw widget (the message and the icon can also be customized see sepal_ui widget doc)
        self.btn = sw.Btn()
        
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "selection_widget", # the id will be used to make the Tile appear and disapear
            title  = ms.selection.title, # the Title will be displayed on the top of the tile
            inputs = [self.start, self.start_picker, self.end, self.end_picker, 
                      self.select, self.l8, self.l7, self.l5, self.l4, self.t2, self.s2_toa, #, self.s2_sr, 
                      self.stats, self.measure, self.annual],
            btn    = self.btn,
            output = self.output
        )
        
        # now that the Tile is created we can link it to a specific function
        self.btn.on_event("click", self._on_run)
        
    
    # PROCESS AFTER ACTIVATING BUTTON
    def _on_run(self, widget, data, event): 
            
        # toggle the loading button (ensure that the user doesn't launch the process multiple times)
        widget.toggle_loading()
            
        # check that the input that you're gonna use are set (Not mandatory)
        if not self.output.check_input(self.aoi_io.get_aoi_name(), ms.process.no_aoi): return widget.toggle_loading()
        # if not self.output.check_input(self.io.year, ms.process.no_slider): return widget.toggle_loading()
       
        # Wrap the process in a try/catch statement 
        try:
            
            dataset = analysis(
                self.aoi_io.get_aoi_ee(),
                self.io.start,
                self.io.end,
                self.io.l8,
                self.io.l7,
                self.io.l5,
                self.io.l4,
                self.io.t2,
                self.io.s2_toa,
                self.output
            )
            
            # change the io values as its a mutable object 
            # useful if the io is used as an input in another tile
            self.io.dataset = dataset

            # release the export btn
            #self.export_tile.asset_btn.disabled = False
            #self.export_tile.sepal_btn.disabled = False

            # conclude the computation with a message
            self.output.add_live_msg(ms.process.end_computation, 'success')
            
            # launch vizualisation
            self.viz_tile._on_change(None)
            
        except Exception as e: 
            self.output.add_live_msg(str(e), 'error')
        
        # release the btn
        widget.toggle_loading()
        
        return