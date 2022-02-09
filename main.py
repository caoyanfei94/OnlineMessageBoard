import pymysql, time
from flask import Flask, render_template, request

app = Flask(__name__)

# 留言板列表
@ app.route('/')
def index():
    # 1。获取所有的留言板数据
    data = execSql('select * from messageboard;')
    # 2。把数据分配到模板中(html页面)
    return render_template('index.html', data = data)

# 定义视图，显示留言添加的页面
@ app.route('/add')
def add():
    # 显示留言添加的页面
    return render_template('add.html')

# 定义视图函数，接受表单数据，完成数据的入库
@ app.route('/insert', methods = ['POST'])
def insert():
    # 1。接受表单数据
    data = request.form.to_dict()
    # 处理数据
    res = None
    if data['nickname']:
        data['messageTime'] = time.strftime('%Y-%m-%d %H-%M-%S')
        # 2。把数据添加到数据库
        sql = f'insert into messageboard values(null, ' \
              f'"{data["nickname"]}", "{data["info"]}", ' \
              f'"{data["messageTime"]}");'
        res = execSql(sql)
    # 3。成功后页面跳转到留言页表页面
    if res:
        # 跳转到列表页
        return '<script>alert("留言发布成功"); location.href = "/"</script>'
    return '<script>alert("留言发布失败"); location.href = "/add"</script>'

# 定义视图函数，接收id，完成数据删除
@ app.route('/delete')
def delMessage():
    # 1。接受id
    id = request.args.get('id')
    # 2。执行删除的sql语句
    sql = f'delete from messageboard where id = {id};'
    res = execSql(sql)

    # 3。判断结果进行跳转
    if res:
        return '<script>alert("留言删除成功"); location.href = "/"</script>'
    return '<script>alert("留言删除失败"); location.href = "/"</script>'

# 定义视图函数，显示留言修改的页面
@ app.route('/modify')
def modifyMessage():
    id = request.args.get('id')
    data = (execSql(f'select * from messageboard where id = {id};'))[0]
    if data:
        return render_template('modify.html', data = data)
    return '<script>alert("留言获取失败"); location.href = "/"</script>'

# 定义视图函数，将要求修改的数据更新到数据库
@ app.route('/update', methods = ['POST'])
def updateMessage():
    data = request.form.to_dict()
    # 处理数据
    res = None
    if data['id'] and data['nickname']:
        data['messageTime'] = time.strftime('%Y-%m-%d %H-%M-%S')
        # 2。把数据添加到数据库
        sql = f'update messageboard set info = "{data["info"]}", ' \
              f'messageTime = "{data["messageTime"]}" ' \
              f'where id = {data["id"]};'
        print(sql)
        res = execSql(sql)
    # 3。成功后页面跳转到留言页表页面
    if res:
        # 跳转到列表页
        return '<script>alert("留言更新成功"); location.href = "/"</script>'
    return '<script>alert("留言更新失败"); location.href = "/"</script>'

# 封装mysql操作方法
def execSql(sql):
    db = pymysql.connect(host='127.0.0.1', user='root', password='',
                         database='dblearning', charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        cursor = db.cursor()

        row = cursor.execute(sql)
        print(row)
        db.commit()

        data = cursor.fetchall()
        # 返回结果，如果有数据则返回，没有数据则返回受影响的行数
        if data:
            return data
        return row
    except:
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug = True, host = '127.0.0.1', port = '80')