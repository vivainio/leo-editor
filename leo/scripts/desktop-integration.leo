<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
  <v t="lkj.20190711235336.1"><vh>Readme</vh></v>
  <v t="maphew.20191007115950.1"><vh>draft</vh>
    <v t="maphew.20191007120048.1"><vh>@adoc desktop-integration.adoc</vh>
      <v t="maphew.20191007115940.1"><vh>Creating Windows file associations</vh>
        <v t="maphew.20191007120254.1"><vh>Desktop Integration</vh></v>
        <v t="maphew.20191007120341.1"><vh>Register Leo</vh></v>
      </v>
    </v>
  </v>
  <v t="ekr.20070615131954"><vh>Startup</vh>
    <v t="ekr.20150302053516.3"><vh>@settings</vh>
      <v t="mhw.20181210131101.1"><vh>@bool put-expansion-bits-in-leo-files = False</vh></v>
    </v>
    <v t="ekr.20070427110751"><vh>@chapters</vh></v>
    <v t="maphew.20190712113401.1"><vh>@ignore</vh>
      <v t="maphew.20190712113412.1"><vh>@button script-button</vh></v>
    </v>
    <v t="maphew.20190712112935.1"><vh>Buttons</vh>
      <v t="maphew.20190712110256.1"><vh>@button Register Leo</vh>
        <v t="mhw-debug-1081.20190216130451.1"><vh>imports</vh></v>
        <v t="maphew.20130510011223.1645"><vh>docstring</vh></v>
        <v t="mhw-debug-1081.20190227224730.1"><vh>get_leo_libpath</vh></v>
        <v t="mhw-debug-1081.20190221070850.1"><vh>get_launch_leo</vh></v>
        <v t="maphew.20130509185752.1607"><vh>register_leo</vh>
          <v t="maphew.20130515233516.1659"><vh>&lt;&lt;filetype&gt;&gt;</vh></v>
          <v t="maphew.20130515233516.1660"><vh>&lt;&lt;association&gt;&gt;</vh></v>
        </v>
        <v t="mhw-debug-1081.20190314005003.1"><vh>relaunch_elevated</vh></v>
        <v t="mhw-debug-1081.20190314004045.1"><vh>get_my_path</vh></v>
        <v t="maphew.20190712112653.1"><vh>Main</vh></v>
      </v>
      <v t="maphew.20190712112409.1"><vh>@button Unregister Leo</vh>
        <v t="mhw-debug-1081.20190216130451.1"></v>
        <v t="mhw-debug-1081.20190216145532.1"><vh>unregister_leo</vh></v>
        <v t="mhw-debug-1081.20190314005003.1"></v>
        <v t="mhw-debug-1081.20190314004045.1"></v>
        <v t="maphew.20190712112633.1"><vh>Main</vh></v>
      </v>
      <v t="mhw.20190730140115.1"><vh>@button add-desktop-links</vh>
        <v t="mhw.20190808083214.1"><vh>main</vh></v>
      </v>
      <v t="mhw.20190806161400.1"><vh>@button remove-desktop-links</vh>
        <v t="mhw.20190808083336.1"><vh>main</vh></v>
      </v>
    </v>
  </v>
  <v t="lkj.20190712001203.1"><vh>scripts</vh>
    <v t="mhw.20190808082948.1"><vh>Any</vh>
      <v t="mhw.20190808083008.1"><vh>@f add-desktop-links.leox</vh></v>
      <v t="mhw.20190808083026.1"><vh>@f remove-desktop-links.leox</vh></v>
    </v>
    <v t="mhw-debug-1081.20190310203401.1"><vh>Windows</vh>
      <v t="maphew.20130611235500.2658"><vh>@f register-leo.leox</vh></v>
      <v t="maphew.20130611235500.2665"><vh>@f unregister-leo.leox</vh></v>
      <v t="ekr.20140704052551.17941"><vh>Notes</vh>
        <v t="maphew.20130510011223.1646"><vh>sample registry outcome</vh></v>
      </v>
    </v>
    <v t="lkj.20190711232707.1"><vh>Linux</vh></v>
    <v t="lkj.20190711232711.1"><vh>Mac</vh></v>
  </v>
</vnodes>
<tnodes>
  <t tx="ekr.20140704052551.17941">@language md

## Test for Leo association
If Leo files are not registered with Windows the following commands will return &quot;not found&quot; errors.

    reg query hkcr\leo.file
    reg query hkcr\.leo
    reg query hkcr\.leox


