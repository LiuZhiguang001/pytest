import pytest
import shutil
import filecmp
l=[1,2]

from UnifiedBuild.BuildPlatform import BuildPlatform
from UnifiedBuild.RepoMgr import RepoMgr
from Manifest import Manifest
from ManagePatchStatus import ManagePatchStatus
import os
import subprocess
import glob

from Manifest import Manifest

#from generatePatch import GeneratePatch
class aaa(object):

    def __init__(self):
        self.savepath=r'D:\pytest1\patch'
        target = r'D:\pytest1\step\Whitely.toml'
        self.manifest = Manifest(target)
        self.workspace = self.manifest.Defines.get("workspace",".")



    def CompareBin(self,clean,increment):
        CleanPath=self.savepath+'\\'+clean+'\\'
        IncrementPath=self.savepath+'\\'+increment+'\\'
        CleanList=os.listdir(CleanPath)
        IncrementList=os.listdir(IncrementPath)
        print(CleanList)
        print(IncrementList)
        #if len(CleanList)!=len(IncrementList):
        #    return False
        CompareResult=filecmp.cmpfiles(CleanPath,IncrementPath,CleanList)
        x =filecmp.dircmp(CleanPath,IncrementPath,CleanList)
        x.report()
        print(CompareResult)
        if len(CompareResult[1])+len(CompareResult[2]) !=0:
            return False
        return True
    def CopyFile(self,destpath):
        NewBinFile=self.savepath+'\\'+destpath+'\\'
        for affix in self.manifest.TestType['IncrementBuild']['FileNeedCompare']:
            binlist=[]
            for BinFile in glob.glob(self.workspace+affix):
                #print(BinFile)
                #print(os.path.getmtime(BinFile))
                binlist.append((BinFile,os.path.getmtime(BinFile)))
            
            binlist=sorted(binlist, key=lambda k: k[1])
            #print(binlist)   
            if '*' in affix:
                index=affix.find('*')
                name=affix[index+1:]
            else:
                if '\\' in affix:
                    index=affix.find('\\')
                    name=affix[index+1:]
                    while index!=-1:
                        name=name[index+1:]
                        index=name.find('\\')
                else:
                    name=affix
            shutil.copyfile(binlist[-1][0],os.path.join(NewBinFile,os.path.basename(name)))


a=aaa()
##a.CopyFile('bbb')
#
##a.CopyFile(BinFile,'CleanPath')
print(a.CompareBin('CleanPath','IncrementPath'))

'''
if __name__ == "__main__":
    target_platform = r'D:\pytest1\step\Ovmf.toml'
    manifest = Manifest(target_platform)
    for e in manifest.RepoConf:
        print(e)
    print(manifest.TestType)
    print(manifest.Defines)
    workspace = manifest.Defines.get("workspace",".")
    repo_conf = manifest.RepoConf
    repo_mgr = RepoMgr(workspace, repo_conf)
    repo_mgr.clean_all()
    repo_mgr.reset_all()
    print(manifest.TestType['IncrementBuild']['FileNeedCompare'])

'''