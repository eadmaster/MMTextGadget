
# Module of reusable code for interfacing with Million Monkeys related files

# GZIP compression for files
import gzip   # GZIP compress files for iso
import shutil # GZIP compress an existing file
# Path related helpers
import os
# Reading / Converting binary data
import struct
import hashlib
import re

# This is a string we know exists near the start of translation
# strings across multiple files. If we find this pattern in a file
# we assume there are more translation strings following it
TRANS_START_PATTERN = b'\xE0\x19\x96\x00'

# Constants
DATA0_OFFSET           = 0x729800
DATA1_OFFSET           = 0x72C800
IN_HEADER_FILENAME     = "DATA0.BIN"
IN_ISO_FILENAME        = "base.iso"
OUT_ISO_FILENAME       = "mm_en_patch.iso"
IN_TRANS_CSV_FILENAME  = "jptxt.csv"
IN_MEM_STRING_FILENAME = "inmemstr.bin"
BIN_INPUT_PATH         = "../bin-input/"
BIN_INPUT_DATA0_PATH   = "../bin-input/DATA0"
BIN_INPUT_DATA1_PATH   = "../bin-input/DATA1"
BIN_INPUT_ISO_PATH     = "../bin-input/ISO"
BIN_INT_PATH           = "../bin-int/"
BIN_OUTPUT_PATH        = "../bin-output/"
TOOLS_PATH             = "../tools/"

