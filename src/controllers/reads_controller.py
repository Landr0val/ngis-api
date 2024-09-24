from src.models.reads_model import Read
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from src.config.db_config import get_db_connection

class ReadsController:

    def create_read(self, read: Read):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO measurement (device_id, unit_id, value, user_id) VALUES (%s, %s, %s, %s)",
                        (
                            read.device_id,
                            read.unit_id,
                            read.value,
                            read.user_id,
                        ),
                    )
                    conn.commit()
            return {"message": "Lectura guardada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_last_read(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM (
                            SELECT *, ROW_NUMBER() OVER (PARTITION BY unit_id ORDER BY created_at DESC) as rn
                            FROM measurement_view
                            WHERE unit_id IN (1, 2)
                        ) sub
                        WHERE rn = 1
                        ORDER BY unit_id
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
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_reads(self):
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