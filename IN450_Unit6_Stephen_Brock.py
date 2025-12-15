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
        self.lock = threading.Lock()

        self.wait_time = 0
        self.room_time = 0
        self.item_count = 0

        self.time_matrix = []
        for i in range(self.open_rooms):
            i = []
            self.time_matrix.append(i)
    
    def releaseRoom(self, count, time, room):
            print(f'Customer{count} is leaving the dressing room after {time} minutes.')
            li = self.time_matrix[room]
            self.wait_time += sum(li)
            li.append(time)

    def requestRoom(self, count, items):
        if items == 0:
            items = random.randrange(1, 7)
        else:
            items = items
        print(f'Customer{count} is waiting for a dressing room.')
        room_time = 0
        with self.room_acess:
            print(f'Customer{count} is using a dressing room.')
            room =  ''
            with self.lock:
                self.item_count += items
                for i in self.time_matrix:
                    if len(i) == 0:
                        room = self.time_matrix.index(i)
                        break
                    else:
                        room_dur = []
                        for i in self.time_matrix:
                            dur = sum(i)
                            room_dur.append(dur)
                        min_dur = min(room_dur)
                        room = room_dur.index(min_dur)
                        break
                for i in range(items):
                    duration = random.randrange(1, 4)
                    time.sleep(0.05)
                    room_time += duration
                    self.room_time += duration
                self.releaseRoom(count, room_time, room)

class Scenario:
    def __init__(self):
        room_count = input('How many rooms are available? ')
        customer_count = int(input('How many customers are there? '))
        item_count = int(input('How many items per customer ("0" is a random number for each customer)? '))

        dressing_room = DressingRoom(room_count)
        threads = []
        for c in range(customer_count):
            t = threading.Thread(target=dressing_room.requestRoom, args=(c+1, item_count))
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