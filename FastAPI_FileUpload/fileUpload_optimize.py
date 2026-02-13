# ==========================================
# 1. 标准库导入 (Standard Library Imports)
# ==========================================
import os  # 用于底层操作系统交互（如删除文件、获取文件名）
import uvicorn  # 用于启动 ASGI 服务器
from pathlib import Path as LibPath  # 用于跨平台路径处理，起别名防止命名冲突
from typing import Annotated  # 用于类型提示增强，使代码更符合 FastAPI 规范

# ==========================================
# 2. 第三方库导入 (Third-party Library Imports)
# ==========================================
import aiofiles  # 异步文件操作库，防止文件 I/O 阻塞事件循环
from fastapi import (  # 从 FastAPI 核心包导入组件
    FastAPI,  # 核心应用对象
    File,  # 用于定义文件字节流参数
    UploadFile,  # 用于定义高性能上传对象
    HTTPException,  # 用于抛出自定义 HTTP 异常
    status,  # 包含标准的 HTTP 状态码（如 400, 500）
)

# ==========================================
# 3. 初始化与配置 (App Initialization & Config)
# ==========================================
app = FastAPI(title="Pro-FileUpload-Service")

# 路径配置：使用绝对路径确保在不同环境下部署时行为一致

"""
__file__：这是 Python 的一个内置变量，代表当前正在运行的 Python 文件的完整路径。

LibPath：这是你在代码开头给 pathlib.Path 起的别名（from pathlib import Path as LibPath）。

LibPath(__file__)：作用是将这个“字符串路径”转化成一个**“路径对象”**。
"""
# .resolve() 会将相对路径转换为当前系统的绝对路径
BASE_DIR = LibPath(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "uploads"

# 确保存储目录存在：parents=True 自动创建多层级父目录
STORAGE_DIR.mkdir(
    # 1. parents=True (递归创建/补全路径):
    # 如果路径中的父文件夹（如 BASE_DIR/uploads 中的 uploads）不存在，会自动创建。
    # 设为 True: “缺啥补啥”，像修路一样把通往终点的所有中间站都修好。
    # 设为 False (默认): 如果父级路径缺失，代码会直接抛出 FileNotFoundError 报错。
    parents=True,
    # 2. exist_ok=True (存在即包容/防止报错):
    # 如果该目录已经存在，程序不会报错并继续执行。
    # 设为 True: “已存在则跳过”，适合程序重启、循环运行等场景。
    # 设为 False (默认): 如果目录已存在，代码会抛出 FileExistsError 报错。
    exist_ok=True,
)

# 性能配置：定义流式传输时每块的大小（1MB）
STREAM_CHUNK_SIZE = 1024 * 1024


# ==========================================
# 4. 路由定义 (API Routes)
# ==========================================


@app.post("/upload/small", summary="小文件快速上传接口")
async def upload_small_file(
    file: Annotated[bytes, File(description="仅限 10MB 以下的小文件")],
):
    """
    【模式 A：一次性内存写入】
    - 将整个文件读入内存。
    - 优点：代码简单，处理速度快。
    - 缺点：大文件会导致内存溢出。
    """
    save_path = STORAGE_DIR / "quick_save.jpg"

    try:
        async with aiofiles.open(save_path, "wb") as buffer:
            await buffer.write(file)
        return {"message": "小文件保存成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/upload/large", summary="大文件流式上传接口")
async def upload_large_file(file: UploadFile):
    """
    【模式 B：流式分块写入】
    - 每次只读取 1MB 放入内存，循环往复。
    - 优点：极度安全，支持上传 GB 级的超大视频或镜像。
    """
    # 1. 验证文件名
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="文件名无效"
        )

    # 2. 安全性：过滤掉用户可能构造的 '../' 攻击性路径
    safe_name = os.path.basename(file.filename)
    dest_path = STORAGE_DIR / safe_name

    try:
        # 3. 异步分块搬运数据
        async with aiofiles.open(dest_path, "wb") as out_file:
            # 使用 Python 3.8+ 海象运算符精简逻辑
            while chunk := await file.read(STREAM_CHUNK_SIZE):
                await out_file.write(chunk)

    except Exception as err:
        # 异常回滚：如果传输中断，删除那个写了一半的损坏文件
        if dest_path.exists():
            os.remove(dest_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"传输中断: {err}",
        )

    finally:
        # 4. 资源释放：关闭 UploadFile 的临时文件句柄（非常重要）
        await file.close()

    return {
        "filename": safe_name,
        "size": f"{dest_path.stat().st_size / 1024:.2f} KB",
        "msg": "上传成功",
    }


# ==========================================
# 4. 路由定义 (续写部分)
# ==========================================


@app.post("/batch-upload/", summary="批量文件上传接口")
async def batch_upload(
    # 使用 list[UploadFile] 让接口能够接收多个文件
    # File(...) 表示这个参数是强制必填的
    files: list[UploadFile] = File(..., description="支持同时上传多个文件")
):
    """
    【批量上传模式】
    - 循环遍历文件列表，对每个文件执行保存逻辑。
    """
    results = []

    for file in files:
        # 1. 为每个文件生成安全的文件名
        safe_name = os.path.basename(file.filename)
        """
        # 场景 A：完整的绝对路径
        path_a = "/home/user/project/uploads/test.jpg"
        print(os.path.basename(path_a))  
        # 输出结果: "test.jpg"

        # 场景 B：只有文件名的路径
        path_b = "quick_save.png"
        print(os.path.basename(path_b))  
        # 输出结果: "quick_save.png"
        
        # 场景 C：以斜杠结尾的路径（目录路径）
        path_c = "/home/user/project/uploads/"
        print(os.path.basename(path_c))  
        # 输出结果: "" (返回空字符串，因为它认为最后是一个文件夹)
        """
        dest_path = STORAGE_DIR / safe_name

        # 2. 保存文件（这里使用简单的一次性写入，实际大文件建议用流式）
        content = await file.read()
        async with aiofiles.open(dest_path, "wb") as f:
            await f.write(content)

        # 3. 记录每个文件的保存状态
        results.append({"filename": safe_name, "status": "success"})

        # 记得关闭每个文件的句柄
        await file.close()

    return {"uploaded_files": results, "total_count": len(files)}


# 限制上传格式：定义允许的后缀名集合（使用 set 查找效率更高）
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


@app.post("/image-upload/", summary="限定格式图片上传")
async def image_upload(file: UploadFile):
    """
    【格式校验模式】
    - 在保存前检查文件的后缀名。
    - 如果格式不符，直接抛出 400 错误，不浪费服务器空间。
    """
    # 1. 提取后缀名并转为小写（防止用户上传 .JPG 绕过校验）
    # file.filename.split(".")[-1] 拿到最后一个点后面的内容
    file_ext = file.filename.split(".")[-1].lower()

    # 2. 验证格式是否在允许列表中
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件格式！仅支持: {ALLOWED_EXTENSIONS}",
        )

    # 3. 验证通过后的保存逻辑
    safe_name = f"verified_{os.path.basename(file.filename)}"
    dest_path = STORAGE_DIR / safe_name

    async with aiofiles.open(dest_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    await file.close()

    return {"msg": "图片校验通过并保存成功", "filename": safe_name}


# ==========================================
# 5. 入口函数 (Main Entry)
# ==========================================
if __name__ == "__main__":
    # 获取当前文件名（不含扩展名），动态传递给 uvicorn
    module_name = LibPath(__file__).stem
    uvicorn.run(
        f"{module_name}:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
