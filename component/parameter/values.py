# possible years to select from
years = [2007, 2008, 2009, 2010, 2015, 2016, 2017]

# speckle filters to select from
speckle_filters = [
    {'text': 'No Speckle filter', 'value': 'NONE'}, 
    {'text': 'Refined Lee (zoom dependent)', 'value': 'REFINED_LEE'},
    {'text': 'Quegan Filter', 'value': 'QUEGAN'}
]

layer_select = [
        {'key': 0, 'label': 'Backscatter RGB (HH, HV, HH/HV power ratio)', 'value': 'RGB'},
        {'key': 1, 'label': 'Radar Forest Degradation Index (RFDI, Mitchard et al. 2012)', 'value': 'RFDI'},
        {'key': 2, 'label': 'Forest/Non-Forest', 'value': 'FNF'}
    ]


# name of the file in the output directory 
def asset_name(aoi_io, io, fnf=False):
    """return the standard name of your asset/file"""
    
    if fnf: 
    
        filename = f"kc_fnf_{aoi_io.get_aoi_name()}_{io.year}"    
    
    else:
        
        filename = f"alos_mosaic_{aoi_io.get_aoi_name()}_{io.year}"

        if io.filter != 'NONE':
            filename += f"_{io.filter.lower()}"

        if io.rfdi:
            filename += '_rfdi'

        if io.ls_mask:
            filename += '_masked'

        if io.dB:
            filename += '_dB'
            
        if io.texture:
            filename += '_texture'
            
        if io.aux:
            filename += '_aux'

    return filename