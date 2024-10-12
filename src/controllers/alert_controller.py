# src/controllers/alert_controller.py

from src.models.alert_model import AlertConfig, Alert, AlertConfigUpdate
from fastapi import HTTPException
from src.config.db_config import get_db_connection
from psycopg2 import sql  # Importación necesaria
import psycopg2  # Asegúrate de que psycopg2 esté instalado

class AlertController:

    def create_alert(self, alert: AlertConfig):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Inicializar las columnas y valores con el campo obligatorio 'user_id'
                    columns = ["user_id"]
                    values = [alert.user_id]

                    # Contador para verificar que al menos uno de los tres campos esté presente
                    data_fields_provided = 0

                    # Agregar los campos de datos si están presentes
                    if alert.temperature is not None:
                        columns.append("temperature")
                        values.append(alert.temperature)
                        data_fields_provided += 1

                    if alert.air_humidity is not None:
                        columns.append("air_humidity")
                        values.append(alert.air_humidity)
                        data_fields_provided += 1

                    if alert.soil_humidity is not None:
                        columns.append("soil_humidity")
                        values.append(alert.soil_humidity)
                        data_fields_provided += 1

                    # Validar que al menos uno de los campos de datos esté presente
                    if data_fields_provided == 0:
                        raise HTTPException(
                            status_code=400,
                            detail="Debe proporcionar al menos uno de los campos: temperature, air_humidity, soil_humidity."
                        )

                    # Agregar los campos opcionales de thresholds si están presentes
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
                        SELECT id, temperature, air_humidity, soil_humidity, temperature_threshold_id, air_humidity_threshold_id, soil_humidity_threshold_id, created_at 
                        FROM alert_config 
                        WHERE user_id = %s
                        """,
                        (user_id,)
                    )
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    result = [dict(zip(columns, row)) for row in rows]
        
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
                        SELECT id, temperature, air_humidity, soil_humidity, temperature_threshold_id, air_humidity_threshold_id, soil_humidity_threshold_id, user_id, created_at 
                        FROM alert_config
                        """
                    )
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    result = [dict(zip(columns, row)) for row in rows]
        
            if result:
                return result
            else:
                return {"message": "No se encontraron configuraciones de alerta para los usuarios especificados"}
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

    def update_alert_config(self, alert_id: int, alert_update: AlertConfigUpdate):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Convertir el modelo Pydantic a un diccionario excluyendo valores None
                    update_data = alert_update.dict(exclude_unset=True)
                    
                    if not update_data:
                        raise HTTPException(
                            status_code=400,
                            detail="Debe proporcionar al menos uno de los campos para actualizar."
                        )
                    
                    # Construir las partes de la consulta SQL dinámicamente
                    set_clauses = []
                    values = []
                    for key, value in update_data.items():
                        set_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
                        values.append(value)
                    
                    # Agregar el alert_id al final de los valores
                    values.append(alert_id)
                    
                    # Construir la consulta SQL completa
                    query = sql.SQL("UPDATE alert_config SET {set_clauses} WHERE id = %s").format(
                        set_clauses=sql.SQL(', ').join(set_clauses)
                    )
                    
                    # Ejecutar la consulta
                    cursor.execute(query, values)
                    
                    # Verificar si alguna fila fue actualizada
                    if cursor.rowcount == 0:
                        raise HTTPException(
                            status_code=404,
                            detail=f"No se encontró una configuración de alerta con id {alert_id}."
                        )
                    
                    conn.commit()
        
            return {"message": "Configuración de alerta actualizada correctamente"}
        
        except psycopg2.Error as e:
            # Manejo específico de errores de psycopg2
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # Manejo general de otros errores
            raise HTTPException(status_code=400, detail=str(e))
