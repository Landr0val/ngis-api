from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.config.db_config import get_db_connection, realease_db_connection
from src.models.users_model import TokenResponse
from src.middleware.access_token import create_access_token
from src.middleware.validation import validate_user_login, verify_password
from psycopg2 import sql

class LoginController:

    def login(self, from_data: OAuth2PasswordRequestForm):
        validate_user_login(from_data)

        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")
        
        try:
            with connection.cursor() as cursor:
                query = sql.SQL("SELECT id, username, password, name, lastname, email, rol_id FROM \"user\" WHERE username = %s")
                cursor.execute(query, [from_data.username])
                user = cursor.fetchone()

                if user is None or not verify_password(from_data.password, user[2]):
                    raise HTTPException(status_code=400, detail="Invalid username or password")

                token_jwt = create_access_token(user_id=user[0], username=user[1], email=user[5], rol_id=user[6])
                return TokenResponse(access_token=token_jwt)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            realease_db_connection(connection)