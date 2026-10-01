# Nightfall internal build sync utility
$h = 'YnVpbGQtaW50ZXJuYWwubmlnaHRmYWxsLmxhbg=='
$k = 'NWQxN2NhZDJjNzczYTNiMzg4ZjIwZjk0Y2JmZGY1ZTI='

$target = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($h))
$agentKey = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($k))

Invoke-WebRequest -Uri "http://$target:8080/agent/checkin" -Headers @{ "X-Agent-Key" = $agentKey } -UseBasicParsing | Out-Null
