def remove_all_spaces(input_str):
    """
    移除字符串中的所有空格。

    参数:
    - input_str (str): 原始字符串。

    返回:
    - str: 移除所有空格后的字符串。

    示例:
    >>> remove_all_spaces("Hello World")
    'HelloWorld'
    """
    return input_str.replace(" ", "")