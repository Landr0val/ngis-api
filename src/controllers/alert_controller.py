from src.models.alert_model import AlertConfig, Alert
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from src.config.db_config import get_db_connection

class AlertController:

    def create_alert(self, alert: AlertConfig):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO alert_config (temperature, air_humidity, soil_humidity, user_id) VALUES (%s, %s, %s, %s)",
                        (
                            alert.temperature,
                            alert.air_humidity,
                            alert.soil_humidity,
                            alert.user_id,
                        ),
                    )
                    conn.commit()
            return {"message": "Alerta guardada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_alert_config(self, user_id: int):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, temperature, air_humidity, soil_humidity, created_at 
                        FROM alert_config 
                        WHERE user_id = %s
                        """,
                        (user_id,)
                    )
                    result = cursor.fetchall()
            
            if result:
                return result
            else:
                return {"message": "No se encontraron configuraciones de alerta para el usuario especificado"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    def get_all_configs(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, temperature, air_humidity, soil_humidity, user_id created_at 
                        FROM alert_config
                        """
                    )
                    result = cursor.fetchall()
            
            if result:
                return result
            else:
                return {"message": "No se encontraron configuraciones de alerta para el usuario especificado"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        def post_alert(self, alert: Alert):
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO alert (temperature, air_humidity, soil_humidity, alert_config_id) VALUES (%s, %s, %s, %s)",
                            (
                                alert.temperature,
                                alert.air_humidity,
                                alert.soil_humidity,
                                alert.alert_config_id,
                            ),
                        )
                        conn.commit()
                return {"message": "Alerta guardada correctamente"}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))