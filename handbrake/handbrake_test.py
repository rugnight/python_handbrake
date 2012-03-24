# -*- coding: utf-8 -*-

# ==================================================
# 
#   使い方
#       convert_media SRC DST SETTING_FILE
# 
#   設定ファイル
#       TITLE_VALID_DURATION    00:00:10
#       CHAPTER_SPRIT           4
# ==================================================

import sys
import commands
import handbrake_media as HB

Usage = "Usage: python convert_media.py SRC DST_DIR SETTING_FILE"

# 引数の処理
argvs = sys.argv;
argc  = len(argvs)

if argc < 4:
    print Usage 
    exit()

TARGET_FILE  = argvs[1]      # 変換対象ファイル名
OUTPUT_DIR   = argvs[2]      # 出力先ディレクトリ名
SETTING_FILE = argvs[3]      # 設定ファイル

# 映像メディアの情報を取得
HB_RESEARCH_COMMAND = "HandBrakeCLI -i %s -t %s" % (TARGET_FILE, "0")
research_cmd_return = commands.getstatusoutput(HB_RESEARCH_COMMAND)
research_result = research_cmd_return[0]
research_lines  = research_cmd_return[1]

# なんか失敗
if research_result == 0:
    print "DVD情報の取得に失敗しました\n"
    exit()

# メディアの情報
media = HB.HandBrakeMedia()
media.set(research_lines)
media.dump()

exit()

#HB_COMMAND = "HandBrakeCLI -i %s -t %s" % (TARGET_FILE, "0")
HB_COMMAND = "ls"

results    = commands.getstatusoutput(HB_COMMAND)
media_info = results[1]
print media_info 

media = HB.HandBrakeMedia()
media.set(f)

# メディアがどういう物か？
analyse = HandBrakeMediaAnalyser()
