

### ALOS Kyoto & Carbon Mosaics by JAXA


This interface facilitates the access to the global ALOS Kyoto & Carbon L-Band SAR mosaics and associated Forest/Non-Forest mask as provided by JAXA. The data is accessed via [Google's Earth Engine](https://earthengine.google.com/) platform. More information on JAXA's K&C initiative can be found [here](https://www.eorc.jaxa.jp/ALOS/en/kyoto/kyoto_index.htm).

At the moment, the mosaics are available for the the years 2007-2010 (based on ALOS-1 PALSAR-1) and 2015, 2016, and 2017 (based on ALOS-2 PALSAR-2 data). Both, backscatter as well as the associated Forest/Non-Forest mask, are made accessible. More detailed information on the global mosaics are available [here](https://www.eorc.jaxa.jp/ALOS/en/palsar_fnf/fnf_index.htm).

The inputs are defined by the year and the Area of Interest (AOI).
Additional pre-processing parameters can be set, such as the automated masking of layover and shadow areas and the scaling to decibel. 

Additional layers can be selected for export, such as the Radar Forest Degradation Index (RFDI, [Mitchard et al. 2012](https://bg.copernicus.org/articles/9/179/2012/bg-9-179-2012.pdf)) or texture layers for both polarizations. 

The output consists of the seleceted layers within the export menu, clippped to the AOI and resampled to the given resolution. Backscatter and associated layers are grouped into one single file and the Forest/Non-Forest mask is delivered in a separate file.

The wrapper is primarily designed to run inside FAO's [SEPAL](https://sepal.io) platfoem.

