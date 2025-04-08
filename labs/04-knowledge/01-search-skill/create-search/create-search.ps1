# Set values for your Search service
$url = "https://aisearchknowledegeai10222932.search.windows.net"
$admin_key = ""

Write-Host "-----"
Write-Host "Creating the data source..."
Invoke-RestMethod -Uri "$url/datasources?api-version=2020-06-30" -Method Post -Headers @{"Content-Type" = "application/json"; "api-key" = $admin_key} -InFile "data_source.json"

Write-Host "-----"
Write-Host "Creating the skillset..."
Invoke-RestMethod -Uri "$url/skillsets/margies-custom-skillset?api-version=2020-06-30" -Method Put -Headers @{"Content-Type" = "application/json"; "api-key" = $admin_key} -InFile "skillset.json"

Write-Host "-----"
Write-Host "Creating the index..."
Invoke-RestMethod -Uri "$url/indexes/margies-custom-index?api-version=2020-06-30" -Method Put -Headers @{"Content-Type" = "application/json"; "api-key" = $admin_key} -InFile "index.json"

# Wait
Start-Sleep -Seconds 3

Write-Host "-----"
Write-Host "Creating the indexer..."
Invoke-RestMethod -Uri "$url/indexers/margies-custom-indexer?api-version=2020-06-30" -Method Put -Headers @{"Content-Type" = "application/json"; "api-key" = $admin_key} -InFile "indexer.json"
