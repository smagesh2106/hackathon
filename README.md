# framework_fastapi

uvicorn main:app --reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
JWT_SECRET=`tr -dc A-Za-z0-9 </dev/urandom | head -c 20 ; echo ''`
Google App password generation URL https://myaccount.google.com/apppasswords
swagger api docs: http://127.0.0.1:8000/docs
