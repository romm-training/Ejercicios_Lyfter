# Crear y activar el entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Generar llaves RS256 (desde Git Bash, en la carpeta keys/)
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out private.pem
openssl rsa -in private.pem -pubout -out public.pem

# Ejecutar
python app.py

# Variables de ambiente
DATABASE_URL 
JWT_PRIVATE_KEY_PATH
JWT_PUBLIC_KEY_PATH.