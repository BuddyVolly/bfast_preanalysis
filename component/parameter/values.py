#measures = ['pixel_count', 'ndvi_median', 'ndvi_stdDev']

measures = [
    {'text': 'Cloud-free pixel count', 'value': 'pixel_count'},
    {'text': 'NDVI Median', 'value': 'ndvi_median'},
    {'text': 'NDVI Std. Dev.', 'value': 'ndvi_stdDev'}
]

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
    

    filename = f"bfast_coverage_{aoi_io.get_aoi_name()}_{io.start}_{io.end}"

    if io.l8 != 'NONE':
        filename += f"_L8"

    if io.l7:
        filename += '_L7'

    if io.l5:
        filename += '_L5'

    if io.l4:
        filename += '_L4'

    if io.s2:
        filename += '_S2'

    if io.sr:
        filename += '_SR'
    else:
        filename += '_TOA'
        
    return filename