# Whoever is looking at this I am so sorry
char_table_start = int(0x889F)
_encode_table = {
    "1" : int(0 + char_table_start),
    "2" : int(1 + char_table_start),
    "3" : int(2 + char_table_start),
    "4" : int(3 + char_table_start),
    "5" : int(4 + char_table_start),
    "6" : int(5 + char_table_start),
    "7" : int(6 + char_table_start),
    "8" : int(7 + char_table_start),
    "9" : int(8 + char_table_start),
    "0" : int(9 + char_table_start),
    "A" : int(10 + char_table_start),
    "B" : int(11 + char_table_start),
    "C" : int(12 + char_table_start),
    "D" : int(13 + char_table_start),
    "E" : int(14 + char_table_start),
    "F" : int(15 + char_table_start),
    "G" : int(16 + char_table_start),
    "H" : int(17 + char_table_start),
    "I" : int(18 + char_table_start),
    "J" : int(19 + char_table_start),
    "K" : int(20 + char_table_start),
    "L" : int(21 + char_table_start),
    "M" : int(22 + char_table_start),
    "N" : int(23 + char_table_start),
    "O" : int(0x88B7),
    "P" : int(25 + char_table_start),
    "Q" : int(26 + char_table_start),
    "R" : int(27 + char_table_start),
    "S" : int(28 + char_table_start),
    "T" : int(29 + char_table_start),
    "U" : int(30 + char_table_start),
    "V" : int(31 + char_table_start),
    "W" : int(32 + char_table_start),
    "X" : int(33 + char_table_start),
    "Y" : int(34 + char_table_start),
    "Z" : int(35 + char_table_start),
    "a" : int(36 + char_table_start),
    "b" : int(37 + char_table_start),
    "c" : int(38 + char_table_start),
    "d" : int(39 + char_table_start),
    "e" : int(40 + char_table_start),
    "f" : int(41 + char_table_start),
    "g" : int(42 + char_table_start),
    "h" : int(43 + char_table_start),
    "i" : int(44 + char_table_start),
    "j" : int(45 + char_table_start),
    "k" : int(46 + char_table_start),
    "l" : int(47 + char_table_start),
    "m" : int(48 + char_table_start),
    "n" : int(49 + char_table_start),
    "o" : int(50 + char_table_start),
    "p" : int(51 + char_table_start),
    "q" : int(52 + char_table_start),
    "r" : int(53 + char_table_start),
    "s" : int(54 + char_table_start),
    "t" : int(55 + char_table_start),
    "u" : int(56 + char_table_start),
    "v" : int(57 + char_table_start),
    "w" : int(58 + char_table_start),
    "x" : int(59 + char_table_start),
    "y" : int(60 + char_table_start),
    "z" : int(61 + char_table_start),
    "あ" : int(62 + char_table_start),
    "い" : int(63 + char_table_start),
    "う" : int(64 + char_table_start),
    "え" : int(65 + char_table_start),
    "お" : int(66 + char_table_start),
    "が" : int(67 + char_table_start),
    "き" : int(68 + char_table_start),
    "く" : int(69 + char_table_start),
    "け" : int(70 + char_table_start),
    "こ" : int(71 + char_table_start),
    "さ" : int(72 + char_table_start),
    "し" : int(73 + char_table_start),
    "す" : int(74 + char_table_start),
    "せ" : int(75 + char_table_start),
    "そ" : int(76 + char_table_start),
    "た" : int(77 + char_table_start),
    "ち" : int(78 + char_table_start),
    "つ" : int(79 + char_table_start),
    "て" : int(80 + char_table_start),
    "と" : int(81 + char_table_start),
    "な" : int(82 + char_table_start),
    "に" : int(83 + char_table_start),
    "ぬ" : int(84 + char_table_start),
    "ね" : int(85 + char_table_start),
    "の" : int(86 + char_table_start),
    "は" : int(87 + char_table_start),
    "ひ" : int(88 + char_table_start),
    "ふ" : int(89 + char_table_start),
    "へ" : int(90 + char_table_start),
    "ほ" : int(91 + char_table_start),
    "ま" : int(92 + char_table_start),
    "み" : int(93 + char_table_start),
    
    "む" : int(97 + char_table_start),
    "め" : int(98 + char_table_start),
    "も" : int(99 + char_table_start),
    "や" : int(100 + char_table_start),
    "ゆ" : int(101 + char_table_start),
    "よ" : int(102 + char_table_start),
    "ら" : int(103 + char_table_start),
    "り" : int(104 + char_table_start),
    "る" : int(105 + char_table_start),
    "れ" : int(106 + char_table_start),
    "ろ" : int(107 + char_table_start),
    "わ" : int(108 + char_table_start),
    "を" : int(109 + char_table_start),
    "ん" : int(110 + char_table_start),
    
    "-" : int(0x89d4),
    #"-" : int(112 + char_table_start),
    "、" : int(113 + char_table_start),
    "。" : int(114 + char_table_start),
    
    #"(" : int(131 + char_table_start),
    #")" : int(132 + char_table_start),
    "(" : int(0x89D0),
    ")" : int(0x89D1),
    
    "ー" : int(175 + char_table_start),
    
    
    "ツ" : int(250 + char_table_start),
    
    " " : int(0x8974),
    "ァ" : int(214 + char_table_start),
    "ア" : int(215 + char_table_start),
    "ィ" : int(216 + char_table_start),
    "イ" : int(217 + char_table_start),
    "ゥ" : int(218 + char_table_start),
    "ウ" : int(219 + char_table_start),
    "ェ" : int(220 + char_table_start),
    "エ" : int(221 + char_table_start),
    "ォ" : int(222 + char_table_start),
    "オ" : int(223 + char_table_start),
    
    "ル" : int(224 + char_table_start),
    
    "カ" : int(225 + char_table_start),
    "ガ" : int(226 + char_table_start),
    "キ" : int(227 + char_table_start),
    "ギ" : int(228 + char_table_start),
    "ク" : int(229 + char_table_start),
    "グ" : int(230 + char_table_start),
    "ケ" : int(231 + char_table_start),
    "ゲ" : int(232 + char_table_start),
    "コ" : int(233 + char_table_start),
    "ゴ" : int(234 + char_table_start),
    "サ" : int(235 + char_table_start),
    "ザ" : int(236 + char_table_start),
    "シ" : int(237 + char_table_start),
    "ジ" : int(238 + char_table_start),
    "ス" : int(239 + char_table_start),
    "ズ" : int(240 + char_table_start),
    "セ" : int(241 + char_table_start),
    "ゼ" : int(242 + char_table_start),
    "ソ" : int(243 + char_table_start),
    "ゾ" : int(244 + char_table_start),
    "タ" : int(245 + char_table_start),
    "ダ" : int(246 + char_table_start),
    "チ" : int(247 + char_table_start),
    "ヂ" : int(248 + char_table_start),
    "ッ" : int(249 + char_table_start),
    
    "ツ" : int(250 + char_table_start),
    "ヅ" : int(251 + char_table_start),
    "テ" : int(252 + char_table_start),
    "デ" : int(253 + char_table_start),
    "ト" : int(254 + char_table_start),
    "ド" : int(255 + char_table_start),
    "ナ" : int(256 + char_table_start),
    "ニ" : int(257 + char_table_start),
    "ヌ" : int(258 + char_table_start),
    "ネ" : int(259 + char_table_start),
    "ノ" : int(260 + char_table_start),
    "ハ" : int(261 + char_table_start),
    "バ" : int(262 + char_table_start),
    "パ" : int(263 + char_table_start),
    "ヒ" : int(264 + char_table_start),
    "ビ" : int(265 + char_table_start),
    "ピ" : int(266 + char_table_start),
    "フ" : int(267 + char_table_start),
    "ブ" : int(268 + char_table_start),
    "プ" : int(269 + char_table_start),
    "ヘ" : int(270 + char_table_start),
    "ベ" : int(271 + char_table_start),
    "ペ" : int(272 + char_table_start),
    "ホ" : int(273 + char_table_start),
    "ボ" : int(274 + char_table_start),
    "ポ" : int(275 + char_table_start),
    "マ" : int(276 + char_table_start),
    "ミ" : int(277 + char_table_start),
    "ム" : int(278 + char_table_start),
    "メ" : int(279 + char_table_start),
    "モ" : int(280 + char_table_start),
    "ャ" : int(281 + char_table_start),
    "ヤ" : int(282 + char_table_start),
    "ュ" : int(283 + char_table_start),
    "ユ" : int(284 + char_table_start),
    "ョ" : int(285 + char_table_start),
    "ヨ" : int(286 + char_table_start),
    "ラ" : int(287 + char_table_start),
    "リ" : int(288 + char_table_start),
    
    "レ" : int(290 + char_table_start),
    "ロ" : int(291 + char_table_start), # Might be wrong?
    
    "ヮ" : int(292 + char_table_start),
    "ワ" : int(293 + char_table_start),
    "ヲ" : int(294 + char_table_start),
    "ン" : int(295 + char_table_start),
    "ヴ" : int(296 + char_table_start),
    "ヵ" : int(297 + char_table_start),
    "ヶ" : int(298 + char_table_start),
    
    "!" : int(303 + char_table_start),
    "?" : int(304 + char_table_start),
    
    ":" : int(314 + char_table_start),
    
    "♂" : int(321 + char_table_start),
    "♀" : int(322 + char_table_start),
    "♪" : int(323 + char_table_start),
    "~" : int(324 + char_table_start),
    "→" : int(325 + char_table_start),
    
    "で": int(0x2573),
    
    "よ": int(0x8963),
    "ろ": int(0x8945),
    "ム": int(0x894A),
    
    "%": int(0x95D7),
    
    "内" : int(2271 + char_table_start),
    "南" : int(2273 + char_table_start),
    "軟" : int(2274 + char_table_start),
    "難" : int(2275 + char_table_start),
    "二" : int(2276 + char_table_start),
    "尼" : int(2277 + char_table_start),
    "弐" : int(2278 + char_table_start),
    "肉" : int(2279 + char_table_start),
    "日" : int(2280 + char_table_start),
    "乳" : int(2281 + char_table_start),
    "入" : int(2282 + char_table_start),
    "尿" : int(2283 + char_table_start),
    
    "熟" : int(0x9190),
    "年" : int(0x9191),
    "念" : int(0x9192),
    
    "中" : int(0x9091),
    "ゅ" : int(0x8971),
    "弟" : int(0x90d0),
    "を" : int(0x894c),
    "抜" : int(0x91c4),
    "差" : int(0x8d4d),
    "だ" : int(0x8960),
    "。" : int(0x8950),
    
    "攻" : int(0x8ccb),
    "撃" : int(0x8c63),
    "力" : int(0x93c8),
    "重" : int(0x8e61),
    "視" : int(0x8dae),
    "げ" : int(0x8959),
    "り" : int(0x8947),
    "ょ" : int(0x8972),
    
    "範" : int(0x91d5),
    "囲" : int(0x89f3),
    "ん" : int(0x894d),
    "広" : int(0x8cc2),
    "め" : int(0x8941),
    "射" : int(0x8dd9),
    "ゃ" : int(0x8970),
    "近" : int(0x8beb),
    
    "当" : int(0x9148),
    "る" : int(0x8948),
    "大" : int(0x9059),
    "が" : int(0x8956),
    "、" : int(0x894f),
    "弾" : int(0x9076),
    
    "数" : int(0x8f53),
    "ず" : int(0x895d),
    "飛" : int(0x91f3),
    "距" : int(0x8bbb),
    "離" : int(0x93ac),
    "が" : int(0x8956),
    "落" : int(0x939e),
    "る" : int(0x8948),
    
    "注" : int(0x9099),
    "意" : int(0x89f7),
    "が" : int(0x8956),
    "必" : int(0x91fa),
    "要" : int(0x938e),
    "ル" : int(0x89c0),
    
    "軍" : int(0x8c42),
    "來" : int(0x939a),
    "襲" : int(0x8e53),
    "緊" : int(0x8be7),
    "急" : int(0x8ba6),
    "." : int(0x89d8),
    "对" : int(0x3135),
    "地" : int(0x9048),
    "衝" : int(0x8e9d),
    "空" : int(0x8bf4),
    
    "交" : int(0x8cb1),
    "代" : int(0x9057),
    "ム" : int(0x89b5),
    "選" : int(0x8fa8),
    "ら" : int(0x8946),
    "戻" : int(0x93d8),
    "も" : int(0x8942),
    "ど" : int(0x8964),
    
    "作" : int(0x8d6d),
    "成" : int(0x8f60),
    "か" : int(0x88e2),
    "本" : int(0x92e0),
    "体" : int(0x9046),
    "電" : int(0x90f0),
    
    "源" : int(0x8c91),
    "切" : int(0x8f87),
    "失" : int(0x8dd0),
    "敗" : int(0x91a6),
    "他" : int(0x8ffc),
    "東" : int(0x914d),
    "京" : int(0x8bbf),
    
    "新" : int(0x8ee5),
    "宿" : int(0x8e64),
    "秋" : int(0x8e4d),
    "葉" : int(0x938d),
    "原" : int(0x8c8c),
    "結" : int(0x8c6a),
    "果" : int(0x8a9e),
    
    "翼" : int(0x9397),
    "ば" : int(0x8966),
    "形" : int(0x8c4c),
    "れ" : int(0x8949),
    "装" : int(0x8fda),
    "備" : int(0x91f4),
    "び" : int(0x8967),
    "羽" : int(0x8a56),
    "ば" : int(0x8966),
    "様" : int(0x9387),
    "天" : int(0x90e7),
    "使" : int(0x8d8e),
    "美" : int(0x91f7),
    "見" : int(0x8c83),
    
    "型" : int(0x8c4a),
    "火" : int(0x8aa3),
    "炎" : int(0x8a75),
    "放" : int(0x92b5),
    "砲" : int(0x92ba),
    "爆" : int(0x91bc),
    "発" : int(0x91c1),
    
    "じ" : int(0x895c),
    "小" : int(0x8e97),
    "回" : int(0x8ab9),
    "わ" : int(0x894b),
    "転" : int(0x90ec),
    "誘" : int(0x9374),
    "導" : int(0x9169),
    "ゆ" : int(0x8944),
    
    "高" : int(0x8ceb),
    "速" : int(0x8fef),
    "移" : int(0x89fc),
    "動" : int(0x9167),
    "ぎ" : int(0x8957),
    "や" : int(0x8943),
    "面" : int(0x934e),
    "っ" : int(0x8965),
    
    "性" : int(0x8f5f),
    "能" : int(0x9196),
    "劣" : int(0x93e3),
    "持" : int(0x8dc0),
    "得" : int(0x9170),
    "弓" : int(0x8ba5),
    "走" : int(0x8fdb),
    "行" : int(0x8cc4),
    
    "右" : int(0x8a54),
    "自" : int(0x8dc9),
    "由" : int(0x9366),
    "操" : int(0x8fcd),
    "ぶ" : int(0x8968),
    "壁" : int(0x9293),
    "へ" : int(0x8969),
    "向" : int(0x8cba),

    "む" : int(0x8940),
    "敵" : int(0x90dc),
    "狙" : int(0x95d0),
    "便" : int(0x929d),
    "利" : int(0x93a5),
    "衛" : int(0x8a5c),
    "星" : int(0x8f63),
    
    "音" : int(0x8a90),
    "量" : int(0x93c5),
    "択" : int(0x905e),
    "遠" : int(0x8a79),
    "弱" : int(0x8dec),
    "多" : int(0x9040),
    "特" : int(0x9172),
    "徵" : int(0x90a7),

    "連" : int(0x93e9),
    "一" : int(0x8a47),
    "威" : int(0x89f5),
    "ろ" : int(0x894a),
    "消" : int(0x8ea7),
    "費" : int(0x91f0),
    "好" : int(0x8cbd),
    "瞬" : int(0x8e70),
    
    "間" : int(0x8b5a),
    "ご" : int(0x895a),
    "何" : int(0x8a94),
    "直" : int(0x90ba),
    "風" : int(0x926d),
    "効" : int(0x8cb7),
    "少" : int(0x8e98),
    "巨" : int(0x8bb3),

    "強" : int(0x8bc8),
    "へ" : int(0x88f9),
    "殊" : int(0x8df3),
    "個" : int(0x8c96),
    "人" : int(0x8ef7),
    "戦" : int(0x8f9a),
    
    "央" : int(0x8a7d),
    "通" : int(0x90c4),
    "地" : int(0x907d),
    "下" : int(0x8a91),
    "基" : int(0x8b6b),
    "ぐ" : int(0x8958),
    "輸" : int(0x9369),
    "送" : int(0x8fdc),
    
    "部" : int(0x926c),
    "隊" : int(0x9056),
    "兵" : int(0x928a),
    "器" : int(0x8b6a),
    "運" : int(0x8a58),
    "込" : int(0x94a0),
    "よ" : int(0x8945),
    "搬" : int(0x91ce),
    
    "阻" : int(0x8fbe),
    "止" : int(0x8da4),
    "破" : int(0x919e),
    "前" : int(0x8fae),
    "探" : int(0x906c),
    "壊" : int(0x8abb),
    "設" : int(0x8f8e),
    "置" : int(0x9084),
    
    "十" : int(0x8e5a),
    "分" : int(0x9284),
    "川" : int(0x8f99),
    "崎" : int(0x94b0),
    "方" : int(0x92b6),
    "建" : int(0x8c76),
    "情" : int(0x8ec7),
    "報" : int(0x92af),
    
    "品" : int(0x924d),
    "経" : int(0x8c57),
    "上" : int(0x8ebd),
    "達" : int(0x9065),
    "占" : int(0x8f96),
    "領" : int(0x93c7),
    "危" : int(0x8b68),
    "険" : int(0x8c88),
    "駅" : int(0x8a68),
    "目" : int(0x9357),
    "指" : int(0x8d9d),
    "さ" : int(0x895b),
    
    "さ" : int(0x88e7),
    "で" : int(0x8963),
    "べ" : int(0x8969),
    "倒" : int(0x9140),
    "引" : int(0x8a4e),
    "続" : int(0x8ff3),
    "づ" : int(0x8962),
    "出" : int(0x8e6b),
    
    "付" : int(0x9255),
    "潜" : int(0x8fa2),
    "伏" : int(0x926f),
    "咫" : int(0x896d),
    "甲" : int(0x8cd4),
    "浮" : int(0x9260),
    "抛" : int(0x8bb8),
    "点" : int(0x90eb),
    
    "評" : int(0x9247),
    "価" : int(0x8a95),
    "獲" : int(0x8ada),
    "途" : int(0x90f6),
    "集" : int(0x8e56),
    "計" : int(0x8c5b),
    "最" : int(0x8d5b),
    "終" : int(0x8e4e),
    
    "変" : int(0x9297),
    "更" : int(0x8ccc),
    "制" : int(0x8f59),
    "限" : int(0x8c95),
    "合" : int(0x8cef),
    "功" : int(0x8cb6),
    "手" : int(0x8df1),
    "ば" : int(0x896b),
    "ば" : int(0x8966),
    "光" : int(0x8cb4),
    "線" : int(0x8fa3),
    "ぞ" : int(0x895f),
    "早" : int(0x8fce),
    
    "定" : int(0x90cb),
    "画" : int(0x8ab1),
    "式" : int(0x8dcb),
    "以" : int(0x89ee),
    "容" : int(0x9380),
    "開" : int(0x8aca),
    "始" : int(0x8d95),
    "雷" : int(0x939b),
    
    "斬" : int(0x95d8),
    "氷" : int(0x9243),
    "満" : int(0x92f2),
    "月" : int(0x8c6c),
    "ぜ" : int(0x895e),
    "ぼ" : int(0x896f),
    "稲" : int(0x9155),
    
    "妻" : int(0x8d56),
    "並" : int(0x9288),
    "技" : int(0x8b8e),
    "ざ" : int(0x895b),
    "掃" : int(0x8fcc),
    "改" : int(0x8ac2),
    "造" : int(0x8fe6),
    "対" : int(0x9048),
    
    "次" : int(0x8dc2),
    "予" : int(0x937a),
    "準" : int(0x8e75),
    "決" : int(0x8c67),
    "勝" : int(0x8e90),
    "編" : int(0x9299),
    "乱" : int(0x93a0),
    "舞" : int(0x926b),
    "艦" : int(0x8b55),
    "解" : int(0x8ac9),
    "除" : int(0x8e8c),
    
    "追" : int(0x90c2),
    "加" : int(0x8a97),
    "与" : int(0x9379),
    "複" : int(0x9276),
    "同" : int(0x9166),
    "時" : int(0x8dc1),
    "增" : int(0x8fe1),
    "減" : int(0x8c90),
    
    "復" : int(0x9272),
    "生" : int(0x8f69),
    "遅" : int(0x9086),
    "現" : int(0x8c93),
    "納" : int(0x9199),
    "男" : int(0x907a),
    "那" : int(0x955d),
    "奈" : int(0x955e),
    
    "茄" : int(0x955f),
    "耶" : int(0x9560),
    "凪" : int(0x9561),
    "汀" : int(0x9562),
    "渚" : int(0x9563),
    "捺" : int(0x9564),
    "仁" : int(0x8ef8),
    "児" : int(0x8dbc),
    
    "若" : int(0x8ded),
    "柔" : int(0x8e5c),
    "女" : int(0x8e88),
    "如" : int(0x8e89),
    "虹" : int(0x9565),
    "錦" : int(0x9566),
    "主" : int(0x8dee),
    "布" : int(0x9259),
    "沼" : int(0x8ea6),
    "乃" : int(0x9567),
    "之" : int(0x9568),
    
    "漂" : int(0x9244),
    "黑" : int(0x8cf9),
    "服" : int(0x9273),
    "白" : int(0x91b7),
    "衣" : int(0x8a42),
    "唯" : int(0x936a),
    "外" : int(0x8acd),
    "着" : int(0x9090),
    
    #"[TRIANGLE]" : int(0x89cd),
    #"[CIRCLE]" : int(0x89ca),
    #"[CROSS]" : int(0x89cb),
    #"[SQUARE]" : int(0x89cc),
    "枚" : int(0x92ea),
    "刀" : int(0x9143),
    "說" : int(0x8f8f),
    "気" : int(0x8b7c),
    
    "打" : int(0x9044),
    "用" : int(0x938a),
    "突" : int(0x9179),
    "道" : int(0x916d),
    "具" : int(0x8bf2),
    "段" : int(0x9079),
    "召" : int(0x8e92),
    "喚" : int(0x8af5),
    
    "横" : int(0x8a84),
    "浜" : int(0x924e),
    "乗" : int(0x8ebf),
    "思" : int(0x8d9c),
    "反" : int(0x91cb),
    "応" : int(0x8a81),
    "場" : int(0x8ec3),
    "存" : int(0x8ff7),
    
    "在" : int(0x8d68),
    "匹" : int(0x91f9),
    "び" : int(0x896c),
    "逃" : int(0x915f),
    "事" : int(0x8db9),
    "態" : int(0x904d),
    "謎" : int(0x95cb),
    "物" : int(0x927b),
    
    "頑" : int(0x8b64),
    "丈" : int(0x8ebe),
    "迷" : int(0x9348),
    "彩" : int(0x8d58),
    "模" : int(0x934f),
    
    "世" : int(0x8f57),
    "騎" : int(0x8b88),
    "士" : int(0x8d94),
    "冑" : int(0x95d9),
    "格" : int(0x8ad7),
    "西" : int(0x8f6f),
    "劇" : int(0x8c62),
    "保" : int(0x92a0),
    
    "安" : int(0x89eb),
    "官" : int(0x8af8),
    "名" : int(0x9345),
    "偵" : int(0x90c8),
    "「" : int(0x95db),
    "」" : int(0x95dc),
    "語" : int(0x8cae),
    "尾" : int(0x91f5),
    "び" : int(0x8967),
    "不" : int(0x9254),
    "議" : int(0x8b94),
    
    "ば" : int(0x896b),
    "削" : int(0x8d6e),
    "明" : int(0x9346),
    "派" : int(0x919d),
    "珍" : int(0x90bd),
    "子" : int(0x8d98),
    "北" : int(0x92d7),
    "欧" : int(0x8a85),
    
    "忍" : int(0x918d),
    "者" : int(0x8ddf),
    "添" : int(0x90ea),
    "真" : int(0x8eeb),
    "赤" : int(0x8f84),
    "知" : int(0x9082),
    "証" : int(0x8eb6),
    "可" : int(0x8a98),
    "殺" : int(0x8d7b),
    
    "魔" : int(0x92e6),
    "法" : int(0x92b8),
    "隕" : int(0x95e3),
    "石" : int(0x8f7e),
    "雨" : int(0x8a57),
    "降" : int(0x8ce8),
    "援" : int(0x8a72),
    "護" : int(0x8cb0),
    
    "裏" : int(0x93aa),
    "剣" : int(0x8c72),
    "旋" : int(0x8f9c),
    "王" : int(0x8a87),
    "呪" : int(0x95e4),
    "歌" : int(0x8aa0),
    "姫" : int(0x9571),
    "球" : int(0x8bac),
    
    "慢" : int(0x92f1),
    "文" : int(0x9285),
    "章" : int(0x8eb1),
    "全" : int(0x8fad),
    "身" : int(0x8ef2),
    "ば" : int(0x8966),
    "悪" : int(0x89e8),
    "水" : int(0x8f47),
    
    "・" : int(0x89d7),
    "狩" : int(0x8df4),
    "警" : int(0x8c5c),
    "察" : int(0x8d77),
    "逮" : int(0x9055),
    "捕" : int(0x92a2),
    "根" : int(0x8d46),
    "ぼ" : int(0x896a),
    
    "至" : int(0x8dad),
    "収" : int(0x8e43),
    "家" : int(0x8a9b),
    "車" : int(0x8de1),
    "再" : int(0x8d55),
    "墜" : int(0x90c1),
    "遭" : int(0x8fdd),
    "遇" : int(0x8bf6),
    "期" : int(0x8b77),
    
    "び" : int(0x896c),
    "古" : int(0x8c97),
    "半" : int(0x91ca),
    "漁" : int(0x8bbd),
    "相" : int(0x8fd3),
    "先" : int(0x8f94),
    "表" : int(0x9246),
    "示" : int(0x8dc7),
    "確" : int(0x8adb),
    "認" : int(0x918e),
    
    "び" : int(0x8967),
    "足" : int(0x8fee),
    "歩" : int(0x92a3),
    "迎" : int(0x8c60),
    "退" : int(0x9054),
    "想" : int(0x8fc9),
    "避" : int(0x91f1),
    "展" : int(0x90e8),
    
    "楽" : int(0x8ae6),
    "映" : int(0x8a5d),
    "像" : int(0x8fe0),
    "伊" : int(0x9457),
    "遊" : int(0x9375),
    "会" : int(0x8ab8),
    "進" : int(0x8ef4),
    "諦" : int(0x95ca),
    "伸" : int(0x8edb),
    "階" : int(0x8acb),
    "+" : int(0x89d3),
    
    "字" : int(0x8dbd),
    "漢" : int(0x8b4c),
    "読" : int(0x9177),
    "取" : int(0x8def),
    "了" : int(0x93bc),
    "完" : int(0x8af7),
    "メ" : int(0x896b),
    "後" : int(0x8cab),
    "状" : int(0x8eca),
    "況" : int(0x8bd0),
    "受" : int(0x8dfb),
    "損" : int(0x8ffa),
    
    "メ" : int(0x89b6),
    "ば" : int(0x896b),
    "ぱ" : int(0x8966),
    
    "び" : int(0x896C),
    "ぴ" : int(0x8967),
  
}

