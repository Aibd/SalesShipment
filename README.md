# SalesShipment
金蝶销售出库同步简道云

## 基础模块
- 简道云 jdy.py
- 金蝶数据库 MSSqlDB.py
- 本地数据库 SQLiteDB.py
- 数据转换  utils.py
- 参数和SQL common.py

## 入库文件
- SalesShipmentMain.py

## 编译打包
'''
nuitka --onefile --windows-disable-console SalesShipmentMain.py --output-file=SalesShipment.exe --output-dir=.dist
'''