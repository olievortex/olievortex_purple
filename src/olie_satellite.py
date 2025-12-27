"""Satellite specific implementations"""
import os
import math

import cartopy
from satpy import Scene
from pyresample.geometry import AreaDefinition
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
matplotlib.use('agg')


class OlieSatellite:
    """Satellite specific Olie methods"""

    def __init__(self):
        self.font_olie = font_manager.FontProperties(fname=os.getenv("OlieFontPath"))
        self.cache_dir = "./resample_cache"

    def create_png_nc(self, source_file: str, dest_file: str,
                   extent: tuple[float, float, float, float], height: int):
        """Convert a .nc file to a .png Olie style"""

        # Figure out the dimensions
        l_width = extent[2] - extent[0]
        l_height = extent[3] - extent[1]
        l_ratio = l_width / l_height
        r_width = height * l_ratio
        olie_area = AreaDefinition("olie", "Olie Area", "Web", "EPSG:4326",
                                   r_width, height, extent)

        # CONUS C02 Satellite
        global_scene = Scene(reader='abi_l1b', filenames=[source_file])
        global_scene.load(['C02'], calibration='reflectance')
        local_scene = global_scene.resample(olie_area, resampler="bilinear",
                                            cache_dir=self.cache_dir,
                                            calibration='reflectance')

        # Output figure configuration
        crs = olie_area.to_cartopy_crs()
        plt.figure(figsize=(r_width / 100, height / 100), dpi=100)
        ax = plt.axes(projection=crs)
        ax.set_facecolor('black')
        ax.set_position([0, 0, 1, 1])

        # Add OlieVortex Analytics Branding
        x_range = np.linspace(extent[0], extent[2], 1000)
        y_range = np.linspace(extent[1], extent[3], 1000)
        font_size = 32.0 * height / 720
        ax.text(x_range[3], y_range[16], r"Olie\/ortex   Analytics", transform=crs,
                fontsize=font_size, fontproperties=self.font_olie, color='black')
        ax.text(x_range[2], y_range[18], r"Olie\/ortex   Analytics", transform=crs,
                fontsize=font_size, fontproperties=self.font_olie, color='darkgoldenrod')

        # https://medium.com/analytics-vidhya/image-equalization-contrast-enhancing-in-python-82600d3b371c
        bins = 101
        image_raw = local_scene['C02'].as_numpy().data
        image_hist = np.zeros(bins)

        # frequency count of each pixel, exclude NaN
        for row in image_raw:
            for pix in row:
                if math.isnan(pix):
                    continue
                das_bin = int(max(0, min(pix, 100)))
                image_hist[das_bin] += 1

        # cummulative sum
        cum_sum = np.cumsum(image_hist)
        norm = (cum_sum - cum_sum.min()) * 255

        # normalization of the pixel values
        n_ = cum_sum.max() - cum_sum.min()
        uniform_norm = norm / n_
        uniform_norm = uniform_norm.astype('int')

        # flat histogram
        image_raw = image_raw.astype('int')
        image_raw = np.clip(image_raw, 0, 100)
        image_eq = uniform_norm[image_raw]

        # Draw the image
        ax.add_feature(cartopy.feature.STATES, edgecolor='black', linewidth=1)
        ax.imshow(image_eq, transform=crs, cmap='gray', extent=crs.bounds,
                  origin='upper')
        plt.savefig(dest_file, bbox_inches='tight', pad_inches=0)

        # Free memory
        ax.cla()
        plt.cla()
        plt.clf()
        plt.close('all')

    def create_png_tif(self, source_file: str, dest_file: str,
                   extent: tuple[float, float, float, float]):
        """Convert a geotif file to a .png Olie style"""

        # Figure out the dimensions
        height = 650
        width = 1500
        olie_area = AreaDefinition("olietiff", "Olie Tiff Area", "Web", "EPSG:4326",
                                   width, height, extent)

        # CONUS C02 Satellite
        global_scene = Scene(reader='generic_image', filenames=[source_file])
        global_scene.load(['image'])
        local_scene = global_scene.resample(olie_area)

        # Output figure configuration
        crs = olie_area.to_cartopy_crs()
        plt.figure(figsize=(width / 100, height / 100), dpi=100)
        ax = plt.axes(projection=crs)
        ax.set_facecolor('black')
        ax.set_position([0, 0, 1, 1])

        # Add OlieVortex Analytics Branding
        x_range = np.linspace(extent[0], extent[2], 1000)
        y_range = np.linspace(extent[1], extent[3], 1000)
        font_size = 32.0 * height / 720
        ax.text(x_range[3], y_range[16], r"Olie\/ortex   Analytics", transform=crs,
                fontsize=font_size, fontproperties=self.font_olie, color='black')
        ax.text(x_range[2], y_range[18], r"Olie\/ortex   Analytics", transform=crs,
                fontsize=font_size, fontproperties=self.font_olie, color='darkgoldenrod')

        # Draw the image
        ax.add_feature(cartopy.feature.STATES, edgecolor='black', linewidth=1)
        ax.imshow(local_scene['image'][0], transform=crs, cmap='gray', extent=crs.bounds,
                  origin='upper')
        plt.savefig(dest_file, bbox_inches='tight', pad_inches=0)

        # Free memory
        ax.cla()
        plt.cla()
        plt.clf()
        plt.close('all')

if __name__ == "__main__":
    l_extent = (-126., 24., -66., 50.)
    HEIGHT = 1080
    SRC = "/Users/olievortex/Downloads/OR_ABI-L1b-RadC-M3C02_G16_s20180192137197_e20180192139570_c20180192140011.nc"
    DST = "/Users/olievortex/Downloads/Dillon.png"

    sat = OlieSatellite()
    sat.create_png_nc(SRC, DST, l_extent, HEIGHT)
