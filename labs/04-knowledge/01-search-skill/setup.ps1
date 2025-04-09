# Set values for your subscription and resource group
$subscriptionId = "YOUR_SUBSCRIPTION_ID"
$resourceGroup = "YOUR_RESOURCE_GROUP"
$location = "YOUR_LOCATION_NAME"

# Generate random numbers to create unique resource names
$randomNum1 = Get-Random -Maximum 32768
$randomNum2 = Get-Random -Maximum 32768
$uniqueId = "{0}{1}" -f $randomNum1, $randomNum2

Write-Host "Creating storage..."
az storage account create --name "ai102str$uniqueId" --subscription $subscriptionId --resource-group $resourceGroup --location $location --sku Standard_LRS --encryption-services blob --default-action Allow --allow-blob-public-access true --only-show-errors --output none

Write-Host "Uploading files..."
# Get the storage key
$keyJson = az storage account keys list --subscription $subscriptionId --resource-group $resourceGroup --account-name "ai102str$uniqueId" --query "[?keyName=='key1'].value" -o tsv
$azureStorageKey = $keyJson

# Create container and upload files
az storage container create --account-name "ai102str$uniqueId" --name margies --public-access blob --auth-mode key --account-key $azureStorageKey --output none
az storage blob upload-batch -d margies -s data --account-name "ai102str$uniqueId" --auth-mode key --account-key $azureStorageKey --output none

Write-Host "Creating search service..."
Write-Host "(If this gets stuck at '- Running ..' for more than a couple minutes, press CTRL+C)"
az search service create --name "ai102srch$uniqueId" --subscription $subscriptionId --resource-group $resourceGroup --location $location --sku basic --output none

Write-Host "-------------------------------------"
Write-Host "Storage account: ai102str$uniqueId"
az storage account show-connection-string --subscription $subscriptionId --resource-group $resourceGroup --name "ai102str$uniqueId"
Write-Host "----"
Write-Host "Search Service: ai102srch$uniqueId"
Write-Host " Url: https://ai102srch$uniqueId.search.windows.net"
Write-Host " Admin Keys:"
az search admin-key show --subscription $subscriptionId --resource-group $resourceGroup --service-name "ai102srch$uniqueId"
Write-Host " Query Keys:"
az search query-key list --subscription $subscriptionId --resource-group $resourceGroup --service-name "ai102srch$uniqueId"

# Create function app node
$funcappRandom = Get-Random -Maximum 999999
$funcapp = "custom-skills-$funcappRandom"
Write-Host "Creating Node.js function app: $funcapp"
az functionapp create -n $funcapp -g $resourceGroup -s "ai102str$uniqueId" --consumption-plan-location $location --runtime node --runtime-version 20 --functions-version 4

# Configure CORS for the function app
Write-Host "Configuring CORS for Node.js function app"
az functionapp cors add --name $funcapp --resource-group $resourceGroup --allowed-origins "*"

# Create the function app python
$funcpyRandom = Get-Random -Maximum 999999
$funcpy = "custom-skills-py-$funcpyRandom"
Write-Host "Creating Python function app: $funcpy"
az functionapp create --name $funcpy --resource-group $resourceGroup --storage-account "ai102str$uniqueId" --consumption-plan-location $location --runtime python --runtime-version 3.11 --functions-version 4 --os-type Linux

Write-Host "Configuring CORS for Python function app"
az functionapp cors add --name $funcpy --resource-group $resourceGroup --allowed-origins "*"
