from fastapi import FastAPI

app = FastAPI()


@app.get("/query1")
def page_limit(page, limit):
    """
    示例一：最基础的查询参数（Query Parameters）

    路由：/query1
    访问方式示例：
        /query1?page=1&limit=10

    说明：
    - 这里没有在函数参数上写类型注解，FastAPI 会默认把它们当作字符串类型 (str) 处理。
    - page、limit 都是「必填」查询参数，如果不传会返回 422 校验错误。
    - 因为没有出现在路径中（路径里没有 {page}、{limit}），所以它们都是 query 参数。
    """

    # 返回前端传入的 page 和 limit
    return {
        "page": page,
        "limit": limit,
    }


@app.get("/query2")
def page_limit2(page, limit=None):
    """
    示例二：带默认值的查询参数（可选参数）

    路由：/query2
    访问方式示例：
        /query2?page=1&limit=10
        /query2?page=1          # 不传 limit

    说明：
    - page 依然是必填查询参数。
    - limit 有默认值 None，因此变成「可选查询参数」：
        * 如果请求中不带 limit，函数里收到的就是 None。
        * 如果请求中携带 limit，则使用请求里的值。
    - 类型同样默认是 str（未加类型注解），只是允许为空（None）。
    """

    return {
        "page": page,
        "limit": limit,
    }


@app.get("/query3")
def page_limit3(page, limit, info: int):
    """
    示例三：混合「未注解」和「有类型注解」的查询参数

    路由：/query3
    访问方式示例：
        /query3?page=1&limit=10&info=100

    说明：
    - page：必填查询参数，类型默认 str。
    - limit：必填查询参数，类型默认 str。
    - info：必填查询参数，带有类型注解 `int`：
        * FastAPI 会尝试把 info 从字符串转换为整数。
        * 如果无法转换（例如 info=abc），会返回 422 校验错误。

    结论：
    - 是否写类型注解，决定了 FastAPI 的数据转换和校验方式。
    """

    return {
        "page": page,
        "limit": limit,
        "info": info,
    }


@app.get("/query4/{page}")
def page_limit4(page, limit, info: int):
    """
    示例四：同时使用「路径参数」和「查询参数」

    路由：/query4/{page}
    访问方式示例：
        /query4/1?limit=10&info=100

    参数来源说明：
    - page：来自「路径参数」：
        * 路由中写了 /query4/{page}，所以 URL 中这一段会被解析为 page。
        * 示例：访问 /query4/1 时，page = "1"（未写类型注解，默认 str）。
    - limit：来自「查询参数」：
        * URL 中的 ?limit=10 这一部分。
        * 未写类型注解，默认 str，且为必填。
    - info：来自「查询参数」：
        * URL 中的 ?info=100 这一部分。
        * 写了 `info: int`，FastAPI 会进行整数转换和校验。

    底层路由解析要点：
    1. FastAPI 根据装饰器 `@app.get("/query4/{page}")` 注册一个路由。
    2. `{page}` 这一段会被识别为「路径参数」，并绑定到函数参数 `page`。
    3. 函数中所有「不在路径声明里的参数」默认都被当作「查询参数」：
        - 这里的 limit、info 都是 query。
    4. 参数是否必填：
        - 没有默认值的参数（page、limit、info）都是必填。
        - 带默认值（如 limit=None）的参数则是可选。

    建议实战中：
    - 给 page、limit、info 都加上类型注解（如 int、str），
      让接口行为和文档更清晰。
    """

    return {
        "page": page,
        "limit": limit,
        "info": info,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("queryParam:app", host="127.0.0.1", port=8000, reload=True)
