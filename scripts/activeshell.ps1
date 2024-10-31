# Load the System.Net.Http assembly
Add-Type -AssemblyName "System.Net.Http"

# Create an HTTP client
$httpClient = New-Object System.Net.Http.HttpClient

# Set up the MultipartFormDataContent for file upload
$content = New-Object System.Net.Http.MultipartFormDataContent
$fileStream = [System.IO.File]::OpenRead("C:\Users\PRAVEEN\Downloads\cartraffic.jpeg")  # Path to your image
$fileContent = New-Object System.Net.Http.StreamContent($fileStream)
$fileContent.Headers.ContentDisposition = New-Object System.Net.Http.Headers.ContentDispositionHeaderValue("form-data")
$fileContent.Headers.ContentDisposition.Name = '"file"'
$fileContent.Headers.ContentDisposition.FileName = '"image.jpg"'
$content.Add($fileContent)

# Send the POST request and catch any errors
try {
    # Send the request
    $response = $httpClient.PostAsync("http://localhost:8000/predict", $content).Result

    # Check if the response is null
    if ($response -eq $null) {
        Write-Host "No response received from the server."
    }
    else {
        # Check if the request was successful (status code 200-299)
        if ($response.IsSuccessStatusCode) {
            # Output the response body
            $responseContent = $response.Content.ReadAsStringAsync().Result
            Write-Host "Response received from server:"
            Write-Host $responseContent
        }
        else {
            Write-Host "HTTP request failed. Status code: $($response.StatusCode)"
            Write-Host "Reason: $($response.ReasonPhrase)"
        }
    }
}
catch {
    Write-Host "An error occurred: $_"
}
