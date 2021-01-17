"""
函数1——extract_all_text()：导出场景触发树内所有文本到txt

然后你可以对txt内的文本做修改（注意看注意事项哦）！

函数2——import_all_text()：从txt导入修改后的文本到场景触发树

填完参数后，运行脚本，按提示操作，最后可另存场景。

脚本主体设计：newtonerdai
版本：0.1
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

# 加载模块
from typing import Any, Union
from AoE2ScenarioParser.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.datasets.conditions import Condition
from AoE2ScenarioParser.datasets import effects
from AoE2ScenarioParser.datasets.players import Player
from AoE2ScenarioParser.datasets.units import Unit
from AoE2ScenarioParser.objects.triggers_obj import TriggerSelect  # 导入这个才能使用 TriggerSelect.index(n)

TS = TriggerSelect  # 定义这个才能使 TS 等效于 TriggerSelect

def extract_all_text(TM,
                     txt_path,
                     read_file = ""):
    """
    导出给定触发管理器下所有触发的所有效果中的文本(message)到给定.txt文件。
    :param TM: TriggersObject，一般传入你的 trigger_manager 即可
    :param txt_path: 导出到指定文件（完整路径）
    :return: None
    """
    print('正在爬取各触发的描述和各效果的文本……')
    # 爬取文本。
    # [(触发ID、触发名称、是否显示在任务栏、详细描述、是否显示在屏幕、简短描述)]
    all_descriptions = []
    # [(触发ID、触发名称、效果ID、效果名称、文本)]
    all_messages = []
    for (i, trigger_i) in enumerate(TM.triggers):
        # 如果详细描述或简短描述有内容，就爬取出来
        if trigger_i.description != '' or trigger_i.short_description != '':
            all_descriptions.append((i, trigger_i.name, trigger_i.display_as_objective, trigger_i.description,
                                     trigger_i.display_on_screen, trigger_i.short_description))
        for (j, effect_i_j) in enumerate(trigger_i.effects):
            # 如果效果里没有内容，就不爬取了
            if effect_i_j.message == '':
                continue
            effect_type_name = effects.effect_names[effect_i_j.effect_type]
            all_messages.append((i, trigger_i.name, j, effect_type_name, effect_i_j.message))

    format_require = """【格式说明】
        1、文本正文内使用英文单引号或反斜杠需用[\\]转义，如【'He\\'s name. 方向为\\\\向'】
        2、文本正文内若想换行，需要用[\\r]代表换行符，如【'诸葛亮：\\r全军戒备！'】
        3、文件自带的引号、逗号、圆/方括号等架构不可随意破坏，以免出现不可预知的BUG.
        4、各项数据的含义如下。其中除了有注明可修改的数据项之外，其他内容都需用于导入时的校验."""

    print('正在把数据导出到文件……')
    # 将待导出列表打印到文件中。
    with open(txt_path, 'wt', encoding='utf-8') as extract_fd:
        print(f'{{"场景文件": "{read_file}"}}\n\n{format_require}\n\n', file=extract_fd)
        # 写入触发描述
        print("[序号, (触发ID, '触发名称', 是否显示在任务栏(可修改), '详细描述(可修改)', 是否显示在屏幕(可修改), '简短描述(可修改)')]", file=extract_fd)
        print('【触发描述开始】', file=extract_fd)
        for (x, tuple_x) in enumerate(all_descriptions):
            print(f"[{x}, {tuple_x}]", file=extract_fd)
        print(f'【触发描述结束】\n共导出 {len(all_descriptions)} 条触发描述数据。\n\n', file=extract_fd)

        # 写入效果文本
        print("[序号, (触发ID, '触发名称', 效果ID, '效果名称', '文本(可修改)')]", file=extract_fd)
        print('【效果文本开始】', file=extract_fd)
        for (x, tuple_x) in enumerate(all_messages):
            print(f"[{x}, {tuple_x}]", file=extract_fd)
        print(f'【效果文本结束】\n共导出 {len(all_messages)} 条效果文本数据。', file=extract_fd)

        print(f'导出完成！共导出 {len(all_descriptions)} 条触发描述数据、{len(all_messages)} 条效果文本数据。')
        return f'导出 {len(all_descriptions)} 条触发描述数据。\n导出 {len(all_messages)} 条效果文本数据。'


def import_all_text(TM, txt_path):
    """
    打开文本文件，分析其中的触发&效果&文本数据，将新的文本数据更新到给定的触发管理器里。
    :param TM: TriggersObject，一般传入你的 trigger_manager 即可
    :param txt_path: 要分析的文本文件（完整路径）
    :return: None
    """
    # 打开文本文件，提取所有行储存起来。
    success_message = ""
    try:
        with open(txt_path, 'rt', encoding='utf-8') as fd:
            all_lines = fd.readlines()
    except OSError as reason:
        print(f"错误：文件读取失败，原因：{reason}")
        return

    # 获取正文首尾行号。
    try:
        dscription_start_index = all_lines.index('【触发描述开始】\n') + 1
        dscription_end_index = all_lines.index('【触发描述结束】\n')
        message_start_index = all_lines.index('【效果文本开始】\n') + 1
        message_end_index = all_lines.index('【效果文本结束】\n')
    except ValueError:
        raise ValueError("错误：文件中缺失【效果文本开始】/【效果文本结束】/【触发描述开始】/【触发描述结束】的单行标记，无法分析")
        return

    format_require = """[格式要求]：
        1、文本正文内使用英文单引号或反斜杠需用[\\]转义，如【'He\\'s name. 方向为\\\\向'】
        2、文本正文内若想换行，需要用[\\r]代表换行符，如【'诸葛亮：\\r全军戒备！'】
        3、文件自带的引号、逗号、圆/方括号等架构不可随意破坏，以免出现不可预知的BUG."""

    def analyze_lines(start_index, end_index):
        """分析各行内容，将行号在两个_index之间的正文数据整理到列表输出。"""
        to_list = []
        for (index, data) in enumerate(all_lines[start_index: end_index]):
            # 该则数据对应在文件中的行号
            line_index = index + start_index + 1
            assert data != '\n', f"错误：文件第{line_index}行处，缺了一行."
            assert '[' in data and ']' in data, f"错误：文件第{line_index}行处，缺少序号/方括号/圆括号等架构，无法拆解该行内容."
            try:
                line_turn_list = eval(data)
                data_firstnum = line_turn_list[0]
                data_tuple = line_turn_list[1]
                assert index == data_firstnum, f"错误：文件第{line_index}行处，数据序号与程序设想的序号不符."
                to_list.append(data_tuple)
            except Exception:
                raise ValueError(f"错误：文件第{line_index}行处，有无法识别的错误.")
                print(format_require)
                return
        return to_list

    all_descriptions = analyze_lines(dscription_start_index, dscription_end_index)
    all_messages = analyze_lines(message_start_index, message_end_index)

    # 用数据里的新文本 替换 触发描述里的旧文本。
    tuple_index = -1
    for (tuple_index, tuple_x) in enumerate(all_descriptions):
        # 该则数据对应在文件中的行号
        line_index = tuple_index + message_start_index + 1
        # tuple_x[0]    tuple_x[1]    tuple_x[2]        tuple_x[3]    tuple_x[4]        tuple_x[4]
        # 触发ID        触发名称      是否显示在任务栏  详细描述      是否显示在屏幕    简短描述
        assert len(tuple_x) == 6, f"错误：文件第{line_index}行处，该行数据项数不足或多余."

        # 获取数据中触发ID对应的触发对象
        trigger_i = TM.get_trigger(TS.index(tuple_x[0]))
        assert tuple_x[1] == trigger_i.name, f"错误：文件第{line_index}行处，触发名称与场景中的触发名称不符，也可能是触发ID错位导致的."

        # 修改详细描述和简短描述
        if tuple_x[2] == 1:
            assert type(tuple_x[3]) == str, f"错误：文件第{line_index}行处，详细描述缺少单引号，不是字符串型."
            trigger_i.description = tuple_x[3]
        if tuple_x[4] == 1:
            assert type(tuple_x[5]) == str, f"错误：文件第{line_index}行处，简短描述缺少单引号，不是字符串型."
            trigger_i.short_description = tuple_x[5]
    print(f"成功导入 {tuple_index + 1} 个触发的描述")
    success_message += f"成功导入 {tuple_index + 1} 个触发的描述" + '\n'

    tuple_index = -1
    # 用数据里的新文本 替换 触发效果里的旧文本。
    for (tuple_index, tuple_x) in enumerate(all_messages):
        # 该则数据对应在文件中的行号
        line_index = tuple_index + message_start_index + 1
        # tuple_x[0]    tuple_x[1]    tuple_x[2]    tuple_x[3]    tuple_x[4]
        # 触发ID        触发名称      效果ID        效果名称      文本
        assert len(tuple_x) == 5, f"错误：文件第{line_index}行处，该行数据项数不足或多余."

        # 获取数据中触发ID对应的触发对象
        trigger_i = TM.get_trigger(TS.index(tuple_x[0]))
        assert tuple_x[1] == trigger_i.name, f"错误：文件第{line_index}行处，触发名称与场景中的触发名称不符，也可能是触发ID错位导致的."

        # 获取数据中效果ID对应的效果对象
        effect_i_j = trigger_i.get_effect(effect_index=tuple_x[2])
        effect_type_name = effects.effect_names[effect_i_j.effect_type]
        assert tuple_x[3] == effect_type_name, f"错误：文件第{line_index}行处，效果名称与场景中的效果名称不符，也可能是效果ID错位导致的."
        assert type(tuple_x[4]) == str, f"错误：文件第{line_index}行处，文本缺少单引号，不是字符串型.\n{format_require}"

        # 修改该效果的文本为数据中的文本
        effect_i_j.message = tuple_x[4]
    print(f"成功导入 {tuple_index + 1} 个效果的文本")
    success_message += f"成功导入 {tuple_index + 1} 个效果的文本"
    return success_message