# prepare inverse map
_decode_table = {v : k for k, v in _encode_table.items()}
    
def decode_jp_header(inBytes):
    a = struct.unpack(">BBBB", inBytes)
    
    return f"[HEADER {a[0] : >3} {a[1] : >3} {a[2] : >3} {a[3] : >3} ]"
    
    
def decode_jp(key):
    outStr = ""
    i = 0
    while(i < len(key)):
        # Check for control codes
        
        cctest = struct.unpack(">B", key[i:i + 1])[0]
        
        # End current line and start on next row
        if (cctest == 0x0A): 
            outStr += "[BREAK]"
            i += 1
            continue
        
        # Furigana start code (Text above JP Characters)
        if (cctest == 0x5B):
            outStr += "[FURIGANA "
            i += 1
            continue
            
        # Furigana end code (Text above JP Characters)
        if (cctest == 0x5D):
            outStr += "]"
            i += 1
            continue
            
        # Used in Mission Descriptions, ends the current page and creates a new one
        if (cctest == 0x3E):
            outStr += "[NEWPAGE]"
            i += 1
            continue
            
        # Only seen once in Mission 1 (Are there more occurances?)
        if (cctest == 0x20):
            outStr += "[SPACE]"
            i += 1
            continue
            
        try: # Script related control code to allow for context sensitive text (EX: How much space on Memory card)
            cctest = struct.unpack(">H", key[i:i + 2])[0]
            if (cctest == 0x2573):
                outStr += "[SCRIPT]"
                i += 2
                continue
        except: pass
        
        try: # JP Character, if this fails we don't account for this character yet so print the hexadecimal representation)
            # If this fails there aren't 2 characters to work with
            cctest = struct.unpack(">H", key[i:i + 2])[0]
            
            try:
                outStr += _decode_table[cctest]
                i += 2
            except:
                outStr += f"[{str(hex(cctest))}]"
                i += 2
        except:
            outStr += f"[{str(hex(cctest))}]"
            i += 1

    return outStr
    
