# Requires administrator privileges.
# Opens the Streamlit and Flask API ports so an Android emulator can reach them.

$ports = @(8501, '5000-5100')
foreach ($port in $ports) {
    $displayName = if ($port -is [string]) { "Fitu API Ports $port" } else { "Fitu Streamlit Port $port" }
    if (-not (Get-NetFirewallRule -DisplayName $displayName -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule -DisplayName $displayName -Direction Inbound -LocalPort $port -Protocol TCP -Action Allow
        Write-Host "Created firewall rule for port $port"
    } else {
        Write-Host "Firewall rule already exists for $port"
    }
}
Write-Host "Firewall rules are configured. If PowerShell failed, run this script as administrator."
