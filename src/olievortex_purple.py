"""Entry point for Olievortex Purple"""
import json
import logging
import subprocess
import sys
from azure.monitor.opentelemetry import configure_azure_monitor

# Import Olie code
from olie_services import OlieServices

# Configure Logging
logging.basicConfig(level=logging.INFO)
configure_azure_monitor(logger_name='olievortex_purple')
logger = logging.getLogger('olievortex_purple')

# Let's get started
olie_services = OlieServices()
logger.info("OlievortexPurple: Attaching to sb://%s/%s", olie_services.sb_namespace,
            olie_services.sb_queue)

try:
    while True:
        results = olie_services.sb_reader.receive_messages()
        if len(results) == 0:
            break

        for result in results:
            message = json.loads(str(result))
            args = ["python", "olievortex_purple_nc_2_png.py", message['Id'],
                    message['EffectiveDate']]

            subprocess.run(args, check=True)
            olie_services.sb_reader.complete_message(result)
#pylint: disable-next=W0718
except Exception as err:
    logger.error(str(err))
    sys.exit(1)

logger.info("OlievortexPurple: Quenched. Clean exit.")
