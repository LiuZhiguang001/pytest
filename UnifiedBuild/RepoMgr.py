import toml
import subprocess
import os
class Repo():
    def __init__(self,workspace,name,link,branch,version,path):

        self.path = os.path.join(workspace,path)
        self.name = name
        self.link = link
        self.branch = branch
        self.version = version
        
    @property
    def Path(self):
        return self.path

    def clone(self):
        ''' clone the repo to local '''
    
    def checkout(self, id=None , newbranch=None):
        ''' check out self.branch '''
        if id:
            cmd='git checkout '+str(id)+' -B '+newbranch
        else:
            cmd='git checkout '+self.branch
            
        rt=subprocess.run(cmd,cwd=self.path,shell=True)
        if rt.returncode != 0:
            print(rt.stderr)
            print(rt.stdout)
            print('"'+cmd+'"'+ ' has error')
            exit(1)
        
    def clean(self):
        ''' clean all the un-tracked files '''
        print("begin clean "+self.name+ "repo")
        cmd = 'git clean -ffdx'
        rt=subprocess.run(cmd,cwd=self.path,shell=True)
        if rt.returncode != 0:
            print(rt.stderr)
            print(rt.stdout)
            print('"'+cmd+'"'+ ' has error')
            exit(1)
        
        
    def reset(self):
        cmd = 'git reset --hard'
        
        #print("begin reset "+self.name+ "repo")
        rt=subprocess.run(cmd,cwd=self.path,shell=True)

        if rt.returncode != 0:
            print(rt.stderr)
            print(rt.stdout)
            print('"'+cmd+'"'+ ' has error')
            exit(1)
        ''' reset the repo to self.version '''
        
    def apply_patches(self, patch_path_list):
        ''' apply the patch_path to specific repo named repo_name '''
        for e in patch_path_list:
            cmd='git am '+str(e)
            rt=subprocess.run(cmd,cwd=self.path,shell=True)
            if rt.returncode != 0:
                print(rt.stderr)
                print(rt.stdout)
                print('"'+cmd+'"'+ ' has error')
                exit(1)        
        
    def status(self):
        ''' 0 is repo does not exist, 1 is repo exists '''
        
class RepoMgr():
    def __init__(self,workspace, repo_conf):
        self.repo_conf = repo_conf
        self.workspace = workspace
        self._repos = None
        
    @property
    def Repos(self):
        if self._repos is None:
            self._repos = []
            for repo_info in self.repo_conf:
                if not repo_info:
                    continue
                self._repos.append(Repo(self.workspace, repo_info['name'],repo_info['git'],repo_info['branch'],repo_info['version'],repo_info['path']))
        return self._repos
    
    @property
    def ReposName(self):
        return [item.name for item in self.Repos]
    
    def get_repo(self,repo_name):
        return self.Repos[self.ReposName.index(repo_name)]
    
    def clone_all(self):
        ''' clone the repo of 'name' to local, if name is not in self.Repos return False, otherwise return clone status '''
    
    def reset_all(self):
        ''' reset all the repo to the revision in config file '''
        for e in self.Repos:
            e.reset()
            e.checkout()
        print("reset all")

    def clean_all(self):
        ''' clean all the repo '''
        for e in self.Repos:
            e.clean()
        print("clean all")

    def setup_repo(self):
        for repo in self.Repos:
            if repo.status() == 0:
                repo.clone()
            elif repo.status() == 1:
                repo.clean()
                repo.reset()
    def apply_cases(self,case):
        print(case)
        return
        for repo_name, patch_path in case.case_patch_list:
            repo = self.get_repo(repo_name)
            repo.apply_patches([patch_path])
            
class Case():
    def __init__(self):
        self.name = ""
        self.descriptoin = ''
        self.case_patch_list = [] # (repo, patch_path)

if __name__ == '__main__':
    manifest = Manifest('D:\pytest1\step\Ovmf.toml')

'''

D:\pytest1\step\Ovmf.toml
'''