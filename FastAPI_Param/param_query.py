from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items1")
def read_item1(item_id: str = Query(123)):
    """
    Docstring for read_item1

    :param item_id: Description
    :type item_id: str  默认值为123，可选是否传入
    """
    return {"item_id": item_id}


@app.get("/items2")
def read_item2(item_id: str = Query(...)):
    """
    Docstring for read_item2

    :param item_id: Description
    :type item_id: str  。。。表示 必须传入
    """
    return {"item_id": item_id}


@app.get("/items3")
def read_item3(item_id: str = Query(..., min_length=3, max_length=10)):
    """
    Docstring for read_item3

    :param item_id: Description
    :type item_id: str 指定具体长度的限制
    """
    return {"item_id": item_id}


@app.get("/items4")
def read_item4(item_id: int = Query(..., gt=0, lt=100)):
    """
    Docstring for read_item4

    :param item_id: Description
    :type item_id: str 限制内容大小
    """
    return {"item_id": item_id}


@app.get("/items5")
def read_item5(item_id: str = Query(..., alias="id")):
    """
    Docstring for read_item5

    :param item_id: Description
    :type item_id: 修改别名，只在前端传递生效，后台使用必须使用item_id
    """
    return {"item_id": item_id}


@app.get("/items6")
def read_item6(item_id: str = Query(..., description="用来筛选产品id")):

    return {"item_id": item_id}


@app.get("/items7")
def read_item7(item_id: str = Query(..., deprecated=True)):
    """
    Docstring for read_item7

    :param item_id: Description
    :type item_id: str  参数被抛弃，能用但是会在前端显示被抛弃
    """
    return {"item_id": item_id}


@app.get("/items8")
def read_item8(item_id: str = Query(..., regex="^a\d{2}$")):
    """
    Docstring for read_item8

    :param item_id: Description
    :type item_id: str 通过正则表达式进行匹配（pattern和regex都表示正则表达式）
    """
    return {"item_id": item_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("param_query:app", host="127.0.0.1", port=8000, reload=True)
