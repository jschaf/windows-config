# Variables
$url = "http://curl.haxx.se/ca/cacert.pem"

# Download the certificates
Write-Host "Downloading Mozilla certificates from $url."
$downloader = New-Object System.Net.WebClient
$rawcerts = $downloader.DownloadString("http://curl.haxx.se/ca/cacert.pem")

# Remove headers and begin/end delimiters and convert into a byte
# stream
$header = "-----BEGIN CERTIFICATE-----`n"
$footer = "`n-----END CERTIFICATE-----"
$match_string = "(?s)$header(.*?)$footer"
$certs_matches = Select-String $match_string -input $rawcerts -AllMatches
$certs_base64 = $certs_matches.matches | %{ $_.Groups[1].Value }
$certs_bytes = $certs_base64 | %{ ,[System.Text.Encoding]::UTF8.GetBytes($_) }

# Install the certificates
$user_root_cert_store = Get-Item Cert:\CurrentUser\Root
$user_root_cert_store.Open("ReadWrite")
foreach ($c in $certs_bytes) {
    $cert = new-object System.Security.Cryptography.X509Certificates.X509Certificate2(,$c)
    $user_root_cert_store.Add($cert)
}
$user_root_cert_store.Close()
Write-Host "Finished installing all certificates."
