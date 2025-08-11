#!/usr/bin/env python
import pika
import threading
import os, sys, time
import random


#constants for how long it takes to do certain actions, but during imp commands can add more time to some actions
AIR_TIME = 3 + random.randint(0,2)
LANDING_TIME = 3 + random.randint(0,2)
GROUND_TIME = 4 + random.randint(0,2)
TAXI_TIME = 4 + random.randint(0,2)
TAKEOFF_TIME = 2 + random.randint(0,2)


class Airplane(threading.Thread): #each object created in its own thread
    def __init__(self, id, state, position, target, origin, destination):
        super().__init__()
        self.id = id
        self.state = state
        self.position = position
        self.origin = origin
        self.destination = destination
        self.target = target
        self.time_running = True
        self.count = 0
        # Start both the main thread and a separate threads for receiving messages
        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.timer_thread = threading.Thread(target=self.timer, daemon=True)
        self.receive_thread.start()
        self.timer_thread.start()
        
        self.start()  # Runs run() in its own thread

    def timer(self):
        """continuously counts"""
        random_int = random.randint(0, 5)
        plane, size, passenger_count = self.get_plane_info(random_int)
        print(f"RANDOMLY GENERATED PLANE:\nPlane Model: {plane}. Length: {size}m. Passenger Count: {passenger_count}")
        while self.time_running:
            self.count += 1
            credentials = pika.PlainCredentials("admin", "AdminPass123!")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='4.172.252.16',  # Your VM's IP
                    port=5672,
                    virtual_host='/',      # Explicitly specify the vhost
                    credentials=credentials
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='flight_telemetry')
            message = f"telemetry, {self.id},{self.state},{self.position},{self.target},{self.origin},{self.destination},{plane},{size},{passenger_count}"
            channel.basic_publish(exchange='', routing_key='flight_telemetry', body=message)
            print(f"T{self.count}: Sent: {message}")
            time.sleep(1)
            if self.count >= 50: #ts takes too long
                try:
                    sys.exit(1)
                    channel.close()
                except KeyboardInterrupt:
                    print('Interrupted')
                    sys.exit(0)

    def get_plane_info(self, random_int): #nice list to get some info on plane 
        info_map = {
            0: {"plane": 'Airbus A320', "size": 38, "passenger_count": random.randint(80, 170)},
            1: {"plane": 'Boeing 737', "size": 39, "passenger_count": random.randint(100, 190)},
            2: {"plane": 'Boeing 777', "size": 74, "passenger_count": random.randint(300, 350)},
            3: {"plane": 'Airbus A380', "size": 80, "passenger_count": random.randint(430, 500)},
            4: {"plane": 'Embraer E190', "size": 28, "passenger_count": random.randint(50, 110)},
            5: {"plane": 'Bombardier CRJ700', "size": 27, "passenger_count": random.randint(50, 100)}
        }
        info = info_map.get(random_int, {"plane": "Unknown", "size": 0, "passenger_count": 0})
        return info["plane"], info["size"], info["passenger_count"]



    def run(self):  # This method is called when start() is executed
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost')
        # )
        # channel = connection.channel()
        # channel.queue_declare(queue='flight_telemetry')

         #random plane type and size:
        
        
        ####### AIR START #######
        #1: approaching runway (target) from specific airspace (position)
        
        if self.state == 'air':
            print('############################################################\n')
            print(f'{self.state}: This plane is approaching ATC airspace,  approaching {self.target}.') #in outer airspace, need message to know which airspace to approach from. (N,S,W,E)
            print(f'{self.state}: This plane is coming from position {self.position}, approaching {self.target}. Begin landing sequence in {AIR_TIME} seconds')
            self.count_mark = self.count
            while (self.count - self.count_mark) < AIR_TIME: #this part may get delayed if all airspaces are busy
                a = 0
            self.state = 'landing' #new state
            self.position = self.target #position now a runway
            self.target = 'loading' #target is loading
            

            print('############################################################\n')
            print(f"{self.state}: Commencing landing on position {self.position} towards {self.target}. Landing takes {LANDING_TIME} seconds to for airplane to reach a gate and begin loading")
            self.count_mark = self.count
            while (self.count - self.count_mark) < LANDING_TIME: #shouldnt be any delays here
                a = 0
            self.state = 'ground'
            self.position = self.target
            self.target = 'none'
            
        
        if self.state == 'ground':
            print('############################################################\n')
            print(f"{self.state}: Airplane now waiting to board passengers at {self.position}. Loading takes {GROUND_TIME} seconds.")
            self.count_mark = self.count
            while (self.count - self.count_mark) < GROUND_TIME:
                a = 0
            self.state = 'taxiing'
            self.position = 'loading' #waiting done, begin moving to a runway
            self.target = 'none'
            
            print('############################################################\n')
            print(f"{self.state}: Airplane now beginning taxiing sequence towards {self.target}. Taxiing takes {TAXI_TIME} seconds.")
            self.count_mark = self.count
            while (self.count - self.count_mark) < TAXI_TIME: #could be delayed to wait for runway availability
                if self.target == 'none':
                    self.count_mark = self.count
            self.state = 'takeoff'
            self.position = self.target #taxiing done, now on a runway
            self.target = 'none'
            self.state = 'takeoff'
            print('############################################################\n')
            print(f"{self.state}: Airplane now beginning takeoff sequence from {self.position} towards {self.target}. Takeoff takes {TAKEOFF_TIME} seconds.")
            self.count_mark = self.count
            while (self.count - self.count_mark) < TAKEOFF_TIME: #could be delayed to wait for airspace availability
                if self.target == 'none':
                    self.count_mark = self.count
            self.state = 'air'
            self.position = self.target
            self.target = 'outer_airspace'
            print('############################################################\n')
            print(f'{self.state}: Airplane has taken off and is now leading the airspace from {self.position}')
            self.count_mark = self.count
            while (self.count - self.count_mark) < 2: #takes 2 seconds to fly out of airspace.
                if self.target == 'none':
                    self.count_mark = self.count
            self.state = 'exit'
            self.position = self.target
            print('############################################################\n')
            print(f'{self.state}: plane has taken off and exited airspace')
            self.count_mark = self.count
            while (self.count - self.count_mark) < 2: #takes 2 seconds to fly out of airspace.just some bonus time so atc can log exit telemetry.
                a = 0   

            
            # message = f"SENDING UPDATE 1, {self.id},{self.state},{self.position},{self.target},{plane},{size},{passenger_count}"
            # channel.basic_publish(exchange='', routing_key='flight_telemetry', body=message)
            # print("Sent:", message)

    def process_command(self, body):
        string_data = body.decode('utf-8')
        #print("COMMAND RECEIVED") #spams u
        #print(string_data)
        parts = string_data.split(",")
        message_1 = parts[0]
        message_2 = parts[1]
        if message_1 == 'update_target':
            self.target = message_2 #can update states n stuff from outside!
            print(f'!!! Updated Target: {self.target} !!!\n','!'*35 )
        elif message_1 == 'update_position':
            self.position = message_2
            print(f'!!! Updated Position: {self.position} !!!\n','!'*35 )
        elif message_1 == 'wait':
            self.count_mark = self.count_mark+int(message_2)
            print(f'!!! Wait at position: {self.position} !!!\n','!'*35 ) 

    def receive(self):
        """ Continuously listen for messages from ATC. """
        credentials = pika.PlainCredentials("admin", "AdminPass123!")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='4.172.252.16',  # Your VM's IP
                port=5672,
                virtual_host='/',      # Explicitly specify the vhost
                credentials=credentials
            )
        )
        channel = connection.channel()
        queue_name = f'commands{self.id}'
        print(f"\nCREATING NEW QUEUE: {queue_name} ")
        channel.queue_declare(queue=queue_name)

        def callback(ch, method, properties, body):
            print("!!!!!!!!!received message!!!!!!!!!")
            self.process_command(body)
        
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(f"[{self.id}] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()  # Keeps running in an infinite loop


if __name__ == '__main__':

    plane_id = sys.argv[1]
    plane_state = sys.argv[2]  # Use as a string (avoid int conversion)
    plane_position = sys.argv[3]  # Use as a string (avoid int conversion)
    plane_target = sys.argv[4]
    plane_origin_country = sys.argv[5]
    plane_destination_country = sys.argv[6]
    if plane_state == 'air':
        if plane_position not in ['outer_airspace']: #['airspace_n', 'airspace_s', 'airspace_e', 'airspace_w']
            print("if plane starting in state air, position must be in outer_airspace")
            print("Usage: airplane.py <id> <state> <position> <target>")
            sys.exit(1)
    elif plane_state == 'ground':
        if plane_position not in ['loading']:
            print("if plane starting in state ground, position must be a loading passenger: 'loading'")
            print("Usage: airplane.py <id> <state> <position> <target>")
            sys.exit(1)
    else:
        print("invalid starting state: must be either approaching the airport or starting on the ground: 'air', 'ground'")
        print("Usage: airplane.py <id> <state> <position> <target>")
        sys.exit(1)

    try:
        plane = Airplane(plane_id, plane_state, plane_position, plane_target, plane_origin_country, plane_destination_country)
        plane.join()  # Wait for the main thread (run method) to finish
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
