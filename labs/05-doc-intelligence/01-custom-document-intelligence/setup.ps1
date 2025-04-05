# Set variable values
$subscriptionId = "YOUR_SUBSCRIPTION_ID"
$resourceGroup = "YOUR_RESOURCE_GROUP"
$location = "YOUR_LOCATION_NAME"
$expiryDate = "2025-04-10T00:00:00Z"

# Get random numbers to create unique resource names
$uniqueId = Get-Random -Maximum 999999

# Connect to Azure if not already connected
$context = Get-AzContext
if (!$context) {
    Connect-AzAccount
}

# Set the subscription context
Set-AzContext -SubscriptionId $subscriptionId

Write-Host "Creating storage..."
# Create a storage account in your Azure resource group
$storageAcct = New-AzStorageAccount `
    -Name "ai102form$uniqueId" `
    -ResourceGroupName $resourceGroup `
    -Location $location `
    -SkuName "Standard_LRS" `
    -EnableHttpsTrafficOnly $true `
    -AllowBlobPublicAccess $true

Write-Host "Uploading files..."
# Get storage account key
$storageKey = (Get-AzStorageAccountKey -ResourceGroupName $resourceGroup -Name "ai102form$uniqueId")[0].Value

# Create storage context
$ctx = New-AzStorageContext -StorageAccountName "ai102form$uniqueId" -StorageAccountKey $storageKey

# Create container
New-AzStorageContainer -Name "sampleforms" -Context $ctx -Permission Blob

# Upload files from local sampleforms folder to the container
Get-ChildItem -Path "./sample-forms/*" -File | ForEach-Object {
    Set-AzStorageBlobContent `
        -Container "sampleforms" `
        -File $_.FullName `
        -Blob $_.Name `
        -Context $ctx `
        -Force
}

# Set storage account name for future use
$storageAcctName = "ai102form$uniqueId"

# Generate a Shared Access Signature (SAS) token for the container
$sasToken = New-AzStorageContainerSASToken `
    -Name "sampleforms" `
    -Context $ctx `
    -Permission "rwl" `
    -ExpiryTime $expiryDate

# Create the full URI with SAS token
$uri = "https://$storageAcctName.blob.core.windows.net/sampleforms$sasToken"

Write-Host "------------------------------------"
Write-Host "SAS URI: $uri"