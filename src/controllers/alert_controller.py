from src.models.alert_model import Alert
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from src.config.db_config import get_db_connection

class AlertController:

    def create_alert(self, alert: Alert):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO measurement (temperature, air_humidity, soil_humidity, user_id) VALUES (%s, %s, %s, %s)",
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

    def get_alerts(self, alert: Alert):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM measurement_view")
                    rows = cursor.fetchall()
                    payload = []

                    for row in rows:
                        payload.append({
                            "id": row[0],
                            "device_id": row[1],
                            "unit_id": row[2],
                            "user_id": row[3],
                            "value": row[4],
                            "created_at": row[5],
                            "updated_at": row[6]
                        })

            return jsonable_encoder(payload)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))