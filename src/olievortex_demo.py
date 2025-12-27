"""Manually create an image without interacting with the back-end"""
import os

from olie_services import OlieServices
from olie_satellite import OlieSatellite

SOURCE_FILE = "sample_files/OR_ABI-L1b-RadC-M6C02_G16_s20211381851159_e20211381853532_c20211381853555.nc"
extent = (-126., 24., -66., 50.)
height = 1080
image_temp = OlieServices.get_temp_file(".png")

os.environ["OlieFontPath"] = 'src/SpicyRice-Regular.ttf'

olie_satellite = OlieSatellite()
olie_satellite.create_png_nc(SOURCE_FILE, image_temp, extent, height)

print(f'Image generated: {image_temp}')
print('Success!')
