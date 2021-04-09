# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v

from component import scripts
from component.message import ms
from component import parameter as pm

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class ExportTile(sw.Tile):
    
    def __init__(self, aoi_io, io, **kwargs):

        # gather the io
        self.aoi_io = aoi_io
        self.io = io

        # create an output alert 
        self.output = sw.Alert()

        # 
        self.backscatter = v.Switch(
                class_  = "ml-5",
                label   = ms.export.backscatter,
                v_model = True
            )

        self.rfdi = v.Switch(
                class_  = "ml-5",
                label   = ms.export.rfdi,
                v_model = True
            )

        self.texture = v.Switch(
                class_  = "ml-5",
                label   = ms.export.texture,
                v_model = False
            )

        self.aux = v.Switch(
                class_  = "ml-5",
                label   = ms.export.aux,
                v_model = False
            )

        self.fnf = v.Switch(
                class_  = "ml-5",
                label   = ms.export.fnf,
                v_model = False
            )

        self.scale = v.TextField(
            label   = ms.export.scale,
            v_model = 25
        )
        
        
        # create buttons
        self.asset_btn = sw.Btn(ms.export.asset_btn, 'mdi-download', disabled=True, class_='ma-5')
        self.sepal_btn = sw.Btn(ms.export.sepal_btn, 'mdi-download', disabled=True, class_='ma-5')
        #self.download_image = sw.DownloadBtn(ms.export.down_btn)

        # bindings
        self.output = sw.Alert() \
            .bind(self.backscatter, self.io, 'backscatter') \
            .bind(self.rfdi, self.io, 'rfdi') \
            .bind(self.texture, self.io, 'texture') \
            .bind(self.aux, self.io, 'aux') \
            .bind(self.fnf, self.io, 'fnf') \
            .bind(self.scale, self.io, 'scale') \

        # note that btn and output are not a madatory attributes 
        super().__init__(
            id_ = "export_widget",
            title = ms.export.title,
            inputs = [self.backscatter, self.rfdi, self.texture, self.aux, self.fnf, self.scale],
            output = self.output,
            btn = v.Layout(row=True, children = [self.asset_btn, self.sepal_btn])
        )

        #link the btn 
        self.asset_btn.on_event('click', self._on_asset_click)
        self.sepal_btn.on_event('click', self._on_sepal_click)

    def _select_layers(self):
        
        dataset = None
        if self.io.backscatter:
            dataset = self.io.dataset.select(['HH', 'HV', 'HHHV_ratio'])
        if self.io.rfdi:
            if dataset:
                dataset = dataset.addBands(self.io.dataset.select(['RFDI']))
            else:
                dataset = self.io.dataset.select(['RFDI'])
        if self.io.texture:
            if dataset:
                dataset = dataset.addBands(self.io.dataset.select(['HH_var', 'HH_idm', 'HH_diss', 'HV_var', 'HV_idm', 'HV_diss']))
            else:
                dataset = self.io.dataset.select(['HH_var', 'HH_idm', 'HH_diss', 'HV_var', 'HV_idm', 'HV_diss'])   
        if self.io.aux:
            if dataset:
                dataset = dataset.addBands(self.io.dataset.select(['angle', 'date', 'qa']))
            else:
                dataset = self.io.dataset.select(['angle', 'date', 'qa'])
                
        fnf_dataset = None
        if self.io.fnf:
            fnf_dataset = self.io.dataset.select('fnf_' + str(self.io.year))
        
        return dataset, fnf_dataset
        
    def _on_asset_click(self, widget, data, event):
        
        widget.toggle_loading()
        self.sepal_btn.toggle_loading()
        
        dataset, fnf_dataset = self._select_layers()
        
        #try:
        # export the results
        
        if dataset: 
            asset_id = scripts.export_to_asset(
                self.aoi_io, 
                dataset, 
                pm.asset_name(self.aoi_io, self.io),
                self.io.scale,
                self.output
            )

        if fnf_dataset:
            asset_id = scripts.export_to_asset(
                self.aoi_io, 
                fnf_dataset, 
                pm.asset_name(self.aoi_io, self.io, True), 
                self.io.scale, 
                self.output
            )
        
        #except Exception as e:
        #    self.output.add_live_msg(str(e), 'error')
            
        widget.toggle_loading()
        self.sepal_btn.toggle_loading()
        
        return
    
    def _on_sepal_click(self, widget, data, event):
        
        widget.toggle_loading()
        self.asset_btn.toggle_loading()
        
        # get selected layers
        dataset, fnf_dataset = self._select_layers()
        
        try:
            
            if dataset:
                # export the results 
                pathname = scripts.export_to_sepal(
                    self.aoi_io, 
                    dataset, 
                    pm.asset_name(self.aoi_io, self.io), 
                    self.io.scale, 
                    self.output
                )
            
            if fnf_dataset:
                # export the results 
                pathname = scripts.export_to_sepal(
                    self.aoi_io, 
                    fnf_dataset, 
                    pm.asset_name(self.aoi_io, self.io, True), 
                    self.io.scale,
                    self.output
                )
                
            # link it in the download btn 
            #self.download_image.set_url(str(pathname))
            #self.download_image.set_url(str(pathname_fnf))
        
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
            
        widget.toggle_loading()
        self.asset_btn.toggle_loading()
        
        return