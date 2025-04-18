$body = @{
    values = @(
        @{
            recordId = "a1"
            data = @{
                text = "Tiger, tiger burning bright in the darkness of the night."
                language = "en"
            }
        },
        @{
            recordId = "a2"
            data = @{
                text = "The rain in spain stays mainly in the plains! That's where you'll find the rain!"
                language = "en"
            }
        }
    )
} | ConvertTo-Json -Depth 10

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:7071/api/wordcount" -ContentType "application/json" -Body $body
$response | ConvertTo-Json -Depth 10
