if (!(Test-Path -Path "venv" -PathType Container)) {
    python -m venv venv
    & ".\venv\Scripts\activate.ps1"
    pip install -r requirements.txt
    & deactivate.ps1
}
& ".\venv\Scripts\activate.ps1"
python main.py