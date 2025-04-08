# Set values for your Search service
$url = "https://aisearchknowledegeai10222932.search.windows.net"
$admin_key = "<your admin key>"

Write-Host "-----"
Write-Host "Updating the skillset..."
Invoke-RestMethod -Uri "$url/skillsets/margies-custom-skillset?api-version=2020-06-30" -Method Put -Headers @{"Content-Type" = "application/json"; "api-key" = $admin_key} -InFile "update-skillset.json"

Write-Host "-----"
Write-Host "Updating the index..."
Invoke-RestMethod -Uri "$url/indexes/margies-custom-index?api-version=2020-06-30" -Method Put -Headers @{"Content-Type" = "application/json"; "api-key" = $admin_key} -InFile "update-index.json"

# Wait
Start-Sleep -Seconds 3

Write-Host "-----"
Write-Host "Updating the indexer..."
Invoke-RestMethod -Uri "$url/indexers/margies-custom-indexer?api-version=2020-06-30" -Method Put -Headers @{"Content-Type" = "application/json"; "api-key" = $admin_key} -InFile "update-indexer.json"

Write-Host "-----"
Write-Host "Resetting the indexer..."
Invoke-RestMethod -Uri "$url/indexers/margies-custom-indexer/reset?api-version=2020-06-30" -Method Post -Headers @{"Content-Type" = "application/json"; "Content-Length" = "0"; "api-key" = $admin_key}

# Wait
Start-Sleep -Seconds 5

Write-Host "-----"
Write-Host "Rerunning the indexer..."
Invoke-RestMethod -Uri "$url/indexers/margies-custom-indexer/run?api-version=2020-06-30" -Method Post -Headers @{"Content-Type" = "application/json"; "Content-Length" = "0"; "api-key" = $admin_key}
