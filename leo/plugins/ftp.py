#@+leo-ver=cub-1-thin
#@0 [ekr.20110110105526.5463] @f ../plugins/ftp.py
"""Uploading of file by ftp."""

# 0.1 05.01.2011 by Ivanov Dmitriy.
#@+<< ftp imports >>
#@> << ftp imports >>
import json
import os
from ftplib import FTP
from leo.core import leoGlobals as g
from leo.core import leoPlugins
from leo.core.leoQt import QAction

#
# Fail fast, right after all imports.
g.assertUi('qt')  # May raise g.UiTypeException, caught by the plugins manager.


#@-<< ftp imports >>
#@+others
#@ init
def init():
    """Return True if the plugin has loaded successfully."""
    if g.app.gui.guiName() != "qt":
        print('ftp.py plugin not loading because gui is not Qt')
        return False
    leoPlugins.registerHandler("after-create-leo-frame", onCreate)
    g.plugin_signon(__name__)
    return True


#@ onCreate
def onCreate(tag, keys):
    c = keys.get('c')
    if c:
        # Check whether the node @data ftp exists in the file being opened.
        # If so, create a button and register.
        p = g.findTopLevelNode(c, '@data ftp')
        if p:
            pluginController(c)


#@ class pluginController
class pluginController:
    #@+others
    #@> __init__(pluginController, ftp.py)
    def __init__(self, c):
        self.c = c
        ib_w = self.c.frame.iconBar.w
        action = QAction('Upload', ib_w)
        self.c.frame.iconBar.add(qaction=action, command=self.upload)

    #@ upload
    def upload(self, event=None):
        c = self.c
        p = c.p
        g.es("upload started")
        p = g.findTopLevelNode(c, '@data ftp')
        if p:
            files = json.loads(p.b)

            # credentials - array of (host, pass) of server,
            # to while the files must be uploaded I suggest that the locations must be the same.
            credentials = files[0]

            for element in credentials:
                g.es(element[0])
                ftp = FTP(element[0])
                ftp.login(element[1], element[2])
                #@+<<upload all the modified files>>
                #@> <<upload all the modified files>>
                #@@c
                for i in range(1, len(files)):
                    file = files[i]

                    n = len(file)
                    if n < 3:
                        file.append(-1)

                    time = os.path.getmtime(file[0])
                    if time != file[2]:
                        files[i][2] = time
                        g.es(files[i][0])
                        FH = open(files[i][0], "rb")
                        ftp.storbinary('STOR ' + files[i][1], FH)
                        FH.close()
                #@-<<upload all the modified files>>

                ftp.quit()
                p.b = json.dumps(files)

            g.es("Upload complete")

    #@-others


#@-others
#@@language python
#@@tabwidth -4
#@-leo
