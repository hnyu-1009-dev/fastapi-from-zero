from fastapi import FastAPI

# 1.路由解析顺序：
# ##FastAPI 会根据路由的定义顺序来处理请求。
# ##如果有多个路由定义重叠的部分（例如 /args3/{id} 和 /args5/{id}/{name}），FastAPI 会按顺序匹配路由，首先匹配到的路由会被执行。
# ##因此，/args5/{id}/{name} 会在 /args3/{id} 之前匹配，因为 /args5/{id}/{name} 更具体，包含更多路径部分。

# 2.路径参数和函数参数的映射：
# ##在 FastAPI 中，路径中的参数（如 {id} 和 {name}）会自动映射到函数的参数。
# ##如果你没有指定类型注解（例如 id: str），FastAPI 会默认将路径参数视为字符串。
# ##如果你指定了类型（例如 id: int），FastAPI 会自动尝试将路径参数转换为相应的类型。如果无法转换，则会返回错误（例如 422 错误）。

# 3.路由顺序的重要性：
# ##在 FastAPI 中，路由的解析顺序是非常重要的。例如，/args3/{id} 和 /args5/{id}/{name} 会有不同的匹配顺序。由于 FastAPI 是按顺序解析路由的，若 /args5/{id}/{name} 在前，/args3/{id} 将无法被匹配到。
# ##如果路径具有多层次的参数（例如 /args5/{id}/{name}），在更具体的路由前面定义较为简单的路由（例如 /args3/{id}）是非常重要的。
# ##创建 FastAPI 应用实例
app = FastAPI()


# 路由 1：简单的路径，不接受任何参数
@app.get("/args1/1")
def path_args1():
    """
    路由：/args1/1
    这是一个非常简单的路由，直接返回固定消息 "id1"。
    """
    return {"message": "id1"}


# 路由 2：路径参数 {id}
@app.get("/args2/{id}")
def path_args2(id: str):
    """
    路由：/args2/{id}
    这个路由从路径中提取参数 'id' 并返回它。
    :param id: 从路径中提取的字符串类型的参数
    """
    return {"message": f"id2: {id}"}


# 路由 3：路径参数 {id}，带有 docstring
@app.get("/args3/{id}")
def path_args3(id: str):
    """
    路由：/args3/{id}
    这个路由也提取路径中的 'id'，但它同时包含了文档字符串说明。
    :param id: 路径参数，描述所接收的 'id'
    函数的顺序就是路由的顺序——FastAPI 会按照定义的顺序解析路径
    """
    return {"message": f"args3 id: {id}"}


# 路由 4：路径参数 {id}，并通过类型注解明确指定类型为 `int`
@app.get("/args4/{id}")
def path_args4(id: int):
    """
    路由：/args4/{id}
    这个路由会将路径中的 'id' 强制转换为整数类型。若路径中的 id 无法转换为整数，将返回 422 错误（Unprocessable Entity）。
    :param id: 路径参数，整数类型
    """
    return {"message": f"id is {id}"}


# 路由 5：两个路径参数 {id} 和 {name}
@app.get("/args5/{id}/{name}")
def path_args5(id: str, name: str):
    """
    路由：/args5/{id}/{name}
    这个路由有两个路径参数，'id' 和 'name'。它会同时接收这两个参数并返回。
    :param id: 路径参数，字符串类型
    :param name: 路径参数，字符串类型
    """
    return {
        "id5": id,
        "name5": name,
    }
