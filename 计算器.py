# 计算器  3+ ((1* 5*3) + ( (3* (8/2)/2) +2 ) *2) *2 + 4

# 思路:
# 1. 先去除空格
# 2. 对特殊字符报错(字母、加减乘除之外的字符)
# 3. 括号都是成对的, 要从最内部的括号开始计算, 由内而外, 计算后得出结果
# 4. 将3步骤得到的结果去替换3步骤匹配到的括号及内部的内容, 然后得到一个新的字符串
# 5. 重复执行3步骤和4步骤, 最终得到一个不包含任何括号的字符串, 计算这个字符串表达式就是最终的结果

import re


def del_space(calc_str):
    """
    去除整个字符串中的空格
    :param calc_str: 原始字符串
    :return: 去除空格后的字符串
    """
    data = calc_str.replace(" ", "")
    return data


def check_special(calc_str):
    """
    检测字符串中是否有字母及非运算的特殊字符,
    :param calc_str: 原始字符串
    :return: True or False, 若为True，则表示存在特殊字符
    """
    pattern = re.compile(r"[^\d\+\-\*\/()]")
    check = pattern.findall(calc_str)
    return check


def calculate(calc_str):
    """
    对字符串中的表达式进行计算
    :param calc_str: 数学计算表达式类型的字符串
    :return: 计算后的结果
    """
    while True:
        if calc_str.find("*") != -1:
            pattern = re.compile(r"(?P<prv>[\d]+[.]?[\d]*)(?P<typ>[*])(?P<after>[\d]+[.]?[\d]*)")
            prv, typ, aft = pattern.search(calc_str).group("prv", "typ", "after")
            # re.sub("%s%s%s" % (prv, typ, aft), str(value), calc_str)
            calc_str = calc_str.replace("%s%s%s" % (prv, typ, aft), str(float(prv) * float(aft)))
            continue
        elif calc_str.find("/") != -1:
            pattern = re.compile(r"(?P<prv>[\d]+[.]?[\d]*)(?P<typ>[/])(?P<after>[\d]+[.]?[\d]*)")
            prv, typ, aft = pattern.search(calc_str).group("prv", "typ", "after")
            calc_str = calc_str.replace("%s%s%s" % (prv, typ, aft), str(float(prv) / float(aft)))
            continue
        elif calc_str.find("+") != -1:
            pattern = re.compile(r"(?P<prv>[\d]+[.]?[\d]*)(?P<typ>[+])(?P<after>[\d]+[.]?[\d]*)")
            prv, typ, aft = pattern.search(calc_str).group("prv", "typ", "after")
            calc_str = calc_str.replace("%s%s%s" % (prv, typ, aft), str(float(prv) + float(aft)))
            continue
        elif calc_str.find("-") != -1:
            pattern = re.compile(r"(?P<prv>[\d]+[.]?[\d]*)(?P<typ>[-])(?P<after>[\d]+[.]?[\d]*)")
            prv, typ, aft = pattern.search(calc_str).group("prv", "typ", "after")
            calc_str = calc_str.replace("%s%s%s" % (prv, typ, aft), str(float(prv) - float(aft)))
            continue
        else:
            break
    return calc_str


def replace_expr(calc_str):
    """
    找到最内部的括号, 计算出值后将值替换到字符串中
    :param calc_str: 纯粹的要计算出结果的字符串
    :return: 当前字符串最内部的值
    """
    try:  # re的search方法如果匹配不到内容就会报错
        pattern = re.compile(r"\((?P<init>[\d\+\-\*\/.]*)\)")
        init_str = pattern.search(calc_str).group("init")
        value = str(calculate(init_str))
        result = re.sub(r"\([\d\+\-\*\/.]*\)", value, calc_str, 1)  # 只替换第一次匹配到的
        return result
    except Exception:
        return None


while True:
    origin_str = input("请输入要计算的内容: ")
    calc_str = del_space(origin_str)
    if check_special(calc_str):
        print("存在特殊字符, 请检查后再计算!")
        continue
    while True:
        str_init = replace_expr(calc_str)
        if str_init:
            calc_str = str_init
        else:
            value = calculate(calc_str)
            print("最终的结果为: ", value)
            break

# 测试: calc_strx = "3+ ((1* 5*3) + ( (3* (8/2)/2) +2 ) *2) *2 - 4"
# 正确结果为:61