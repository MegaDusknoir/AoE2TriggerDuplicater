
from AoE2ScenarioParser.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.datasets.units import Unit
from AoE2ScenarioParser.datasets.players import Player
from AoE2ScenarioParser.helper.helper import Tile
from AoE2ScenarioParser.helper.retriever_object_link import RetrieverObjectLink
from AoE2ScenarioParser.objects.aoe2_object import AoE2Object
from AoE2ScenarioParser.objects.unit_obj import UnitObject
from AoE2ScenarioParser.objects.units_obj import UnitsObject

unit_names = {
	0: "可移动的地图视野",
	1: "罗马军",
	2: "罗马军 (死亡)",
	3: "步弓手 (死亡)",
	4: "步弓手",
	5: "火枪手",
	6: "精锐掷矛手",
	7: "掷矛手",
	8: "长弓兵",
	9: "抛射物",
	10: "靶场 (城堡时代)",
	11: "蒙古突骑",
	12: "兵营",
	13: "渔船",
	14: "靶场 (帝王时代)",
	15: "小帆船",
	16: "手推炮 (死亡)",
	17: "贸易船",
	18: "铁匠铺 (城堡时代)",
	19: "铁匠铺 (帝王时代)",
	20: "兵营 (帝王时代)",
	21: "战舰",
	22: "狂战士 (隐藏兵种) (死亡)",
	23: "轻型冲车 (死亡)",
	24: "弩手",
	25: "条顿武士",
	26: "弩手 (死亡)",
	27: "甲胄骑兵 (死亡)",
	28: "诸葛弩 (死亡)",
	29: "贸易船 (死亡)",
	30: "修道院 (封建时代)",
	31: "修道院 (城堡时代)",
	32: "修道院 (帝王时代)",
	33: "堡垒",
	34: "骑射手 (死亡)",
	35: "轻型冲车 (城堡时代)",
	36: "手推炮",
	37: "轻骑兵 (隐藏兵种)",
	38: "骑士",
	39: "骑射手",
	40: "甲胄骑兵",
	41: "近卫军",
	42: "巨型投石机",
	43: "鹿 (死亡)",
	44: "马穆鲁克 (死亡)",
	45: "船坞",
	46: "苏丹亲兵",
	47: "船坞 (城堡时代)",
	48: "野猪",
	49: "攻城武器厂",
	50: "农田",
	51: "船坞 (帝王时代)",
	52: "皇家苏丹亲兵",
	53: "河鲈",
	54: "附加抛射物",
	55: "渔船 (死亡)",
	56: "渔夫 (男)",
	57: "渔夫 (女)",
	58: "渔夫 (男) (死亡)",
	59: "浆果丛",
	60: "渔夫 (女) (死亡)",
	61: "海豚群",
	62: "近卫军 (死亡)",
	63: "增强城门 (/)",
	64: "城门 (/)",
	65: "鹿",
	66: "金矿",
	67: "增强城门 (/) (开启)",
	68: "磨坊",
	69: "海滨鱼群",
	70: "房屋",
	71: "城镇中心 (封建时代)",
	72: "木栅栏",
	73: "诸葛弩",
	74: "民兵",
	75: "剑士",
	76: "重装剑士",
	77: "长剑士",
	78: "城门 (/) (开启)",
	79: "瞭望箭塔",
	80: "增强城门 (旗帜)",
	81: "城门 (旗帜)",
	82: "城堡",
	83: "村民 (男)",
	84: "市场",
	85: "增强城门 (\)",
	86: "马厩 (城堡时代)",
	87: "靶场",
	88: "城门 (\)",
	89: "豺狼",
	90: "增强城门 (\) (开启)",
	91: "城门 (\) (开启)",
	92: "增强城门 (旗帜)",
	93: "长矛兵",
	94: "狂战士 (隐藏兵种)",
	95: "城门 (旗帜)",
	96: "鹰",
	97: "无主抛射物 (箭矢)",
	98: "火枪手 (死亡)",
	99: "重装剑士 (死亡)",
	100: "精锐掷矛手 (死亡)",
	101: "马厩",
	102: "石矿",
	103: "铁匠铺",
	104: "修道院",
	105: "铁匠铺 (封建时代)",
	106: "莱夫·埃里克松",
	107: "苏丹亲兵 (死亡)",
	108: "小帆船 (死亡)",
	109: "城镇中心",
	110: "贸易工厂",
	111: "骑士 (死亡)",
	112: "小地图标记",
	113: "轻骑兵 (隐藏兵种) (死亡)",
	114: "斯托尔特贝克",
	115: "长弓兵 (死亡)",
	116: "市场 (城堡时代)",
	117: "石墙",
	118: "建筑工 (男)",
	119: "硬木栅栏",
	120: "采集者 (男)",
	121: "轻型投石车 (死亡)",
	122: "猎人 (男)",
	123: "伐木工 (男)",
	124: "石矿工 (男)",
	125: "僧侣",
	126: "狼",
	127: "旧探索者",
	128: "贸易车 (空)",
	129: "磨坊 (封建时代)",
	130: "磨坊 (城堡时代)",
	131: "磨坊 (帝王时代)",
	132: "兵营 (城堡时代)",
	133: "船坞 (封建时代)",
	134: "僧侣 (死亡)",
	135: "蒙古突骑 (死亡)",
	136: "战象 (死亡)",
	137: "市场 (帝王时代)",
	138: "Spy",
	139: "重装骑士 (死亡)",
	140: "长矛兵 (死亡)",
	141: "城镇中心 (城堡时代)",
	142: "城镇中心 (帝王时代)",
	143: "碎石 1 x 1 (建筑残骸)",
	144: "碎石 2 x 2 (建筑残骸)",
	145: "碎石 3 x 3 (建筑残骸)",
	146: "碎石 4 x 4 (建筑残骸)",
	147: "碎石 6 x 6 (建筑残骸)",
	148: "碎石 8 x 8 (建筑残骸)",
	149: "弩炮 (死亡)",
	150: "攻城武器厂 (城堡时代)",
	151: "日本武士 (死亡)",
	152: "民兵 (死亡)",
	153: "马厩 (帝王时代)",
	154: "剑士 (死亡)",
	155: "垛墙",
	156: "修理工 (男)",
	157: "掷斧兵 (死亡)",
	158: "盗贼",
	159: "圣物推车 (旧版)",
	160: "狮心王理查",
	161: "黑太子",
	162: "旗帜 X (隐藏单位)",
	163: "塔克修士",
	164: "诺丁汉的郡长",
	165: "查理曼",
	166: "罗兰",
	167: "贝利撒留",
	168: "哥特人狄奥多利克",
	169: "艾息尔弗力夫",
	170: "齐格菲",
	171: "红发埃里克",
	172: "帖木儿",
	173: "亚瑟王",
	174: "兰斯洛特",
	175: "高文",
	176: "莫德雷德",
	177: "大主教",
	178: "贸易车 (空) (死亡)",
	179: "贸易工厂 (帝王时代)",
	180: "长剑士 (死亡)",
	181: "条顿武士 (死亡)",
	182: "奇观 (从属单位)",
	183: "TMISB",
	184: "意大利佣兵 (真)",
	185: "投石手",
	186: "投石手 (死亡)",
	187: "抛射物 (投石手)",
	188: "喷火车",
	189: "喷火车 (死亡)",
	190: "喷火塔",
	191: "房屋 (「游牧」科技) (城堡时代)",
	192: "房屋 (「游牧」科技) (帝王时代)",
	193: "弗拉德·德古拉",
	194: "巨型投石机 (死亡)",
	195: "北畠氏",
	196: "源氏",
	197: "亚历山大·涅夫斯基",
	198: "熙德 (步行)",
	199: "养鱼场",
	200: "罗宾汉",
	201: "FLR_R",
	202: "恶狼",
	203: "瓦斯科·达·伽马",
	204: "贸易车 (满)",
	205: "贸易车 (满) (死亡)",
	206: "村民戴夫·刘易斯",
	207: "帝王骆驼兵",
	208: "塔墙 (隐藏单位)",
	209: "大学",
	210: "大学 (帝王时代)",
	211: "村民 (女) (死亡)",
	212: "建筑工 (女)",
	213: "建筑工 (女) (死亡)",
	214: "农夫 (女)",
	215: "农夫 (女) (死亡)",
	216: "猎人 (女)",
	217: "猎人 (女) (死亡)",
	218: "伐木工 (女)",
	219: "伐木工 (女) (死亡)",
	220: "石矿工 (女)",
	221: "石矿工 (女) (死亡)",
	222: "修理工 (女)",
	223: "哥特国王阿拉里克",
	224: "村民 (男) (死亡)",
	225: "建筑工 (男) (死亡)",
	226: "农夫 (男) (死亡)",
	227: "猎人 (男) (死亡)",
	228: "伐木工 (男) (死亡)",
	229: "石矿工 (男) (死亡)",
	230: "贝拉四世国王",
	231: "水渠",
	232: "菘蓝突击者",
	233: "菘蓝突击者 (死亡)",
	234: "警戒箭塔",
	235: "大型箭塔",
	236: "炮塔",
	237: "狼 (死亡)",
	238: "掷矛手 (死亡)",
	239: "战象",
	240: "TERRC",
	241: "裂缝",
	242: "无主抛射物 (炮弹)",
	243: "DOPL",
	244: "无主抛射物 (炮弹)",
	245: "无主抛射物 (弩箭)",
	246: "无主抛射物 (弩箭)",
	247: "尾迹烟雾",
	248: "石料堆",
	249: "资源堆",
	250: "龙头战舰",
	251: "罗马圆形竞技场",
	252: "黄金堆",
	253: "木材堆",
	254: "碎石 1 x 1 (隐藏单位)",
	255: "碎石 2 x 2 (隐藏单位)",
	256: "碎石 3 x 3 (隐藏单位)",
	257: "碎石 4 x 4 (隐藏单位)",
	258: "碎石 6 x 6 (隐藏单位)",
	259: "农夫 (男)",
	260: "OLD-FISH3",
	261: "碎石 8 x 8 (隐藏单位)",
	262: "一堆食物",
	263: "罗马斗兽场",
	264: "峭壁",
	265: "峭壁",
	266: "峭壁",
	267: "峭壁",
	268: "峭壁",
	269: "峭壁",
	270: "峭壁",
	271: "峭壁",
	272: "峭壁",
	273: "",
	274: "小地图标记",
	275: "百夫长",
	276: "世界奇观",
	277: "百夫长 (死亡)",
	278: "废弃渔网",
	279: "弩炮",
	280: "轻型投石车",
	281: "掷斧兵",
	282: "马穆鲁克",
	283: "重装骑士",
	284: "树 TD",
	285: "圣物",
	286: "带着圣物的僧侣",
	287: "不列颠圣物",
	288: "拜占庭圣物",
	289: "中国圣物",
	290: "法兰克圣物",
	291: "日本武士",
	292: "哥特圣物",
	293: "村民 (女)",
	294: "日本圣物",
	295: "波斯圣物",
	296: "萨拉森圣物",
	297: "条顿圣物",
	298: "土耳其圣物",
	299: "强盗",
	300: "帝王骆驼兵 (死亡)",
	301: "草坪，绿",
	302: "灌木丛 A",
	303: "海鸥",
	304: "篝火",
	305: "羊驼",
	306: "黑格",
	307: "瓜特穆斯",
	308: "哨站 (隐藏单位)",
	309: "带着土耳其圣物的僧侣",
	310: "山脉 1",
	311: "山脉 2",
	312: "无主抛射物 (箭矢)",
	313: "炮弹",
	314: "无主抛射物 (炮弹)",
	315: "无主抛射物 (箭矢)",
	316: "无主抛射物 (箭矢)",
	317: "无主抛射物 (箭矢)",
	318: "无主抛射物 (箭矢)",
	319: "无主抛射物 (箭矢)",
	320: "无主抛射物 (箭矢)",
	321: "无主抛射物 (箭矢)",
	322: "无主抛射物 (箭矢)",
	323: "无主抛射物 (炮弹)",
	324: "无主抛射物 (炮弹)",
	325: "无主抛射物 (炮弹)",
	326: "无主抛射物 (炮弹)",
	327: "无主抛射物 (炮弹)",
	328: "附加抛射物 (化学)",
	329: "骆驼兵",
	330: "重装骆驼兵",
	331: "巨型投石机 (可移动)",
	332: "小地图标记",
	333: "鹿 (隐藏兵种)",
	334: "花朵 1",
	335: "花朵 2",
	336: "花朵 3",
	337: "花朵 4",
	338: "小路 4",
	339: "小路 1",
	340: "小路 2",
	341: "小路 3",
	342: "TERRU",
	343: "TERRV",
	344: "TERRW",
	345: "废墟",
	346: "TERRY",
	347: "TERRZ",
	348: "树木 (竹林)",
	349: "树木 (橡树)",
	350: "树木 (松林)",
	351: "树木 (棕榈林)",
	352: "铁矿",
	353: "采集者 (男) (死亡)",
	354: "采集者 (女)",
	355: "采集者 (女) (死亡)",
	356: "野猪 (死亡)",
	357: "废弃农田",
	358: "长枪兵",
	359: "长戟兵",
	360: "无主抛射物",
	361: "北欧剑士",
	362: "北欧剑士 (死亡)",
	363: "抛射物",
	364: "抛射物",
	365: "抛射物",
	366: "抛射物",
	367: "抛射物 / 附加抛射物",
	368: "抛射物",
	369: "附加抛射物",
	370: "城墙",
	371: "抛射物",
	372: "抛射物",
	373: "抛射物",
	374: "抛射物",
	375: "抛射物 (化学)",
	376: "抛射物 (化学)",
	377: "抛射物 (化学)",
	378: "抛射物 / 附加抛射物 (化学)",
	379: "",
	380: "抛射物",
	381: "无主抛射物 (弩箭)",
	382: "",
	383: "",
	384: "",
	385: "无主抛射物 (弩箭)",
	386: "",
	387: "",
	388: "",
	389: "礁石 1",
	390: "TERRB",
	391: "TERRD",
	392: "TERRE",
	393: "TERRF",
	394: "TERRH",
	395: "TERRI",
	396: "礁石 2",
	397: "TERRK",
	398: "TERRL",
	399: "树 A",
	400: "树 B",
	401: "树 C",
	402: "树 D",
	403: "树 E",
	404: "树 F",
	405: "树 G",
	406: "树 H",
	407: "树 I",
	408: "树 J",
	409: "树 K",
	410: "树 L",
	411: "树木 (橡林)",
	412: "僧侣 (清真学堂) (死亡)",
	413: "树木 (雪松)",
	414: "树木 (丛林)",
	415: "树桩",
	416: "DEBRI",
	417: "尘埃",
	418: "猛狮亨利",
	419: "BDEBR",
	420: "炮舰",
	421: "炮舰 (死亡)",
	422: "中型冲车",
	423: "中型冲车 (死亡)",
	424: "查理·马特",
	425: "弗朗西斯科·德·奥雷利亚纳",
	426: "哈拉尔·哈德拉达",
	427: "贡萨洛·皮萨罗",
	428: "行者荷夫",
	429: "腓特烈·巴巴罗萨",
	430: "村女贞德",
	431: "村女贞德 (死亡)",
	432: "威廉·华莱士",
	433: "威廉·华莱士 (死亡)",
	434: "国王",
	435: "国王 (死亡)",
	436: "幽灵船",
	437: "布里陀毗罗阇",
	438: "破坏者船",
	439: "弗朗切斯科·斯福尔扎",
	440: "爆破兵",
	441: "翼骑兵",
	442: "大型战舰",
	443: "大型战舰 (死亡)",
	444: "城镇中心 (可移动)",
	445: "伯恩纳里城堡",
	446: "港口",
	447: "浅滩",
	448: "斥候骑兵",
	449: "斥候骑兵 (死亡)",
	450: "枪鱼群 (←)",
	451: "枪鱼群 (→)",
	452: "海豚群 (隐藏单位)",
	453: "阿陶尔夫",
	454: "鱼群 (隐藏单位)",
	455: "剑鱼群",
	456: "大马哈鱼群",
	457: "金枪鱼群",
	458: "食人鱼群",
	459: "FISH5",
	460: "大鱼 (隐形鱼)",
	461: "大鱼 (隐形鱼)",
	462: "无主抛射物 (炮弹)",
	463: "房屋 (封建时代)",
	464: "房屋 (城堡时代)",
	465: "房屋 (帝王时代)",
	466: "抛射物 (化学)",
	467: "",
	468: "附加抛射物 (化学)",
	469: "抛射物 (化学)",
	470: "抛射物 (化学)",
	471: "抛射物 (化学)",
	472: "战利品",
	473: "双手剑士",
	474: "重装骑射手",
	475: "抛射物 (化学)",
	476: "抛射物 (化学)",
	477: "抛射物",
	478: "抛射物",
	479: "轻型投石车 (可移动)",
	480: "翼骑兵 (死亡)",
	481: "城镇中心 (主楼) (城堡时代)",
	482: "城镇中心 (楼柱) (城堡时代)",
	483: "城镇中心 (屋檐) (城堡时代)",
	484: "城镇中心 (从属单位) (城堡时代)",
	485: "无主抛射物 (箭矢)",
	486: "熊",
	487: "城门 (/) (关闭)",
	488: "增强城门 (/) (关闭)",
	489: "熊 (死亡)",
	490: "城门 (\) (关闭)",
	491: "增强城门 (\) (关闭)",
	492: "劲弩手",
	493: "重装弩手",
	494: "骆驼兵 (死亡)",
	495: "重装骆驼兵 (死亡)",
	496: "劲弩手 (死亡)",
	497: "重装弩手 (死亡)",
	498: "兵营 (封建时代)",
	499: "火炬 A",
	500: "双手剑士 (死亡)",
	501: "长枪兵 (死亡)",
	502: "长戟兵 (死亡)",
	503: "无主抛射物 (箭矢)",
	504: "抛射物",
	505: "抛射物 / 附加抛射物",
	506: "抛射物",
	507: "抛射物",
	508: "抛射物",
	509: "抛射物",
	510: "抛射物 / 附加抛射物",
	511: "抛射物",
	512: "抛射物 / 附加抛射物",
	513: "抛射物",
	514: "抛射物",
	515: "抛射物",
	516: "无主抛射物 (箭矢)",
	517: "抛射物 (化学)",
	518: "抛射物 / 附加抛射物 (化学)",
	519: "抛射物 (化学)",
	520: "抛射物 (化学)",
	521: "抛射物 (化学)",
	522: "抛射物 / 附加抛射物 (化学)",
	523: "抛射物 (化学)",
	524: "抛射物 / 附加抛射物 (化学)",
	525: "抛射物 (化学)",
	526: "抛射物 (化学)",
	527: "爆破船",
	528: "重型爆破船",
	529: "喷火船",
	530: "精锐长弓兵",
	531: "精锐掷斧兵",
	532: "快速喷火船",
	533: "精锐龙头战舰",
	534: "精锐菘蓝突击者",
	535: "登舰战船",
	536: "重型登舰战船",
	537: "无主抛射物 (箭矢)",
	538: "无主抛射物 (箭矢)",
	539: "箭船",
	540: "抛射物",
	541: "抛射物 (化学)",
	542: "重型弩炮",
	543: "重型弩炮 (死亡)",
	544: "飞天犬",
	545: "运输船",
	546: "轻骑兵",
	547: "轻骑兵 (死亡)",
	548: "重型冲车",
	549: "重型冲车 (死亡)",
	550: "中型投石车",
	551: "无主抛射物 (石块)",
	552: "无主抛射物 (火球)",
	553: "精锐甲胄骑兵",
	554: "精锐条顿武士",
	555: "精锐近卫军",
	556: "精锐马穆鲁克",
	557: "精锐苏丹亲兵",
	558: "精锐战象",
	559: "精锐诸葛弩",
	560: "精锐日本武士",
	561: "精锐蒙古突骑",
	562: "伐木场",
	563: "伐木场 (封建时代)",
	564: "伐木场 (城堡时代)",
	565: "伐木场 (帝王时代)",
	566: "瞭望箭塔 (隐藏单位)",
	567: "冠军剑士",
	568: "冠军剑士 (死亡)",
	569: "游侠",
	570: "游侠 (死亡)",
	571: "特攻步弓手",
	572: "特攻步弓手 (死亡)",
	573: "特攻剑士",
	574: "特攻剑士 (死亡)",
	575: "特攻轻骑兵",
	576: "特攻轻骑兵 (死亡)",
	577: "特攻骑射手",
	578: "特攻骑射手 (死亡)",
	579: "金矿工 (男)",
	580: "金矿工 (男) (死亡)",
	581: "金矿工 (女)",
	582: "金矿工 (女) (死亡)",
	583: "标枪骑兵 (征服者)",
	584: "采矿场",
	585: "采矿场 (封建时代)",
	586: "采矿场 (城堡时代)",
	587: "采矿场 (帝王时代)",
	588: "重型投石车",
	589: "重型投石车 (死亡)",
	590: "牧羊人 (女)",
	591: "牧羊人 (女) (死亡)",
	592: "牧羊人 (男)",
	593: "牧羊人 (男) (死亡)",
	594: "绵羊",
	595: "绵羊 (死亡)",
	596: "精锐标枪骑兵 (征服者)",
	597: "城镇中心 (从属单位) (帝王时代)",
	598: "哨站",
	599: "大教堂",
	600: "旗帜 A",
	601: "旗帜 B",
	602: "旗帜 C",
	603: "旗帜 D",
	604: "旗帜 E",
	605: "桥 A--顶部",
	606: "桥 A--中部",
	607: "桥 A--底部",
	608: "桥 B--顶部",
	609: "桥 B--中部",
	610: "桥 B--底部",
	611: "城镇中心 (主楼) (帝王时代)",
	612: "城镇中心 (楼柱) (帝王时代)",
	613: "城镇中心 (屋檐) (帝王时代)",
	614: "城镇中心 (主楼) (封建时代)",
	615: "城镇中心 (楼柱) (封建时代)",
	616: "城镇中心 (屋檐) (封建时代)",
	617: "城镇中心 (从属单位) (封建时代)",
	618: "城镇中心 (主楼)",
	619: "城镇中心 (楼柱)",
	620: "城镇中心 (屋檐)",
	621: "城镇中心 (从属单位)",
	622: "精锐标枪骑兵 (征服者)(死亡)",
	623: "岩石 1",
	624: "大帐篷 A",
	625: "大帐篷 C",
	626: "大帐篷 B",
	627: "抛射物 / 附加抛射物",
	628: "抛射物 / 附加抛射物 (化学)",
	629: "圣女贞德",
	630: "圣女贞德 (死亡)",
	631: "重装骑射手 (死亡)",
	632: "法兰克游侠",
	633: "法兰克游侠 (死亡)",
	634: "梅兹爵士",
	635: "烧毁的建筑 (未使用)",
	636: "贝查德爵士",
	637: "天坛",
	638: "阿朗松公爵",
	639: "企鹅",
	640: "拉海尔",
	641: "企鹅 (死亡)",
	642: "格拉维尔勋爵",
	643: "格拉维尔勋爵 (死亡)",
	644: "让·洛兰",
	645: "让·洛兰 (死亡)",
	646: "利修蒙元帅",
	647: "利修蒙元帅 (死亡)",
	648: "盖伊·乔瑟林",
	649: "盖伊·乔瑟林 (死亡)",
	650: "让·比罗",
	651: "让·比罗 (死亡)",
	652: "约翰·法斯托尔夫爵士",
	653: "约翰·法斯托尔夫爵士 (死亡)",
	654: "尾迹烟雾 (化学)",
	655: "清真寺",
	656: "抛射物",
	657: "炮弹 (影子)",
	658: "抛射物 (化学)",
	659: "城门 (-)",
	660: "增强城门 (-)",
	661: "城门 (-) (开启)",
	662: "增强城门 (-) (开启)",
	663: "城门 (旗帜)",
	664: "增强城门 (旗帜)",
	665: "城门 (-) (关闭)",
	666: "增强城门 (-) (关闭)",
	667: "城门 (|)",
	668: "增强城门 (|)",
	669: "城门 (|) (开启)",
	670: "增强城门 (|) (开启)",
	671: "城门 (旗帜)",
	672: "增强城门 (旗帜)",
	673: "城门 (|) (关闭)",
	674: "增强城门 (|) (关闭)",
	675: "中型投石车 (死亡)",
	676: "抛射物",
	677: "抛射物尾迹",
	678: "沙蒂永的雷纳德",
	679: "沙蒂永的雷纳德 (死亡)",
	680: "圣殿骑士团大团长",
	681: "圣殿骑士团大团长 (死亡)",
	682: "坏邻居",
	683: "神之弓",
	684: "诅咒之塔",
	685: "腐败之塔",
	686: "神射手",
	687: "神射手 (死亡)",
	688: "圣十字架真品的碎片",
	689: "金字塔",
	690: "圆顶清真寺",
	691: "精锐炮舰",
	692: "狂战士",
	693: "狂战士 (死亡)",
	694: "精锐狂战士",
	695: "精锐狂战士 (死亡)",
	696: "大金字塔",
	697: "小地图标记",
	698: "速不台",
	699: "速不台 (死亡)",
	700: "猎狼",
	701: "猎狼 (死亡)",
	702: "屈出律",
	703: "托巴·尤潘基",
	704: "沙阿",
	705: "奶牛 A",
	706: "破坏者",
	707: "灰狼柯鲁",
	708: "灰狼柯鲁 (死亡)",
	709: "仙人掌",
	710: "骨骸",
	711: "毛毯",
	712: "蒙古包 A",
	713: "蒙古包 B",
	714: "蒙古包 C",
	715: "蒙古包 D",
	716: "蒙古包 E",
	717: "蒙古包 F",
	718: "蒙古包 G",
	719: "蒙古包 H",
	720: "九旄大纛",
	721: "船只遗骸 A",
	722: "船只遗骸 B",
	723: "弹坑",
	724: "标枪骑兵 (征服者)(死亡)",
	725: "豹勇士",
	726: "精锐豹勇士",
	727: "",
	728: "冰",
	729: "神之弓 (可移动)",
	730: "坏邻居 (可移动)",
	731: "成吉思汗",
	732: "成吉思汗 (死亡)",
	733: "装在桶里的皇帝",
	734: "装在桶里的皇帝 (死亡)",
	735: "巨型投石机 (可移动) (死亡)",
	736: "抛射物",
	737: "竹桩",
	738: "桥 A--损毁",
	739: "桥 A--损毁的顶部",
	740: "桥 A--损毁的底部",
	741: "桥 B--损毁",
	742: "桥 B--损毁的顶部",
	743: "桥 B--损毁的底部",
	744: "山脉 3",
	745: "山脉 4",
	746: "抛射物",
	747: "抛射物 (化学)",
	748: "眼镜蛇跑车",
	749: "库西·尤潘基",
	750: "豹勇士 (死亡)",
	751: "鹰斥候",
	752: "精锐鹰勇士",
	753: "鹰勇士",
	754: "鹰斥候 (死亡)",
	755: "答剌罕骑兵",
	756: "答剌罕骑兵 (死亡)",
	757: "精锐答剌罕骑兵",
	758: "烧毁的建筑",
	759: "近卫军 (兵营)",
	760: "近卫军 (兵营) (死亡) (弃用)",
	761: "精锐近卫军 (兵营)",
	762: "精锐近卫军 (兵营) (死亡)",
	763: "羽箭手",
	764: "羽箭手 (死亡)",
	765: "精锐羽箭手",
	766: "精锐羽箭手 (死亡)",
	767: "抛射物",
	768: "Blue Tree",
	769: "",
	770: "",
	771: "征服者",
	772: "征服者 (死亡)",
	773: "精锐征服者",
	774: "精锐征服者 (死亡)",
	775: "传教士",
	776: "传教士 (死亡)",
	777: "阿提拉",
	778: "独木舟",
	779: "布莱达",
	780: "羊驼 (死亡)",
	781: "教宗利奥一世",
	782: "教宗利奥一世 (死亡)",
	783: "西徐亚的野女人",
	784: "西徐亚的野女人 (死亡)",
	785: "海塔",
	786: "无主抛射物",
	787: "无主抛射物 (箭矢)",
	788: "海墙",
	789: "木城门 (/)",
	790: "木城门 (/) (开启)",
	791: "木城门 (旗帜)",
	792: "木城门 (/) (关闭)",
	793: "木城门 (\)",
	794: "木城门 (\) (开启)",
	795: "木城门 (旗帜)",
	796: "木城门 (\) (关闭)",
	797: "木城门 (-)",
	798: "木城门 (-) (开启)",
	799: "木城门 (旗帜)",
	800: "木城门 (-) (关闭)",
	801: "木城门 (|)",
	802: "木城门 (|) (开启)",
	803: "木城门 (旗帜)",
	804: "木城门 (|) (关闭)",
	805: "船坞 (隐藏单位)",
	806: "船坞 (隐藏单位) (封建时代)",
	807: "船坞 (隐藏单位) (城堡时代)",
	808: "船坞 (隐藏单位) (帝王时代)",
	809: "树桩",
	810: "铁甲野猪",
	811: "铁甲野猪 (死亡)",
	812: "美洲豹",
	813: "美洲豹 (死亡)",
	814: "马 A",
	815: "马 A (死亡)",
	816: "金刚鹦鹉",
	817: "雕像 A",
	818: "植物",
	819: "标记",
	820: "墓地",
	821: "头",
	822: "西猯",
	823: "西猯 (死亡)",
	824: "熙德·坎培多尔",
	825: "亚马逊勇士",
	826: "纪念碑",
	827: "战车",
	828: "战车 (死亡)",
	829: "精锐战车",
	830: "精锐战车 (死亡)",
	831: "龟甲船",
	832: "精锐龟甲船",
	833: "火鸡",
	834: "火鸡 (死亡)",
	835: "野马",
	836: "野马 (死亡)",
	837: "地图启示者",
	838: "桑乔国王",
	839: "岩石(石矿)",
	840: "阿方索国王",
	841: "岩石(金矿)",
	842: "伊玛目",
	843: "奶牛 A (死亡)",
	844: "李舜臣将军",
	845: "织田信长",
	846: "毛驴",
	847: "亨利五世",
	848: "毛驴 (死亡)",
	849: "征服者威廉",
	850: "亚马逊射手",
	851: "全效工作室旗帜",
	852: "西徐亚的斥候",
	853: "西徐亚的斥候 (死亡)",
	854: "火炬 A (可转化)",
	855: "古石头像",
	856: "罗马遗址",
	857: "干草堆",
	858: "损坏的手推车",
	859: "花床",
	860: "狂猴",
	861: "狂猴 (死亡)",
	862: "暴风犬",
	863: "碎石 1 x 1",
	864: "碎石 2 x 2",
	865: "碎石 3 x 3",
	866: "热那亚弩手",
	867: "热那亚弩手 (死亡)",
	868: "精锐热那亚弩手",
	869: "马扎尔骠骑",
	870: "马扎尔骠骑 (死亡)",
	871: "精锐马扎尔骠骑",
	872: "坎佩尔大教堂",
	873: "骑象射手",
	874: "骑象射手 (死亡)",
	875: "精锐骑象射手",
	876: "贵族铁骑",
	877: "贵族铁骑 (死亡)",
	878: "精锐贵族铁骑",
	879: "印加枪兵长",
	880: "印加枪兵长 (死亡)",
	881: "精锐印加枪兵长",
	882: "意大利佣兵",
	883: "意大利佣兵 (死亡)",
	884: "野骆驼",
	885: "攻城塔 (遗朝)",
	886: "答剌罕骑兵 (马厩)",
	887: "精锐答剌罕骑兵 (马厩)",
	888: "Llama building",
	889: "Disabled TC spawn",
	890: "Empty TC annex",
	891: "攻城塔 (遗朝) (死亡)",
	892: "重装长枪兵 (战役)",
	893: "重装长枪兵 (战役) (死亡)",
	894: "东方剑士",
	895: "东方剑士 (死亡)",
	896: "瀑布 (覆盖物)",
	897: "骆驼",
	898: "骆驼 (死亡)",
	899: "君士坦丁凯旋门",
	900: "雨 (弃用)",
	901: "旗帜 F (弃用)",
	902: "烟 (铁匠铺) (弃用)",
	903: "",
	904: "木桥 A--顶部 (弃用)",
	905: "木桥 A--中部 (弃用)",
	906: "木桥 A--底部 (弃用)",
	907: "木桥 B--顶部 (弃用)",
	908: "木桥 B--中部 (弃用)",
	909: "木桥 B--底部 (弃用)",
	910: "悬钉的尸体 (弃用)",
	911: "木桥 A--顶部 (重复) (弃用)",
	912: "木桥 A--中部 (重复) (弃用)",
	913: "木桥 A--底部 (重复) (弃用)",
	914: "采石场 (弃用)",
	915: "木材场 (弃用)",
	916: "货物 (弃用)",
	917: "秃鹫 (弃用)",
	918: "岩石 2 (弃用)",
	919: "亚马逊勇士 (弃用) (死亡)",
	920: "亚马逊射手 (弃用) (死亡)",
	921: "僧侣 (阿拉伯) (弃用) (死亡)",
	922: "带着圣物的僧侣 (弃用)",
	923: "皇后 (弃用)",
	924: "皇后 (弃用) (死亡)",
	925: "姗悦姬妲 (弃用)",
	926: "布里陀毗 (弃用)",
	927: "金德·伯勒达伊 (弃用)",
	928: "僧侣 (亚洲) (死亡)",
	929: "萨拉丁 (弃用)",
	930: "霍斯劳 (弃用)",
	931: "贵族首领 (弃用)",
	932: "萨瓦尔 (弃用)",
	933: "木桶 (弃用)",
	934: "羊驼阿弗瑞德 (弃用)",
	935: "羊驼阿弗瑞德 (弃用) (死亡)",
	936: "野象 (弃用)",
	937: "野象 (弃用) (死亡)",
	938: "龙舟 (弃用)",
	939: "火焰 1 (弃用)",
	940: "火焰 2 (弃用)",
	941: "火焰 3 (弃用)",
	942: "火焰 4 (弃用)",
	943: "奥斯曼 (弃用)",
	944: "圣物推车 (弃用)",
	945: "沙阿 (弃用) (死亡)",
	946: "",
	947: "",
	948: "",
	949: "",
	950: "",
	951: "",
	952: "",
	953: "",
	954: "",
	955: "",
	956: "",
	957: "",
	958: "",
	959: "",
	960: "",
	961: "",
	962: "",
	963: "",
	964: "",
	965: "",
	966: "",
	967: "",
	968: "",
	969: "",
	970: "",
	971: "",
	972: "",
	973: "",
	974: "",
	975: "",
	976: "",
	977: "",
	978: "",
	979: "",
	980: "",
	981: "",
	982: "",
	983: "",
	984: "",
	985: "",
	986: "",
	987: "",
	988: "",
	989: "",
	990: "",
	991: "",
	992: "",
	993: "",
	994: "",
	995: "",
	996: "",
	997: "",
	998: "",
	999: "",
	1000: "",
	1001: "风琴炮",
	1002: "风琴炮 (死亡)",
	1003: "精锐风琴炮",
	1004: "卡拉维尔战舰",
	1005: "PORTU_D",
	1006: "精锐卡拉维尔战舰",
	1007: "骆驼射手",
	1008: "骆驼射手 (死亡)",
	1009: "精锐骆驼射手",
	1010: "标枪骑兵",
	1011: "标枪骑兵 (死亡)",
	1012: "精锐标枪骑兵",
	1013: "飞刀女兵",
	1014: "飞刀女兵 (死亡)",
	1015: "精锐飞刀女兵",
	1016: "弯刀勇士",
	1017: "弯刀勇士 (死亡)",
	1018: "精锐弯刀勇士",
	1019: "斑马",
	1020: "斑马 (死亡)",
	1021: "大商站",
	1022: "龙头战舰 (登舰战船)",
	1023: "祭司",
	1024: "祭司 (死亡)",
	1025: "带着圣物的僧侣 (祭司) (弃用)",
	1026: "鸵鸟",
	1027: "鸵鸟 (死亡)",
	1028: "鹳",
	1029: "狮子",
	1030: "狮子 (死亡)",
	1031: "鳄鱼",
	1032: "鳄鱼 (死亡)",
	1033: "草坪，干枯",
	1034: "穆萨·伊本·努赛尔",
	1035: "松迪亚塔",
	1036: "塔里克·伊本·齐亚德",
	1037: "理查·德·克莱尔",
	1038: "特里斯坦",
	1039: "游娣特公主",
	1040: "亨利二世",
	1041: "山脉 5",
	1042: "山脉 6",
	1043: "山脉 7",
	1044: "山脉 8",
	1045: "雪山 1",
	1046: "雪山 2",
	1047: "雪山 3",
	1048: "石堆 1",
	1049: "石堆 2",
	1050: "石堆 3",
	1051: "树木 (龙血树)",
	1052: "树木 (猴面包树)",
	1053: "灌木丛 B",
	1054: "灌木丛 C",
	1055: "抛射物",
	1056: "隼鹰",
	1057: "抛射物",
	1058: "抛射物 (化学)",
	1059: "果树丛",
	1060: "山羊",
	1061: "山羊 (死亡)",
	1062: "篱笆",
	1063: "树木 (刺槐)",
	1064: "耶库诺·阿姆拉克",
	1065: "篱笆 (废墟)",
	1066: "游娣特",
	1067: "伊兹科阿图",
	1068: "穆斯塔法·帕夏",
	1069: "帕柯二世",
	1070: "巴布尔",
	1071: "阿伯哈拉战象",
	1072: "古列尔莫·安布里科",
	1073: "苏定方",
	1074: "帕查库提",
	1075: "瓦伊纳·卡帕克",
	1076: "米克罗斯·陶笛",
	1077: "小约翰",
	1078: "黑扎维沙",
	1079: "标枪骑兵 (真)",
	1080: "苏曼古鲁",
	1081: "仓库",
	1082: "棚屋 A",
	1083: "棚屋 B",
	1084: "棚屋 C",
	1085: "棚屋 D",
	1086: "棚屋 E",
	1087: "棚屋 F",
	1088: "棚屋 G",
	1089: "谷仓",
	1090: "路障 A (-)",
	1091: "动物骨骼",
	1092: "石碑 A",
	1093: "石碑 B",
	1094: "石碑 C",
	1095: "托架",
	1096: "宫殿",
	1097: "帐篷 A",
	1098: "帐篷 B",
	1099: "帐篷 C",
	1100: "帐篷 D",
	1101: "帐篷 E",
	1102: "增强防御塔",
	1103: "火艨艟",
	1104: "爆破筏",
	1105: "攻城塔",
	1106: "达纳罕",
	1107: "攻城塔 (死亡)",
	1108: "达纳罕 (死亡)",
	1109: "极大汗",
	1110: "极大汗 (死亡)",
	1111: "抛射物",
	1112: "抛射物 (化学)",
	1113: "抛射物",
	1114: "抛射物 (化学)",
	1115: "FACAHOLE",
	1116: "鹰勇士 (死亡)",
	1117: "精锐鹰勇士 (死亡)",
	1118: "Inca llama annex",
	1119: "附加抛射物 (风琴炮)",
	1120: "重弩战象",
	1121: "重弩战象 (死亡)",
	1122: "精锐重弩战象",
	1123: "爪刀勇士",
	1124: "爪刀勇士 (死亡)",
	1125: "精锐爪刀勇士",
	1126: "飞镖骑兵",
	1127: "飞镖骑兵 (死亡)",
	1128: "精锐飞镖骑兵",
	1129: "藤甲弓兵",
	1130: "藤甲弓兵 (死亡)",
	1131: "精锐藤甲弓兵",
	1132: "象兵",
	1133: "象兵 (死亡)",
	1134: "精锐象兵",
	1135: "科莫多巨蜥",
	1136: "科莫多巨蜥 (死亡)",
	1137: "老虎",
	1138: "老虎 (死亡)",
	1139: "犀牛",
	1140: "犀牛 (死亡)",
	1141: "箱龟",
	1142: "水牛",
	1143: "水牛 (死亡)",
	1144: "树木 (红树林)",
	1145: "忍者",
	1146: "树木 (雨林)",
	1147: "忍者 (死亡)",
	1148: "石头(海滩)",
	1149: "石头(树林)",
	1150: "旗帜 G",
	1151: "旗帜 H",
	1152: "旗帜 I",
	1153: "旗帜 J",
	1154: "精锐象兵 (死亡)",
	1155: "帝王掷矛手",
	1156: "帝王掷矛手 (死亡)",
	1157: "加扎·玛达",
	1158: "贾亚纳加拉",
	1159: "拉登甲亮",
	1160: "巽他皇家侍卫",
	1161: "巽他皇家侍卫 (死亡)",
	1162: "苏耶跋摩一世",
	1163: "乌达雅迭耶跋摩一世",
	1164: "阇耶毗罗跋摩",
	1165: "莽应龙",
	1166: "莽瑞体",
	1167: "抛射物 / 附加抛射物",
	1168: "抛射物 / 附加抛射物 (化学)",
	1169: "抛射物",
	1170: "抛射物 (化学)",
	1171: "佛像 A",
	1172: "佛像 B",
	1173: "佛像 C",
	1174: "佛像 D",
	1175: "羊齿植物丛",
	1176: "特鲁乌兰门",
	1177: "陶瓷花瓶",
	1178: "黎利",
	1179: "黎来 (替身)",
	1180: "黎来",
	1181: "李篆",
	1182: "刘仁澍",
	1183: "裴备",
	1184: "丁礼",
	1185: "王通",
	1186: "使者",
	1187: "水稻田",
	1188: "废弃水稻田",
	1189: "巨港",
	1190: "加扎·玛达 (死亡)",
	1191: "浮屠佛塔",
	1192: "城门 (旗帜)",
	1193: "FARMDROP",
	1194: "FARMSTACK",
	1195: "RFARMDROP",
	1196: "军帐 A",
	1197: "军帐 B",
	1198: "军帐 C",
	1199: "军帐 D",
	1200: "军帐 E",
	1201: "宝塔 A",
	1202: "宝塔 B",
	1203: "宝塔 C",
	1204: "桥 C--顶部",
	1205: "桥 C--中部",
	1206: "桥 C--底部",
	1207: "桥 D--顶部",
	1208: "桥 D--中部",
	1209: "桥 D--底部",
	1210: "桥 C--损毁",
	1211: "桥 C--损毁的顶部",
	1212: "桥 C--损毁的底部",
	1213: "桥 D--损毁",
	1214: "桥 D--损毁的顶部",
	1215: "桥 D--损毁的底部",
	1216: "桑奇佛塔",
	1217: "古尔墓庙",
	1218: "路障 B (/)",
	1219: "路障 C (|)",
	1220: "路障 D (\)",
	1221: "伊兹科阿图 (死亡)",
	1222: "骑鲨圣猫",
	1223: "抛射物",
	1224: "丁礼 (死亡)",
	1225: "龙骑兵",
	1226: "龙骑兵 (死亡)",
	1227: "精锐龙骑兵",
	1228: "怯薛",
	1229: "怯薛 (死亡)",
	1230: "精锐怯薛",
	1231: "钦察骑射手",
	1232: "钦察骑射手 (死亡)",
	1233: "精锐钦察骑射手",
	1234: "皇家骑士",
	1235: "皇家骑士 (死亡)",
	1236: "精锐皇家骑士",
	1237: "双峰骆驼",
	1238: "双峰骆驼 (死亡)",
	1239: "羱羊",
	1240: "羱羊 (死亡)",
	1241: "雪豹",
	1242: "雪豹 (死亡)",
	1243: "鹅",
	1244: "鹅 (死亡)",
	1245: "猪",
	1246: "猪 (死亡)",
	1247: "野双峰骆驼",
	1248: "树木 (秋季橡树)",
	1249: "树木 (雪中的秋季橡树)",
	1250: "树木 (枯树)",
	1251: "营垒",
	1252: "龙骑兵 (下马)",
	1253: "精锐龙骑兵 (下马)",
	1254: "龙骑兵",
	1255: "精锐龙骑兵",
	1256: "精锐龙骑兵 (死亡)",
	1257: "龙骑兵 (下马) (死亡)",
	1258: "轻型冲车",
	1259: "精锐钦察骑射手 (雇佣) (真)",
	1260: "精锐钦察骑射手 (雇佣)",
	1261: "精锐钦察骑射手 (禁用)",
	1262: "脱脱迷失汗",
	1263: "火焰骆驼",
	1264: "祭坛",
	1265: "伊瓦依洛",
	1266: "康斯坦丁沙皇",
	1267: "可泰安汗",
	1268: "库曼首领",
	1269: "吉艮汗",
	1270: "已拆卸的推车",
	1271: "牛拉车",
	1272: "牛拉车 (死亡)",
	1273: "牛货车",
	1274: "牛货车 (死亡)",
	1275: "可汗",
	1276: "兀鲁思汗",
	1277: "可汗 (死亡)",
	1278: "维陶塔斯大帝 (死亡)",
	1279: "雕像 (文明)",
	1280: "雕像 B",
	1281: "维陶塔斯大帝",
	1282: "旗帜 K",
	1283: "旗帜 L",
	1284: "旗帜 M",
	1285: "FE 旗帜",
	1286: "康斯坦丁沙皇 (死亡)",
	1287: "可泰安汗 (死亡)",
	1288: "库曼首领 (死亡)",
	1289: "吉艮汗 (死亡)",
	1290: "伊瓦依洛 (下马)",
	1291: "隐形续命单位",
	1292: "皇后",
	1293: "姗悦姬妲",
	1294: "布里陀毗",
	1295: "金德·伯勒达伊",
	1296: "萨拉丁",
	1297: "霍斯劳",
	1298: "首领",
	1299: "萨瓦尔",
	1300: "羊驼阿弗瑞德",
	1301: "野象",
	1302: "龙舟",
	1303: "奥斯曼",
	1304: "圣物推车",
	1305: "秃鹫",
	1306: "雨",
	1307: "旗帜 F",
	1308: "烟 (铁匠铺)",
	1309: "木桥 A--顶部",
	1310: "木桥 A--中部",
	1311: "木桥 A--底部",
	1312: "木桥 B--顶部",
	1313: "木桥 B--中部",
	1314: "木桥 B--底部",
	1315: "悬钉的尸体",
	1316: "木桥 A--顶部 (重复)",
	1317: "木桥 A--中部 (重复)",
	1318: "木桥 A--底部 (重复)",
	1319: "采石场",
	1320: "木材场",
	1321: "货物",
	1322: "雕像 (柱)",
	1323: "岩石 2",
	1324: "亚马逊勇士 (死亡)",
	1325: "亚马逊射手 (死亡)",
	1326: "僧侣 (阿拉伯) (死亡)",
	1327: "带着圣物的僧侣",
	1328: "皇后 (死亡)",
	1329: "僧侣 (亚洲) (死亡)",
	1330: "木桶",
	1331: "羊驼阿弗瑞德 (死亡)",
	1332: "野象 (死亡)",
	1333: "火焰 1",
	1334: "火焰 2",
	1335: "火焰 3",
	1336: "火焰 4",
	1337: "沙阿 (死亡)",
	1338: "马车",
	1339: "CLF01",
	1340: "CLF02",
	1341: "CLF03",
	1342: "CLF04",
	1343: "雕像 (面朝左)",
	1344: "CLF06",
	1345: "雕像 (面朝右)",
	1346: "CLF08",
	1347: "树木 (柏树)",
	1348: "树木 (意大利松)",
	1349: "树木 (橄榄树)",
	1350: "树木 (芦苇)",
	1351: "植物 (丛林)",
	1352: "植物 (热带矮树丛)",
	1353: "植物 (矮树丛)",
	1354: "植物 (雨林)",
	1355: "植物 (雨林矮树丛)",
	1356: "马 B",
	1357: "马 B (死亡)",
	1358: "草地，绿",
	1359: "草地，干枯",
	1360: "植物 (灌木丛，绿)",
	1361: "植物 (灌木丛，干枯)",
	1362: "植物 (灌木，绿)",
	1363: "植物 (灌木，干枯)",
	1364: "植物 (野草)",
	1365: "植物 (枯死)",
	1366: "植物 (鲜花)",
	1367: "桑科雷清真学堂",
	1368: "伦敦塔",
	1369: "圣母升天大教堂",
	1370: "草原突骑",
	1371: "草原突骑 (死亡)",
	1372: "精锐草原突骑",
	1373: "精锐草原突骑 (死亡)",
	1374: "易洛魁战士",
	1375: "易洛魁战士 (死亡)",
	1376: "火炬 B",
	1377: "火炬 B (可转化)",
	1378: "磐石教堂",
	1379: "海门 (/)",
	1380: "海门 (/) (开启)",
	1381: "海门 (旗帜)",
	1382: "海门 (/) (关闭)",
	1383: "海门 (\)",
	1384: "海门 (\) (开启)",
	1385: "海门 (旗帜)",
	1386: "海门 (\) (关闭)",
	1387: "海门 (-)",
	1388: "海门 (-) (开启)",
	1389: "海门 (旗帜)",
	1390: "海门 (-) (关闭)",
	1391: "海门 (|)",
	1392: "海门 (|) (开启)",
	1393: "海门 (旗帜)",
	1394: "海门 (|) (关闭)",
	1395: "松迪亚塔 (死亡)",
	1396: "锁链",
	1397: "锁链",
	1398: "锁链",
	1399: "锁链",
	1400: "圣物祭司",
	1401: "萨瓦尔 (死亡)",
	1402: "兵营 (黑暗时代) (废墟)",
	1403: "房屋 (黑暗时代) (废墟)",
	1404: "磨坊 (黑暗时代) (废墟)",
	1405: "哨站 (黑暗时代) (废墟)",
	1406: "城门地基 (废墟)",
	1407: "木栅栏 (废墟)",
	1408: "城镇中心 (黑暗时代) (废墟)",
	1409: "伐木场 (废墟)",
	1410: "采矿场 (废墟)",
	1411: "磨坊 (封建时代) (废墟)",
	1412: "磨坊 (城堡时代) (废墟)",
	1413: "兵营 (封建时代) (废墟)",
	1414: "兵营 (城堡时代) (废墟)",
	1415: "靶场 (封建时代) (废墟)",
	1416: "靶场 (城堡时代) (废墟)",
	1417: "马厩 (封建时代) (废墟)",
	1418: "马厩 (城堡时代) (废墟)",
	1419: "铁匠铺 (封建时代) (废墟)",
	1420: "铁匠铺 (城堡时代) (废墟)",
	1421: "修道院 (废墟)",
	1422: "市场 (封建时代) (废墟)",
	1423: "市场 (城堡时代) (废墟)",
	1424: "市场 (帝王时代) (废墟)",
	1425: "攻城武器厂 (封建时代) (废墟)",
	1426: "攻城武器厂 (城堡时代) (废墟)",
	1427: "大学 (城堡时代) (废墟)",
	1428: "大学 (帝王时代) (废墟)",
	1429: "贸易工厂 (废墟)",
	1430: "城堡 (废墟)",
	1431: "城镇中心 (封建时代) (废墟)",
	1432: "城镇中心 (城堡时代) (废墟)",
	1433: "城镇中心 (帝王时代) (废墟)",
	1434: "房屋 (封建时代) (废墟)",
	1435: "房屋 (城堡时代) (废墟)",
	1436: "瞭望箭塔 (废墟)",
	1437: "警戒箭塔 (废墟)",
	1438: "大型箭塔 (废墟)",
	1439: "炮塔 (废墟)",
	1440: "木城门 (/) (废墟)",
	1441: "木城门 (\) (废墟)",
	1442: "木城门 (-) (废墟)",
	1443: "木城门 (|) (废墟)",
	1444: "增强防御塔 (废墟)",
	1445: "奇观 (废墟)",
	1446: "大商站 (废墟)",
	1447: "蒙古包 A (废墟)",
	1448: "蒙古包 B (废墟)",
	1449: "蒙古包 C (废墟)",
	1450: "蒙古包 D (废墟)",
	1451: "蒙古包 E (废墟)",
	1452: "蒙古包 F (废墟)",
	1453: "蒙古包 G (废墟)",
	1454: "蒙古包 H (废墟)",
	1455: "棚屋 A (废墟)",
	1456: "棚屋 B (废墟)",
	1457: "棚屋 C (废墟)",
	1458: "棚屋 D (废墟)",
	1459: "棚屋 E (废墟)",
	1460: "棚屋 F (废墟)",
	1461: "棚屋 G (废墟)",
	1462: "帐篷 A (废墟)",
	1463: "帐篷 B (废墟)",
	1464: "帐篷 C (废墟)",
	1465: "帐篷 D (废墟)",
	1466: "帐篷 E (废墟)",
	1467: "军帐 A (废墟)",
	1468: "军帐 B (废墟)",
	1469: "军帐 C (废墟)",
	1470: "军帐 D (废墟)",
	1471: "军帐 E (废墟)",
	1472: "路障 A (废墟)",
	1473: "路障 B (废墟)",
	1474: "路障 C (废墟)",
	1475: "路障 D (废墟)",
	1476: "大帐篷 A (废墟)",
	1477: "大帐篷 B (废墟)",
	1478: "大帐篷 C (废墟)",
	1479: "营垒 (废墟)",
	1480: "大教堂 (废墟)",
	1481: "天坛 (废墟)",
	1482: "圆顶清真寺 (废墟)",
	1483: "祭坛 (废墟)",
	1484: "仓库 (废墟)",
	1485: "君士坦丁凯旋门 (废墟)",
	1486: "堡垒 (废墟)",
	1487: "古尔墓庙 (废墟)",
	1488: "伯恩纳里城堡 (废墟)",
	1489: "坎佩尔大教堂 (废墟)",
	1490: "桑奇佛塔 (废墟)",
	1491: "桑科雷清真学堂 (废墟)",
	1492: "伦敦塔 (废墟)",
	1493: "圣母升天大教堂 (废墟)",
	1494: "诅咒之塔 (废墟)",
	1495: "腐败之塔 (废墟)",
	1496: "清真寺 (废墟)",
	1497: "碎石 4 x 4",
	1498: "碎石 8 x 8",
	1499: "谷仓 (废墟)",
	1500: "城门 (/) (废墟)",
	1501: "城门 (\) (废墟)",
	1502: "城门 (-) (废墟)",
	1503: "城门 (|) (废墟)",
	1504: "增强城门 (/) (废墟)",
	1505: "增强城门 (\) (废墟)",
	1506: "增强城门 (-) (废墟)",
	1507: "增强城门 (|) (废墟)",
	1508: "石墙 (废墟)",
	1509: "垛墙 (废墟)",
	1510: "城墙门 (/) (废墟)",
	1511: "城墙门 (\) (废墟)",
	1512: "城墙门 (-) (废墟)",
	1513: "城墙门 (|) (废墟)",
	1514: "罗马圆形竞技场 (废墟)",
	1515: "金字塔 (废墟)",
	1516: "大金字塔 (废墟)",
	1517: "亚琛大教堂 (废墟)",
	1518: "城门 (旗帜) (废墟)",
	1519: "增强城门 (旗帜) (废墟)",
	1520: "罗马斗兽场 (废墟)",
	1521: "木城门 (旗帜) (废墟)",
	1522: "水渠 (废墟)",
	1523: "",
	1524: "",
	1525: "",
	1526: "",
	1527: "",
	1528: "",
	1529: "",
	1530: "",
	1531: "",
	1532: "",
	1533: "",
	1534: "",
	1535: "",
	1536: "",
	1537: "",
	1538: "",
	1539: "",
	1540: "",
	1541: "",
	1542: "",
	1543: "",
	1544: "",
	1545: "",
	1546: "",
	1547: "",
	1548: "",
	1549: "",
	1550: "桥 E--顶部",
	1551: "桥 E--中部",
	1552: "桥 E--底部",
	1553: "桥 F--顶部",
	1554: "桥 F--中部",
	1555: "桥 F--底部",
	1556: "桥 E--损毁",
	1557: "桥 E--损毁的顶部",
	1558: "桥 E--损毁的底部",
	1559: "桥 F--损毁",
	1560: "桥 F--损毁的顶部",
	1561: "桥 F--损毁的底部",
	1562: "牌坊",
	1563: "努比亚金字塔",
	1564: "箭靶 A",
	1565: "箭靶 B",
	1566: "神庙遗迹",
	1567: "井",
	1568: "马上日本武士",
	1569: "马上日本武士 (死亡)",
	1570: "索洛托勇士",
	1571: "索洛托勇士 (死亡)",
	1572: "商人",
	1573: "商人 (死亡)",
	1574: "索索人护卫",
	1575: "索索人护卫 (死亡)",
	1576: "皇家苏丹亲兵 (死亡)",
	1577: "光枪人",
	1578: "光枪人 (死亡)",
	1579: "城墙门 (/)",
	1580: "城墙门 (/) (开启)",
	1581: "城墙门 (旗帜)",
	1582: "城墙门 (/) (关闭)",
	1583: "城墙门 (\)",
	1584: "城墙门 (\) (开启)",
	1585: "城墙门 (旗帜)",
	1586: "城墙门 (\) (关闭)",
	1587: "城墙门 (-)",
	1588: "城墙门 (-) (开启)",
	1589: "城墙门 (旗帜)",
	1590: "城墙门 (-) (关闭)",
	1591: "城墙门 (|)",
	1592: "城墙门 (|) (开启)",
	1593: "城墙门 (旗帜)",
	1594: "城墙门 (|) (关闭)",
	1595: "抛射物 (光枪)",
	1596: "奶牛 B",
	1597: "奶牛 B (死亡)",
	1598: "奶牛 C",
	1599: "奶牛 C (死亡)",
	1600: "奶牛 D",
	1601: "奶牛 D (死亡)",
	1602: "马 C",
	1603: "马 C (死亡)",
	1604: "马 D",
	1605: "马 D (死亡)",
	1606: "马 E",
	1607: "马 E (死亡)",
	1608: "蝴蝶 1",
	1609: "蝴蝶 2",
	1610: "蝴蝶 3",
	1611: "Animal Blood Small",
	1612: "Animal Blood Large",
	1613: "Terrain blocker",
	1614: "Bolt explosion",
	1615: "弗朗切斯科·斯福尔扎 (死亡)",
	1616: "塔里克·伊本·齐亚德 (死亡)",
	1617: "弗拉德·德古拉 (死亡)",
	1618: "速不台 (死亡)",
	1619: "阿提拉 (死亡)",
	1620: "哥特国王阿拉里克 (死亡)",
	1621: "苏曼古鲁 (死亡)",
	1622: "亚琛大教堂",
	1623: "黎利 (死亡)",
	1624: "阿陶尔夫 (死亡)",
	1625: "游娣特 (死亡)",
	1626: "库西·尤潘基 (死亡)",
	1627: "布里陀毗罗阇 (死亡)",
	1628: "首领 (死亡)",
	1629: "伊瓦依洛 (死亡)",
	1630: "伊瓦依洛 (下马) (死亡)",
	1631: "The Middlebrook",
	1632: "奥斯曼 (死亡)",
	1633: "帕查库提 (死亡)",
	1634: "STUMBAO",
	1635: "瀑布 (背景)",
	1636: "使者 (死亡)",
	1637: "莽应龙 (死亡)",
	1638: "屈出律 (死亡)",
	1639: "Monument resources enabler",
	1640: "中国村民奖励 (男)",
	1641: "中国村民奖励 (女)",
	1642: "中国村民奖励器",
	1643: "玛雅村民奖励 (男)",
	1644: "玛雅村民奖励器",
	1645: "玛雅村民奖励 (女)",
	1646: "MRKT",
	1647: "TDWS4",
	1648: "Trail Smoke (Gunpowder)",
	1649: "Trophy None",
	1650: "Trophy Bronze",
	1651: "Trophy Silver",
	1652: "Trophy Gold",
	1653: "Trophy Platinum",
	1654: "Resources",
	1655: "马上轻装兵",
	1656: "马上轻装兵 (死亡)",
	1657: "精锐马上轻装兵",
	1658: "萨金特卫兵",
	1659: "精锐萨金特卫兵",
	1660: "萨金特卫兵 (城楼)",
	1661: "精锐萨金特卫兵 (城楼)",
	1662: "萨金特卫兵 (死亡)",
	1663: "弗拉芒民兵 (男村民)",
	1664: "弗拉芒民兵 (男村民) (死亡)",
	1665: "城楼",
	1666: "骑士 (死亡) (勃艮第)",
	1667: "重装骑士 (死亡) (勃艮第)",
	1668: "游侠 (死亡) (勃艮第)",
	1669: "长腿爱德华",
	1670: "长腿爱德华 (死亡)",
	1671: "吉尔伯特·德·克莱尔",
	1672: "吉尔伯特·德·克莱尔 (死亡)",
	1673: "无畏的约翰",
	1674: "无畏的约翰 (死亡)",
	1675: "好人腓力",
	1676: "好人腓力 (死亡)",
	1677: "罗伯特·吉斯卡尔",
	1678: "罗伯特·吉斯卡尔 (死亡)",
	1679: "罗杰·博索",
	1680: "罗杰·博索 (死亡)",
	1681: "博希蒙德",
	1682: "博希蒙德 (死亡)",
	1683: "卢埃林·阿颇·格鲁菲德",
	1684: "卢埃林·阿颇·格鲁菲德 (死亡)",
	1685: "达菲德·阿颇·格鲁菲德",
	1686: "达菲德·阿颇·格鲁菲德 (死亡)",
	1687: "阿马尼亚克的伯纳德",
	1688: "阿马尼亚克的伯纳德 (死亡)",
	1689: "闪烁 (永久)",
	1690: "战狼号巨型投石机",
	1691: "战狼号巨型投石机 (组装)",
	1692: "埃诺的杰奎琳",
	1693: "鞑靼绵羊奖励 1",
	1694: "鞑靼绵羊奖励器 1",
	1695: "鞑靼绵羊奖励 2",
	1696: "鞑靼绵羊奖励器 2",
	1697: "弗拉芒民兵 (女村民)",
	1698: "弗拉芒民兵 (女村民) (死亡)",
	1699: "弗拉芒民兵",
	1700: "鞑靼绵羊奖励 3"
}

