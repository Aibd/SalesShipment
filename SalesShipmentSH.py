from MSSqlDB import MSSqlDBManager
from SQLiteDB import SqliteDBManager
from jdy import JDYApi
from logger import Logger
from common import Common
import time
import random
import utils


# 简道云批量删除数据
def delete_jdy_data(company, jdy_api, kdata):
    query_data = Common.query_data
    ids = []
    for data in kdata:
        finterid = data[0]
        fentryid = data[1]
        query_data["filter"]["cond"][0]["value"] = finterid
        query_data["filter"]["cond"][1]["value"] = fentryid
        query_data["filter"]["cond"][2]["value"] = company
        id = jdy_api.query_dataid(query_data)
        if id:
            ids.append(id[0])
    if ids:
        jdy_api.batch_delete(entry_id=Common.entry_id, ids=ids)


# Sqlite批量删除数据
def delete_sqlite_data(company, dbname, tablename, kdata):
    with SqliteDBManager(dbname) as sqlitemanager:
        for data in kdata:
            id = data[0]
            entryid = data[1]
            company = company
            sqlitemanager.execute(
                f"DELETE FROM {tablename} WHERE id = {id} AND entryid = {entryid} AND company = '{company}'")


def SalesShipmentSH(company, dbname, tablename):
    jdy_api = JDYApi(Common.api_key, Common.app_id)
    log = Logger('main', 'SalesShipment.log')

    # 获取金蝶销售出库数据
    with MSSqlDBManager(company) as msmanager:
        kdata = msmanager.execute(Common.SalesShipmentSH_query_sql, fetch=True)

    # 将最新数据插入本地Sqlite临时表temp中
    with SqliteDBManager(dbname) as sqlitemanager:
        # 插入前先清除缓存表数据
        sqlitemanager.execute('DELETE FROM temp')
        sqlitemanager.execute(Common.insert_temp_sql, params=kdata)

    # 在sqlite中比对两侧数据
    # 比对删除数据，删除被同步端数据
    with SqliteDBManager(dbname) as sqlitemanager:
        query_sql = Common.deleted_query_sql.format(company=company)
        deleted_kdata = sqlitemanager.execute(query_sql, fetch=True)
    if deleted_kdata:
        # 删除简道云数据
        delete_jdy_data(company, jdy_api, deleted_kdata)
        # 删除成功 输出日志，同时删除sqlite映射数据
        delete_sqlite_data(company, dbname, tablename, deleted_kdata)
        log.info('deleted_kdata: ' + deleted_kdata)
    # 比对更新和增量数据，同步数据（同步时校验被同步端是否存在，存在则删除后同步最新数据）
    with SqliteDBManager(dbname) as sqlitemanager:
        diff_sql = Common.differences_sql.format(company=company)
        diff_data = sqlitemanager.execute(diff_sql, fetch=True)
        differences = [list(tup) for tup in diff_data]

    if differences:
        # 由于简道云限制 每次只能上传100条数据，同时每秒只能上传10次，所以大于100我们分批上传
        batch_size = 100
        if len(differences) > batch_size:
            # 处理批次数据
            for batch in [differences[i:i + batch_size] for i in range(0, len(differences), batch_size)]:
                # 先判断新增数据是否已存在，如果已存在先删除再添加
                delete_jdy_data(company, jdy_api, batch)
                delete_sqlite_data(company, dbname, tablename, batch)

                # 上传简道云并写入本地Sqlite映射表
                processed_data = utils.data_process(company, batch, Common.jdy_salesshipment_data)
                result = jdy_api.upload(processed_data)
                if result is not None:
                    log.info("简道云上传结果：" + str(batch))
            # 插入到本地sqlite中
            with SqliteDBManager(dbname) as sqlitemanager:
                sqlitemanager.execute(Common.insert_salesshipment_sql, params=differences)
        else:
            # 先判断新增数据是否已存在，如果已存在先删除再添加
            delete_jdy_data(company, jdy_api, differences)
            # 上传简道云并写入本地Sqlite映射表
            processed_data = utils.data_process(company, differences, Common.jdy_salesshipment_data)
            result = jdy_api.upload(processed_data)
            if result is not None:
                log.info("简道云上传结果：" + str(differences))
                # 插入到本地sqlite中
                with SqliteDBManager(dbname) as sqlitemanager:
                    # 插入前先清除缓存表数据
                    sqlitemanager.execute(Common.insert_salesshipment_sql, params=differences)
    else:
        log.info('本次查询无上传数据，简道云同步任务结束！！！')


if __name__ == '__main__':
    company = '希肤上海'
    dbname = 'SalesShipment.db'
    tablename = 'salesshipment'
    SalesShipmentSH(company, dbname, tablename)
