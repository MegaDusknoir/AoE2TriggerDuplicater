import os
import tkinter as tk
import tkinter.ttk
import tkinter.messagebox
import base64
import copy
from typing import List
from aoespicon import img
from AoE2ScenarioParser.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.datasets.conditions import Condition
from AoE2ScenarioParser.datasets.effects import Effect
from AoE2ScenarioParser.datasets.players import Player
from AoE2ScenarioParser.datasets.units import Unit
from AoE2ScenarioParser.objects.triggers_obj import *
from TextExporter import extract_all_text
from TextExporter import import_all_text
from TriggerReorderor import reorder_by_id
from TriggerReorderor import reorder_by_display
from UnitsListCreate import get_unit_as_string
from UnitsListCreate import get_single_unit
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

global scenario
global trigger_manager
global unit_manager
global tid
global uid
global openfile
global duplicate_config_string
global duplicate_config

class DuplicateConfig:
	def __init__(self,
					text_config: List[List[str]],
					location_config: List[List[List[int]]],
					object_config: List[List[int]]
					):

		self.text_config = text_config
		self.location_config = location_config
		self.object_config = object_config

openfile = ""
duplicate_config = DuplicateConfig([],[],[])
duplicate_config_string = """【方括号标头 + 8 个坐标，若匹配首个坐标，会被复制成其他 7 个坐标】
0,0
0,0
0,0
0,0
0,0
0,0
0,0
0,0
【方括号标头 + 字符串，若匹配到首个字符串，会被复制成其他 7 个字符串】
<BLUE>
<RED>
<GREEN>
<YELLOW>
<AQUA>
<PURPLE>
<GREY>
<ORANGE>
【方括号标头 + ID + 标记，若匹配到首个单位，会被复制成其他 7 个单位】
1000 - Unit
1000 - Unit
1000 - Unit
1000 - Unit
1000 - Unit
1000 - Unit
1000 - Unit
1000 - Unit
"""
current_index = 0

def open_scen():
	global scenario
	global trigger_manager
	global openfile

	# 选择场景
	open_success = False
	while open_success == False:
		openfile_t = askopenfilename(title='选择 AoE2 DE 场景文件', filetypes=[('决定版场景', '*.aoe2scenario'), ('所有文件', '*')])
		if openfile_t.strip() == "" and openfile.strip() != "":
			# 未选择文件，非首次打开 => 放弃操作
			return 0
		else:
			openfile = openfile_t
		if openfile.strip() == "":
			# 未选择文件，首次打开 => 新建场景
			openfile = '临时/default0.aoe2scenario'
			scenario_folder = '临时/'
			input_file = 'default0'
			scenario = AoE2Scenario.create_default()
			break
		# 分析场景路径
		scenario_folder, input_file = os.path.split(openfile)
		scenario_folder += "/"
		input_file, fileext = os.path.splitext(input_file)
		if fileext == "":
			fileext = ".aoe2scenario"
		try:
			scenario = AoE2Scenario.from_file(scenario_folder + input_file + fileext)
			open_success = True
		except Exception as reason:
			if len(reason.args) != 0:
				if reason.args[0] == 'Currently unsupported version. Please read the message above. Thank you.':
					reason = '场景文件格式过旧，请使用游戏编辑器重新保存场景。\n\n——亦或场景文件格式版本过新，请检查当前工具的版本。'
			tk.messagebox.showerror(title='打开失败', message=f'无法读取场景，原因：\n{reason}')
			open_success = False
		except:
			tk.messagebox.showerror(title='打开失败', message=f'无法读取场景，原因：\n未知原因。')
			open_success = False
	
	window.title(window_title + ' - [' + input_file + '.aoe2scenario]')
	trigger_manager = scenario.trigger_manager
	trigger_relist()
	get_units_list()
	
	return 0;

def trigger_relist():
	global trigger_manager
	global current_index
	if current_index == 0 or current_index == 1:
		# 拉取触发列表
		t_Duplicater.config(state='normal')
		t_Duplicater.delete(1.0,tk.END)
		t_Duplicater.insert(tk.END, '< 触发及变量列表 >\n' + trigger_manager.get_summary_as_string())
		t_Duplicater.config(state='disabled')
	
		t_Exporter.config(state='normal')
		t_Exporter.delete(1.0,tk.END)
		t_Exporter.insert(tk.END, t_Duplicater.get('0.0','end'))
		t_Exporter.config(state='disabled')

# 保存场景
def save_scen():
	global scenario
	global openfile
	if openfile == '临时/default0.aoe2scenario':
		openfile_t = saveas_scen()
		# 分析场景路径
		if openfile_t.strip() == "":
			return
		openfile = openfile_t
		scenario_folder, input_file = os.path.split(openfile)
		window.title(window_title + ' - [' + input_file + ']')
		return
	savefile = openfile
	scenario.write_to_file(savefile)