def extract_input_filenames():
    outFiles = os.listdir(f"{BIN_INPUT_PATH}DATA1/")
    return outFiles
     
def extract_jp_text_to_dict(inFilename):
    outStrData = []
    outByteData = []
    with open(inFilename, 'rb') as f:
        s = f.read()
        
        s.find(TRANS_START_PATTERN)
        print(hex(s.find(TRANS_START_PATTERN)))
        
        # First, check if this file has any translation strings in it
        if(s.find(TRANS_START_PATTERN) != -1):
            # Seek to the translation strings
            f.seek( s.find(TRANS_START_PATTERN), 0)
            
            # Set cnt to a non-zero value, so we can start the while loop
            cnt = 255
        
            # We make the assumption that as long as the next string isn't length 0
            # There are more strings we need to parse
            idx = 0
            while(cnt != 0):
                strDictInst = {}
                strDictInst['header']  = bytearray()
                strDictInst['len']     = bytearray()
                strDictInst['bytes']   = bytearray()
                strDictInst['escape']  = bytearray()
                
                #print(f"String {idx : <4} {cnt : <4} {hex(f.tell() - 1)}")
                
                # First read the parameters for this string
                strDictInst['header'] += f.read(4)
                a = struct.unpack(">BBBB", strDictInst['header'])
                
                # Next read how big this string is
                strDictInst['len'] += f.read(4)
                cnt = int.from_bytes(strDictInst['bytes'], "little")
                
                # Then read in all the string bytes
                strDictInst['bytes'] += f.read(cnt)
                
                strDictInst['jpstr'] = f"[HEADER {a[0]} {a[1] : >3} {a[2] : >3} {a[3] : >3} {a[4] : >3} ]{decode_jp(cnt, strDictInst['bytes'][9:])}"
                if strDictInst not in outStrData:
                    outStrData.append(strDictInst)
                
                # Read the potential next string length
                f.seek(5, 1)
                test = f.read(1)
                test = int.from_bytes(test, "little")
                if(test == 0):
                    break;
                f.seek(-6, 1)
                
                idx += 1
        else:
            pass
            #print("No Translation strings in the file")
    return outStrData

