# src/controllers/alert_controller.py

from src.models.alert_model import AlertConfig, Alert
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from src.config.db_config import get_db_connection
from psycopg2 import sql  # Importación necesaria
import psycopg2  # Asegúrate de que psycopg2 esté instalado

class AlertController:

    def create_alert(self, alert: AlertConfig):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Definir las columnas y valores obligatorios
                    columns = ["temperature", "air_humidity", "soil_humidity", "user_id"]
                    values = [
                        alert.temperature,
                        alert.air_humidity,
                        alert.soil_humidity,
                        alert.user_id
                    ]

                    # Validar que los valores obligatorios no sean None
                    if None in values:
                        raise HTTPException(status_code=400, detail="Faltan valores obligatorios")

                    # Agregar los campos opcionales si están presentes
                    if alert.temperature_threshold_id is not None:
                        columns.append("temperature_threshold_id")
                        values.append(alert.temperature_threshold_id)
                    
                    if alert.air_humidity_threshold_id is not None:
                        columns.append("air_humidity_threshold_id")
                        values.append(alert.air_humidity_threshold_id)
                    
                    if alert.soil_humidity_threshold_id is not None:
                        columns.append("soil_humidity_threshold_id")
                        values.append(alert.soil_humidity_threshold_id)

                    # Construir dinámicamente la consulta SQL
                    query = sql.SQL("INSERT INTO alert_config ({fields}) VALUES ({placeholders})").format(
                        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                        placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values))
                    )

                    # Ejecutar la consulta con los valores dinámicos
                    cursor.execute(query, values)
                    conn.commit()

            return {"message": "Alerta guardada correctamente"}
        
        except psycopg2.Error as e:
            # Manejo específico de errores de psycopg2
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # Manejo general de otros errores
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
        except psycopg2.Error as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    def get_all_configs(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, temperature, air_humidity, soil_humidity, user_id, created_at 
                        FROM alert_config
                        """
                    )
                    result = cursor.fetchall()
        
            if result:
                return result
            else:
                return {"message": "No se encontraron configuraciones de alerta para el usuario especificado"}
        except psycopg2.Error as e:
            raise HTTPException(status_code=400, detail=str(e))
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
