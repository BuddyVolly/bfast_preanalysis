from pathlib import Path

result_dir = Path().home().joinpath('module_results/bfast_preanalysis')

start = """  
### Start date selection

Pick the date of the timeseries' start.
"""

end = """  
### End date selection

Pick the date of the timeseries' end.
"""

select = """  
### Satellite selection

Select the satellite(s) you want to include for the pre-analysis.
"""

stats = """  
### Selection of statistics

Select the statistical measure you want to apply and switch on annual for per-year calculations
"""

measures = ['pixel_count', 'ndvi_median', 'ndvi_stdDev']

visParamNDVIMean = {
    'min': 0,
    'max': 1,
    'palette': ['white', 'brown', 'orange', 'lightgreen', 'green', 'darkgreen']
}

visParamNDVIStdDev = {
    'min': 0,
    'max': 1,
    'palette': ['white','orange', 'red', 'brown']
}

visParamCount = {
    'min': 0,
    'max': 100,
    'palette': ['purple', 'red', 'orange', 'white', 'lightgreen', 'green', 'darkgreen']
}