def get_hash_from_bytes(inBytes):
    tempHash = hashlib.sha256()
    tempHash.update(inBytes)
    outHash = tempHash.hexdigest()
    return outHash

def split_string(inStr):
    # Split the string on [ and ] for control codes
    # We can then do some logic to check for control codes
    outStr = re.split('\[|\]', inStr)
    outStr[:] = [x for x in outStr if x]
    return outStr
    
def get_string_len(inStrList):
    strLen = 0
    for x in inStrList:
        # Control code for parameters for the following string
        if(x.find("HEADER", 0, 6) != -1):
            #print("HEADER LINE")
            continue
        # Control code break string for a new line
        if(x.find("BREAK", 0, 5) != -1 and len(x) == 5):
            #print("BREAK LINE")
            strLen += 1
            continue
        # Control code for new page in Mission Description
        if(x.find("NEWPAGE", 0, 7) != -1):
            #print("NEWPAGE LINE")
            strLen += 1
            continue
        # Control code found once in Mission 1 Description
        if(x.find("SPACE", 0, 5) != -1):
            #print("SPACE LINE")
            strLen += 1
            continue
        # Control code for script
        if(x.find("SCRIPT", 0, 6) != -1):
            #print("SCRIPT LINE")
            strLen += 2
            continue
        # Control code for furigana characters (chars above the line)
        # WARNING: This currently fails if the furigana scope contains an unmapped character
        if(x.find("FURIGANA", 0, 8) != -1):
            #print("FURIGANA LINE")
            tempStr = x.split(" ")
            tempStr[:] = [x for x in tempStr if x]
            #print(tempStr)
            strLen += 1
            for y in tempStr[1]:
                strLen += 2
            strLen += 1
            
            continue
        # Raw hexadecimal value, this has not been mapped yet
        if(x.find("0x", 0, 2) != -1):
            tempint = int(x, 0)
            #print(f"CODE: {tempint}")
            strLen += 2
            continue
        # If we get this far we are assuming these are not control codes
        #print("RAW CHARACTERS")
        for y in x:
            strLen += 2
        continue
    return strLen
    