Example of success:

    C:\&gt; reg query hkcr\leo.file
    
    HKEY_CLASSES_ROOT\leo.file
        (Default)    REG_SZ    Leo Editor File
    
    HKEY_CLASSES_ROOT\leo.file\DefaultIcon
    HKEY_CLASSES_ROOT\leo.file\Shell</t>
  <t tx="lkj.20190711232707.1">{placeholder for future functions}</t>
  <t tx="lkj.20190711232711.1">{placeholder for future functions}</t>
  <t tx="lkj.20190711235336.1">_Desktop integration buttons (under the menu bar)_

## All Platforms - Linux, Mac, Windows ##

[add-desktop-links] - Creates launch shortcuts in desktop and system menu

[remove-desktop-links] - Removes the launch shortcuts


## Windows ## 

[Register-leo] - Creates registry keys for Leo file type and .leo file association. Afterwards .leo files will show Leo icon and double-clicking them will open in Leo Editor.

[Unregister-leo] - Removes the above


### Manually ###

From a Windows console with administrator privilege.

1. Define the Leo file type

Leo has been installed with pip:

    ftype LeoFile=&quot;&lt;path to python&gt;\Scripts\leo.exe&quot; &quot;%1&quot; %*

Running Leo from a source code copy:

    ftype LeoFile=&quot;&lt;path to python&gt;\pythonw.exe&quot; &quot;&lt;path to launchLeo.py&gt;\launchLeo.py&quot; &quot;%1&quot; %*


2. Associate Leo's file type

    assoc .leo=LeoFile

