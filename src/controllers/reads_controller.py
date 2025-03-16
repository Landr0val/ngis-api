import psycopg2
from src.models.reads_model import Read
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from src.config.db_config import get_db_connection, realease_db_connection

class ReadsController:

    def create_read(self, read: Read):

        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")
        
        try:
            with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO measurement (device_id, unit_id, value, user_id) VALUES (%s, %s, %s, %s)",
                        (read.device_id,read.unit_id,read.value,read.user_id)
                        )
                    
                    connection.commit()

            return {"message": "Lectura guardada correctamente"}
        
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
        finally:
            realease_db_connection(connection)

    
    def get_last_read(self):

        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")
        
        try:
            with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY unit_id ORDER BY created_at DESC) as rn
                          FROM measurement
                          WHERE unit_id IN (1, 2) AND device_id = 1
                        ) sub
                        WHERE rn = 1
                        UNION
                        SELECT * FROM (
                          SELECT *, ROW_NUMBER() OVER (ORDER BY created_at DESC) as rn
                          FROM measurement
                          WHERE device_id = 2 AND unit_id = 2
                        ) sub2
                        WHERE rn = 1
                        ORDER BY unit_id;
                    """)
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
        
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
        finally:
            realease_db_connection(connection)

    def get_reads(self):

        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")
        
        try:
            with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM measurement")
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
        
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
        finally:
            realease_db_connection(connection)

    def get_read(self, user_id: int):
        
        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")
        
        try:
            with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM measurement WHERE user_id = %s", (user_id,))
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
        
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
        finally:
            realease_db_connection(connection)