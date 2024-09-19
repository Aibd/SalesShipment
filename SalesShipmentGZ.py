from MSSqlDB import MSSqlDBManager
from SQLiteDB import SqliteDBManager
from jdy import JDYApi
from logger import Logger
from common import Common
import time
import random
import utils


# 简道云批量删除数据
def delete_jdy_data(jdy_api, kdata):
    query_data = Common.query_data
    ids = []
    for data in kdata:
        finterid = data[0]
        fentryid = data[1]
        query_data["filter"]["cond"][0]["value"] = finterid
        query_data["filter"]["cond"][1]["value"] = fentryid
        query_data["filter"]["cond"][2]["value"] = '希肤广州'
        id = jdy_api.query_dataid(Common.query_data)
        if id:
            ids.append(id[0])
    if ids:
        result = jdy_api.batch_delete(entry_id=Common.entry_id, ids=ids)
        if result:
            return result


# Sqlite批量删除数据
def delete_sqlite_data(dbname, tablename, kdata):
    with SqliteDBManager(dbname) as sqlitemanager:
        for data in kdata:
            id = data[0]
            entryid = data[1]
            company = '希肤广州'
            sqlitemanager.execute(
                f"DELETE FROM {tablename} WHERE ID = {id} AND EntryID = {entryid} AND Company = {company}")


def SalesShipmentGZ():
    jdy_api = JDYApi(Common.api_key, Common.app_id)
    log = Logger('main', 'SalesShipment.log')

    # 获取金蝶销售出库数据
    with MSSqlDBManager('希肤广州') as msmanager:
        kdata = msmanager.execute(Common.SalesShipmentGZ_query_sql, fetch=True)

    # 将最新数据插入本地Sqlite临时表temp中
    with SqliteDBManager('SalesShipment.db') as sqlitemanager:
        # 插入前先清除缓存表数据
        sqlitemanager.execute('DELETE FROM temp')
        sqlitemanager.execute(Common.insert_temp_sql, params=kdata)

    # 在sqlite中比对两侧数据
    # 比对删除数据，删除被同步端数据
    with SqliteDBManager('SalesShipment.db') as sqlitemanager:
        query_sql = Common.deleted_query_sql.format(company='希肤广州')
        deleted_kdata = sqlitemanager.execute(query_sql, fetch=True)
    if deleted_kdata:
        # 删除简道云数据
        result = delete_jdy_data(jdy_api, deleted_kdata)
        # 删除成功 输出日志，同时删除sqlite映射数据
        log.info(result)
        delete_sqlite_data('SalesShipment.db', 'salesshipment', deleted_kdata)
        log.info('deleted_kdata: ',deleted_kdata)
    # 比对更新和增量数据，同步数据（同步时校验被同步端是否存在，存在则删除后同步最新数据）
    with SqliteDBManager('SalesShipment.db') as sqlitemanager:
        diff_sql = Common.differences_sql.format(company='希肤广州')
        diff_data = sqlitemanager.execute(diff_sql, fetch=True)
        differences = [list(tup) for tup in diff_data]

    if differences:
        # 由于简道云限制 每次只能上传100条数据，同时每秒只能上传10次，所以大于100我们分批上传
        batch_size = 100
        if len(differences) > batch_size:
            # 处理批次数据
            for batch in [differences[i:i + batch_size] for i in range(0, len(differences), batch_size)]:
                # 先判断新增数据是否已存在，如果已存在先删除再添加
                delete_jdy_data(jdy_api, batch)
                # 上传简道云并写入本地Sqlite映射表
                processed_data = utils.data_process(batch, Common.jdy_salesshipment_data)
                result = jdy_api.upload(processed_data)
                if result is not None:
                    log.info("简道云上传结果：" + str(result))
                    # 插入到本地sqlite中
                    with SqliteDBManager('SalesShipment.db') as sqlitemanager:
                        # 插入前先清除缓存表数据
                        sqlitemanager.execute(Common.insert_salesshipment_sql, params=batch)
                time.sleep(random.randint(1, 5))
        else:
            # 先判断新增数据是否已存在，如果已存在先删除再添加
            delete_jdy_data(jdy_api, differences)
            # 上传简道云并写入本地Sqlite映射表
            processed_data = utils.data_process(differences, Common.jdy_salesshipment_data)
            result = jdy_api.upload(processed_data)
            if result is not None:
                log.info("简道云上传结果：" + str(result))
                # 插入到本地sqlite中
                with SqliteDBManager('SalesShipment.db') as sqlitemanager:
                    # 插入前先清除缓存表数据
                    sqlitemanager.execute(Common.insert_salesshipment_sql, params=differences)
    else:
        log.info('本次查询无上传数据，简道云同步任务结束！！！')


if __name__ == '__main__':
    SalesShipmentGZ()
    # while True:
    #     main()
    #     time.sleep(1800)
