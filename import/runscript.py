import clr
clr.AddReference("DHI.Solutions.Application")
from DHI.Solutions.Application import *

clr.AddReference("DHI.Solutions.ScriptManager.Interfaces")
from DHI.Solutions.ScriptManager.Interfaces import *

clr.AddReference("System")
from System import String, Object
from System.IO import Path, File
from System.Collections.Generic import IDictionary, Dictionary

import sys

def _runscript():

    try:
        # loading config
        iniFile = Path.ChangeExtension(sys.argv[0],".ini")
        configLines = File.ReadAllLines(iniFile)
        config = {}
        for line in configLines:
            kv = line.split("=")
            config[kv[0].upper()] = kv[1]

            print "construct"
            app = Application()
            print "set connection"
            app.SetConnection("Host=" + config["HOST"]+";Database="+config["DATABASE"]+";port="+config["PORT"]+";dbflavour="+ config["DBFLAVOUR"]);
            print "login"
            app.Login(config["USER"],config["PW"],config["WORKSPACE"]);
            print "startup"
            app.StartUp();
            print "ready"

            scriptPath = sys.argv[1]
            print "scriptPath=" + scriptPath

            scr = app.Modules.Get("Script Manager")
            script = scr.ScriptList.Fetch(scriptPath)
            print "Setting up parameters ... "
            dictParam = Dictionary[String, Object]()
            for i in range(2,len(sys.argv)):
                kv = sys.argv[i].split('=')
                k = kv[0].strip()
                v = kv[1].strip()
                if v.startswith('"') and v.endswith('"'): v = v[1:-1]
                print k,"=",v
                dictParam.Add(k,v)
                print "Running " + scr.ScriptList.GetEntityDescriptor(script)
                output =  clr.Reference[String]()
                # avoid conflicting overloaded versions of ExecuteScript by supplying arguments by name
                result = scr.ExecuteScript(script=script, arguments=dictParam, tag=None, output=output)
                print "result=",result
                print "output:"
                print output.Value

                print "done"
    except Exception as e:
        print "ERROR"
        print str(e)


# start the execution
_runscript()
