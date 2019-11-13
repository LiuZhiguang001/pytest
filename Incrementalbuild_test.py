import pytest
import shutil
import filecmp
from UnifiedBuild.BuildPlatform import BuildPlatform
from UnifiedBuild.RepoMgr import RepoMgr
from Manifest import Manifest
from ManagePatchStatus import ManagePatchStatus
import os
import subprocess
import glob

class Test_IncrementBuild(object):

    def CopyFile(self,destpath):
        NewBinFile=self.savepath+'\\'+destpath+'\\'
        for affix in self.manifest.TestType['IncrementBuild']['FileNeedCompare']:
            binlist=[]
            print('-----')
            print(affix)
            print(self.workspace)
            for BinFile in glob.glob(self.workspace+affix):
                binlist.append((BinFile,os.path.getmtime(BinFile)))
            binlist=sorted(binlist, key=lambda k: k[1])  
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
            if binlist!=[]:
                shutil.copyfile(binlist[-1][0],os.path.join(NewBinFile,os.path.basename(name)))
            else:
                raise NameError('no such file')

    def CompareBin(self,clean,increment):
        CleanPath=self.savepath+'\\'+clean+'\\'
        IncrementPath=self.savepath+'\\'+increment+'\\'
        CleanList=os.listdir(CleanPath)
        IncrementList=os.listdir(IncrementPath)
        print(CleanList)
        print(IncrementList)
        if len(CleanList)!=len(IncrementList):
            return False
        CompareResult=filecmp.cmpfiles(CleanPath,IncrementPath,CleanList)
        if len(CompareResult[1])+len(CompareResult[2]) !=0:
            return False
        return True

    def CleanOldFile(self):
        BinFilePath=self.savepath+'\\'+'CleanPath'+'\\'
        if os.path.exists(BinFilePath):
            shutil.rmtree(BinFilePath)
        os.makedirs(BinFilePath)
        BinFilePath=self.savepath+'\\'+'IncrementPath'+'\\'
        if os.path.exists(BinFilePath):
            shutil.rmtree(BinFilePath)
        os.makedirs(BinFilePath)

    @pytest.mark.IncrementBuild
    def test_IncrementBuild(self,PatchList):

        print('begin to test')
        self.CleanOldFile()
        self.repo_mgr.clean_all()
        self.repo_mgr.reset_all()

        #Clean build
        self.TargetRepo.checkout(PatchList[1],'clean')
        self.TargetRepo.apply_patches([PatchList[0]])
        BuildPlatform(self.manifest.Defines.get("workspace"),self.manifest.BuildCate.get("Basic"),[],self.repo_mgr)
        self.CopyFile('CleanPath')

        self.repo_mgr.clean_all()
        self.repo_mgr.reset_all()

        #Incremental build
        self.TargetRepo.checkout(PatchList[1],'increment')
        BuildPlatform(self.manifest.Defines.get("workspace"),self.manifest.BuildCate.get("Basic"),[],self.repo_mgr) 
        self.TargetRepo.apply_patches([PatchList[0]])
        BuildPlatform(self.manifest.Defines.get("workspace"),self.manifest.BuildCate.get("Basic"),['BuildClean'],self.repo_mgr)   
        self.CopyFile('IncrementPath')


        assert self.CompareBin('CleanPath','IncrementPath')
