# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask,request,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import base64
import random
app = Flask(__name__)
# CORS(app)
# cors = CORS(app,resources={r"/*":{"origins":"http://localhost:63342"}})
app.config['SECRET_KEY'] = 'helloworld'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:seansean@localhost:3306/car'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# locate = '/home/sean/PycharmProjects/car_connect/imge/'
locate = '/root/car/car_connect/imge/'
locate1 = '/root/car/car_connect/'
class Parks(db.Model):
    __tablename__ = 'parks'
    id = db.Column(db.Integer,primary_key=True)
    plate = db.Column(db.String(30))
    img = db.Column(db.String(200))
    address = db.Column(db.String(100))
    level = db.Column(db.Integer)
    time = db.Column(db.Integer)
    uid = db.Column(db.Integer,db.ForeignKey('id'))
    status = db.Column(db.Boolean) #是否被处理
    extra = db.Column(db.String(100))

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    wx_name = db.Column(db.String(100))
    openId = db.Column(db.String(100))
    session_key = db.Column(db.String(200))
    status = db.Column(db.Boolean)  #是否通过管理员审核
    level = db.Column(db.Integer)   #用户等级
    extra = db.Column(db.String(100))

#通过注册之后将消息发送到小程序管理页面来审核
@app.route('/register',methods=['POST'])
def register():
    content = request.get_json(force=True)
    if content['openId'] == None or content['openId'] == '':
        return jsonify({'msg':'注册异常','code':1})
    if content['username'] == None or content['username']== '':
        return jsonify({'msg':'请填写相关信息','code':2})
    checkUser = Users.query.filter_by(openId=content["openId"])
    if checkUser is None or len(checkUser) != 0:
        return jsonify({'msg':'您已注册，无需重复注册','code':3})
    user = Users(username = content['username'],wx_name = content['wx_name'],openId = content['openId'],session_key = content['session_key'],status = False,level = 1)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg':'注册成功，请等待管理员审核','code':0})

@app.route('/',methods=['POST'])
def handle_image():
    content = request.get_json(force=True)
    openId = content['openId']
    address = content['address']
    time = content['time']
    post_img = content['img'][0]
    level = content['level']

    #检测用户登录
    user_info = Users.query.filter_by(openId = openId)
    if user_info is None or len(user_info) == 0:
        return jsonify({'msg':'账号不存在','code':4})
    if user_info.status == False:
        return jsonify({'msg':'管理员审核中，请稍后','code':5})

    img_name = str(str(time)+str(random.randint(0,65535)))
    img = open(locate+img_name+'.jpg','wb')
    # img = open('q.jpg','wb')
    img_temp = base64.b64decode(post_img)
    img.write(img_temp)
    # plate = readImg.read_img()
    # plate = pp.SimpleRecognizePlate(read_img)
    # plate_temp = ['shibai']
    # print plate
    # plate = '识别失败'
    import os
    print os.path
    os.chdir(locate1)
    process = os.popen('python read_plate.py '+locate+img_name+'.jpg')
    # process = os.popen('python read_plate 14.JPG')
    output = process.read()
    print output
    plate = output.split('start')[1]
    plate = plate.split('end')[0]
    print plate
    plate = plate.decode('utf-8')
    # print plate
    # if plate != None and plate != []:
    #     plate = plate[0]
    if plate == '识别失败':
        return jsonify({'msg':'车牌识别失败','code':6})

    user = Users.query.filter_by(openId = openId)
    uid = user.id
    park = Parks(img = 'http://101.132.144.11/getImg/'+img_name+'.jpg',level = level,time = time,address = address,plate = plate,uid = uid,status = False)
    db.session.add(park)
    db.session.commit()
    search_res = Parks.query.filter_by(id = park.id)
    id = search_res.id
    address = search_res.address
    level = search_res.level
    img_address = "http://101.132.144.11/getImg/"+img_name
    time = search_res.time

    count = Users.query.filter_by(plate = plate).count()

    img.close()
        #失败之后对图片进行删除
        # count = search(plate)
    result = jsonify({'msg':'success','code':0,'address':address,'time':time,'plate':plate,'id':id,'img':img_address,'level':level,'count':count})
    # else:
    #     result = jsonify({'msg': 'fail', 'address': address, 'time': time, 'plate': plate, 'id': id,'img':img_address})
    return result

@app.route('/searchAll')
def searchAll():
    search_res = Parks.query.filter_by(status = False).all()
#    print search_res
    res = []
    plateDicts = {}
    for temp in search_res:
#        print temp.plate
        if temp['plate'] in plateDicts:
            plateDicts[temp['plate']] += 1
        else:
            plateDicts[temp['plate']] = 1
    for key,value in plateDicts.items():
        res.append({key,value})
    if len(res) == 0:
        return jsonify({'msg':'无违规信息','code':7})
    return jsonify({'data':res,'msg':'success','code':0})

@app.route('/search',methods=['POST'])
def search():
    content = request.get_json(force=True)
    id = content['id']
    search_res  = Parks.query.filter_by(id = id).all()
    search_res =search_res[0]
    res = {'plate':search_res.plate,'id':search_res.id,'img':search_res.img,'address':search_res.address,'time':search_res.time,'level':search_res.level}
    return jsonify(res)

@app.route('/changePlate',methods=['POST'])
def change_plate():
    content = request.get_json(force=True)
    id = content['id']
#   print content
    search_res = Parks.query.filter_by(id = id).first()
#    print content['plate']
    search_res.plate = content['plate']
    search_res.address = content['address']
    search_res.level = content['level']
    db.session.commit()
    return jsonify({'msg':'success','code':0})

@app.route('/searchByPlate',methods=['POST'])
def searchByPlate():
    content = request.get_json(force=True)
    plate = content['plate']
    search_res = Parks.query.filter_by(plate = plate,status = False).all()
    res = []
    dicts = {}
    for temp in search_res:
        dicts['id'] = temp.id
        dicts['img'] = temp.img
        dicts['address'] = temp.address
        dicts['time'] = temp.time
        dicts['level'] = temp.level
        res.append(dicts.copy())
    if len(res) == 0:
        return jsonify({'msg':'none','code':8})
    return jsonify({'data':res,'msg':'success','code':0})



@app.route('/delete',methods = ['POST'])
def delete():
    content = request.get_json(force=True)
    id = content['id']
    search_res = Parks.query.filter_by(id=id).first()
    if search_res is not None:
        db.session.delete(search_res)
        db.session.commit()
        return jsonify({'msg':'success','code':0})
    return jsonify({'msg':'fail','code':10})

@app.route('/getImg/<imgAddress>')
def getImg(imgAddress):
    if os.path.exists(locate+imgAddress) is True:
        img = file(locate+imgAddress.format(imgAddress))
        resp = Response(img,mimetype='image/jpeg')
        return resp
    else:
        return jsonify({'msg':'fail','code':9})



if __name__ == '__main__':
    # handle_imagereferenced()
    db.create_all()
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True,host = '0.0.0.0',port=80)