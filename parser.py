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
        The constructor for ComplexNumber class.

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
            zip_url_res=self.get_zip_url()
            if zip_url_res["status"]:
                # fetch and extract zip file
                zip_url=zip_url_res["data"]
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
                print(str('zips' + '/' + z.namelist()[0]))
                csv_path=str('zips' + '/' + z.namelist()[0])

                # Get redis connection
                redis_conn_res=get_redis_connection()
                if redis_conn_res["status"]:
                    redis_conn=redis_conn_res["data"]
                else:
                    return redis_conn_res

                # Open csv file and read it
                csv_list = csv.DictReader(open(csv_path, 'r'))
                redis_pipeline = redis_conn.pipeline(transaction=True) #start redis pipeline,with transaction
                redis_pipeline.flushdb()
                for row in csv_list:
                    stripped_key = row['SC_CODE'].rstrip()+":"+row['SC_NAME'].rstrip()
                    value = {'name': row['SC_NAME'].rstrip(), 'code': row['SC_CODE'], 'open': row['OPEN'],
                             'close': row['CLOSE'], 'high': row['HIGH'], 'low': row['LOW']}
                    redis_pipeline.hmset(stripped_key, dict(value))
                    percentage = round(((float(row['CLOSE']) - float(row['OPEN'])) / float(row['OPEN'])) * 100, 2)
                    print(percentage)
                    redis_pipeline.zadd("search_sorted",{stripped_key: percentage})
                redis_pipeline.execute()
            else:
                return zip_url_res
        except Exception as e:
            traceback.print_exc()
            res["data"] = "Something went wrong, Kindly try again."
            return res

a=EqBhavCopyParser()
a.load_zip_to_redis()
