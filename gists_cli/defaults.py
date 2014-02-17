#!/usr/bin/env python

#-------------------------------------------

public = False
description = ""
content = "No Content"
file = "default.md"
download = True
max_width = 100
forceDelete = True

cmds = {}
cmds['#'] = ['#','.','%',':']
cmds['Help'] = ["help", "--help", "h", "-h"]
cmds['Token'] = ["token", "--token", "t", "-t"]
cmds['List'] = ["list", "--list", "l", "-l"]
cmds['View'] = ["view", "--view", "v", "-v"]
cmds['Download'] = ["get", "--get", "g", "-g"]
cmds['Update'] = ["update", "--update", "u", "-u"]
cmds['Append'] = ["append", "--append", "a", "-a"]
cmds['Delete'] = ["delete", "--delete", "del", "--del", "d", "-d"]
cmds['Backup'] = ["backup", "--backup", "b", "-b"]
cmds['Search'] = ["search", "--search", "query", "--query", "q", "-q"]
cmds['New'] = ["new", "--new", "n", "-n", "create", "--create", "c", "-c"]
cmds['Debug'] = ["debug","--debug"]
cmds['Supress'] = ["silent","--silent","supress","--supress"]
cmds['all'] = cmds['Help'] + cmds['Token'] + cmds['List'] + cmds['View'] + cmds['Download'] + cmds['Update'] + cmds['Append'] + cmds['Delete'] + cmds['Backup'] + cmds['Search'] + cmds['New']
