from bilibili_api import search, sync
import time, json, tools


def search_from_bilibili(page=1) -> list[dict]:
    """
    搜索某一页结果
    :param page: 搜索结果的页码
    """
    # 搜索关键词
    keyword = "红石"
    # 搜索类型，这里指定为视频
    search_type = search.SearchObjectType.VIDEO
    # 排序类型，这里指定为按发布日期排序
    order_type = search.OrderVideo.PUBDATE

    # 搜索函数
    async def search_videos():
        return await search.search_by_type(keyword, search_type=search_type, order_type=order_type, page=page)

    # 同步执行搜索函数
    res = sync(search_videos())

    # 过滤出最近1天的、包含标签“我的世界”的视频
    recent_videos = []
    target_time = time.time() - 86400
    for i in res['result']:
        if i['pubdate'] > target_time and '我的世界' in i['tag']:
            recent_videos.append(i)
    return recent_videos


def search_video() -> list[dict]:
    """
    在b站进行一次搜索
    :return: 一个list, 其中每一个元素为一条搜索结果
    """
    # 初始化标志位
    flag = True
    # 初始化页码计数器
    i = 0
    # 初始化搜索结果列表
    search_result = []
    # 当标志位为真时循环执行以下操作
    while flag:
        # 计数器页码加一
        i += 1
        # 调用search_from_bilibili函数，传入计数器作为参数并获得结果
        result = search_from_bilibili(i)
        search_result.extend(result)
        # 如果当前结果列表的长度小于20，则跳出循环
        if len(result) < 20:
            break
        # 打印搜索冷却中并等待30秒
        for i in range(30):
            print('搜索冷却中... ' + str(30 - i) + 's')
            time.sleep(1)
    # 返回搜索结果列表
    return search_result
