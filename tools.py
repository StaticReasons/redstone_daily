import time, json, crawler, tools
from bilibili_api import search, sync, video as bilivideo, credential


def is_video_compliant(title, description, tags):
    # 处理标题数据
    flag = False
    tmp_string = ''
    for i in title:
        if i == '<':
            flag = True
        if flag:
            if i == '>':
                flag = False
            continue
        tmp_string += i
    title = tmp_string

    # 创建一个权重,用于分析视频数据
    weight = 1
    # 判断是否包含关键字,如果包含则权重变化
    keyword_list = [
        {'keyword': '服务器', 'weight': 0},
        {'keyword': '游戏实况', 'weight': 0},
        {'keyword': '实况', 'weight': 0},
        {'keyword': '机械动力', 'weight': 0},
        {'keyword': '模组', 'weight': 0},
        {'keyword': 'MOD', 'weight': 0},
        {'keyword': '生存', 'weight': 0.3},
        {'keyword': '生电', 'weight': 1.5},
        {'keyword': '数电', 'weight': 1.5},
        {'keyword': '模电', 'weight': 1.5},
        {'keyword': '械电', 'weight': 1.5},
        {'keyword': '储电', 'weight': 1.5},
        {'keyword': '炮电', 'weight': 1.5},
        {'keyword': '音乐', 'weight': 0},
        {'keyword': '红石电路', 'weight': 2},
        {'keyword': '红石科技', 'weight': 2},
        {'keyword': '沙雕红石', 'weight': 2},
    ]
    print('title= ', title, ' description= ', description, ' tag= ', tags)
    for i in keyword_list:
        if i['keyword'] in title:
            weight *= i['weight']
        if i['keyword'] in description:
            weight *= i['weight']
        if i['keyword'] in tags:
            weight *= i['weight']
    if '红石' not in title:
        weight *= 0.6
    if '红石' not in description:
        weight *= 0.6
    if '红石' not in tags:
        weight *= 0.6
    if '红石' in tags:
        weight *= 1.37
    # 如果权重小于0.5则返回False,否则返回True
    if weight < 0.5:
        return False
    else:
        return True


def filter_video(video: dict):
    return is_video_compliant(video['title'], video['description'], video['tag'])


# 计算视频综合得分
def calc_score(like, view, favorite, coin, share):
    return view + like * 3 + favorite * 4 + coin * 10 + share * 4


def get_today_video(credential_obj):
    # 使用crawler模块搜索并获取今日视频列表
    video_list = crawler.search_video()

    # 检查视频列表是否为空，如果为空则输出提示信息，并返回'NO_VIDEO'
    if len(video_list) == 0:
        print('今天居然没有视频 ERR_CODE=NO_VIDEO')
        return 'NO_VIDEO'

    filter(filter_video, video_list)

    # 检查经过筛选后的视频列表是否为空，如果为空则输出提示信息，并返回'NOT_FOUND'
    if len(video_list) == 0:
        print('今天居然没有符合规则的视频 ERR_CODE=NOT_FOUND')
        return 'NOT_FOUND'

    # 初始化结果列表用于存放处理后的视频信息
    result_list = []

    # 遍历符合规则的视频列表，获取每个视频的各项详细信息
    for video in video_list:
        # 创建bilivideo.Video对象并获取其详细信息
        video_obj = bilivideo.Video(bvid=video["bvid"], credential=credential_obj)
        res = sync(video_obj.get_info())
        # 获取视频字幕信息
        conclude = sync(video_obj.get_ai_conclusion(res['cid']))

        title = video['title']  # 视频标题
        description = video['description']  # 视频描述
        tags = video['tag']  # 视频标签
        author = video['author']  # 视频作者
        url = video['arcurl']  # 视频链接
        bvid = video['bvid']  # B站视频唯一标识符
        cover_url = video['pic']  # 视频封面链接
        upic = video['upic']  # UP主头像链接
        play = video['play']  # 视频播放次数
        review = video['review']  # 视频评论数量
        like = video['like']  # 视频点赞数
        coin = res['stat']['coin']  # 视频投币数
        share = res['stat']['share']  # 视频分享数
        favorite = video['favorites']  # 视频收藏数

        # 将视频信息封装为一个字典并添加到结果列表中
        result = {
            'title': title,
            'description': description,
            'tags': tags,
            'author': author,
            'url': url,
            'bvid': bvid,
            'cover_url': cover_url,
            'upic': upic,
            'play': play,
            'review': review,
            'like': like,
            'coin': coin,
            'share': share,
            'favorite': favorite,
            'score': calc_score(like, play, favorite, coin, share)
        }
        result_list.append(result)

        # 为了避免频繁请求，暂停3秒后再处理下一个视频
        time.sleep(3)

    # 返回处理完成的视频信息列表
    return result_list