def string_to_bytes(inStrList, inStrLen):
    outBytes = bytearray()
    for x in inStrList:
        # Control code for parameters for the following string
        if(x.find("HEADER", 0, 6) != -1):
            #print("HEADER LINE")
            tempStr = x.split(" ")
            tempStr[:] = [x for x in tempStr if x]
            outBytes += struct.pack("<B", int(tempStr[1]))
            outBytes += struct.pack("<B", int(tempStr[2]))
            outBytes += struct.pack("<B", int(tempStr[3]))
            outBytes += struct.pack("<B", int(tempStr[4]))
            #print(tempStr[1])
            #print(x)
            outBytes += struct.pack("<I", int(inStrLen))
            
            continue
        # Control code break string for a new line
        if(x.find("BREAK", 0, 5) != -1 and len(x) == 5):
            #print("BREAK LINE")
            outBytes += struct.pack("<B", 0x0A)
            continue
        # Control code for new page in Mission Description
        if(x.find("NEWPAGE", 0, 7) != -1):
            #print("NEWPAGE LINE")
            outBytes += struct.pack("<B", 0x3E)
            continue
        # Control code found once in Mission 1 Description
        if(x.find("SPACE", 0, 5) != -1):
            #print("SPACE LINE")
            outBytes += struct.pack("<B", 0x20)
            continue
        # Control code for script
        if(x.find("SCRIPT", 0, 6) != -1):
            #print("SCRIPT LINE")
            outBytes += struct.pack(">H", 0x2573)
            continue
        # Control code for furigana characters (chars above the line)
        if(x.find("FURIGANA", 0, 8) != -1):
            #print("FURIGANA LINE")
            tempStr = x.split(" ")
            tempStr[:] = [x for x in tempStr if x]
            outBytes += struct.pack("<B", 0x5B)
            for y in tempStr[1]:
                outBytes += _encode_table[y].to_bytes(2, 'big')
            outBytes += struct.pack("<B", 0x5D)
            #print(tempStr)
            continue
        # Raw hexadecimal value, this has not been mapped yet
        if(x.find("0x", 0, 2) != -1):
            tempint = int(x, 0)
            #print(f"CODE: {tempint}")
            #print(len(x))
            if len(x) > 4:
                outBytes += struct.pack(">H", tempint)
            else:
                outBytes += struct.pack(">B", tempint)
            continue
        # If we get this far we are assuming these are not control codes
        #print("RAW CHARACTERS")
        for y in x:
            try:
                outBytes += _encode_table[y].to_bytes(2, 'big')
            except:
                print(f"UNABLE TO PARSE STRING {x}")
                exit(1)
        continue
        
    return outBytes


