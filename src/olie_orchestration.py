"""Orchestration functions"""
from logging import Logger
import time
from datetime import datetime, timezone
from olie_cosmos import OlieCosmos
from olie_satellite import OlieSatellite
from olie_services import OlieServices

def create_satellite_image(nc_id: str, effective_date: str, logger: Logger):
    """Take a satellite .nc file from blob storage and create
    an OlieVortex Analytics .png file"""
    olie_services = OlieServices()
    olie_satellite = OlieSatellite()
    olie_cosmos = OlieCosmos()

    # Configuration
    extent = (-126., 24., -66., 50.)
    height = 1080
    start_time = time.perf_counter()

    # Obtain the record
    logger.info("OlievortexPurple: Get %s", nc_id)
    item = olie_cosmos.satellite_aws_product_read(nc_id, effective_date)

    # Short circuit if the record is complete
    if item['Path1080'] is not None:
        logger.info('OlievortexPurple: Already complete %s', nc_id)
        return

    # Download the source satellite file from blob storage
    source = str(item['PathSource'])
    satellite_temp = OlieServices.get_local_file(source)
    logger.info("OlievortexPurple: Download %s", source)
    olie_services.download_blob(source, satellite_temp)

    # Create the image
    image_temp = OlieServices.get_temp_file(".png")
    logger.info("OlievortexPurple: Generate %s", image_temp)
    if nc_id.endswith('.nc'):
        olie_satellite.create_png_nc(satellite_temp, image_temp, extent, height)
    else:
        olie_satellite.create_png_tif(satellite_temp, image_temp, extent)

    # Upload the image to blob storage
    destination = source \
        .replace('bronze', 'gold') \
        .replace('.nc', '.png') \
        .replace('.tif', '.png')
    logger.info("OlievortexPurple: Upload %s", destination)
    olie_services.upload_blob(image_temp, destination, "image/png")

    # Clean up temp files
    olie_services.delete_file(satellite_temp)
    olie_services.delete_file(image_temp)

    # Update the database
    duration = time.perf_counter() - start_time

    item['Path1080'] = destination
    item['IsComplete'] = True
    item['Timestamp'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    item['TotalSecondsTaken'] = int(duration)

    olie_cosmos.satellite_aws_product_update(item)