def get_unit_as_string(unit_manager = UnitsObject):
	return_string = "\n·单位列表：\n"
	for player in range(len(unit_manager.units)):
		if len(unit_manager.units[player]) != 0:
			if player == 0:
				return_string += f'\n——大地之母 ——\n\n'
			else:
				return_string += f'\n——玩家 {player} ——\n\n'
		for unit in unit_manager.units[player]:
			try:
				name = unit_names[unit.unit_const]
			except:
				name = f'<{unit_const}>'
			return_string += f'[ID:{unit.reference_id}] {name}({unit.unit_const})\n'
			return_string += f'\t位置：[{unit.x},{unit.y},{unit.z}]  相位：{round(unit.rotation / 3.1415927410125732 * 4)}/4 pi\n'
			return_string += f'\t驻扎于：{unit.garrisoned_in_id}  状态：{unit.status}  帧位：{unit.initial_animation_frame}\n'
	return_string += '\n'
	return return_string

def get_single_unit(unit_manager = UnitsObject, unit_id = int):
	return_string = ""
	for player in range(len(unit_manager.units)):
		for unit in unit_manager.units[player]:
			if unit.reference_id == unit_id:
				try:
					name = unit_names[unit.unit_const]
				except:
					name = f'<{unit_const}>'
				return_string += f'单位ID：{unit.reference_id}\n'
				return_string += f'名称：{name}\n'
				return_string += f'种类ID：{unit.unit_const}\n'
				return_string += f'属于：玩家 {player}\n'
				return_string += f'位置：{unit.x}, {unit.y}, {unit.z}\n'
				return_string += f'相位：{round(unit.rotation / 3.1415927410125732 * 4)}/4 pi\n'
				return_string += f'驻扎于：{unit.garrisoned_in_id}\n'
				return_string += f'状态：{unit.status}\n'
				return_string += f'帧位：{unit.initial_animation_frame}\n'
				return return_string, unit
	return return_string, -1