import traceback
from config import get_redis_connection
from parser import EqBhavCopyParser


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
                if total_count == 0:
                    """
                    If data is not loaded, call parser to load it.
                    """
                    res=self.get_latest_stocks()
                    if res["status"]:
                        total_count = redis_conn.zcount("search_sorted", "-inf", "+inf")
                    else:
                        return res
            start_index=page_no*self.pagination_size
            end_index=start_index+self.pagination_size-1

            keys=redis_conn.zrevrange("search_sorted", start_index, end_index, withscores=False)
            top_stacks=[]
            for key in keys:
                reg = redis_conn.hgetall(key)
                top_stacks.append(reg)
            print(top_stacks)
            date=redis_conn.get("latest_date")
            res["status"],res["data"],res["count"],res["date"]=1,top_stacks,total_count,date
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
            print(type(keys))
            for key in keys:
                reg = redis_conn.hgetall(key)
                stacks.append(reg)
            print(stacks)
            res["status"], res["data"] = 1, stacks
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
        return res

    def get_latest_stocks(self):
        """
        Calls parser to fetch new bhav copy zip and load it to redis
        :param
            name: name to search
        :return:
            success response : {"status":1,"data":"--dict of stocks--"}
            fail response : {"status":0,"data":"--error message--"}
        """
        res = {"status": 0, "data": ""}
        try:
            parser=EqBhavCopyParser()
            res=parser.load_zip_to_redis()
            print("==================")
            print(res)
            return res
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
        return res