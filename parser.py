#https://www.bseindia.com/download/BhavCopy/Equity/EQ080719_CSV.ZIP
import redis
from config import get_redis_connection, BHAV_COPY_URL
import traceback
import zipfile
import requests
import io
import csv

class EqBhavCopyParser():
    """
    This is a class for parsing and loading data into redis.

    Attributes:

    """

    def __init__(self):
        """
        The constructor for EqBhavCopyParser class.

        Parameters:
        """
        pass

    def get_zip_url(self):
        """
        The function to parse and fetch zip url from html.
        return:
            dict:
                success response : {"status":1,"data":"--zip_url--"}
                fail response : {"status":0,"data":"--error message--"}
        """
        try:
            """
            https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx
            Parsing this URL with beautiful soap library.
            """
            res={"status":1,"data":"https://www.bseindia.com/download/BhavCopy/Equity/EQ080719_CSV.ZIP"}
            return res


        except Exception as e:
            traceback.print_exc()
            res = {"status": 0, "data": "Something went wrong, Kindly try again."}
            return res

    def extract_csv_file(self,zip_url):
        """
        The function to extexct zip and store CSV file
        return:
            dict:
                success response : {"status":1,"data":"--csv_path--","name":"--csv_file_name--}
                fail response : {"status":0,"data":"--error message--"}
        """
        res = {"status": 0, "data": ""}
        try:
            try:
                zip_file = requests.get(zip_url)
            except requests.exceptions.HTTPError as errh:
                res["data"] = "HTTP error, Kindly try again."
                return res
            except requests.exceptions.ConnectionError as errc:
                res["data"] = "Connection error, Kindly check internet connection."
                return res
            except requests.exceptions.Timeout as errt:
                res["data"] = "Request timeout, Kindly check internet connection."
                return res
            except Exception as e:
                res["data"] = "Something went wrong, Kindly try again."
                return res

            z = zipfile.ZipFile(io.BytesIO(zip_file.content))
            z.extractall('zips')
            csv_file_name = z.namelist()[0]
            print(str('zips' + '/' + csv_file_name))
            csv_path = str('zips' + '/' + csv_file_name)
            res["status"]=1;
            res["data"] = csv_path;
            res["name"] = csv_file_name;
            return res
        except Exception as e:
            traceback.print_exc()
            res = {"status": 0, "data": "Something went wrong, Kindly try again."}
            return res

    def load_zip_to_redis(self):
        """
        The function to parse zip and load data to redis.
        return:
            dict:
                success response : {"status":1,"data":"--success message--"}
                fail response : {"status":0,"data":"--error message--"}
        """
        res = {"status": 0, "data": ""}
        try:
            #Fetch Zip URL
            zip_url_res=self.get_zip_url()
            if not zip_url_res["status"]:
                return zip_url_res

            # fetch and extract zip file
            csv_file_res=self.extract_csv_file(zip_url_res['data'])
            if not csv_file_res["status"]:
                return csv_file_res
            csv_path=csv_file_res["data"]
            csv_file_name=csv_file_res["name"]


            # Get redis connection
            redis_conn_res=get_redis_connection()
            if not redis_conn_res["status"]:
                return redis_conn_res
            redis_conn = redis_conn_res["data"]

            # Open csv file and read it
            csv_list = csv.DictReader(open(csv_path, 'r'))
            # start redis pipeline,with transaction
            redis_pipeline = redis_conn.pipeline(transaction=True)
            redis_pipeline.flushdb()
            for row in csv_list:
                #
                stripped_key = "STOCK:"+row['SC_CODE'].rstrip()+":"+row['SC_NAME'].rstrip()
                value = {'name': row['SC_NAME'].rstrip(), 'code': float(row['SC_CODE']), 'open': float(row['OPEN']),
                         'close': float(row['CLOSE']), 'high': float(row['HIGH']), 'low': float(row['LOW'])}
                redis_pipeline.hmset(stripped_key, dict(value))

                #Assiming logic of top 10 stock entries must be "Highest positive percentage movement first"
                #Using sorted set and putting percentage as score
                #
                percentage = round(((value['close'] - value['open']) / value['open']) * 100, 2)
                redis_pipeline.zadd("search_sorted",{stripped_key: percentage})

            #Storing date for withc bhavcopy has been loaded to redis
            print("latest_date", csv_file_name[2:4] + "-" + csv_file_name[4:6] + "-20" + csv_file_name[6:8])
            redis_pipeline.set("latest_date", csv_file_name[2:4] + "-" + csv_file_name[4:6] + "-20" + csv_file_name[6:8])

            #execute the pipeline
            redis_pipeline.execute()

            #todo
            #disconnect redis

            res["status"] = 1
            res["data"] = "Done."
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
            return res

a=EqBhavCopyParser()
a.load_zip_to_redis()
