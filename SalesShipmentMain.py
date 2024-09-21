from SalesShipmentGZ import SalesShipmentGZ
from SalesShipmentSH import SalesShipmentSH
from apscheduler.schedulers.blocking import BlockingScheduler
import random


def salesshipment_function():
    companygz = '希肤广州'
    companysh = '希肤广州'
    dbname = 'SalesShipment.db'
    tablename = 'salesshipment'
    SalesShipmentGZ(companygz, dbname, tablename)
    SalesShipmentSH(companysh, dbname, tablename)


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(salesshipment_function, 'interval', minutes=random.randint(10, 30))
    sched.start()
