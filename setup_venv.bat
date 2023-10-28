py -3 -m venv %~dp0\journal_venv
call %~dp0\journal_venv\Scripts\activate
pip install -r requirements.txt
call %~dp0\journal_venv\Scripts\deactivate
cmd /k