# 另存为场景
def saveas_scen():
	global scenario
	savefile = asksaveasfilename(title='保存 AoE2 DE 场景文件', filetypes=[('决定版场景', '*.aoe2scenario')])
	if savefile.strip() != "":
		savefilename,savefileext = os.path.splitext(savefile)
		if savefileext.strip() == "":
			savefile += ".aoe2scenario"
		scenario.write_to_file(savefile)
	else:
		print("\n"
			  "未选择文件，操作取消。\n")
	return savefile

# 另存为场景（快捷键）
def saveas_scen_handle(event):
	saveas_scen()
	
def copy_trigger_per_player_fix(trigger_obj: TriggersObject,
								from_player,
								trigger_select,
								change_from_player_only=False,
								include_player_source=True,
								include_player_target=False,
								trigger_ce_lock=None,
								exclude_self=False,
								include_gaia: bool = False,
								create_copy_for_players: List[IntEnum] = None) -> Dict[Player, TriggerObject]:
	"""
	Copies a trigger for all or a selection of players. Every copy will change desired player attributes with it.

	Args:
		from_player (IntEnum): The central player this trigger is created for. This is the player that will not get
			a copy.
		trigger_select (TriggerSelect): An object used to identify which trigger to select.
		change_from_player_only (bool): If set to True, only change player attributes in effects and conditions that
			are equal to the player defined using the `from_player` parameter.
		include_player_source (bool): If set to True, allow player source attributes to be changed while copying.
			Player source attributes are attributes where a player is defined to perform an action such as create an
			object. If set to False these attributes will remain unchanged.
		include_player_target (bool): If set to True, allow player target attributes to be changed while copying.
			Player target attributes are attributes where a player is defined as the target such as change ownership
			or sending resources. If set to False these attributes will remain unchanged.
		trigger_ce_lock (TriggerCELock): The TriggerCELock object. Used to lock certain (types) of conditions or
			effects from being changed while copying.
		include_gaia (bool): If True, GAIA is included in the copied list. (Also when `create_copy_for_players` is
			defined)
		create_copy_for_players (List[IntEnum]): A list of Players to create a copy for. The `from_player` will be
			excluded from this list.

		exclude_self: If target trigger has a 1 -> 7 or 7 -> 1 effect group, set this to duplicate effects for
			7 players excluding from_player.

	Returns:
		A dict with all the new created triggers. The key is the player for which the trigger is
			created using the IntEnum associated with it. Example:
			{Player.TWO: TriggerObject, Player.FIVE: TriggerObject}

	Raises:
		ValueError: if more than one trigger selection is used. Any of (trigger_index, display_index or trigger)
			Or if Both `include_player_source` and `include_player_target` are `False`

	:Authors:
		KSneijders

	"""
	trigger_index, display_index, trigger = trigger_obj._validate_and_retrieve_trigger_info(trigger_select)
	if not include_player_source and not include_player_target:
		raise ValueError("Cannot exclude player source and target.")

	if create_copy_for_players is None:
		create_copy_for_players = [
			Player.ONE, Player.TWO, Player.THREE, Player.FOUR,
			Player.FIVE, Player.SIX, Player.SEVEN, Player.EIGHT
		]
	if include_gaia and Player.GAIA not in create_copy_for_players:
		create_copy_for_players.append(Player.GAIA)

	alter_conditions, alter_effects = TriggersObject._find_alterable_ce(trigger, trigger_ce_lock)

	return_dict: Dict[Player, TriggerObject] = {}
	for player in create_copy_for_players:
		if not player == from_player:
			new_trigger = trigger_obj.copy_trigger(TS.trigger(trigger))
			# 移除库函数添加的(copy)后缀
			if new_trigger.name.endswith(" (copy)"):
				new_trigger.name = new_trigger.name[:-7]
			new_trigger.name += f" (p{player})"
			return_dict[player] = new_trigger

			# 条件遍历
			for cond_x in alter_conditions:
				cond = new_trigger.conditions[cond_x]
				# 起始单位
				for object in duplicate_config.object_config:
					if object[1] == cond.unit_object:
						cond.unit_object = object[player]
				# 目标单位
				for object in duplicate_config.object_config:
					if object[1] == cond.next_object:
						cond.next_object = object[player]
				# 目标区域坐标 1
				for location in duplicate_config.location_config:
					if location[1][0] == cond.area_1_x and location[1][1] == cond.area_1_y:
						cond.area_1_x = location[player][0]
						cond.area_1_y = location[player][1]
				# 目标区域坐标 2
				for location in duplicate_config.location_config:
					if location[1][0] == cond.area_2_x and location[1][1] == cond.area_2_y:
						cond.area_2_x = location[player][0]
						cond.area_2_y = location[player][1]
				# 坐标顺序校正
				if cond.area_1_x > cond.area_2_x:
					cond.area_1_x, cond.area_2_x = cond.area_2_x, cond.area_1_x
				if cond.area_1_y > cond.area_2_y:
					cond.area_1_y, cond.area_2_y = cond.area_2_y, cond.area_1_y
				# 跳过无玩家条件
				if cond.source_player == -1:
					continue
				# 跳过非起始玩家条件
				if change_from_player_only:
					if not cond.source_player == from_player:
						continue
				# 改变起始玩家
				if include_player_source:
					cond.source_player = Player(player)
				# 改变目标玩家
				if include_player_target:
					cond.target_player = Player(player)

			# 效果遍历
			for effect_x in alter_effects:
				effect = new_trigger.effects[effect_x]
				# 效果文本
				for text in duplicate_config.text_config:
					if effect.message.find(text[1]) > 0:
						effect.message = effect.message.replace(text[1], text[player])
				# 目标区域坐标 1
				for location in duplicate_config.location_config:
					if location[1][0] == effect.area_1_x and location[1][1] == effect.area_1_y:
						effect.area_1_x = location[player][0]
						effect.area_1_y = location[player][1]
				# 目标区域坐标 2
				for location in duplicate_config.location_config:
					if location[1][0] == effect.area_2_x and location[1][1] == effect.area_2_y:
						effect.area_2_x = location[player][0]
						effect.area_2_y = location[player][1]
				# 坐标顺序校正
				if effect.area_1_x > effect.area_2_x:
					effect.area_1_x, effect.area_2_x = effect.area_2_x, effect.area_1_x
				if effect.area_1_y > effect.area_2_y:
					effect.area_1_y, effect.area_2_y = effect.area_2_y, effect.area_1_y
				# 目标点坐标
				for location in duplicate_config.location_config:
					if location[1][0] == effect.location_x and location[1][1] == effect.location_y:
						effect.location_x = location[player][0]
						effect.location_y = location[player][1]
				# 选择单位
				for object in duplicate_config.object_config:
					for (object_enum, object_id) in enumerate(effect.selected_object_ids):
						if object[1] == object_id:
							effect.selected_object_ids[object_enum] = object[player]
				# 目标点单位
				for object in duplicate_config.object_config:
					if object[1] == effect.location_object_reference:
						effect.location_object_reference = object[player]
				# 一对多/多对一型效果
				if exclude_self and effect.source_player == from_player and effect.target_player == Player(player):
					effect.source_player = Player(player)
					effect.target_player = from_player
					continue
				if exclude_self and effect.target_player == from_player and effect.source_player == Player(player):
					effect.source_player = from_player
					effect.target_player = Player(player)
					continue
				if exclude_self and effect.source_player == Player(player):
					effect.source_player = from_player
					continue
				if exclude_self and effect.target_player == Player(player):
					effect.target_player = from_player
					continue
				# 跳过无玩家效果
				if effect.source_player == -1:
					continue
				# 跳过非起始玩家效果
				if change_from_player_only:
					if not (
						(include_player_source and effect.source_player == from_player)
						or (include_player_target and effect.target_player == from_player)
						):
						continue
				# 改变起始玩家
				if include_player_source:
					effect.source_player = Player(player)
				# 改变目标玩家
				if include_player_target:
					effect.target_player = Player(player)

	return return_dict

