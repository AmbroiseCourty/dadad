import pathlib


MODULES_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = MODULES_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
USERS_CSV_FILE = DATA_DIR / "users.csv"
HASH_CSV_FILE = DATA_DIR / "rockyou" / "hash_comp.csv"
ROCKYOU_FILE = DATA_DIR / "rockyou" / "rockyou.txt"

GESTION_PROD_DIR = MODULES_DIR / "gestion_prod"
GESTION_USERS_DIR = MODULES_DIR / "gestion_users"
PASSWORD_COMP_DIR = MODULES_DIR / "password_comp"

API_FILE = PASSWORD_COMP_DIR / "api.py"
FONCTION_PROD_FILE = GESTION_PROD_DIR / "fonction_prod.py"
TRI_FILE = GESTION_PROD_DIR / "tri.py"
FONCTION_USERS_FILE = GESTION_USERS_DIR / "fonction_users.py"
HASH_SESSIONS_FILE = GESTION_USERS_DIR / "hash-sessions.py"


PATHS_FILE = MODULES_DIR / "paths.py"