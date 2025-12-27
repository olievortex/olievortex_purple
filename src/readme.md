## Create a Docker image

    docker build -t olievortex/olievortex-purple . --platform=linux/amd64
    docker image ls

## Run a local container

    SECRET={secret}
    docker container rm magical_shirley
    docker run --env AZURE_CLIENT_SECRET=$SECRET --name magical_shirley olievortex/olievortex-purple
    docker start magical_shirley

## Push an image to Azure Registration

    az acr login --name olieregistry
    docker tag olievortex/olievortex-purple olieregistry.azurecr.io/olievortex-purple:v0.1.10
    docker push olieregistry.azurecr.io/olievortex-purple:v0.1.10

## Create the container

    PULL_PASSWORD={secret}
    RESOURCE_ID=$(az identity show --resource-group rg-olievortex-public --name id-spcintegration --query id --output tsv)
    az container create \
        --resource-group rg-container \
        --name olievortex-purple-1 \
        --image olieregistry.azurecr.io/olievortex-purple:v0.1.10 \
        --restart-policy OnFailure \
        --environment-variables 'AZURE_CLIENT_ID'='5fee7033-192a-4ee7-860d-3ca7478b2c97' \
        --assign-identity $RESOURCE_ID \
        --os-type linux --cpu 1 --memory 2 \
        --registry-login-server olieregistry.azurecr.io \
        --registry-username 3167d1f6-55b5-4747-92a4-ab86e190f46c \
        --registry-password $PULL_PASSWORD
