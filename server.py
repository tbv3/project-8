import socket
import psycopg2
from datetime import datetime, timedelta, timezone
import pytz

#hidden for privacy- replace with .env info
DB_CONFIG = {
    'dbname': 'DB_NAME',
    'user': 'DB_USER',
    'password': 'DB_PASS',
    'host': 'DB_HOST',
    'port': '5432',
    'sslmode': 'require'
}

DEVICE_METADATA = {
    "fridge1": {"device_id": 1, "device_type": "fridge", "timezone": "UTC", "unit": "moisture_percent"},
    "fridge2": {"device_id": 2, "device_type": "fridge", "timezone": "UTC", "unit": "electricity_kwh"},
    "dishwasher": {"device_id": 3, "device_type": "dishwasher", "timezone": "UTC", "unit": "water_liters"}
}

def convert_to_pst(utc_time):
    utc_dt = pytz.utc.localize(utc_time)
    pst_dt = utc_dt.astimezone(pytz.timezone('US/Pacific'))
    return pst_dt.strftime("%Y-%m-%d %H:%M:%S")

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def handle_query(query):
    conn = connect_db()
    cur = conn.cursor()

    try:
        if "moisture" in query:
            three_hours_ago = datetime.now(timezone.utc) - timedelta(hours=3)
            cur.execute("""
                SELECT AVG(moisture) FROM fridge_data 
                WHERE device_id = %s AND timestamp >= %s
            """, (DEVICE_METADATA["fridge1"]["device_id"], three_hours_ago))
            avg = cur.fetchone()[0]
            return f"Average Moisture (RH%) in Kitchen Fridge (last 3 hours): {round(avg,2)}%" if avg else \
                "No recent moisture data found."

        elif "water consumption" in query:
            cur.execute("""
                SELECT AVG(water_usage) FROM dishwasher_data 
                WHERE device_id = %s
            """, (DEVICE_METADATA["dishwasher"]["device_id"],))
            avg = cur.fetchone()[0]
            gallons = round(avg * 0.264172, 2) if avg else None
            return f"Average Water per Cycle: {gallons} gallons" if gallons else \
                "No dishwasher water data found."

        elif "electricity" in query:
            usage = {}
            for name, meta in DEVICE_METADATA.items():
                device_id = meta["device_id"]
                cur.execute("""
                    SELECT SUM(electricity) FROM device_energy_data 
                    WHERE device_id = %s
                """, (device_id,))
                total = cur.fetchone()[0] or 0
                usage[name] = total

            top_device = max(usage, key=usage.get)
            return f"{top_device.capitalize()} used the most electricity: {usage[top_device]:.2f} kWh"

        else:
            return "Invalid query."

    except Exception as e:
        return f"Database error: {str(e)}"
    finally:
        cur.close()
        conn.close()

def server_echo():
    HOST = input("Enter server IP: ")
    PORT = int(input("Enter server port: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on port {PORT}...")

        while True:
            client_socket, addr = s.accept()
            with client_socket:
                print("Client connected:", addr)
                query = client_socket.recv(4096).decode()

                if not query:
                    continue

                print("Received query:", query)
                response = handle_query(query)
                client_socket.sendall(response.encode())

if __name__ == '__main__':
    server_echo()
