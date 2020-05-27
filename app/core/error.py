import datetime
from dataclasses import dataclass


class ResCode:
    """
    10000: 创建
    20000: 修改
    30000: 操作
    40000：删除
    50000：权限验证

    1000: 成功
    2000: 操作冲突
    3000: 内部错误
    4000: 外部错误

    100: Tourney / 比赛
    200: Matches / 对局
    300: Mappool / 图池
    400: Maps / 谱面
    500: Users / 用户
    600: Ewc / 周赛
    """

    RES_CODE = {
        # 10001: '添加对局成功！等待elo重新计算完成。',
        # 10002: 'event排除成功！重新计算后生效。',
        11101: '创建比赛(Tourney)成功！',
        12101: '这个比赛(Tourney)已被注册过啦！请检查名称、缩写、中文名是否冲突。',

        11301: '创建图池(Mappool)成功!',
        12301: '这个图池(Mappool)已被注册过啦！换个名字吧~',
        11302: '创建图池(Mappool)谱面成功!',
        11303: '创建评价成功！',
        12303: '同一图池每个玩家只能评价一次！尝试修改评价吧~',

        # 10005: '玩家信息初始化成功！',
        # 10006: '注册队伍成功!',
        # 10007: '加入队伍成功!',
        # 10008: '退出队伍成功!',
        # 10010: 'elo计算成功！',
        # 10011: '添加图池成功！',

        # 20001: '玩家信息已经更新！',
        21301: '图池(Mappool)信息已经更新！',
        21302: '图池谱面(Mappool_Map)信息已经更新！',

        30001: '这场对局(Match)已经被上传过咯！',


        32303: '没有查询到相应评价。',

        41303: '删除评价成功！下次再来噢~'
        # 30002: 'event已经被添加过！',
        # 30006: '这张图已经有MOD了，如需修改请联系管理员。',

        # 40000: '官网未查询到这场比赛',
        # 40001: '未查询到此比赛信息！请输入正确的比赛名称。',
        # 40002: '未查询到此比赛的图池信息！',
        # 40003: '未查询符合条件的对局！',
        # 40004: '未查询到这位玩家的elo信息！',
        # 40005: '这位玩家已经去世...',
        # 40006: '这位玩家还未诞生...',
        # 40007: '这厮没打过比赛...',
        # 40008: '未查询到比赛或者相应图池信息。',
        # 40009: '这人都没rank你查毛啊！',
        # 40010: '队伍已存在，换个名字吧。',
        # 40011: '队伍已满，换个队伍吧。',
        # 40012: '查不到这个队伍，打错了吗？',
        # 40013: '您的elo不符合队伍要求。。。',
        # 40014: '您不在这队啊！！！！！',
        # 40015: '队伍空空如也。',
        # 40016: '队伍上下限elo超过了规定数值！请elo最高玩家主动退队。',
        # 40017: '没有相应分段的队伍存在！',
        # 40018: '每个人限加入两个队伍！',
        # 40019: '您已经在这队了啊！！',
        # 40020: '您已经注册过队伍了！！',
        # 40021: '您没有加入任何队伍！',
        # 40022: '您没有注册过队伍!',
        #
        # 50001: '验证密码错误，滚！'
    }

    @staticmethod
    def raise_success(error_code, *args, **kwargs):
        res = {'message': ResCode.RES_CODE[error_code], 'code': error_code, 'time': str(datetime.datetime.now()),
               'status': 1}
        if kwargs:
            for k, v in kwargs.items():
                res[k] = v
        return res

    @staticmethod
    def raise_error(error_code, *args, **kwargs):
        try:
            code = ResCode.RES_CODE[error_code]
        except KeyError as e:
            raise Exception('Error Code Error', e)
        res = {'message': code, 'code': error_code, 'time': str(datetime.datetime.now()),
               'status': 0}
        if kwargs:
            for k, v in kwargs.items():
                res[k] = v
        return res
