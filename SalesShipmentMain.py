from SalesShipmentGZ import SalesShipmentGZ
from SalesShipmentSH import SalesShipmentSH
from apscheduler.schedulers.blocking import BlockingScheduler
import random


def salesshipment_function():
    SalesShipmentGZ()
    SalesShipmentSH()


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(salesshipment_function, 'interval', minutes=random.randint(10, 30))
    sched.start()
