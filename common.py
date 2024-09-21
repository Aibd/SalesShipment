class Common:
    # 简道云参数
    api_key = "1ENC5lt8m3pf97kiKnATic26eTIXQKR5"
    app_id = "65bc6159daf9cea1dbb5be86"
    entry_id = "66b472d858625f3414c88c04"

    # 简道云查询参数
    query_data = {
        "app_id": app_id,
        "entry_id": entry_id,
        "limit": 10000,
        "fields": ["_id", "fid", "fentryid"],
        "rel": "and",
        "filter": {
            "cond": [
                {
                    "field": "fid",
                    "method": "eq",
                    "value": 10
                },
                {
                    "field": "fentryid",
                    "method": "eq",
                    "value": 10
                },
                {
                    "field": "company",
                    "method": "eq",
                    "value": "希肤上海"
                }]
        }
    }

    # 简道云销售出库表单接口数据包格式
    jdy_salesshipment_data = {
        "op": "data_create",
        "app_id": "65bc6159daf9cea1dbb5be86",
        "entry_id": "66b472d858625f3414c88c04",
        "transaction_id": "87cd7d71-c6df-4281-9927-469094395677",
        "data_list": [{
            "fid": {
                "value": 10
            },
            "fentryid": {
                "value": 10
            },
            "fstatus": {
                "value": "Peter"
            },
            "fdate": {
                "value": "2018-01-01T10:10:10.000Z"
            },
            "fbillno": {
                "value": "Peter"
            },
            "custname": {
                "value": "Peter"
            },
            "fauxmastercode": {
                "value": "Peter"
            },
            "fauxmastername": {
                "value": "Peter"
            },
            "itemnumber": {
                "value": "Peter"
            },
            "itemname": {
                "value": "Peter"
            },
            "model": {
                "value": "Peter"
            },
            "selfb0186": {
                "value": "Peter"
            },
            "fbatchno": {
                "value": "Peter"
            },
            "unit": {
                "value": "Peter"
            },
            "qty": {
                "value": 10
            },
            "fprice": {
                "value": 10
            },
            "fconsignprice": {
                "value": 10
            },
            "famount": {
                "value": 10
            },
            "amountexcludingtax": {
                "value": 10
            },
            "fconsignamount": {
                "value": 10
            },
            "gprofit": {
                "value": 10
            },
            "grossprofitmargin": {
                "value": 10
            },
            "invoiceqty": {
                "value": 10
            },
            "invoiceamount": {
                "value": 10
            },
            "ardate": {
                "value": "2018-01-01T10:10:10.000Z"
            },
            "billnumber": {
                "value": "Peter"
            },
            "cp": {
                "value": 10
            },
            "bp": {
                "value": 10
            },
            "tp": {
                "value": 10
            },
            "salesuser": {
                "value": "jian"
            },
            "devuser": {
                "value": "Peter"
            },
            "ordnumber": {
                "value": "Peter"
            },
            "dept": {
                "value": 12
            },
            "company": {
                "value": "Peter"
            }
        }]
    }


    # 希肤上海查询金蝶销售出库单数据
    SalesShipmentSH_query_sql = '''
        SELECT
            t2.FInterID                                   单据ID,
            t2.FEntryID                                   单据行ID,
            CASE
                 WHEN t1.FStatus = 0 THEN '未审核'
                 WHEN t1.FStatus = 1 THEN '已审核'
                 WHEN t1.FStatus = 2 THEN '部分行关闭'
                 WHEN t1.FStatus = 3 THEN '已关闭'
                 ELSE '未知状态'
                 END                                       单据状态,
             CONVERT(VARCHAR, t1.FDate, 126) + 'Z'         出库日期,
             t1.FBillNo                                    出库单号,
             t3.FName                                      客户,
             t5.F_106                                      商品牌号,
             t5.F_107                                      商品名,
             t5.FNumber                                    产品编码,
             t5.FName                                      产品名称,
             t5.FModel                                     规格型号,
             t8.FName                                      客户产品名称,
             t2.FBatchNo                                   批号,
             t6.FName                                      单位,
             CAST(t2.FQty AS FLOAT)                        出库数量,
             CAST(t2.FPrice AS FLOAT)                      成本单价,
             CAST(t2.FConsignPrice AS FLOAT)               销售单价,
             CAST(t2.FAmount AS FLOAT)                     成本金额,
             CAST(t2.FConsignAmount/1.13 AS FLOAT)             不含税金额,
             CAST(t2.FConsignAmount AS FLOAT)              含税金额,
             CAST(t2.FConsignAmount/1.13 - t2.FAmount AS FLOAT) 毛利润,
             CASE
                 WHEN t2.FConsignAmount/1.13 = 0 THEN 0
                 ELSE CAST(ROUND((t2.FConsignAmount/1.13 - t2.FAmount)/(t2.FConsignAmount/1.13),2) AS FLOAT)
             END 毛利润率,
             CAST(t2.FQtyInvoice AS FLOAT)                 开票数量,
             CAST(t2.FQtyInvoice * t2.FPrice AS FLOAT)     开票金额,
             CONVERT(VARCHAR, t1.FSettleDate, 126) + 'Z'   应收日期,
             CASE
                 WHEN ISNUMERIC(t2.FEntrySelfB0170) = 0 THEN  NULL
                 ELSE t2.FEntrySelfB0170
             END                                           第几单,
             CAST(t2.FEntrySelfB0174 AS FLOAT)             CP,
             CAST(t2.FEntrySelfB0175 AS FLOAT)             BP,
             CAST(t2.FEntrySelfB0176 AS FLOAT)             TP,
             t4.FName                                      业务员,
             convert(varchar(100), t9.FName)               开发员,
             t7.FOrderBillNo                               订单编号,
             '华东销售'                                      部门,
             '希肤上海'                                      公司
        FROM ICStockBill t1
               RIGHT JOIN ICStockBillEntry t2 ON t1.FInterID = t2.FInterID
               LEFT JOIN T_Organization t3 ON t1.FSupplyID = t3.FItemID
               LEFT JOIN T_Emp t4 ON t1.FEmpID = t4.FItemID
               LEFT JOIN T_ICItem t5 ON t2.FItemID = t5.FItemID
               LEFT JOIN T_MeasureUnit t6 ON t2.FUnitID = t6.FMeasureUnitID
               LEFT JOIN (SELECT a.FInterID,
                                 b.FEntryID,
                                 b.FOrderBillNo
                          FROM ICStockBill a
                                   RIGHT JOIN ICStockBillEntry b ON a.FInterID = b.FInterID
                          WHERE a.FTranType = 21
                            AND a.FStatus <> 0
                            AND b.FEntryID = 1) t7 ON t7.FInterID = t1.FInterID
               LEFT JOIN t_Item_3016 t8 ON t2.FEntrySelfB0171 = t8.FItemID
               LEFT JOIN T_Emp t9 ON t1.FHeadSelfB0177 = t9.FItemID
        WHERE t1.FTranType = 21
        AND t1.FStatus <> 0
    '''

    # 希肤广州查询金蝶销售出库单数据
    SalesShipmentGZ_query_sql = '''
        SELECT
               t2.FInterID                                   单据ID,
               t2.FEntryID                                   单据行ID,
                CASE
                     WHEN t1.FStatus = 0 THEN '未审核'
                     WHEN t1.FStatus = 1 THEN '已审核'
                     WHEN t1.FStatus = 2 THEN '部分行关闭'
                     WHEN t1.FStatus = 3 THEN '已关闭'
                     ELSE '未知状态'
                     END                                       单据状态,
                 CONVERT(VARCHAR, t1.FDate, 126) + 'Z'         出库日期,
                 t1.FBillNo                                    出库单号,
                 t3.FName                                      客户,
                 t5.FAuxMasterCode                             商品牌号,
                 t5.FAuxMasterName                             商品名,
                 t5.FNumber                                    产品编码,
                 t5.FName                                      产品名称,
                 t5.FModel                                     规格型号,
                 t2.FEntrySelfB0186                            客户产品名称,
                 t2.FBatchNo                                   批号,
                 t6.FName                                      单位,
                 CAST(t2.FQty AS FLOAT)                        出库数量,
                 CAST(t2.FPrice AS FLOAT)                      成本单价,
                 CAST(t2.FConsignPrice AS FLOAT)               销售单价,
                 CAST(t2.FAmount AS FLOAT)                     成本金额,
                 CAST(t2.FConsignAmount/1.13 AS FLOAT)             不含税金额,
                 CAST(t2.FConsignAmount AS FLOAT)              含税金额,
                 CAST(t2.FConsignAmount/1.13 - t2.FAmount AS FLOAT) 毛利润,
                 CASE
                     WHEN t2.FConsignAmount/1.13 = 0 THEN 0
                     ELSE CAST(ROUND((t2.FConsignAmount/1.13 - t2.FAmount)/(t2.FConsignAmount/1.13),2) AS FLOAT)
                 END 毛利润率,
                 CAST(t2.FQtyInvoice AS FLOAT)                 开票数量,
                 CAST(t2.FQtyInvoice * t2.FPrice AS FLOAT)     开票金额,
                 CONVERT(VARCHAR, t1.FSettleDate, 126) + 'Z'   应收日期,
                 t2.FEntrySelfB0163                            第几单,
                 CAST(t2.FEntrySelfB0189 AS FLOAT)             CP,
                 CAST(t2.FEntrySelfB0190 AS FLOAT)             BP,
                 CAST(t2.FEntrySelfB0191 AS FLOAT)             TP,
                 t4.FName                                      业务员,
                 convert(varchar(100), t1.FHeadSelfB0153)      开发员,
                 t7.FOrderBillNo                               订单编号,
                 '华南销售'                                    部门,
                 '希肤广州'                                    公司
          FROM ICStockBill t1
                   RIGHT JOIN ICStockBillEntry t2 ON t1.FInterID = t2.FInterID
                   LEFT JOIN T_Organization t3 ON t1.FSupplyID = t3.FItemID
                   LEFT JOIN T_Emp t4 ON t1.FEmpID = t4.FItemID
                   LEFT JOIN T_ICItem t5 ON t2.FItemID = t5.FItemID
                   LEFT JOIN T_MeasureUnit t6 ON t2.FUnitID = t6.FMeasureUnitID
                   LEFT JOIN (SELECT a.FInterID,
                                     b.FEntryID,
                                     b.FOrderBillNo
                              FROM ICStockBill a
                                       RIGHT JOIN ICStockBillEntry b ON a.FInterID = b.FInterID
                              WHERE a.FTranType = 21
                                AND a.FStatus <> 0
                                AND b.FEntryID = 1) t7 ON t7.FInterID = t1.FInterID
          WHERE t1.FTranType = 21
            AND t1.FStatus <> 0
    '''

    # 插入本地Sqlite临时表temp
    insert_temp_sql = '''
        INSERT INTO temp (
        ID, EntryID, Status, OutboundDate, OutboundNumber, Customer, ProductCode, ProductName, ProdCode, ProdName, Spec, CustProdName, BatchNumber, Unit, OutboundQty, CostUnitPrice, SalesUnitPrice, CostAmount, AmountExTax, AmountIncTax, GrossProfit, GrossProfitMargin, InvoiceQty, InvoiceAmount, ReceivableDate, OrderCount, CP, BP, TP, Salesperson, Developer, OrderNumber, Department, Company
    ) VALUES (
       ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
    ) 
    '''
    # 插入本地Sqlite映射表salesshipment
    insert_salesshipment_sql = '''
         INSERT INTO salesshipment (
         ID, EntryID, Status, OutboundDate, OutboundNumber, Customer, ProductCode, ProductName, ProdCode, ProdName, Spec, CustProdName, BatchNumber, Unit, OutboundQty, CostUnitPrice, SalesUnitPrice, CostAmount, AmountExTax, AmountIncTax, GrossProfit, GrossProfitMargin, InvoiceQty, InvoiceAmount, ReceivableDate, OrderCount, CP, BP, TP, Salesperson, Developer, OrderNumber, Department, Company
     ) VALUES (
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
     ) 
     '''

    # 简道云销售出库增量更新比对sql
    differences_sql = '''
    SELECT
        t1.ID, t1.EntryID, t1.Status, t1.OutboundDate, t1.OutboundNumber, t1.Customer, t1.ProductCode, t1.ProductName, t1.ProdCode, t1.ProdName, t1.Spec, t1.CustProdName, t1.BatchNumber, t1.Unit, t1.OutboundQty, t1.CostUnitPrice, t1.SalesUnitPrice, t1.CostAmount, t1.AmountExTax, t1.AmountIncTax, t1.GrossProfit, t1.GrossProfitMargin, t1.InvoiceQty, t1.InvoiceAmount, t1.ReceivableDate, t1.OrderCount, t1.CP, t1.BP, t1.TP, t1.Salesperson, t1.Developer, t1.OrderNumber, t1.Department, t1.Company
    FROM temp t1
        LEFT JOIN salesshipment t2 ON t2.ID = t1.ID
            AND t2.EntryID = t1.EntryID
            AND t2.Status = t1.Status
            AND t2.OutboundQty = t1.OutboundQty
            AND t2.GrossProfit = t1.GrossProfit
            AND t2.InvoiceAmount = t1.InvoiceAmount
            AND t2.Company = t1.Company
    WHERE t1.company = '{company}' AND t2.ID is null 
    '''
    # 简道云销售出库已删除数据比对sql
    deleted_query_sql = '''
    SELECT
        t1.ID, t1.EntryID, t1.Status, t1.OutboundDate, t1.OutboundNumber, t1.Customer, t1.ProductCode, t1.ProductName, t1.ProdCode, t1.ProdName, t1.Spec, t1.CustProdName, t1.BatchNumber, t1.Unit, t1.OutboundQty, t1.CostUnitPrice, t1.SalesUnitPrice, t1.CostAmount, t1.AmountExTax, t1.AmountIncTax, t1.GrossProfit, t1.GrossProfitMargin, t1.InvoiceQty, t1.InvoiceAmount, t1.ReceivableDate, t1.OrderCount, t1.CP, t1.BP, t1.TP, t1.Salesperson, t1.Developer, t1.OrderNumber, t1.Department, t1.Company
    FROM salesshipment t1
        LEFT JOIN temp t2 ON t2.ID = t1.ID AND t2.EntryID = t1.EntryID AND t2.Company = t1.Company
    WHERE t1.company = '{company}' AND t2.ID is null 
    '''