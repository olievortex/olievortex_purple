FROM python:3.11.11-bookworm

WORKDIR /usr/src/app

ENV OlieServiceBusNamespace=sb-olievortex.servicebus.windows.net
ENV OlieServiceBusQueue=satellite_aws_posters
ENV OlieBlobAccount=https://salrsolievortex.blob.core.windows.net
ENV OlieBlobOutContainer=olie-spc-integration
ENV OlieBlobInContainer=olie-historian-subscribers
ENV OlieCosmosEndpoint=https://cos-olievortex.documents.azure.com:443/
ENV OlieCosmosDatabase=common
ENV OlieFontPath=./SpicyRice-Regular.ttf
ENV AZURE_TENANT_ID=3f57b1c9-54d7-4638-90eb-21c0dbe7f61e
ENV AZURE_CLIENT_ID=5fee7033-192a-4ee7-860d-3ca7478b2c97
ENV APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=1e66165a-27bc-4844-8670-3b7e08549502;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/;ApplicationId=3e62bc5e-d659-4522-914c-bb3aecea8e06

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "olievortex_purple.py"]