from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

# ===============================
# CONFIGURACIÓN JWT
# ===============================
SECRET_KEY = "SUPER_SECRET_KEY_CAMBIAR"  # luego lo pasas a .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ===============================
# PASSWORD HASHING
# ===============================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ===============================
# PASSWORD HELPERS
# ===============================
def hash_password(password: str) -> str:
    """
    Genera el hash seguro de un password
    """
    password = password.strip()[:72]  # bcrypt límite
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica password contra su hash
    """
    plain_password = plain_password.strip()[:72]
    return pwd_context.verify(plain_password, hashed_password)

# ===============================
# JWT TOKEN
# ===============================
def create_access_token(data: dict) -> str:
    """
    Crea un JWT válido
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