# 触发多人复制
def duplicate():
	global trigger_manager
	global tid
	try:
		idtmp = int(tid.get())
	except:
		tk.messagebox.showerror(title='参数不正确', message='参数输入错误，无法识别为整数。')
		print("\n"
		"参数输入错误，无法识别为整数。\n")
		tid.set("")
		return
	try:
		copied_triggers = copy_trigger_per_player_fix(
		trigger_obj = trigger_manager,
		from_player = 1,
		change_from_player_only = frm_plyr_only.get(),
		include_player_source = src_plyr.get(),
		include_player_target = tgt_plyr.get(),
		exclude_self = self_exclude.get(),
		trigger_select = TriggerSelect.display(idtmp),
		create_copy_for_players = [1,2,3,4,5,6,7,8]
		)
		sel_dis = idtmp
		for i in range (1,9):
			if i != Player.ONE:
				print(f"\n => 触发 {trigger_manager.trigger_display_order[idtmp]} (p{i}) 已复制")
		for i in range (8,1,-1):
			new_dis_id = trigger_manager.trigger_display_order.pop()
			trigger_manager.trigger_display_order.insert(sel_dis + 1, new_dis_id)
		if reo_auto.get() == 1:
			reorder_by_display(trigger_manager)
		trigger_relist()
		t_Duplicater.see(f'{sel_dis + 22}.0')
		if (ignore_success.get() == False):
			tk.messagebox.showinfo(title='提示', message='复制完成。')
		print("\n")
	except:
		tk.messagebox.showerror(title='触发 ID 不正确', message='触发不存在。')
		print("\n"
		"触发不存在。\n")
		return
	#tid.set("")
	tid.set(f'{idtmp + 8}')