# Class for handling the read / write operations related to a Million Monkeys String
class MMStrEntry:
    def __init__(self):
        self.header   = bytearray()
        self.strLen   = 0
        self.strbytes = bytearray()
        self.strHash  = None
        
    def read(self, inFile):
        # First, read the header for this string
        self.header = inFile.read(4)
        
        # Next, read in the string length in bytes
        self.strLen = int.from_bytes(inFile.read(4), "little")
        
        # Then, read in all the string bytes
        self.strbytes = inFile.read(self.strLen)
        
        # After, advance past the string terminator
        inFile.read(1)
        
        # Finally, calculate a hash for this string for fast lookups
        self.strHash = get_hash_from_bytes(bytes(self.pack_bytes_DATA1()))
        
    def readString(self, inString):
        strList = split_string(inString)
        self.strLen = get_string_len(strList)
        self.strbytes = string_to_bytes(strList, self.strLen)

    # Return a bytearray of how this string entry will look like in the DATA1.BIN file
    def pack_bytes_DATA1(self):
        # Init our bytearray
        outBytes = bytearray()
        
        # String header
        outBytes += self.header
        outBytes += struct.pack("<I", self.strLen)
        outBytes += self.strbytes
        outBytes += b'\x00' # String is null terminated
        
        return outBytes
        
    # Return a bytearray of how this string entry will look like while in game
    def pack_bytes_ingame(self):
        # Init our bytearray
        outBytes = bytearray()

        # String header
        outBytes += struct.pack("<I", self.strLen)
        outBytes += struct.pack("<I", self.strLen)
        outBytes += struct.pack("<I", 0x01)
        
        # String bytes
        outBytes += self.strbytes
        
        return outBytes
        
    def __eq__(self, other):
        return(self.strHash == other.strHash)
        
