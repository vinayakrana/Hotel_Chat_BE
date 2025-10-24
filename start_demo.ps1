# Start both API and Streamlit servers
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host "🏨 Hotel Chatbot - Starting Servers"
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated!" -ForegroundColor Yellow
    Write-Host "Run: venv\Scripts\activate" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne "y") {
        exit
    }
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your GROQ_API_KEY" -ForegroundColor Red
    exit
}

Write-Host "🚀 Starting API Server..." -ForegroundColor Green
Start-Process python -ArgumentList "main.py" -WindowStyle Normal

Write-Host "⏳ Waiting for API to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "🎨 Starting Streamlit App..." -ForegroundColor Green
Start-Process python -ArgumentList "-m streamlit run app.py" -WindowStyle Normal

Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Streamlit will open at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "📚 API docs available at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Demo Credentials:" -ForegroundColor Yellow
Write-Host "   Guest: guest@hotel.com / guest123"
Write-Host "   Staff: staff@hotel.com / staff123"
Write-Host ""
Write-Host "Close the terminal windows to stop the servers"
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