# 删除并防止触发树紊乱
def remove_safe(trigger_select: TriggerSelect) -> None:
	global trigger_manager
	tri_id, dis_id_t, trigger_t = trigger_manager._validate_and_retrieve_trigger_info(trigger_select)
	removed_triggers = trigger_manager.remove_trigger(trigger_select)
	for trigger in trigger_manager.triggers:
		for effect in trigger.effects:
			if effect.trigger_id == tri_id:
				effect.trigger_id = -1
			elif effect.trigger_id > tri_id:
				effect.trigger_id = effect.trigger_id - 1

# 触发多人删除
def multi_remove():
	global trigger_manager
	global tid
	try:
		distmp = int(tid.get())
	except:
		tk.messagebox.showerror(title='参数不正确', message='参数输入错误，无法识别为整数。')
		print("\n"
		"参数输入错误，无法识别为整数。\n")
		tid.set("")
		return
	if distmp + 8 > len(trigger_manager.trigger_display_order):
		tk.messagebox.showerror(title='触发 ID 不正确', message='可供删除的剩余触发过少。')
		return
	for i in range (2,9):
		removed_triggers = remove_safe(trigger_select = TriggerSelect.display(distmp + 1))
	if reo_auto.get() == 1:
		reorder_by_display(trigger_manager)
	trigger_relist()
	t_Duplicater.see(f'{distmp + 22}.0')
	if (ignore_success.get() == False):
		tk.messagebox.showinfo(title='提示', message='删除完成。')
	tid.set(f'{distmp + 1}')
	
# 触发批量移动
def trigger_move(begin = 0, end = 0, tgt = 0):
	global trigger_manager
	for i in range (begin, end + 1):
		crt_dis_id = trigger_manager.trigger_display_order.pop(i)
		trigger_manager.trigger_display_order.insert(tgt + i - begin, crt_dis_id)

# 触发批量移动处理
def trigger_move_handle():
	global trigger_manager
	global dis_begin
	global dis_end
	global dis_tgt
	try:
		begin = int(dis_begin.get())
		end = int(dis_end.get())
		tgt = int(dis_tgt.get())
	except:
		tk.messagebox.showerror(title='参数不正确', message='参数输入错误，无法识别为整数。')
		print("\n"
		"参数输入错误，无法识别为整数。\n")
		return
	# 选定范围检查
	if begin > end:
		begin, end = end, begin
	if end >= len(trigger_manager.trigger_display_order):
		tk.messagebox.showerror(title='触发 ID 不正确', message='无效的触发范围。')
		return
	# 目标位置检查
	if tgt >= begin and tgt <= end + 1 or tgt > len(trigger_manager.trigger_display_order):
		tk.messagebox.showerror(title='触发 ID 不正确', message='无效的目标位置。')
		return
	if tgt > end + 1:
		t_begin = end + 1
		t_end = tgt - 1
		t_tgt = begin
		trigger_move(t_begin, t_end, t_tgt)
	else:
		trigger_move(begin, end, tgt)
	if reo_auto.get() == 1:
		reorder_by_display(trigger_manager)
	trigger_relist()
	t_Duplicater.see(f'{tgt + 22}.0')
	if (ignore_success.get() == False):
		tk.messagebox.showinfo(title='提示', message='已完成移动。')

# 触发重排序
def reorder():
	global trigger_manager
	reorder_by_display(trigger_manager)
	trigger_relist()
	if (ignore_success.get() == False):
		tk.messagebox.showinfo(title='提示', message='重排序完成。')

# 主窗体
window_title = 'Trigger Duplicater'
window_title_suffix = 'Powered by AoE2SP'
icotmp = open("_tmp.ico","wb+")
icotmp.write(base64.b64decode(img))
icotmp.close()
window = tk.Tk()
window.title(window_title + ' - ' + window_title_suffix)
window.iconbitmap("_tmp.ico")
window.geometry('1200x600')
window.resizable(width=False, height=False)
os.remove("_tmp.ico")

# 选项卡
notebook = tkinter.ttk.Notebook(window)
f_Duplicater = tkinter.Frame()
f_Exporter = tkinter.Frame()
f_Units = tkinter.Frame()

# 选框
ignore_success = tk.IntVar()
ignore_success.set(False)

# 选项卡 0 - 触发复制
# region

def dup_switch_handle():
	global b_dup
	if dup_switch.get() == True:
		b_dup = tk.Button(f_Duplicater, text=f'向下删除 7 条', width=14, height=1, command=multi_remove)
		b_dup.place(x=340, y=10)
	else:
		b_dup = tk.Button(f_Duplicater, text='复制到所有玩家', width=14, height=1, command=duplicate)
		b_dup.place(x=340, y=10)
		
def player_check():
	if src_plyr.get() == False and tgt_plyr.get() == False:
		tk.messagebox.showerror(title='参数不允许', message='必须转换起始玩家或目标玩家中的一个以上。')
		src_plyr.set(True)
				
