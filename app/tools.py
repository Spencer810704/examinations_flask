import MySQLdb
import MySQLdb.cursors


class MySQLHelper(object):
    def __init__(self, host, db, user, password, port=3306):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, db=self.db, user=self.user, password=self.password,
                                    cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
        self.cursor.close()

    def get_one(self, sql, *args):
        result = ()
        self.connect()

        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchone()
            self.conn.commit()

        except Exception:
            self.conn.rollback()

        return result

    def get_all(self, sql):
        result = ()
        self.connect()

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.conn.commit()

        except Exception:
            self.conn.rollback()

        return result

    def execute(self, sql, args):

        count = 0
        self.connect()

        try:
            count = self.cursor.execute(sql, args)
            self.conn.commit()
            print("Success")
        except Exception:
            self.conn.rollback()
            print("Failed")

        return count


class RequestDataHelper(object):
    CONNECTION_INFO = {
        "host": "db",
        "port": 3306,
        "db": "exam",
        "user": "exam_user",
        "password": "exam_passwd",
    }

    def __init__(self, data, user_id):
        helper = MySQLHelper(**self.CONNECTION_INFO)

        # 取得原用戶的相關欄位資訊
        get_user_sql = """
            SELECT 
                `id`, `name`, `job_title`, `email`, `mobile`
            FROM 
                `user` 
            INNER JOIN 
                `contact` 
            ON 
                `user`.id = `contact`.user_id 
            WHERE 
                `user`.id = %s AND `user`.is_delete=0 AND `contact`.is_delete=0;
        """
        user_instance = helper.get_one(get_user_sql, user_id)

        # 如果請求沒有包含欄位，則使用原資料表內的欄位值作為預設值。
        self.name = data.get('name', user_instance['name'])
        self.job_title = data.get('job_title', user_instance['job_title'])

        # 第二層嵌套的communicate_information如果不存在就直接指定資料庫內的值
        communicate_information = data.pop('communicate_information', None)
        if communicate_information:
            self.email = communicate_information.get('email', user_instance['email'])
            self.mobile = communicate_information.get('mobile', user_instance['mobile'])
        else:
            self.email = user_instance['email']
            self.mobile = user_instance['mobile']
