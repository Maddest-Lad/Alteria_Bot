IF NOT EXIST venv (
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    call deactivate.bat
)
call venv\Scripts\activate.bat
python main.py