# Class for handling the reading / writing of the dat files found within DATA1.BIN
class MMDatFile:
    def __init__(self):
        self.filename       = None
        self.beforeStrings  = bytearray()
        self.stringCnt      = 0
        self.stringEntries  = []
        self.afterStrings   = bytearray()
        self.TransByteCount = 0

    # Read the input file into this class
    def read_dat_file(self, inFilePath, inFileName):
        self.filename = inFileName
        with open(inFilePath, 'rb') as f_in:
        
            # First, check if this file has any translation strings in it
            s = f_in.read()
            f_in.seek(0, 0)
            if(s.find(TRANS_START_PATTERN) == -1):
                print(f"[{inFilePath}] - No translation strings in file")
                return False
            else:
                print(f"[{inFilePath}] - Found translation strings ")  
            
            # If we got this far we have translation strings, lets pick this file apart
            self.beforeStrings = f_in.read(s.find(TRANS_START_PATTERN))
            
            # Read in all the translation strings
            self.stringCnt = int.from_bytes(self.beforeStrings[-4:], 'little')
            for x in range(self.stringCnt):
                thisStrEntry = MMStrEntry()
                thisStrEntry.read(f_in)
                self.TransByteCount += thisStrEntry.strLen
                self.stringEntries.append(thisStrEntry)
                
            # Read the rest of the file
            self.afterStrings = f_in.read()
        
        return True
    
    # Write out this file
    def write_dat_file(self):
        # First we write out the uncompressed dat file as is
        with open(f"{BIN_INT_PATH}{self.filename}", 'wb') as f_out:
            f_out.write( self.beforeStrings )
            
            for strEntry in self.stringEntries:
                f_out.write( strEntry.pack_bytes_DATA1() )
            
            f_out.write( self.afterStrings )    
            
        # Then we'll write out the gzip compressed file
        with open(f"{BIN_INT_PATH}{self.filename}", 'rb') as mf_in:
            with gzip.open(f"{BIN_INT_PATH}{self.filename}.gz", 'wb') as f_out:
                shutil.copyfileobj(mf_in, f_out)




