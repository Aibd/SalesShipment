import uuid
from copy import deepcopy
from jdy import JDYApi


# 金蝶字段转换为简道云对应值的字段编号
def kdata_field_to_jdy(company, kdata):
    kingdee_data = deepcopy(kdata)
    # 简道云表单查询接口调用
    api_key = "1ENC5lt8m3pf97kiKnATic26eTIXQKR5"
    app_id = "65bc6159daf9cea1dbb5be86"
    jdy_api = JDYApi(api_key, app_id)
    users = jdy_api.get_usernumber()
    dept = {
        '华南销售': 618367622,
        '华东销售': 860190201
    }
    for k, v in enumerate(kingdee_data):
        # 业务员替换为简道云用户
        if kingdee_data[k][29] in users.keys():
            kingdee_data[k][29] = users[kingdee_data[k][29]]
        else:
            kingdee_data[k][29] = users['张木森']  # 处理键不存在的情况
        # 开发人员替换为简道云用户
        if kingdee_data[k][30] in users.keys():
            kingdee_data[k][30] = users[kingdee_data[k][30]]
        else:
            kingdee_data[k][30] = users['张木森']
        if company == '希肤上海':
            kingdee_data[k][32] = dept['华东销售']
        elif company == '希肤广州':
            kingdee_data[k][32] = dept['华南销售']

    return kingdee_data


# 金蝶数据转换为简道云接口payload数据包格式
def data_process(company, kingdee_data, jdy_data):
    kdata = kdata_field_to_jdy(company, kingdee_data)
    jdy_data["transaction_id"] = str(uuid.uuid4())
    data_dict = jdy_data['data_list'][0]
    fields = list(data_dict.keys())
    datalist = [deepcopy(data_dict) for _ in kdata]
    for temp, new_values in zip(datalist, kdata):
        for field, new_value in zip(fields, new_values):
            temp[field]["value"] = new_value

    jdy_data['data_list'] = datalist
    return jdy_data