def trigger_detail_handle():
	global tid
	global trigger_manager
	try:
		trigger_id = int(tid.get())
	except:
		tk.messagebox.showerror(title='参数不正确', message='参数输入错误，无法识别为整数。')
		print("\n"
		"参数输入错误，无法识别为整数。\n")
		tid.set("")
		return
	try:
		trigger_detail = trigger_manager.get_trigger_as_string(trigger_select = TriggerSelect.display(trigger_id))
	except:
		tk.messagebox.showerror(title='触发 ID 不正确', message='触发不存在。')
		tid.set("")
		return
	w_trigger_detail=tk.Toplevel(master=window)
	w_trigger_detail.title(f'触发 {trigger_id}')
	icotmp = open("_tmp.ico","wb+")
	icotmp.write(base64.b64decode(img))
	icotmp.close()
	w_trigger_detail.iconbitmap("_tmp.ico")
	w_trigger_detail.geometry('640x480')
	w_trigger_detail.resizable(width=False, height=False)
	os.remove("_tmp.ico")

	t_TriggerDetail = tk.scrolledtext.ScrolledText(w_trigger_detail, width=80, height=32)
	t_TriggerDetail.pack()
	t_TriggerDetail.delete(1.0,tk.END)
	t_TriggerDetail.insert(tk.END, trigger_detail)
	t_TriggerDetail.config(state='disabled')
	
	def trigger_detail_close_handle():
		w_trigger_detail.quit()
		w_trigger_detail.destroy()

	b_commit = tk.Button(w_trigger_detail, text='关闭', width=18, height=1, command=trigger_detail_close_handle)
	b_commit.pack(anchor = 's')
	
	w_trigger_detail.grab_set()
	w_trigger_detail.mainloop()

# Todo			
def trigger_multiple_add_handle():
	global tid
	global trigger_manager
	try:
		trigger_id = int(tid.get())
	except:
		tk.messagebox.showerror(title='参数不正确', message='参数输入错误，无法识别为整数。')
		print("\n"
		"参数输入错误，无法识别为整数。\n")
		tid.set("")
		return
	trigger_detail = trigger_manager.get_trigger_as_string(trigger_select = TriggerSelect.display(trigger_id))

	w_trigger_multiple_add=tk.Toplevel(master=window)
	w_trigger_multiple_add.title(f'触发批量生成')
	icotmp = open("_tmp.ico","wb+")
	icotmp.write(base64.b64decode(img))
	icotmp.close()
	w_trigger_multiple_add.iconbitmap("_tmp.ico")
	w_trigger_multiple_add.geometry('640x480')
	w_trigger_multiple_add.resizable(width=False, height=False)
	os.remove("_tmp.ico")

	t_TriggerAdd = tk.scrolledtext.ScrolledText(w_trigger_multiple_add, width=80, height=32)
	t_TriggerAdd.pack()
	t_TriggerAdd.delete(1.0,tk.END)
	t_TriggerAdd.insert(tk.END, trigger_detail)
	
	def trigger_multiple_add_commit_handle():
		w_trigger_multiple_add.quit()
		w_trigger_multiple_add.destroy()

	b_commit = tk.Button(w_trigger_multiple_add, text='提交', width=18, height=1, command=trigger_multiple_add_commit_handle)
	b_commit.pack(anchor = 's')
	
	w_trigger_multiple_add.grab_set()
	w_trigger_multiple_add.mainloop()

