from fastapi import FastAPI
import asyncio
import time

app = FastAPI()


# --- 异步方案：并发执行 ---
# 场景：当需要同时发起多个网络请求或数据库查询时使用
@app.get("/async")
async def async_endpoint():
    start = time.time()

    # 1. 创建任务列表：这里并没有立即执行，只是创建了 5 个协程对象
    # 模拟 5 个各耗时 1 秒的异步 I/O 操作
    tasks = [asyncio.sleep(1) for _ in range(5)]

    # 2. 关键点：使用 asyncio.gather 并发执行
    # 事件循环会同时启动这 5 个任务，由于它们都在“等待”，
    # CPU 会在这些任务之间快速切换，而不是傻傻地等待某一个完成
    await asyncio.gather(*tasks)
    end = time.time()
    # 结果：总耗时仅约为 1 秒左右（因为是同时等的）
    return {"异步时长": f"{end - start:.2f}秒"}


# --- 同步方案：顺序执行 ---
# 场景：传统的阻塞式编程
@app.get("/sync")
def sync_endpoint():
    start = time.time()

    # 1. 模拟 5 次同步 I/O 操作
    # time.sleep 是阻塞性的，它会“霸占”当前线程，不准 CPU 做任何其他事
    for _ in range(5):
        # 必须等前一个 sleep(1) 完成了，才会进入下一个循环
        time.sleep(1)

    end = time.time()
    # 结果：总耗时为 5 秒（1+1+1+1+1）
    return {"同步时长": f"{end - start:.2f}秒"}


if __name__ == "__main__":
    import uvicorn

    # 运行服务器：app 是实例名，app.py 是文件名（这里需确保文件名匹配）
    uvicorn.run("test_async:app", host="127.0.0.1", port=8000, reload=True)
