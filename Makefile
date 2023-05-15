
make: exportar_app exportar_env run
	source venv-api/bin/activate

exportar_app:
	export FLASK_APP=app.py

exportar_env:
	FLASK_ENV=development 

run:
	uvicorn app:app --reload

