# Standard library imports
import json
import os
import time
from functools import wraps
import asyncio

# Third-party library imports
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException

# Application-specific imports
from apiKeysDatabase import ApiKeysDatabase
from techniques.EquivalencePartition import EquivalencePartition
from techniques.LimitValueAnalysis import LimitValueAnalysis
from techniques.OrthogonalArray import OrthogonalArray

import smtplib
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()
master_apikey = api_key = os.getenv("API_KEY")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Initialize API keys database
apikeys = ApiKeysDatabase(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "https://test-case-recuder-front-end.vercel.app",
    "test-case-recuder-front-end-git-main-testcasereducer.vercel.app",
    "https://test-case-recuder-front-25xphy323-testcasereducer.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def api_key_required(f):
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        api_key = request.query_params.get('api_key', '')
        if not api_key or (api_key != master_apikey and api_key not in apikeys.get_all_api_keys()):
            return JSONResponse(content={'error': 'API key inválida'}, status_code=status.HTTP_403_FORBIDDEN)
        return await f(request, *args, **kwargs)
    return decorated_function

@app.get('/api')
@api_key_required
async def process_request(request: Request):
    technique = request.query_params.get('technique', '')
    parameters = request.query_params.get('parameters', '')

    if not technique or not parameters:
        return JSONResponse(content={'error': 'Parámetros inválidos'}, status_code=status.HTTP_400_BAD_REQUEST)

    try:
        parameters = json.loads(parameters)
    except json.JSONDecodeError:
        return JSONResponse(content={'error': 'Entrada inválid'}, status_code=status.HTTP_400_BAD_REQUEST)

    start_time = time.time()
    test_cases = []

    try:

        if technique == 'EP':
            test_cases = EquivalencePartition(parameters).build_test_cases()
        elif technique == 'LVA':
            test_cases = LimitValueAnalysis(parameters).build_test_cases()
        elif technique == 'OA':
            test_cases = OrthogonalArray(parameters).build_test_cases()
        response = {
            'error' : False,
            'technique': technique,
            'test-cases': test_cases,
            'elapsed-time' : '{:.5f}'.format(time.time() - start_time)
        }
    except Exception as e:
        response = {
            'error' : True,
            'error-message': str(e),
            'elapsed-time' : '{:.5f}'.format(time.time() - start_time)
        }

    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@app.post('/api/create_user')
@api_key_required
async def create_user(request: Request, email: str):
    if request.query_params.get('api_key') != master_apikey:
        raise HTTPException(status_code=403, detail="API key maestra requerida")
    
    if not email:
        raise HTTPException(status_code=400, detail="El email es requerido")
    try:
        api_key = apikeys.get_api_key(email)
        if not api_key:
            api_key = apikeys.create_api_key(email)
        sent = await send_api_key_with_timeout(email, api_key)
        assert sent == True
        return {"success": True , "message": "API Key enviada correctamente."}
    except Exception as e:
        return {"success": False, "message": str(e)}



async def send_api_key_with_timeout(email, api_key):
    try:
        sent = await asyncio.wait_for(send_api_key_email(email, api_key), timeout=6)
    except asyncio.TimeoutError:
        sent = None
    return sent



async def send_api_key_email(email, api_key):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    subject = "Tu API Key"
    body = f"Hola,\n\nAquí tu Api key: {api_key}\n\nPor favor, no comparta esta clave con otros.\n\nGracias!"
    
    msg = MIMEText(body)
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = subject

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            sent = server.sendmail(smtp_user, email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False



if __name__ == "__main__":
    app.run(debug=True)