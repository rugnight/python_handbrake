# -*- coding: utf-8 -*-

import sys
import commands
import handbrake_media as HB

#( all | chapter | setting_file )

# 引数の処理
argvs = sys.argv;
argc  = len(argvs)

TARGET_FILE = argvs[1]      # 変換対象ファイル名

#HB_COMMAND = "HandBrakeCLI -i %s -t %s" % (TARGET_FILE, "0")
HB_COMMAND = "ls"

results    = commands.getstatusoutput(HB_COMMAND)
media_info = results[1]
print media_info 

exit()

f = open("dvdinfo", "r")
media = HB.HandBrakeMedia()
media.set(f)
media.dump()

# メディアがどういう物か？
analyse = HandBrakeMediaAnalyser()

# メディアにあった変換ルールがあるか？

# 

f.close()

