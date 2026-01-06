import threading
import time
import random

class Customer:
    def __init__(self, count, items, assigned_room):
        self.assigned_room = assigned_room
        self.count = count
        if items == 0:
            self.items = random.randrange(1, 7)
        else:
            self.items = items
        
    def useRoom(self):
        room_time = 0
        print(f'Customer{self.count} is using a dressing room.')
        room =  ''
        for i in range(self.items):
            duration = random.randrange(1, 4)
            time.sleep(0.05)
            room_time += duration
        with self.assigned_room.lock:
            self.assigned_room.item_count += self.items
            empty = next((idx for idx, li in enumerate(self.assigned_room.time_matrix) if not li), None)
            if empty is not None: 
                room = empty 
            else: 
                totals = [sum(li) for li in self.assigned_room.time_matrix] 
                room = totals.index(min(totals))
            self.assigned_room.time_matrix[room].append(self.assigned_room.OCCUPIED_PLACEHOLDER)
        return self.count, room_time, room

class DressingRoom:
    def __init__(self, open_rooms):
        if open_rooms == '':
            self.open_rooms = 3
        else:   
            self.open_rooms = int(open_rooms)

        self.room_access = threading.Semaphore(self.open_rooms)
        self.lock = threading.Lock()
        self.OCCUPIED_PLACEHOLDER = 9999

        self.item_count = 0
        self.wait_time = 0
        self.room_time = 0

        self.time_matrix = []
        for i in range(self.open_rooms):
            i = []
            self.time_matrix.append(i)
    
    def releaseRoom(self, count, time, room):
        print(f'Customer{count} is leaving the dressing room after {time} minutes.')
        li = self.time_matrix[room]
        with self.lock:
            self.room_time += time
            self.wait_time += sum(li)
            li[-1] = time
        self.room_access.release()

    def requestRoom(self, count):
        print(f'Customer{count} is waiting for a dressing room.')
        self.room_access.acquire()

    def service_customer(self, customer: Customer):
        self.requestRoom(customer.count)
        count, time, room = customer.useRoom()
        self.releaseRoom(count, time, room)

class Scenario:
    def __init__(self):
        room_count = input('How many rooms are available? ')
        customer_count = int(input('How many customers are there? '))
        item_count = int(input('How many items per customer ("0" is a random number for each customer)? '))

        dressing_room = DressingRoom(room_count)
        threads = []
        for c in range(customer_count):
            customer = Customer(c+1, item_count, dressing_room)
            t = threading.Thread(target=dressing_room.service_customer, args=(customer,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total_time = []
        for i in dressing_room.time_matrix:
            total = 0
            for time in i:
                total += time
            total_time.append(total)
        
        total_time = max(total_time)

        avg_time = int(dressing_room.wait_time/customer_count)
        avg_use = int(dressing_room.room_time/customer_count)
        avg_items = int(dressing_room.item_count/customer_count)

        print()
        print(f'Total number of customers: {customer_count}')
        print(f'Total time to service all customers: {total_time} minutes')
        print(f'Average customer wait time: {avg_time} minutes')
        print(f'Average number of items per customer: {avg_items} items')
        print(f'Average room use time: {avg_use} minutes')

if __name__ == '__main__':
    scen1 = Scenario()