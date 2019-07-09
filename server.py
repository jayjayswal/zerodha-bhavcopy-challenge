import traceback
import cherrypy
from controller import EqBhavCopyController
import json

class SockSever(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def get_top_stocks(self,page_no=None):
        """
        top stocks by name webservice endpoint
        return:
            json:
                success response : {"status":1,"data":"--dict of stocks--","count":"--total count of stocks--"}
                fail response : {"status":0,"data":"--error message--"}
        """
        res = {"status": 0, "data": ""}
        try:
            page_no=0 if page_no is None else int(page_no)
            con=EqBhavCopyController()
            res=con.get_top_stocks(page_no)
            print("============================")
            print(res)
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
        return json.dumps(res)

    @cherrypy.expose
    def get_stock_by_name(self,name_to_search=None):
        """
        Search stocks by name webservice endpoint
        :return:
            json:
                success response : {"status":1,"data":"--dict of stocks--"}
                fail response : {"status":0,"data":"--error message--"}
        """

        res = {"status": 0, "data": ""}
        try:
            if name_to_search is None or name_to_search.strip() == "":
                res["data"] = "Kindly provide valid name"
            else:
                con = EqBhavCopyController()
                res = con.get_stock_by_name(name_to_search.strip())
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
        return json.dumps(res)




if __name__ == '__main__':
    cherrypy.quickstart(SockSever())