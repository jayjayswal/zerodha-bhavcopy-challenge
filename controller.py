import traceback
from config import get_redis_connection


class EqBhavCopyController():
    """
    This is a class for providing webservices data.

    Attributes:

    """

    def __init__(self):
        """
        The constructor for EqBhavCopyController class.

        Parameters:
        """
        self.pagination_size=10
        pass

    def get_top_stocks(self,page_no):
        """
        get top stocks from the redis and return in dict format
        :param
            page_no: page no for pagination
        :return:
            success response : {"status":1,"data":"--dict of stocks--","count":"--total count of stocks--"}
            fail response : {"status":0,"data":"--error message--"}
        """
        res = {"status": 0, "data": ""}
        try:
            redis_conn_res = get_redis_connection()
            if not redis_conn_res["status"]:
                return redis_conn_res
            redis_conn = redis_conn_res["data"]

            total_count=0
            if page_no==0:
                total_count=redis_conn.zcount("search_sorted","-inf","+inf")
            start_index=page_no*10
            end_index=start_index+9

            keys=redis_conn.zrevrange("search_sorted", start_index, end_index, withscores=False)
            top_stacks=[]
            for key in keys:
                reg = redis_conn.hgetall(key)
                top_stacks.append(reg)
            print(top_stacks)
            res["status"],res["data"],res["count"]=1,top_stacks,total_count
            return res
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
            return res

    def get_stock_by_name(self,name):
        """
        get stocks from the redis with pattern matching and return in dict format
        :param
            name: name to search
        :return:
            success response : {"status":1,"data":"--dict of stocks--"}
            fail response : {"status":0,"data":"--error message--"}
        """
        res = {"status": 0, "data": ""}
        try:
            redis_conn_res = get_redis_connection()
            if not redis_conn_res["status"]:
                return redis_conn_res
            redis_conn = redis_conn_res["data"]

            keys = redis_conn.scan_iter(match='STOCK:*'+str(name).upper()+'*')
            stacks = []
            for key in keys:
                reg = redis_conn.hgetall(key)
                stacks.append(reg)
            print(stacks)
            res["status"], res["data"] = 1, stacks
            return res
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
            return res

# a=EqBhavCopyController()
# a.get_stock_by_name("LAB")