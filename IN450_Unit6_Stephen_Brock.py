import threading
import time
import random

class DressingRoom:
    def __init__(self, open_rooms):
        if open_rooms == '':
            self.open_rooms = 3
        else:   
            self.open_rooms = int(open_rooms)
        self.room_acess = threading.Semaphore(self.open_rooms)

        self.time = 0
        self.wait_time = 0
        self.room_time = 0
        self.item_count = 0
    
    def releaseRoom(self, count, time):
        print(f'Customer{count} is leaving the dressing room after {time} minutes.')

    def requestRoom(self, count, items):
        print(f'Customer{count} is waiting for a dressing room.')
        start_time = self.time
        if items == 0:
            items = random.randrange(1, 7)
        else:
            items = items
        self.item_count += items
        with self.room_acess:
            print(f'Customer{count} is using a dressing room.')
            end_time = self.time
            room_time = 0
            for i in range(items):
                duration = random.randrange(1, 4)
                time.sleep(0.05)
                self.time += duration
                room_time += duration
                self.room_time += room_time
        wait_time = end_time - start_time
        self.wait_time += wait_time
        self.releaseRoom(count, room_time)

class Scenario:
    def __init__(self):
        self.room_count = input('How many rooms are available? ')
        self.customer_count = int(input('How many customers are there? '))
        self.item_count = int(input('How many items per customer ("0" is a random number for each customer)? '))

        self.dressing_room = DressingRoom(self.room_count)
        self.threads = []
        for c in range(self.customer_count):
            t = threading.Thread(target=self.dressing_room.requestRoom, args=(c+1, self.item_count))
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()

        avg_time = int(self.dressing_room.wait_time/self.customer_count)
        avg_use = int(self.dressing_room.room_time/self.customer_count)
        avg_items = int(self.dressing_room.item_count/self.customer_count)

        print()
        print(f'Total number of customers: {self.customer_count}')
        print(f'Total time to service all customers: {self.dressing_room.time} minutes')
        print(f'Average customer wait time: {avg_time} minutes')
        print(f'Average number of items per customer: {avg_items} items')
        print(f'Average room use time: {avg_use} minutes')

scen1 = Scenario()