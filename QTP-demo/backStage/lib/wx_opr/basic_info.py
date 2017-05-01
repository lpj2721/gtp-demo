# -*- coding: utf-8 -*-
from db_conn.cont_mongo import MongoConn
from datetime import datetime
import time
import traceback
import copy

class basic_info():
    def __init__(self):
        self.db = MongoConn().db

    def getBusinessInfo(self, store_id):
        # 获取商家信息、所有菜系及相应菜品
        # 返回每种菜系 及每种菜系下所有菜品 组成前端需要的json
        business_info = self.db['business_info'].find_one({'_id': store_id})
        return business_info

    def add_user(self, **kwargs):
        try:
            self.db['open_users'].insert_one(kwargs)
            kwargs['order_list'] = []
            self.db['consumer_info'].insert_one(kwargs)
            return True
        except Exception:
            return traceback.format_exc()

    def find_user(self, user_id):
        result = self.db['open_users'].find_one(user_id)
        return result

    def get_dishInfo(self, store_id):
        dishInfo = self.db['business_info'].find_one(store_id, {'_id': 0, 'dishes': 1, 'dish': 1})
        dish_type = sorted(dishInfo['dishes'], key=lambda type_sn: type_sn['type_sn'])
        #菜品
        dish_cont = dishInfo['dish']
        result = []
        food = {}
        str_dix = "cate"
        if dish_type:
            for item in dish_type:
                #分类
                food['cate_id'] = str_dix + item['id']
                food['cate_name'] = item['type_name']
                food['cate_mark'] = item['type_remark']
                dish_dix = "dish" + item['id'] + "-"
                sn = 0
                dishs = []
                if len(dish_cont) == 0:
                    food['dishs'] = dishs
                else:
                    #菜品筛选
                    for each in dish_cont:
                        dish = {}
                        if item['type_name'] == each['type_name']:
                            #下架菜品不返回给前端
                            if each['dish_num'] ==1:
                                break
                            dish['dish_id'] = dish_dix + str(sn)
                            dish['dish_name'] = each['dish_name']
                            dish['dish_price'] = each['price']
                            dish['discount'] = each['discount']
                            dish['dish_count'] = 0
                            dish['dish_pic'] = each['image_url']
                            dish['dish_sale'] = each['sales']
                            copy_d = copy.deepcopy(dish)
                            dishs.append(copy_d)
                            sn = sn + 1
                        else:
                            pass
                    food['dishs'] = copy.deepcopy(dishs)
                copy_f = copy.deepcopy(food)
                result.append(copy_f)
            for j in range(len(result) - 1, -1, -1):
                if len(result[j]['dishs']) == 0:
                    result.pop(j)
            return result
        else:
            return result

    def get_storeInfo(self, store_id):
        storeInfo = self.db['business_info'].find_one(store_id, {'_id': 0, 'b_name':1,'b_notice': 1})
        return storeInfo

    def sub_order(self, **kwargs):
        serial_num = kwargs['_id']
        store_id = kwargs['business_id']
        user_id = kwargs['consumer_id']
        dish_name = kwargs['dishs'][0]['dish_name']
        dish_count = kwargs['count']
        create_time = kwargs['create_time']
        status = kwargs['status']
        money = kwargs['money']
        pay_for = kwargs['pay_for']
        desk_id = kwargs['desk_id']
        timestamp = time.time() * 1000
        create_times = create_time[:10]
        local_str_time = create_times.replace("-", "")
        order_list = self.db['consumer_info'].find_one(user_id, {'_id': 0, 'order_list': 1})
        order_list['order_list'].insert(0, serial_num)
        self.db['consumer_info'].update_one({"_id": user_id}, {"$set": {'order_list': order_list['order_list']}})
        order_info = {
            'id': timestamp,
            'serial_num': serial_num,
            'status': status,
            'dish_name': dish_name,
            'dish_count': dish_count,
            'desk_id': desk_id,
            'money': money,
            'create_time': create_time,
            'pay_for': pay_for
        }
        if self.db[store_id].find_one(local_str_time):
            # 商户订单表更新
            self.db[store_id].update_one({"_id": local_str_time}, {"$push": {'order_list': order_info}})
            self.db[store_id].update_one({"_id": local_str_time}, {"$inc": {'order_total': 1}})
        else:
            order_list = []
            order_list.append(order_info)
            day_orders = {
                '_id': local_str_time,
                'money_total': 0,
                'order_total': 1,
                'order_list': order_list
            }
            self.db[store_id].insert_one(day_orders)
        result = self.db['order_info'].insert_one(kwargs)
        if result.inserted_id:
            return True
        else:
            return False

    def modify_order(self, pay_serial_num=None,store_id=None, serial_num=None, status=None):
        order_info  = self.db['order_info'].find_one(serial_num,{"_id":0,"create_time":1})
        create_time = order_info['create_time'][:10]
        local_str_time = create_time.replace("-", "")
        list = self.db[store_id].find_one(local_str_time, {"_id": 0})
        if list is None:
            return False
        order_list = list['order_list']
        for order in order_list:
            if order['serial_num'] == serial_num:
                order['status'] = status
                # if status == 3:
                #     print order['money']
                #     self.db[store_id].update_one({"_id": local_str_time}, {"$inc": {'money_total': order['money']}})
                #     order['status'] = status
                #     break
                # else:
                #     order['status'] = status
                #     break
        self.db[store_id].update_one({'_id': local_str_time}, {"$set": {"order_list": order_list}})
        self.db['order_info'].update_one({'_id': serial_num},
                                         {"$set": {"status": status,"pay_serial_num":pay_serial_num}})
        return True

    def list_order(self, user_id, page, index):
        pages = (page - 1) * index
        list = self.db['order_info'].find({'consumer_id': user_id}, {"consumer_id":0,"business_id":0,"pay_serial_num":0}).sort("create_time",
                                                                                  direction=-1).skip(pages).limit(index)
        result = []
        for team in list:
            result.append(team)
        return result
        pass

    def find_order(self, id):
        result = self.db['order_info'].find_one(id,{"pay_serial_num":0})
        return result

    def dish_sales(self,store_id,dish):
        dish_info = self.db['business_info'].find_one(store_id, {'_id': 0, 'dish': 1})
        dish_list = dish_info['dish']
        for each in dish_list:
            for item in dish:
                if item['dish_name'] == each['dish_name']:
                    each['sales'] = each['sales'] + item['dish_count']
        self.db['business_info'].update_one({'_id':store_id},{'$set':{'dish':dish_list}})

if __name__ == "__main__":

    pass
