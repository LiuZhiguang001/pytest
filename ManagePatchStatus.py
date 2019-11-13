import subprocess
import os
import glob
import pickle
class ManagePatchStatus(object):
    def __init__(self,PicklePath=None):
        self.PicklePath=PicklePath
        try:
            pkl_file = open(PicklePath, 'rb')
            pickedata=pickle.load(pkl_file)
            pkl_file.close()
            if pickedata[0]=='Pickle data 1.0':
                self.StatusList=pickedata[2]
                print('-'*5+' patch list '+'-'*5)
                for e in self.StatusList:
                    print(e)
                print('-'*22)
        except:
            raise('Wrong Pickle file')
    @property
    def AllPatchList(self):
        return self.StatusList
    
    def SaveAllPatchList(self):
        output = open(self.PicklePath, 'wb')
        pickedata=['Pickle data 1.0',self.StatusList]
        pickle.dump(pickedata, output, protocol=None)
        output.close()

class GeneratePatch(ManagePatchStatus):
    def __init__(self,AfterDate=None,Number=None,repo=r'D:\DCG\DCG10nm\Intel',PatchDir=r'D:\pytest1\patch',PicklePath=None):
        if PatchDir:
            self.PatchDir=PatchDir
            if not os.path.exists(self.PatchDir):
                os.makedirs(self.PatchDir)
        else:
            raise("Please specify the directory where patches can be saved")
        if PicklePath:
            self.PicklePath=PicklePath
        else:
            self.PicklePath = os.path.join(self.PatchDir,'status.pickle')
        
        self.repo=repo

        for OldPatchFile in glob.glob(os.path.join(self.PatchDir, '*.patch')):
            os.remove(OldPatchFile)
        
        if os.path.exists(self.PicklePath):
            os.remove(self.PicklePath)

        if Number or AfterDate:
            if Number:
                self.commit_limit=' -{0}'.format(Number)
                if AfterDate:
                    raise("Can't assain both AfterDate and Number")
            if AfterDate:
                self.commit_limit=' ---since='+AfterDate
        else:
            self.commit_limit=' -5'
        self.OutputPatch()
        print('-'*5+' patch list '+'-'*5)
        for e in self.AllPatchList:
            print(e)
        print('-'*22)

    def GenerateCommit(self):
        cmd='git log --format=%H'+self.commit_limit
        rt=subprocess.run(cmd,cwd=self.repo,text=True,capture_output=True)
        if rt.returncode != 0:
            print(rt.stderr)
            print(rt.stdout)
            print('"'+cmd+'"'+ ' has error')
            exit(1)
        CommitList=rt.stdout.split('\n')
        CommitList.pop()
        cmd='git log --format=%H'+' -'+str(len(CommitList)+1)

        rt=subprocess.run(cmd,cwd=self.repo,text=True,capture_output=True)
        if rt.returncode != 0:
            print(rt.stderr)
            print(rt.stdout)
            print('"'+cmd+'"'+ ' has error')
            exit(1)

        CommitList=rt.stdout.split('\n')
        CommitList.pop()
        return CommitList[::-1]
    
    def OutputPatch(self):
        cmd = 'git format-patch '+self.commit_limit+ ' -o' + self.PatchDir
        rt=subprocess.run(cmd,cwd=self.repo,text=True,capture_output=True)
        if rt.returncode != 0:
            print(rt.stderr)
            print(rt.stdout)
            print('"'+cmd+'"'+ ' has error')
            exit(1)

        PatchList=rt.stdout.split('\n')
        PatchList.pop()
        if len(PatchList) != 1:
            PatchList=PatchList[1:]

        self.StatusList=[]
        CommitList=self.GenerateCommit()
        for i in range(len(PatchList)):
            self.StatusList.append([PatchList[i],CommitList[i],'NotTest'])
        output = open(self.PicklePath, 'wb')
        pickedata=['Pickle data 1.0',self.repo,self.StatusList]
        pickle.dump(pickedata, output, protocol=None)
        output.close()
        return self.StatusList
        
if __name__ == '__main__':
    a=ManagePatchStatus(PicklePath=r'D:\pytest1\patch\status.pickle')
    a.AllPatchList[0][2]='Tested_OK'
    a.SaveAllPatchList()

