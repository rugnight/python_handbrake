# -*- coding: utf-8 -*-

# ==================================================
#   使い方
#       convert_media SRC DST SETTING_FILE
# 
#   設定ファイル
#       TITLE_VALID_DURATION    00:00:10
#       CHAPTER_SPRIT           4
# ==================================================

import sys
import commands
import handbrake_media as HB_MEDIA
import handbrake_setting as HB_SETTING
import handbrake_commander as HB_COMMANDER

Usage = "Usage: python convert_media.py SRC_MEDIA DST_DIR SETTING_FILE"

# 引数の処理
argvs = sys.argv;
argc  = len(argvs)

if argc < 4:
    print Usage 
    exit()

TARGET_FILE  = argvs[1]      # 変換対象ファイル名
OUTPUT_DIR   = argvs[2]      # 出力先ディレクトリ名
SETTING_FILE = argvs[3]      # 設定ファイル

# メディアの情報
media = HB_MEDIA.HandBrakeMedia()
if media.set(TARGET_FILE) == False:
    print "this media have no titles"
    exit()

# 設定ファイル読み込み
setting = HB_SETTING.HandBrakeSetting()
if setting.set(SETTING_FILE) == False:
    print "invalid setting file"
    exit()

# HandBrake実行コマンドを生成
commands = HB_COMMANDER.HandBrakeCommander()
if commands.set(media, setting, OUTPUT_DIR) == False:
    print "command generate failed"
    exit()

commands.dump()    
print "done..."
exit()
