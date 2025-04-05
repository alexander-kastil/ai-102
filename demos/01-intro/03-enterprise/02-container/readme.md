# Using Containers

[Azure AI Container](https://learn.microsoft.com/en-us/training/modules/investigate-container-for-use-with-ai-services/3-use-ai-services-container)

## Demos

Run the Azure AI services in a container with the following command:

```bash
docker run --rm -it -p 5000:5000 --memory 8g --cpus 1 mcr.microsoft.com/azure-cognitive-services/textanalytics/sentiment:latest Eula=accept Billing=https://westeurope.api.cognitive.microsoft.com ApiKey=1d666e39628e473b9e8ad1ed91def4d8
```
