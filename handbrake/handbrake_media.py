# -*- coding: utf-8 -*-

import re
import sys
import string
import commands

# ==================================================
class HandBrakeChapter:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no          = 0
        self.cells_begin = 0
        self.cells_end   = 0
        self.blocks      = 0
        self.hour        = 0
        self.minute      = 0
        self.second      = 0
    # ------------------------------
    def set(self, hb_chapter_line):
        # 与えられた文字列がチャプター情報かどうか
        if re.match(r"^\s{4,4}\+\s(\d+?): cells", hb_chapter_line) == None:
            return False

        # + と : と , を削除
        hb_chapter_line = hb_chapter_line.translate(string.maketrans("", ""), "+,")
        hb_chapter_line = hb_chapter_line.replace(":", " ")
        hb_chapter_line = hb_chapter_line.replace("->", " ")
        # 先頭と末尾の空白を除去
        hb_chapter_line = hb_chapter_line.strip()

        # 情報を抽出
        list = hb_chapter_line.split(" ")
        self.no          = int(list[0])
        self.cells_begin = int(list[3])
        self.cells_end   = int(list[4])
        self.blocks      = int(list[5])
        self.hour        = int(list[8])
        self.minute      = int(list[9])
        self.second      = int(list[10])
        return True
    # ------------------------------
    def dump(self):
        print "    %d: cells %d->%d, %d blocks, duration %02d:%02d:%02d" % (self.no, self.cells_begin, self.cells_end, self.blocks, self.hour, self.minute, self.second)

# ==================================================
class HandBrakeAudioTrack:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no     = 0
        self.locale = ""
    # ------------------------------
    def set(self, line):
        # 与えられた文字列が音声情報か
        if re.match(r"^\s{4,4}\+\s(\d+?),\s(Japanese|English)\s(\(AC3\)|\(DTS\)|\(LPCM\))", line) == None:
            return False
        # 先頭と末尾の空白を除去
        list = line.translate(string.maketrans("", ""), "+,()").strip().split()
        self.no     = int(list[0])
        self.locale = list[1]
        return True
    # ------------------------------
    def dump(self):
        print "    %d, %s" % (self.no, self.locale)

# ==================================================
class HandBrakeSubtitleTrack:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no     = 0
        self.locale = ""
    # ------------------------------
    def set(self, line):
        # 与えられた文字列がサブタイトル情報か
        # オーディオ情報と似ているので、先にオーディオ情報化を調べてください
        if re.match(r"^\s{4,4}\+\s(\d+?),\s(Japanese|English)", line) == None:
            return False
        # 先頭と末尾の空白を除去
        list = line.translate(string.maketrans("", ""), "+,()").strip().split()
        self.no     = int(list[0])
        self.locale = list[1]
        return True
    # ------------------------------
    def dump(self):
        print "    %d, %s" % (self.no, self.locale)

# ==================================================
class HandBrakeTitle:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no     = 0
        self.hour   = 0
        self.minute = 0
        self.second = 0

        self.chapters  = []
        self.audios    = []
        self.subtitles = []
    # ------------------------------
    def set_title_line(self, line):
        line = line.replace(":", "")
        list = line.split(" ")
        self.no = int(list[2])
    # ------------------------------
    def set_duration(self, line):
        match = re.search(r"\d\d:\d\d:\d\d", line)
        if match != None:
            list = match.group().split(":")
            self.hour   = int(list[0])
            self.minute = int(list[1])
            self.second = int(list[2])
    # ------------------------------
    def add_chapter(self, chapter):
        self.chapters.append(chapter)
    # ------------------------------
    def add_audio_track(self, audio_track):
        self.audios.append(audio_track)
    # ------------------------------
    def add_subtitle_track(self, subtitle_track):
        self.subtitles.append(subtitle_track)
    # ------------------------------
    def set(self, line):
        chapter        = HandBrakeChapter()
        audio_track    = HandBrakeAudioTrack()
        subtitle_track = HandBrakeSubtitleTrack()

        if re.match(r"^\+\stitle", line) != None:
            self.set_title_line(line)
        elif re.match(r"^\s{2,2}\+\s(duration)", line) != None:
            self.set_duration(line)
        elif chapter.set(line) == True:
            self.add_chapter(chapter) # 各チャプター情報の行マッチ
        elif audio_track.set(line) == True:
            self.add_audio_track(audio_track)
        #elif subtitle_track.set(line) == True:
        #    self.add_subtitle_track(subtitle_track)

    # ------------------------------
    def dump(self):
        print "title %d" % self.no
        print "  duration %02d:%02d:%02d" % (self.hour, self.minute, self.second)
        self.dump_chapters()
        self.dump_audios()
        self.dump_subtitles()
    # ------------------------------
    def dump_chapters(self):
        if len(self.chapters) == 0:
            return
        print "  chapters %d" % len(self.chapters)
        for chapter in self.chapters:
            chapter.dump()
    # ------------------------------
    def dump_audios(self):
        if len(self.audios) == 0:
            return
        print "  audios"
        for track in self.audios:
            track.dump()
    # ------------------------------
    def dump_subtitles(self):
        if len(self.subtitles) == 0:
            return
        print "  subtitles"
        for track in self.subtitles:
            track.dump()

# ==================================================
class HandBrakeMedia:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.name   = ""
        self.titles = []
    # ------------------------------
    def set(self, media_file):
        self.name   = media_file
        # 映像メディアの情報を取得
        HB_RESEARCH_COMMAND = "HandBrakeCLI -i %s -t %s" % (self.name, "0")
        research_cmd_return = commands.getstatusoutput(HB_RESEARCH_COMMAND)
        research_result = research_cmd_return[0]
        research_lines  = research_cmd_return[1].split("\n")

        # リサーチコマンドがなんか失敗
        if research_result != 0:
            print "failed research command : %s" % HB_RESEARCH_COMMAND 
            print research_lines
            return False

        title = None
        for line in research_lines:
            # 先頭が `+` で始まる行ならばtitleの開始位置
            if re.match(r"^\+", line) != None:
                if title != None:
                    self.titles.append(title)
                title = HandBrakeTitle()
                title.set(line)
            # 先頭が空白1～4個かつ`+` で始まる行ならばtitle内の情報
            elif re.match(r"^\s{1,4}\+\s", line) != None:
                title.set(line)
            else:
                if title != None:
                    self.titles.append(title)
                    title = None
        # タイトル見つからなかった
        if len(self.titles) < 1:
            return False
        return True

    # ------------------------------
    def dump(self):
        for title in self.titles:
            title.dump()
