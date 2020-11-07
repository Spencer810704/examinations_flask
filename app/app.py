from flask import Flask, request
from flask import jsonify
from tools import MySQLHelper, RequestDataHelper

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CONNECTION_INFO = {
    "host": "db",
    "port": 3306,
    "db": "exam",
    "user": "exam_user",
    "password": "exam_passwd",
}


# 查詢單一用戶
@app.route('/api/v1/users/<int:user_id>/', methods=['GET'])
def user(user_id):
    helper = MySQLHelper(**CONNECTION_INFO)
    sql = """
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
    user = helper.get_one(sql, user_id)

    if user:
        data = {
            "id": user['id'],
            "name": user['name'],
            "job_title": user['job_title'],
            "communicate_information": {
                "email": user['email'],
                "mobile": user['mobile']
            }
        }

    else:
        data = {
            "status": "user not found"
        }

    return jsonify(data), 200


# 查詢所有用戶
@app.route('/api/v1/users/', methods=['GET'])
def all_user():
    helper = MySQLHelper(**CONNECTION_INFO)
    get_all_user_sql = """ 
            SELECT 
                `id`,`name`,`job_title`,`email`,`mobile` 
            FROM 
                `user` 
            INNER JOIN 
                `contact` 
            ON 
                `user`.id = `contact`.user_id 
            WHERE 
                `user`.is_delete=0 AND `contact`.is_delete=0
    """
    user_list = helper.get_all(get_all_user_sql)
    data = []
    if user_list:
        for user in user_list:
            data.append(
                {
                    "id": user['id'],
                    "name": user['name'],
                    "job_title": user['job_title'],
                    "communicate_information": {
                        "email": user['email'],
                        "mobile": user['mobile']
                    }
                }
            )
    else:
        data = {
            "status": 'no user record'
        }

    return jsonify(data), 200


# 增加用戶
@app.route('/api/v1/users/', methods=['POST'])
def create_user():
    helper = MySQLHelper(**CONNECTION_INFO)

    # 獲取POST請求數據
    data = request.json
    # 將第二層的字典取出
    communicate_information = data.pop('communicate_information')

    # 取值
    name = data.get('name', '')
    job_title = data.get('job_title', '')
    email = communicate_information.get('email', '')
    mobile = communicate_information.get('mobile', '')

    # 取得表中最後一筆的ID值再加上1作為新數據的ID欄位
    get_max_id_sql = "SELECT max(id) AS id FROM user;"
    next_id = helper.get_one(sql=get_max_id_sql)['id']
    if next_id:
        next_id = next_id + 1
    else:
        next_id = 1

    insert_user_sql = "INSERT INTO user(id,name,job_title) VALUES(%s,%s,%s);"
    user_insert_count = helper.execute(sql=insert_user_sql, args=(next_id, name, job_title))
    if user_insert_count:
        insert_contact_sql = "INSERT INTO contact(user_id,email,mobile) VALUES(%s,%s,%s);"
        count_insert_count = helper.execute(sql=insert_contact_sql, args=(next_id, email, mobile))
        if count_insert_count:
            data = {
                "id": next_id,
                "name": name,
                "job_title": job_title,
                "communicate_information": communicate_information
            }

            return jsonify(data), 200


# 修改用戶資訊
@app.route('/api/v1/users/<user_id>/', methods=['PUT'])
def edit_user(user_id):
    # 獲取POST請求數據
    body_instance = RequestDataHelper(data=request.json, user_id=user_id)

    helper = MySQLHelper(**CONNECTION_INFO)

    # 更新沒有被邏輯刪除的用戶資訊
    update_user_sql = """
        UPDATE 
            `user` 
        INNER JOIN 
            `contact` 
        ON 
            `user`.id = `contact`.user_id 
        SET 
            `user`.name = %(name)s,
            `user`.job_title = %(job_title)s,
            `contact`.email = %(email)s,
            `contact`.mobile = %(mobile)s
        WHERE
            `user`.id = %(user_id)s AND `user`.is_delete=0;
    """

    args = {
        'name': body_instance.name,
        'job_title': body_instance.job_title,
        'email': body_instance.email,
        'mobile': body_instance.mobile,
        'user_id': user_id
    }

    result = helper.execute(sql=update_user_sql, args=args)

    if result:
        data = {
            'status': 'edit success'
        }
    else:
        data = {
            'status': 'edit failed'
        }

    return jsonify(data), 200


# 刪除用戶(邏輯刪除)
@app.route('/api/v1/users/<user_id>/', methods=['DELETE'])
def delete_user(user_id):
    helper = MySQLHelper(**CONNECTION_INFO)

    delete_user_sql = """
        UPDATE 
            `user` 
        INNER JOIN 
            `contact` 
        ON 
            `user`.id = `contact`.user_id 
        SET 
            `user`.is_delete = 1,
            `contact`.is_delete = 1
        WHERE
            `user`.id = %s;
    """

    result = helper.execute(sql=delete_user_sql, args=(user_id,))

    if result:
        data = {
            'status': 'delete success'
        }
    else:
        data = {
            'status': 'delete failed'
        }

    return jsonify(data), 200


if __name__ == '__main__':
    app.run()