def duplicate_config_handle():
	global duplicate_config_string
	global duplicate_config
	w_dup_cfg=tk.Toplevel(master=window)
	w_dup_cfg.title(f'配置复杂复制')
	icotmp = open("_tmp.ico","wb+")
	icotmp.write(base64.b64decode(img))
	icotmp.close()
	w_dup_cfg.iconbitmap("_tmp.ico")
	w_dup_cfg.geometry('640x480')
	w_dup_cfg.resizable(width=False, height=False)
	os.remove("_tmp.ico")

	t_Configedit = tk.scrolledtext.ScrolledText(w_dup_cfg, width=50, height=28)
	t_Configedit.pack()
	
	def config_commit_handle():
		global duplicate_config_string
		config_string = t_Configedit.get(1.0,tk.END)
		duplicate_config.text_config.clear()
		duplicate_config.location_config.clear()
		duplicate_config.object_config.clear()
		while True:
			try:
				# 先分割映射组
				config_group = config_string.split('【')
				for config_member in config_group:
					if config_member.strip() != "":
						# 每个组按换行符分为八项及标头
						config_list = config_member.split('\n')
						config_list[0] = '【' + config_list[0]
						map_type = 0x01 + 0x02
						# 坐标映射校验
						for i in range (1,9):
							if config_list[i].count(',') != 1:
								map_type &= ~0x01
								break
						# 单位映射校验
						if not map_type & 0x01:
							for i in range (1,9):
								if config_list[i].count('- Unit') != 1:
									map_type &= ~0x02
									break
						# 判定坐标映射
						if map_type & 0x01:
							config_line_int = []
							config_line_int.append(config_list[0])
							for line in range(1,9):
								config_line_int.append(list(map(int,config_list[line].split(','))))
							duplicate_config.location_config.append(config_line_int)
						# 判定单位映射
						elif map_type & 0x02:
							config_line_int = []
							config_line_int.append(config_list[0])
							for line in range(1,9):
								config_line_int.append(int("".join(filter(str.isdigit, config_list[line]))))
							duplicate_config.object_config.append(config_line_int)
						# 其余判定为文本映射
						else:
							while len(config_list) > 9:
								config_list.pop()
							duplicate_config.text_config.append(config_list)
				break
			except:
				result = tk.messagebox.askokcancel(title='提交失败', message='格式可能不正确，是否放弃编辑？', parent=w_dup_cfg)
				if result == True:
					w_dup_cfg.quit()
					w_dup_cfg.destroy()
				return
		duplicate_config_string = ""
		for text in duplicate_config.text_config:
			for i in range(0,9):
				duplicate_config_string += text[i] + '\n'
		for location in duplicate_config.location_config:
			duplicate_config_string += location[0] + '\n'
			for i in range(1,9):
				duplicate_config_string += f'{location[i][0]},{location[i][1]}' + '\n'
		for object in duplicate_config.object_config:
			duplicate_config_string += object[0] + '\n'
			for i in range(1,9):
				duplicate_config_string += f'{object[i]} - Unit' + '\n'

		w_dup_cfg.quit()
		w_dup_cfg.destroy()

	b_commit = tk.Button(w_dup_cfg, text='提交配置', width=16, height=1, command=config_commit_handle)
	b_commit.place(x=200, y=400)

	def config_saveas_handle():
		tk.messagebox.showinfo(title='鸽了！', message='这个功能还没有做，还是直接动手复制来的快罢。', parent=w_dup_cfg)

	b_saveas = tk.Button(w_dup_cfg, text='另存为', width=16, height=1, command=config_saveas_handle)
	b_saveas.place(x=340, y=400)
	
	t_Configedit.delete(1.0,tk.END)
	t_Configedit.insert(tk.END, duplicate_config_string)
	w_dup_cfg.grab_set()
	w_dup_cfg.mainloop()

# 文本框
t_Duplicater = tk.scrolledtext.ScrolledText(f_Duplicater, width=140, height=36)
t_Duplicater.place(x=160, y=60)
t_Duplicater.config(state='disabled')

tid = tk.StringVar()
e = tk.Entry(f_Duplicater, textvariable = tid, width = 12)
e.place(x=215, y=14)

# 输入框
dis_begin = tk.StringVar()
e_dis_begin = tk.Entry(f_Duplicater, textvariable = dis_begin, width = 10)
e_dis_begin.place(x=730, y=5)
dis_end = tk.StringVar()
e_dis_end = tk.Entry(f_Duplicater, textvariable = dis_end, width = 10)
e_dis_end.place(x=830, y=5)
dis_tgt = tk.StringVar()
e_dis_tgt = tk.Entry(f_Duplicater, textvariable = dis_tgt, width = 10)
e_dis_tgt.place(x=730, y=30)

# 按钮
b_dup = tk.Button(f_Duplicater, text='复制到所有玩家', width=14, height=1, command=duplicate)
b_dup.place(x=340, y=10)

b_reo = tk.Button(f_Duplicater, text='以显示序重排ID (测试)', width=18, height=1, command=reorder)
b_reo.place(x=1020, y=10)

b_mov = tk.Button(f_Duplicater, text='以显示序移动', width=12, height=1, command=trigger_move_handle, font=('', 8))
b_mov.place(x=825, y=30)

b_chk = tk.Button(f_Duplicater, text='查看触发内容', width=14, height=1, command=trigger_detail_handle)
b_chk.place(x=20, y=10)

b_cfg = tk.Button(f_Duplicater, text='配置复杂复制', width=14, height=1, command=duplicate_config_handle)
b_cfg.place(x=20, y=60)

# 变量
reo_auto = tk.IntVar()
#frm_plyr = tk.IntVar()
frm_plyr_only = tk.IntVar()
src_plyr = tk.IntVar()
tgt_plyr = tk.IntVar()
self_exclude = tk.IntVar()
dup_switch =  tk.IntVar()
src_plyr.set(True)
dup_switch.set(False)
self_exclude.set(False)

