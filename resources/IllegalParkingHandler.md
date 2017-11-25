### 违停处理工具文档

---

#### 接口说明

#### 微信端：

    "/":  POST
    Request:
    {
        "time":         //时间戳
        "address":      //地址
        "img":          //原始图片
        "username":     //用户信息
    }
    Response:
    {
        "res":          //"fail" or "success"
        "id":           //违规的id
        "time":         //时间戳
        "address":      //地址
        "img":          //图片的url地址
        "plate":        //车牌号
        "allcount":     //违规次数
        "count":        //待处理违规次数
    }


    "/changePlate": POST
    Request:
    {
        "id":           //违规id
        "plate":        //车牌号
        "address":      //地点
    }
    Response:
    {
        "res":          //"fail" or "success"
        "plate":        //车牌号
        "address":      //地址
    }
  
    "getImg/<imgAddress>":  GET (注意：<imgAddress>是图片的url地址)
    Response:
    成功时直接返回图片,
    失败时返回：
    {
        "res":"fail"          
    }


    "/searchAll"： GET
    Response:
    [
        "res":          //"fail" or "success" or"none"
        {
            "id":       //违规的id
            "time":     //时间戳
            "address":  //地址
            "img":      //图片的url地址
            "plate":    //车牌号
            "allcount": //总的违规次数
            "count":    //待处理违规次数
        },
        {
            "id":       //违规的id
            "time":     //时间戳
            "address":  //地址
            "img":      //图片的url地址
            "plate":    //车牌号
            "allcount": //总的违规次数
            "count":    //待处理违规次数
        },
        ...
    ]


    "/search":  POST
    Request:
    {
        "id":           //违规的id
    }
    Response:
    {
        "res":          //"fail" or "success" or "none"
        "id":           //违规的id
        "time":         //时间戳
        "address":      //地址
        "img":          //图片的url地址
        "plate":        //车牌号
        "allcount":     //总的违规次数
        "count":        //待处理违规次数
    }
    

#### 网页端：

    "/searchAll"： GET
    Response:
    [
        "res":          //"fail" or "success" or "none"
        {
            "id":       //违规的id
            "time":     //时间戳
            "address":  //地址
            "img":      //图片的url地址
            "plate":    //车牌号
            "allcount": //总的违规次数
            "count":    //待处理违规次数
        },
        {
            "id":       //违规的id
            "time":     //时间戳
            "address":  //地址
            "img":      //图片的url地址
            "plate":    //车牌号
            "allcount": //总的违规次数
            "count":    //待处理违规次数
        },
        ...
    ]


    "/search":  POST
    Request:
    {
        "id":           //违规的id
    }
    Response:
    {
        "res":          //"fail" or "success" or "none"
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
        "res":          //"fail" or "success"
    }
    

