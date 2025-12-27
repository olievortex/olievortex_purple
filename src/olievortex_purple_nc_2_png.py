"""Module is called from the command line to convert a .nc file to png"""
import logging
import sys
from azure.monitor.opentelemetry import configure_azure_monitor

from olie_orchestration import create_satellite_image

# Configure Logging
logging.basicConfig(level=logging.INFO)
configure_azure_monitor(logger_name='olievortex_purple')
logger = logging.getLogger('olievortex_purple')

def main():
    """Entry point for the command"""
    try:
        args = sys.argv
        nc_id = args[1]
        effective_date = args[2]

        create_satellite_image(nc_id, effective_date, logger)
    #pylint: disable-next=W0718
    except Exception as err:
        logger.error(str(err))
        sys.exit(1)


if __name__ == "__main__":
    main()