# 选框
c_reo_auto = tk.Checkbutton(f_Duplicater, text='自动',variable=reo_auto, onvalue=1, offvalue=0)
c_reo_auto.place(x=960, y=12)
c_frm_plyr_only = tk.Checkbutton(f_Duplicater, text='仅限对应玩家',variable=frm_plyr_only, onvalue=1, offvalue=0)
c_frm_plyr_only.place(x=560, y=2)
c_src_plyr = tk.Checkbutton(f_Duplicater, text='转换起始玩家',variable=src_plyr, onvalue=1, offvalue=0, command=player_check)
c_src_plyr.place(x=460, y=2)
c_tgt_plyr = tk.Checkbutton(f_Duplicater, text='转换目标玩家',variable=tgt_plyr, onvalue=1, offvalue=0, command=player_check)
c_tgt_plyr.place(x=460, y=30)
c_dup_switch = tk.Checkbutton(f_Duplicater, variable=dup_switch, onvalue=1, offvalue=0, command=dup_switch_handle)
c_dup_switch.place(x=310, y=12)
c_exclude = tk.Checkbutton(f_Duplicater, text='一对七/七对一',variable=self_exclude, onvalue=1, offvalue=0)
c_exclude.place(x=560, y=30)
# c_exclude.config(state='disabled')


# 标识
l = tk.Label(f_Duplicater, text='显示序：')
l.place(x=160, y=14)

l2 = tk.Label(f_Duplicater, text='范围：')
l2.place(x=680, y=5)

l3 = tk.Label(f_Duplicater, text='~')
l3.place(x=810, y=5)

l4 = tk.Label(f_Duplicater, text='目标：')
l4.place(x=680, y=30)

# endregion 触发复制

# 选项卡 1 - 文本导出
# region

# 文本框
t_Exporter = tk.scrolledtext.ScrolledText(f_Exporter, width=140, height=36)
t_Exporter.place(x=100, y=60)
t_Exporter.config(state='disabled')

def export_handle():
	global trigger_manager
	savetext = asksaveasfilename(title='保存触发文本文件', filetypes=[('文本文档', '*.txt')])
	if savetext.strip() != "":
		savefilename,savefileext = os.path.splitext(savetext)
		if savefileext.strip() == "":
			savefilename += ".txt"
			savetext += ".txt"
		else:
			savefilename += savefileext
		success_message = extract_all_text(trigger_manager, savetext, openfile)
		if (ignore_success.get() == False):
			tk.messagebox.showinfo(title='导出成功', message= success_message)
	else:
		print("\n"
			  "未选择文件，操作取消。\n")

def import_handle():
	global trigger_manager
	opentext = askopenfilename(title='选择触发文本文件', filetypes=[('文本文档', '*.txt'), ('所有文件', '*')])
	if opentext.strip() == "":
		return -1;

	# 分析场景路径
	text_folder, input_file = os.path.split(opentext)
	text_folder += "/"
	input_file, fileext = os.path.splitext(input_file)
	
	try:
		success_message = import_all_text(trigger_manager, opentext)
	except AssertionError as reason:
		tk.messagebox.showerror(title='导入失败', message=f'无法导入文本，原因：\n{reason}')
		raise
		return
	except ValueError as reason:
		tk.messagebox.showerror(title='导入失败', message=f'无法导入文本，原因：\n{reason}')
		return
	except:
		tk.messagebox.showerror(title='导入失败', message=f'无法导入文本，原因：\n未知错误。')
		return
	if (ignore_success.get() == False):
		tk.messagebox.showinfo(title='导入成功', message= success_message)
	trigger_relist()
	
# 按钮
b_exp = tk.Button(f_Exporter, text='导出触发文本', width=18, height=1, command=export_handle)
b_exp.place(x=100, y=10)
b_imp = tk.Button(f_Exporter, text='导入触发文本', width=18, height=1, command=import_handle)
b_imp.place(x=300, y=10)

# endregion

# 选项卡 2 - 单位管理
# region

# 文本框
t_Units = tk.scrolledtext.ScrolledText(f_Units, width=140, height=36)
t_Units.place(x=100, y=60)
t_Units.config(state='disabled')

# 输入框
uid = tk.StringVar()
e_uid = tk.Entry(f_Units, textvariable = uid, width = 12)
e_uid.place(x=155, y=14)

def get_units_list():
	global unit_manager
	if current_index == 2:
		unit_manager = scenario.unit_manager
		t_Units.config(state='normal')
		t_Units.delete(1.0,tk.END)
		t_Units.insert(tk.END, get_unit_as_string(unit_manager))
		t_Units.config(state='disabled')
		
