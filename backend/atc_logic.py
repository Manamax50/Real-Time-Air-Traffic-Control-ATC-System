# atc_logic.py
import pika
import json
import os
import time
import datetime
from collections import deque
from supabase import create_client, Client


class ATCLogic:
    def __init__(self):
        self.airspaces = {
            'airspace_n': None,
            'airspace_s': None,
            'airspace_w': None,
            'airspace_e': None
        }
        self.runways = {
            'runway_1': None,
            'runway_2': None
        }
        self.airplanes = {}
        self.loading = []
        self.messages = []
        self.message_history = deque(maxlen=10)
        self.MAX_MESSAGES = 100
        self.DUPLICATE_WINDOW_SECONDS = 30
        self.runonce = 0
        self.plane_mode_global = ""

        # Supabase setup
        self.supabase_url = "https://rxyrnoobahmtvmbgdvlo.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4eXJub29iYWhtdHZtYmdkdmxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzOTMzMzAsImV4cCI6MjA1ODk2OTMzMH0.u7DmI5KcRzPK8B8HMyfa2l-qFxKMQqPz_w8T6szQtvo"
        self.supabase = create_client(self.supabase_url, self.supabase_key)

        self._init_data_files()

    def _init_data_files(self):
        os.makedirs("data", exist_ok=True)
        with open("data/plane_data.txt", 'w') as f:
            json.dump(self.airplanes, f, indent=4)
        with open("data/runways.txt", 'w') as f:
            json.dump(self.runways, f, indent=4)
        with open("data/airspaces.txt", 'w') as f:
            json.dump(self.airspaces, f, indent=4)
        with open("data/loading.txt", 'w') as f:
            json.dump(self.loading, f, indent=4)
        with open("data/messages.txt", 'w') as f:
            json.dump(self.messages, f, indent=4)

    def add_airplane(self, air_bool, airplane):
        """Assigns an airplane to the first available runway or airspace."""
        if not air_bool:
            for key in self.runways:
                if self.runways[key] == airplane:
                    return 'ok'
        else:
            for key in self.airspaces:
                if self.airspaces[key] == airplane:
                    return 'ok'

        if not air_bool:
            for key in self.runways:
                if self.runways[key] is None:
                    self.runways[key] = airplane
                    self.log_message(f"{airplane} assigned to {key}", airplane)
                    with open("data/runways.txt", 'w') as f:
                        json.dump(self.runways, f, indent=4)
                    return key
            else:
                self.log_message(f"No available runway space for {airplane}", airplane)
        else:
            for key in self.airspaces:
                if self.airspaces[key] == airplane:
                    return 'ok'
                if self.airspaces[key] is None:
                    self.airspaces[key] = airplane
                    self.log_message(f"{airplane} assigned to {key}", airplane)
                    with open("data/airspaces.txt", 'w') as f:
                        json.dump(self.airspaces, f, indent=4)
                    return key
            else:
                self.log_message(f"No available airspace for {airplane}", airplane)
        return None

    def remove_airplane(self, air_bool, airplane):
        """Removes an airplane from runways or airspaces."""
        if not air_bool:
            for key in self.runways:
                if self.runways[key] == airplane:
                    self.runways[key] = None
                    self.log_message(f"{airplane} removed from {key}", airplane)
                    with open("data/runways.txt", 'w') as f:
                        json.dump(self.runways, f, indent=4)
                    return key
        else:
            for key in self.airspaces:
                if self.airspaces[key] == airplane:
                    self.airspaces[key] = None
                    self.log_message(f"{airplane} removed from {key}", airplane)
                    with open("data/airspaces.txt", 'w') as f:
                        json.dump(self.airspaces, f, indent=4)
                    return key
        return None

    def check_available(self, air_bool):
        """Returns the first available (None) position in runways or airspaces."""
        if not air_bool:
            for key, value in self.runways.items():
                if value is None:
                    return key
        else:
            for key, value in self.airspaces.items():
                if value is None:
                    return key
        return None

    def sending_commands(self, message, plane_id):
        queue_name = f'commands{plane_id.strip()}'
        credentials = pika.PlainCredentials("admin", "AdminPass123!")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='4.172.252.16',
                port=5672,
                virtual_host='/',
                credentials=credentials
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        connection.close()

    def log_message(self, message, plane_id="SYSTEM"):
        current_time = time.time()

        # Check for duplicates
        for msg, msg_time in self.message_history:
            if msg == message and (current_time - msg_time) < self.DUPLICATE_WINDOW_SECONDS:
                return

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_message = {
            "timestamp": timestamp,
            "plane_id": plane_id,
            "message": message
        }

        self.messages.append(full_message)
        if len(self.messages) > self.MAX_MESSAGES:
            self.messages.pop(0)

        with open("data/messages.txt", 'w') as f:
            json.dump(self.messages, f, indent=4)

        self.message_history.append((message, current_time))

    def process_telemetry(self, body):
        string_data = body.decode('utf-8')
        parts = string_data.split(",")

        try:
            plane_id = parts[1].strip()
            plane_state = parts[2]
            plane_position = parts[3]
            plane_target = parts[4]
            plane_origin = parts[5]
            plane_destination = parts[6]
            plane_model = parts[7]
            plane_size = parts[8]
            plane_pascount = parts[9]
        except IndexError:
            self.log_message(f"Invalid telemetry format: {string_data}", "SYSTEM")
            return

        updated_data = {
            "plane_id": plane_id,
            "plane_state": plane_state,
            "plane_position": plane_position,
            "plane_target": plane_target,
            "plane_model": plane_model,
            "plane_size": plane_size,
            "plane_pascount": plane_pascount,
            "origin_country": plane_origin,
            "destination_country": plane_destination
        }

        self.airplanes[plane_id] = updated_data
        self.plane_mode_global = plane_model

        with open("data/plane_data.txt", 'w') as f:
            json.dump(self.airplanes, f, indent=4)

        supabase_data = {
            "plane_id": plane_id,
            "origin_country": updated_data["origin_country"],
            "destination_country": updated_data["destination_country"],
            "plane_model": plane_model,
            "plane_size": int(plane_size) if str(plane_size).isdigit() else 0,
            "passenger_count": int(plane_pascount) if str(plane_pascount).isdigit() else 0,
            "created_at": datetime.datetime.now().isoformat()
        }

        self.store_flight_data(plane_id, supabase_data)

        if plane_state == 'air':
            if plane_position == 'outer_airspace':
                self.log_message(f"Plane {plane_id} approaching from outer airspace", plane_id)
                new_position = self.add_airplane(True, plane_id)
                if new_position:
                    message = f'update_position,{new_position}'
                else:
                    message = 'wait,1'

                if new_position != 'ok' or new_position is None:
                    self.sending_commands(message, plane_id)

            elif plane_position in ['airspace_n', 'airspace_s', 'airspace_e', 'airspace_w']:
                self.log_message(f"Plane {plane_id} in {plane_position} requesting runway", plane_id)
                new_target = self.add_airplane(False, plane_id)
                if new_target:
                    message = f'update_target,{new_target}'
                else:
                    message = 'wait,1'

                if new_target != 'ok' or new_target is None:
                    self.sending_commands(message, plane_id)

        elif plane_state == 'landing':
            self.log_message(f"Plane {plane_id} beginning landing sequence on {plane_position}", plane_id)
            self.remove_airplane(True, plane_id)

        elif plane_state == 'ground':
            self.log_message(f"Plane {plane_id} now at gate loading passengers", plane_id)
            self.remove_airplane(False, plane_id)
            if plane_id not in self.loading:
                self.loading.append(plane_id)
                with open('data/loading.txt', 'w') as f:
                    json.dump(self.loading, f, indent=4)

        elif plane_state == 'taxiing':
            if plane_id in self.loading:
                self.loading.remove(plane_id)
                self.log_message(f"Plane {plane_id} finished loading passengers and left gate", plane_id)
                with open('data/loading.txt', 'w') as f:
                    json.dump(self.loading, f, indent=4)

            self.log_message(f"Plane {plane_id} beginning taxi to runway", plane_id)
            new_target_runway = self.add_airplane(False, plane_id)
            message = f'update_target,{new_target_runway}' if new_target_runway else 'wait,1'

            if new_target_runway != 'ok' or new_target_runway is None:
                self.sending_commands(message, plane_id)

        elif plane_state == 'takeoff':
            self.log_message(f"Plane {plane_id} beginning takeoff sequence from {plane_position}", plane_id)
            new_target_airspace = self.add_airplane(True, plane_id)
            message = f'update_target,{new_target_airspace}' if new_target_airspace else 'wait,1'

            if new_target_airspace != 'ok' or new_target_airspace is None:
                self.sending_commands(message, plane_id)

        elif plane_state == 'exit':
            removed_from_airspace = self.remove_airplane(True, plane_id)
            removed_from_runway = self.remove_airplane(False, plane_id)

            if plane_id in self.airplanes:
                del self.airplanes[plane_id]
                with open("data/plane_data.txt", 'w') as f:
                    json.dump(self.airplanes, f, indent=4)

    def store_flight_data(self, plane_id: str, plane_data: dict):
        self.runonce += 1
        try:
            response = self.supabase.table("flights").insert(plane_data).execute()
            if hasattr(response, 'error') and response.error:
                self.log_message(f"Supabase insert failed for {plane_id}: {response.error.message}", "SYSTEM")
        except Exception as e:
            self.log_message(f"Supabase error: {str(e)}", "SYSTEM")

    def run(self):
        credentials = pika.PlainCredentials("admin", "AdminPass123!")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='4.172.252.16',
                port=5672,
                virtual_host='/',
                credentials=credentials
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='flight_telemetry')

        def callback(ch, method, properties, body):
            print(f"Airspaces: {self.airspaces}")
            print(f"Runways: {self.runways}")
            print(f"Planes at Gates: {self.loading}")
            self.process_telemetry(body)

        channel.basic_consume(queue='flight_telemetry',
                              on_message_callback=callback,
                              auto_ack=True)
        print(' [*] ATC Logic waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


if __name__ == '__main__':
    atc = ATCLogic()
    atc.run()