$NGROK = "C:\Users\Santiago\AppData\Local\Microsoft\WinGet\Packages\Ngrok.Ngrok_Microsoft.Winget.Source_8wekyb3d8bbwe\ngrok.exe"
$PROYECTO = "C:\Users\Santiago\Core-Agent"

Write-Host "Iniciando Core Agent..." -ForegroundColor Cyan

# Detener procesos previos
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process -Name ngrok  -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1

function Start-Flask {
    Write-Host "[Flask] Iniciando servidor..." -ForegroundColor Green
    return Start-Process -FilePath "python" -ArgumentList "$PROYECTO\app.py" `
        -WorkingDirectory $PROYECTO -PassThru -NoNewWindow
}

function Start-Ngrok {
    Write-Host "[ngrok] Iniciando tunel..." -ForegroundColor Yellow
    return Start-Process -FilePath $NGROK -ArgumentList "http 5000" `
        -PassThru -WindowStyle Hidden
}

$flask = Start-Flask
Start-Sleep -Seconds 3
$ngrok = Start-Ngrok
Start-Sleep -Seconds 4

# Mostrar URL publica
try {
    $tunnels = (Invoke-WebRequest -Uri "http://127.0.0.1:4040/api/tunnels" -UseBasicParsing | ConvertFrom-Json).tunnels
    $url = $tunnels | Select-Object -ExpandProperty public_url | Where-Object { $_ -like "https://*" }
    Write-Host ""
    Write-Host "URL publica: $url" -ForegroundColor Magenta
    Write-Host "Webhook URL: $url/webhook" -ForegroundColor Magenta
    Write-Host ""
} catch {
    Write-Host "[ngrok] No se pudo obtener la URL todavia, espera unos segundos." -ForegroundColor Red
}

Write-Host "Ambos servicios corriendo. Presiona Ctrl+C para detener." -ForegroundColor Cyan
Write-Host ""

# Loop de supervision
while ($true) {
    Start-Sleep -Seconds 10

    if ($flask.HasExited) {
        Write-Host "[Flask] Se cayo, reiniciando..." -ForegroundColor Red
        $flask = Start-Flask
        Start-Sleep -Seconds 3
    }

    if ($ngrok.HasExited) {
        Write-Host "[ngrok] Se cayo, reiniciando..." -ForegroundColor Red
        $ngrok = Start-Ngrok
        Start-Sleep -Seconds 4
    }
}
