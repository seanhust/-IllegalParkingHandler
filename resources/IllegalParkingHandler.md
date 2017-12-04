### 违停处理工具文档

---

#### 接口说明

#### 微信端：

    "/register": POST
    Request:
    {
        "username":     //用户真实姓名
        "openId":       //微信端的openId
        "wx_name":      //微信名
        "session_key":  //微信返回的session_key
    }
    Request:
    {
        "msg":          //返回的提示信息
        "code":         //状态码
    }


    "/":  POST
    Request:
    {
        "time":         //时间戳
        "address":      //地址
        "img":          //原始图片
        "level"         //用户违规等级
        "openId":       //
    }
    Response:
    {
        "msg":          //返回的信息
        "code"          //状态码
        "id":           //违规的id
        "time":         //时间戳
        "address":      //地址
        "img":          //图片的url地址
        "plate":        //车牌号
        "level"         //违规等级
        "allcount":     //违规次数
        "count":        //待处理违规次数
    }


    "/changePlate": POST
    Request:
    {
        "id":           //违规id
        "plate":        //车牌号
        "address":      //地点
        "level":         //违规等级
        "count":        //违规的次数
    }
    Response:
    {
        "msg":          //返回的信息
        "code"          //状态码
        "plate":        //车牌号
        "address":      //地址
    }
  
    "getImg/<imgAddress>":  GET (注意：<imgAddress>是图片的url地址)
    Response:

    Response:
    {
        "msg":          //返回的信息
        "code"          //状态码
        "img"           //返回的图片
    }


    "/searchAll"： GET
    Response:
    {
        "msg":
        "code":
        "data": [{"plate":count},......]
    }


    "/search":  GET
    Request:
    {
        "id":       //
    }
    Response:
    {
        'msg':
        'code':
        "id":           //违规的id
        "time":         //时间戳
        "address":      //地址
        "img":          //图片的url地址
        "plate":        //车牌号
        "count":        //待处理违规次数
    }

    "/searchByPlate" POST
    Request:
    {
        "plate":
    }
    Response:
    {
        "msg":
        "code":
        "data":[{'id':,'time':,'address','img':,},......]
    }

#### 网页端：
 "/searchAll"： GET
    Response:
    {
        "msg":
        "code":
        "data": [{"plate":count},......]
    }


    "/search":  GET
    Request:
    {
        "id":       //
    }
    Response:
    {
        'msg':
        'code':
        "id":           //违规的id
        "time":         //时间戳
        "address":      //地址
        "img":          //图片的url地址
        "plate":        //车牌号
        "allcount":     //总的违规次数
        "count":        //待处理违规次数
    }

    "/searchByPlate" POST
    Request:
    {
        "plate":
    }
    Response:
    {
        "msg":
        "code":
        "data":[{'id':,'time':,'address','img':,},......]
    }


    "/search":  POST
    Request:
    {
        "id":           //违规的id
    }
    Response:
    {
        "msg":          //返回的信息
        "code"          //状态码
        "id":           //违规的id
        "time":         //时间戳
        "address":      //地址
        "img":          //图片的url地址
        "plate":        //车牌号
        "allcount":     //总的违规次数
        "count":        //待处理违规次数
    }


    "/delete":  POST
    Request:
    {
        "id":           //违规的id
    }
    Response:
    {
        "msg":          //返回的信息
        "code"          //状态码
    }
    