More info:
 - https://ss64.com/nt/ftype.html
 - https://superuser.com/questions/963464/find-path-of-standard-executable-for-a-given-file-type-in-windows</t>
  <t tx="maphew.20130509185752.1607">def register_leo(pyexe, launchLeo, icon):
    &quot;&quot;&quot;Create registry key for Leo file type, set default icon and launch command    
    &quot;&quot;&quot;
    g.es_print(&quot;Attempting to register leo filetype with Windows...&quot;)
    g.es_print(&quot;  Python:&quot;, pyexe)
    g.es_print(&quot;  Leo:&quot;, launchLeo)

    if g.os_path_exists(icon):
        g.es_print(&quot;  Found:&quot;, icon)
        &lt;&lt;filetype&gt;&gt;
        &lt;&lt;association&gt;&gt;
    else:
        g.es_print(&quot;  LeoDoc.ico not in expected location, can't continue.&quot;)
</t>
  <t tx="maphew.20130510011223.1645">&quot;&quot;&quot;Tell Windows how to handle .leo files, enables double clicking on them to open.

To run: in Leo make this the active node and press [Ctrl-B] (execute-script)
        
Requires elevated User Account Control (UAC) privileges.
See http://superuser.com/questions/88491/force-cmd-exe-to-run-as-admin/

Resources used:
   @url  http://stackoverflow.com/questions/2331690/how-to-set-a-icon-file-while-creating-file
   @url http://stackoverflow.com/questions/771689/how-can-i-set-an-icon-for-my-own-file-extension
   @url https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
&quot;&quot;&quot;
</t>
  <t tx="maphew.20130510011223.1646">This is what the resulting registry key should look like, once exported from
regedit. The translated hex code for Open Command is:
    
    &quot;d:\Python27\python.exe&quot; &quot;C:\Users\Matt\Dropbox\apps\leo-editor\launchLeo.py&quot; &quot;%1&quot; %*


```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\.leo]
@=&quot;Leo.File&quot;

[HKEY_CLASSES_ROOT\.leox]
@=&quot;Leo.File&quot;

[HKEY_CLASSES_ROOT\Leo.File]
@=&quot;Leo Editor File&quot;

[HKEY_CLASSES_ROOT\Leo.File\DefaultIcon]
@=&quot;C:\\Users\\Matt\\Dropbox\\apps\\leo-editor\\leo\\Icons\\LeoDoc.ico&quot;

[HKEY_CLASSES_ROOT\Leo.File\Shell]

[HKEY_CLASSES_ROOT\Leo.File\Shell\Open]

[HKEY_CLASSES_ROOT\Leo.File\Shell\Open\Command]
@=hex(2):22,00,64,00,3a,00,5c,00,50,00,79,00,74,00,68,00,6f,00,6e,00,32,00,37,\
  00,5c,00,70,00,79,00,74,00,68,00,6f,00,6e,00,2e,00,65,00,78,00,65,00,22,00,\
  20,00,22,00,43,00,3a,00,5c,00,55,00,73,00,65,00,72,00,73,00,5c,00,4d,00,61,\
  00,74,00,74,00,5c,00,44,00,72,00,6f,00,70,00,62,00,6f,00,78,00,5c,00,61,00,\
  70,00,70,00,73,00,5c,00,6c,00,65,00,6f,00,2d,00,65,00,64,00,69,00,74,00,6f,\
  00,72,00,5c,00,6c,00,61,00,75,00,6e,00,63,00,68,00,4c,00,65,00,6f,00,2e,00,\
  70,00,79,00,22,00,20,00,22,00,25,00,31,00,22,00,20,00,25,00,2a,00,00,00
```</t>
  <t tx="maphew.20130515233516.1659">try:
    leoKey = CreateKey(HKEY_CLASSES_ROOT, &quot;Leo.File&quot;)
    iconKey = CreateKey(leoKey, &quot;DefaultIcon&quot;)
    shellKey = CreateKey(leoKey, &quot;Shell&quot;)
    openKey = CreateKey(shellKey, &quot;Open&quot;)
    cmdKey = CreateKey(openKey, &quot;Command&quot;)

    SetValue(leoKey, None, REG_SZ, &quot;Leo Editor File&quot;)
    SetValue(iconKey, None, REG_SZ, icon)

    if &quot;launchLeo.py&quot; in launchLeo:
        SetValueEx(
            cmdKey,
            None,
            None,
            REG_EXPAND_SZ,
            '&quot;{0}&quot; &quot;{1}&quot; &quot;%1&quot; %*'.format(pyexe, launchLeo),
        )
    else:
        SetValueEx(cmdKey, None, None, REG_EXPAND_SZ, '&quot;{0}&quot; &quot;%1&quot; %*'.format(launchLeo))

    for k in (leoKey, iconKey, shellKey, openKey, cmdKey):
        CloseKey(k)

    g.es_print(&quot;  Registered!&quot;)

except WindowsError as e:
    g.es_print(&quot;  Failed:&quot;, e)
</t>
  <t tx="maphew.20130515233516.1660">try:
    leoKey = CreateKey(HKEY_CLASSES_ROOT, &quot;.leo&quot;)
    SetValue(leoKey, None, REG_SZ, &quot;Leo.File&quot;)
    # SetValue(leoKey, &quot;Content Type&quot;, REG_SZ, &quot;text/xml&quot;)  #creates a sub_key instead of a value :(
    CloseKey(leoKey)

    leoKey = CreateKey(HKEY_CLASSES_ROOT, &quot;.leox&quot;)
    SetValue(leoKey, None, REG_SZ, &quot;Leo.File&quot;)
    CloseKey(leoKey)

    leoKey = CreateKey(HKEY_CLASSES_ROOT, &quot;.leojs&quot;)
    SetValue(leoKey, None, REG_SZ, &quot;Leo.File&quot;)
    CloseKey(leoKey)

    g.es_print(&quot;  .leo, .leojs and .leox files associated as 'Leo.File'&quot;)

except WindowsError as e:
    g.es_print(&quot;  Failed:&quot;, e)
</t>
  <t tx="maphew.20190712110256.1">@path win

@first # -*- coding: utf-8 -*-
@language python
@tabwidth -4
'''Add registry keys for Leo file type and .leo file association'''
@others

</t>
  <t tx="maphew.20190712112409.1">@path win

@language python
@tabwidth -4
'''Remove registry key for Leo file type and .leo file association'''
@others

</t>
  <t tx="maphew.20190712112633.1"># define script names and paths
scripts_path = os.path.realpath(os.path.join(leo.__path__[0], 'scripts/win'))
elevate = os.path.join(scripts_path, 'elevate.py')
this_script = get_my_path()

import ctypes, sys
if not ctypes.windll.shell32.IsUserAnAdmin():
    g.es_print(&quot;No admin privileges&quot;)
    relaunch_elevated(this_script)
else:
    g.es_print(&quot;--- Running unregister-leo Leo script&quot;)
    g.es_print(&quot;  Attempting to un-register leo filetype with Windows...&quot;)
    unregister_leo()
    g.es_print('--- end of script')</t>
  <t tx="maphew.20190712112653.1"># define script names and paths
scripts_path = os.path.realpath(os.path.join(leo.__path__[0], 'scripts/win'))
elevate = os.path.join(scripts_path, 'elevate.py')
this_script = get_my_path()

g.es_print(&quot;--- Running register-leo Leo script&quot;)
import ctypes, sys
if not ctypes.windll.shell32.IsUserAnAdmin():
    g.es_print(&quot;No admin privileges&quot;)
    relaunch_elevated(this_script)
else:
    pyexe = g.sys.executable
    pywexe = pyexe.replace('python.exe', 'pythonw.exe')
    #launchLeo = g.os_path_finalize_join(g.computeLeoDir(), '../launchLeo.py')
    launchLeo = get_launch_leo()
    icon = &quot;%s\Icons\LeoDoc.ico&quot; % get_leo_libpath()
    
    # # 'pyexe' to launch GUI with a console window for messages
    # # 'pywexe' to launch GUI only (will lose messages that bypass log)
    
    register_leo(pywexe, launchLeo, icon)

g.es_print('--- end of script')</t>
  <t tx="maphew.20190712112935.1">These buttons are just convenience wrappers around the `@file` scripts, by cloning the at-file nodes.

Todo: move desktop-links code into external files also (enables running from command line).

</t>
  <t tx="maphew.20191007115940.1">From *Settings* menu select **Open Desktop Integration**.
The new Leo file that opens will add 2 buttons under the menu bar:

*[Register-leo]* - Creates registry keys for Leo file type and .leo
file association. Afterwards .leo files will show Leo icon and
double-clicking them will open in Leo Editor.

*[Unregister-leo]* - Removes the above.
</t>
  <t tx="maphew.20191007120254.1">_Desktop integration buttons (under the menu bar)_

## All Platforms - Linux, Mac, Windows ##

[add-desktop-links] - Creates launch shortcuts in desktop and system menu

[remove-desktop-links] - Removes the launch shortcuts


## Windows ## 

[Register-leo] - Creates registry keys for Leo file type and .leo file association. Afterwards .leo files will show Leo icon and double-clicking them will open in Leo Editor.

[Unregister-leo] - Removes the above
</t>
  <t tx="maphew.20191007120341.1">*[Register-leo]* - Creates registry keys for Leo file type and .leo
file association. Afterwards .leo files will show Leo icon and
double-clicking them will open in Leo Editor.

*[Unregister-leo]* - Removes the above.
</t>
  <t tx="mhw-debug-1081.20190216130451.1">import leo
import leo.core.leoGlobals as g
import os
import sys
import shutil
import subprocess
from winreg import *
</t>
  <t tx="mhw-debug-1081.20190216145532.1">def unregister_leo():
    try:
        leoKey = OpenKey(HKEY_CLASSES_ROOT, &quot;Leo.File&quot;)
        DeleteKey(leoKey, &quot;Shell\\Open\\Command&quot;)
        DeleteKey(leoKey, &quot;Shell\\Open&quot;)
        DeleteKey(leoKey, &quot;Shell&quot;)
        DeleteKey(leoKey, &quot;DefaultIcon&quot;)
        DeleteKey(HKEY_CLASSES_ROOT, &quot;Leo.File&quot;)
        # CloseKey(leoKey)
        g.es_print(&quot;  Leo file type has been removed from registry&quot;)
    except WindowsError as e:
        g.es_print(&quot;  Unregistering Leo file type failed: &quot;, e)

    try:
        DeleteKey(HKEY_CLASSES_ROOT, &quot;.leo&quot;)
        DeleteKey(HKEY_CLASSES_ROOT, &quot;.leox&quot;)
        g.es_print(&quot;  .leo, .leox file associations removed from registry&quot;)
    except WindowsError as e:
        g.es_print(&quot;  Removing .leo, leox associations failed: &quot;, e)

    # May not have the (newer) .leojs file association
    try:
        DeleteKey(HKEY_CLASSES_ROOT, &quot;.leojs&quot;)
        g.es_print(&quot;  .leojs file association removed from registry&quot;)
    except WindowsError as e:
        g.es_print(&quot;  Removing .leojs associations failed: &quot;, e)
</t>
  <t tx="mhw-debug-1081.20190221070850.1">def get_launch_leo():
    &quot;&quot;&quot;Prefer leo exe script in PATH over launchLeo.py relative to Leo library&quot;&quot;&quot;
    leo_script = os.path.join(sys.exec_prefix, &quot;Scripts&quot;, &quot;leo.exe&quot;)
    if os.path.isfile(leo_script):
        return leo_script
    else:
        leo_script = os.path.join(get_leo_libpath(), &quot;../launchLeo.py&quot;)
    if os.path.isfile(leo_script):
        return leo_script
    return None
</t>
  <t tx="mhw-debug-1081.20190227224730.1">def get_leo_libpath():
    &quot;&quot;&quot;Return Leo's library path (ie: ./leo-editor/leo or PYTHONHOME/Lib/site-packages/leo)&quot;&quot;&quot;
    import leo

    return leo.__path__[0]
</t>
  <t tx="mhw-debug-1081.20190310203401.1">Scripts only of interest when on Microsoft Windows platform.
@path win
</t>
  <t tx="mhw-debug-1081.20190314004045.1">def get_my_path():
    &quot;&quot;&quot;Return full path of currently running script or executable
    
   Thanks to
        https://stackoverflow.com/questions/2632199/
            how-do-i-get-the-path-of-the-current-executed-file-in-python
        @jose-crespo-barrios, https://stackoverflow.com/a/44592299/14420
    &quot;&quot;&quot;
    import inspect

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    return filename
</t>
  <t tx="mhw-debug-1081.20190314005003.1">def relaunch_elevated(script):
    g.es_print(&quot;--- Relaunching and asking for elevated permissions&quot;)
    g.execute_shell_commands([&quot;&amp;{} {} {}&quot;.format(sys.executable, elevate, script)])
    g.es_print(&quot;---&quot;)
</t>
  <t tx="mhw.20181210131101.1">True (recommended):
    Write &quot;E&quot; attribute bits in &lt;v&gt; elements.
    Leo outlines will record the expansion state of all nodes.
    
False: (Good for files like unitTest.leo)
    Suppress &quot;E&quot; attribute bits in &lt;v&gt; elements.
    Only the ancestors of the presently selected node will
    be expanded when Leo opens an outline.</t>
  <t tx="mhw.20190730140115.1">@language python
@tabwidth -4
@others
</t>
  <t tx="mhw.20190806161400.1">@language python
@tabwidth -4
@others
</t>
  <t tx="mhw.20190808083214.1">&quot;&quot;&quot;Create Leo Editor desktop shortcut link
  Assumes Leo has been installed with pip and that Leo's launcher scripts are in PATH.
&quot;&quot;&quot;
import os
import sys
import shutil
import platform
import leo.core.leoGlobals as g
from pyshortcuts import make_shortcut
from os.path import splitext

debug = False
iconpath = g.os_path_realpath(g.os_path_join(g.__file__, &quot;../../Icons/LeoApp.ico&quot;))

g.es_print(f&quot;\n----- Running add-desktop-links -----&quot;)

leocmd = shutil.which(&quot;leo&quot;)
if platform.system() == &quot;Windows&quot;:
    leocmd = shutil.which(&quot;leo-messages&quot;)
if not leocmd:
    raise ValueError(&quot;leocmd not defined&quot;)

# cosmetic: ensure extension is lower case for nicer reporting
leocmd = splitext(leocmd)[0] + splitext(leocmd)[1].lower()

scut = make_shortcut(leocmd, name=&quot;Leo Editor&quot;, icon=iconpath)

g.es_print(
    f&quot;Created shortcut '{scut.target}' in: \n   {scut.desktop_dir}\n   {scut.startmenu_dir}&quot;
)

if debug:
    g.es_print(f&quot;\n*** debug:\n{(scut)}&quot;)
</t>
  <t tx="mhw.20190808083336.1">&quot;&quot;&quot;Remove Leo Editor shortcuts from desktop and system menu

The approach is naive:
    first we create links for the current environment, overwriting if already exist
    then we remove them

So this won't delete links created from a different Leo directory or source code
checkout (unless they have same filename).
&quot;&quot;&quot;
import os
import sys
import shutil
import platform
import leo.core.leoGlobals as g
from pyshortcuts import make_shortcut
from os.path import splitext

debug = False
iconpath = g.os_path_realpath(g.os_path_join(g.__file__, &quot;../../Icons/LeoApp.ico&quot;))

g.es_print(f&quot;\n----- Running remove-desktop-links -----&quot;)

leocmd = shutil.which(&quot;leo&quot;)
if platform.system() == &quot;Windows&quot;:
    leocmd = shutil.which(&quot;leo-messages&quot;)
if not leocmd:
    raise ValueError(&quot;leocmd not defined&quot;)

# cosmetic: ensure extension is lower case for nicer reporting
leocmd = splitext(leocmd)[0] + splitext(leocmd)[1].lower()

scut = make_shortcut(leocmd, name=&quot;Leo Editor&quot;, icon=iconpath)

lnkfiles = [
    os.path.join(scut.desktop_dir, scut.target),
    os.path.join(scut.startmenu_dir, scut.target),
]
for fil in lnkfiles:
    os.remove(fil)
    g.es_print(f&quot;Removed '{fil}' &quot;)

if debug:
    g.es_print(f&quot;\n*** debug:\n{(scut)}&quot;)
</t>
</tnodes>
</leo_file>
