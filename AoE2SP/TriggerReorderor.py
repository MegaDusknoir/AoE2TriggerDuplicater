
from typing import Any, Union
import copy
from AoE2ScenarioParser.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.helper import helper
from AoE2ScenarioParser.datasets.conditions import Condition
from AoE2ScenarioParser.datasets import effects
from AoE2ScenarioParser.datasets.players import Player
from AoE2ScenarioParser.datasets.units import Unit
from AoE2ScenarioParser.objects.triggers_obj import *
TS = TriggerSelect  # 使 TS 等效于 TriggerSelect

# region
def reorder_by_id(trigr_obj, reorder_effects=True, reorder_conditions=True):
    """
    Modify the display IDs of [triggers in whole scenario]/[effects&conditions in a trigger].(display ID <= execute ID)
    So as to let their display order be consistent with the order of execution.
    修改 场景下各触发 或 触发下各效果和条件 的显示ID。（显示ID←执行ID）
    以此使它们的显示顺序与执行顺序一致。

    :param trigr_obj: The object which contains triggers / effects&conditions to reorder. Accept TriggersObject, TriggerObject or TriggerSelect.
                      含有所要重排的触发/效果&条件的对象。可以是触发管理器(TriggersObject)、触发对象(TriggerObject)或触发选择器(TriggerSelect)
    :param reorder_effects: Whether to reorder effects in the trigger(s) or not.
                      是否重排触发下的效果。
    :param reorder_conditions: Whether to reorder conditions in the trigger(s) or not.
                      是否重排触发下的条件。
    :return: None
    """
    def reorder_eff_cond(trigger):
        if reorder_effects:
            trigger.effect_order.sort()
        if reorder_conditions:
            trigger.condition_order.sort()

    if type(trigr_obj) == TriggersObject:
        trigr_obj.trigger_display_order.sort()
        # Reorder effects or conditions of every trigger (added an <if> for performance)
        # 重排每个触发下的条件和效果（处于性能考虑添加了一个if结构）
        if reorder_effects or reorder_conditions:
            for each_trigger in trigr_obj.triggers:
                reorder_eff_cond(each_trigger)
    elif type(trigr_obj) == TriggerObject or type(trigr_obj) == TriggerSelect:
        reorder_eff_cond(trigr_obj)
    else:
        raise TypeError("参数 <trigr_obj> 应为 TriggersObject, TriggerObject 或 TriggerSelect 对象。")


def reorder_by_display(tm_to_ts):
    """
    按显示ID重排 场景下各触发 或 触发下各效果 的执行ID。
    重整全部触发的执行顺序，或某个触发内各效果的执行顺序，使执行顺序与显示顺序一致（执行ID←显示ID）。
    :param tm_to_ts: 要重整的对象。可以是触发管理器(TriggersObject)、触发对象(TriggerObject)或触发选择器(TriggerSelect)
    :return: tuple (旧执行ID→新执行ID的字典映射, 执行ID上浮了的“危险触发”的列表（触发名称，旧执行ID，新执行ID）)【Todo#1】
    """
    # 深拷贝用于引用
    tm_temp = copy.deepcopy(tm_to_ts)
    # 旧执行ID→新执行ID的字典映射
    old2new = {}
    # 执行ID上浮了的“危险触发”的列表，储存元组：(触发名称，旧执行ID，新执行ID)
    inversed_triggers = []
    if type(tm_to_ts) == TriggersObject:
        for (display_id, trigger_id) in enumerate(tm_to_ts.trigger_display_order):
            # 如果ID即将上浮，就要把这个触发和效果记录下来（用于告知用户这个触发组可能会因顺序颠倒而出问题）
            if display_id < trigger_id:
                inversing_trigger = tm_to_ts.triggers[display_id]
                inversed_triggers.append((inversing_trigger.name, trigger_id, display_id))
            # 原份中第[显示ID(1,2,0...)]个触发 重定义为 深拷贝中第[执行ID(0,1,2...)]个触发（执行ID为旧，显示ID为新）
            tm_to_ts.triggers[display_id] = tm_temp.triggers[trigger_id]
            # 字典[新ID] = 旧ID
            old2new[tm_to_ts.triggers[display_id].trigger_id] = display_id
            # 这个触发的ID属性也要改
            tm_to_ts.triggers[display_id].trigger_id = display_id
        # 正序排列双ID对照表
        tm_to_ts.trigger_display_order.sort()
        # 正向排序“危险触发”列表（依据新执行ID(亦即显示顺序)）【Todo#1】
        # inversed_triggers.【Todo#1】
        # 重定向激活/关闭触发的效果里的触发执行ID
        for trigger in tm_to_ts.triggers:
            # 逐个遍历触发→逐个遍历效果→若效果的trigger_id有效，则更改为该 旧ID 在字典映射中所对应的 新ID。
            for effect in trigger.effects:
                if effect.trigger_id > 0:
                    effect.trigger_id = old2new[effect.trigger_id]

    elif type(tm_to_ts) == TriggerObject or TriggerSelect:
        for (display_id, effect_id) in enumerate(tm_to_ts.effect_order):
            # 第[显示ID]个效果重定义为第[执行ID]个效果。
            tm_to_ts.effects[display_id] = tm_temp.effects[effect_id]
            old2new[tm_to_ts.triggers[display_id].effect_id] = effect_id
            tm_to_ts.effects[display_id].effect_id = effect_id
        # 正序排列双ID对照表
        tm_to_ts.effect_order.sort()
    else:
        raise TypeError("输入参数需为TriggersObject、TriggerObject或TriggerSelect对象.")
    return (old2new, inversed_triggers)
# endregion
