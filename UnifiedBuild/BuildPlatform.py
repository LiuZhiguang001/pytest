import toml
import subprocess
import os
from UnifiedBuild.RepoMgr import RepoMgr

def BuildPlatform(PlatformWorkingPath,BuildSteps,ignore_steps=None,repo_mgr=None):
    if ignore_steps is None:
        ignore_steps = []
    env_dict = os.environ
    env_dict['PYTHON_HOME'] = r"c:\python27"
    for step in BuildSteps.get('step'):
        if step['name'] in ignore_steps:
            continue
        print('----------')
        print(step)
        print('----------')
        cmds = []
        comm_name = step.get('command').get("cmd")
        cmds.append(comm_name)
        paras = step.get('command').get("parameters")
        if paras:
            cmds.extend(paras)
        output_type = step.get('command').get("output_type")
        need_capture_output = False
        if "EnvVar" in output_type:
            cmds.append(">nul")
            cmds.append("&")
            cmds.append("set")
            need_capture_output = True
        print(cmds)
        path = step.get('command').get("path")
        workpath=PlatformWorkingPath
        if path[0]!='':
            workpath=repo_mgr.get_repo(path[0]).path
        workpath=os.path.join(workpath,path[1])
        print(workpath)
        rt = subprocess.run(cmds,capture_output=need_capture_output,cwd=workpath,shell=True,text=True,env=env_dict)
        if rt.returncode != 0:
            print(rt.stderr)
            print(rt.stdout)
            exit(1)
        if "EnvVar" in output_type:
            envirmentvar = rt.stdout
            for envi in envirmentvar.split("\n"):
                try:
                    name=envi[:envi.index('=')]
                    value=envi[envi.index('=')+1:]
                    env_dict[name.strip()] = value.strip()
                except:
                    continue

if __name__ == "__main__":
    BuildPlatform()