def edit_unit():
	global uid
	global unit_manager
	try:
		unit_id = int(uid.get())
	except:
		tk.messagebox.showerror(title='参数不正确', message='参数输入错误，无法识别为整数。')
		print("\n"
		"参数输入错误，无法识别为整数。\n")
		uid.set("")
		return
	unit_info, unit_to_edit = get_single_unit(unit_manager, unit_id)
	if unit_info == "":
		tk.messagebox.showerror(title='单位不存在', message='不存在 ID 对应的单位。')
		uid.set("")
		return
	w_unit_edit=tk.Toplevel(master=window)
	w_unit_edit.title(f'编辑单位 {unit_id}')
	icotmp = open("_tmp.ico","wb+")
	icotmp.write(base64.b64decode(img))
	icotmp.close()
	w_unit_edit.iconbitmap("_tmp.ico")
	w_unit_edit.geometry('300x200')
	w_unit_edit.resizable(width=False, height=False)
	os.remove("_tmp.ico")

	t_Unitedit = tk.scrolledtext.ScrolledText(w_unit_edit, width=30, height=11)
	t_Unitedit.pack()
	
	def unit_edit_commit_handle():
		unit_info = t_Unitedit.get(1.0,tk.END)
		while True:
			try:
				info_text, info_temp = unit_info.split("单位ID：", 1)
				arg_id, info_temp = info_temp.split("\n", 1)
				info_text, info_temp = info_temp.split("种类ID：", 1)
				arg_cns, info_temp = info_temp.split("\n", 1)
				info_text, info_temp = info_temp.split("属于：玩家 ", 1)
				arg_ply, info_temp = info_temp.split("\n", 1)
				info_text, info_temp = info_temp.split("位置：", 1)
				arg_loc, info_temp = info_temp.split("\n", 1)
				arg_loc_x, arg_loc_y, arg_loc_z = arg_loc.split(",")
				info_text, info_temp = info_temp.split("相位：", 1)
				arg_rot, info_temp = info_temp.split("/4 pi\n", 1)
				info_text, info_temp = info_temp.split("驻扎于：", 1)
				arg_gar, info_temp = info_temp.split("\n", 1)
				info_text, info_temp = info_temp.split("状态：", 1)
				arg_sts, info_temp = info_temp.split("\n", 1)
				info_text, arg_frm = info_temp.split("帧位：", 1)
				new_unit_id = int(arg_id)
				new_unit_const = int(arg_cns)
				new_unit_player = Player(int(arg_ply))
				new_unit_x = float(arg_loc_x)
				new_unit_y = float(arg_loc_y)
				new_unit_z = float(arg_loc_z)
				new_unit_rotation = int(arg_rot) / 4.0 * 3.1415927410125732
				new_unit_garrison = int(arg_gar)
				new_unit_status = int(arg_sts)
				new_unit_frame = int(arg_frm)
				break
			except:
				result = tk.messagebox.askokcancel(title='提交失败', message='格式可能不正确，是否放弃编辑？', parent=w_unit_edit)
				if result == True:
					w_unit_edit.quit()
					w_unit_edit.destroy()
				return
		#unit_to_edit.player=new_unit_player
		unit_to_edit.reference_id=new_unit_id
		unit_to_edit.unit_const=new_unit_const
		unit_to_edit.x=new_unit_x
		unit_to_edit.y=new_unit_y
		unit_to_edit.z=new_unit_z
		unit_to_edit.garrisoned_in_id=new_unit_garrison
		unit_to_edit.status=new_unit_status
		unit_to_edit.initial_animation_frame=new_unit_frame
		if round(unit_to_edit.rotation / 3.1415927410125732 * 4) != int(arg_rot):
			unit_to_edit.rotation=new_unit_rotation
		get_units_list()
		w_unit_edit.quit()
		w_unit_edit.destroy()

	b_commit = tk.Button(w_unit_edit, text='提交更改', width=18, height=1, command=unit_edit_commit_handle)
	b_commit.pack(anchor = 's')
	
	t_Unitedit.delete(1.0,tk.END)
	t_Unitedit.insert(tk.END, unit_info)
	w_unit_edit.grab_set()
	w_unit_edit.mainloop()

# 按钮
b_unit = tk.Button(f_Units, text='编辑单位', width=14, height=1, command=edit_unit)
b_unit.place(x=280, y=10)

# 标识
l5 = tk.Label(f_Units, text='单位ID：')
l5.place(x=100, y=14)

# endregion


def notebook_click_handle(event):
	global current_index
	current_index = event.widget.index("current")
	if current_index == 2:
		get_units_list()
		
# 选项卡 2
notebook.add(f_Duplicater, text='触发复制')
notebook.add(f_Exporter, text='文本导出')
notebook.add(f_Units, text='单位管理')
notebook.pack(padx=10, pady=5, fill=tkinter.BOTH, expand=True)
notebook.bind('<ButtonRelease-1>',notebook_click_handle)

# 菜单
# region

menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='文件', menu=filemenu)
filemenu.add_command(label='打开', command=open_scen)
filemenu.add_command(label='保存', command=save_scen)
filemenu.add_command(label='另存为..', command=saveas_scen, accelerator='Ctrl+S')
filemenu.add_separator()
filemenu.add_command(label='退出', command=window.quit)

#def undo_handle(event):

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='编辑', menu=editmenu)
#editmenu.add_command(label='撤销', command=undo_handle, accelerator='Ctrl+Z', state=DISABLED)
#editmenu.add_separator()
editmenu.add_checkbutton(label='忽略操作成功提示（慎用）', variable=ignore_success, onvalue=1, offvalue=0)

window.config(menu=menubar)
window.bind_all("<Control-s>", saveas_scen_handle)
#window.bind_all("<Control-z>", undo_handle)

# endregion

if open_scen():
	os._exit(0)

window.mainloop()