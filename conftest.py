import pytest
import os,sys
import subprocess
sys.path.append(os.getcwd()) 

from ManagePatchStatus import GeneratePatch
from ManagePatchStatus import ManagePatchStatus
from UnifiedBuild.BuildPlatform import BuildPlatform
from UnifiedBuild.RepoMgr import RepoMgr

from Manifest import Manifest

def pytest_addoption(parser):
    parser.addoption(
        "--NewTestCaseNumber", 
        action="store", 
        default=" ",
        dest="TestCaseNumber",
        help="Creat a new TestCase"
    )
    parser.addoption(
        "--TestCasePath", 
        action="store", 
        default=" ",
        dest="TestCasePath",
        help="Specify a existed test case path"
    )
    parser.addoption(
        "--run", 
        action="store_true", 
        default=False,
        dest="IsRun",
        help="Indicate that test will run"
    )
    parser.addoption(
        "--NewTestCasePath", 
        action="store", 
        default="D:\\pytest1\\patch",
        dest="NewTestCasePath",
        help="Specify a new test case path"
    )
    parser.addoption(
        "--Target", 
        action="store", 
        default=r'D:\pytest1\step\Whitely.toml',
        dest="Target",
        help="Specify a platform target"
    )



def pytest_generate_tests(metafunc):

    TestCaseNumber=metafunc.config.getoption("TestCaseNumber")
    TestCasePath=metafunc.config.getoption("TestCasePath")
    IsRun=metafunc.config.getoption("IsRun")
    NewTestCasePath=metafunc.config.getoption("NewTestCasePath")
    Target=metafunc.config.getoption("Target")
    Marker=metafunc.config.getoption("-m")
    print(Marker)

    # get repo information and reset all the repos
    manifest = Manifest(Target)
    workspace = manifest.Defines.get("workspace",".")
    print(workspace)
    if not workspace:
        assert 0
    repo_conf = manifest.RepoConf
    if not repo_conf:
        assert 0
    repo_mgr = RepoMgr(workspace, repo_conf)
    repo_mgr.clean_all()
    repo_mgr.reset_all()

    TargetRepo=repo_mgr.get_repo(manifest.TestType['IncrementBuild']['TargetRepo'])
    if TestCaseNumber!=" ":
        if TestCaseNumber.isnumeric():
            TestCaseNumber=int(TestCaseNumber)
            PatchList=GeneratePatch(Number=TestCaseNumber,repo=TargetRepo.path,PatchDir=NewTestCasePath)
            PatchList.OutputPatch()
        else:
            print("Error: need a number after --NewTestCase")
            metafunc.parametrize("PatchList", [])
            return 
    if TestCasePath!=" ":
        PatchList=ManagePatchStatus(PicklePath=TestCasePath)
    if IsRun:
        metafunc.cls.workspace=workspace
        metafunc.cls.repo_mgr=repo_mgr
        metafunc.cls.manifest=manifest
        metafunc.cls.savepath=NewTestCasePath
        metafunc.cls.TargetRepo=TargetRepo
        metafunc.parametrize("PatchList", PatchList.AllPatchList)
        return
        #metafunc.parametrize("repo", PatchList.AllPatchList)
    try:
        #print(PatchList.AllPatchList)
        print("TestCaseNumber :"+str(TestCaseNumber))
        print("Intel Repo :"+str(repo_mgr.get_repo('Intel').path))
        print("NewTestCasePath :"+NewTestCasePath)
        print("TestCasePath :"+TestCasePath)
        print("IsRun :"+str(IsRun))
        print("IsRun is not set, so test didn't begin")
    except:
        print("Argument is not right")
    metafunc.parametrize("PatchList", [])

def a():
    print("999999")

'''

C:\Python37\Scripts\pytest.exe d_test.py --Target D:\pytest1\step\Whitely.toml --NewTestCaseNumber 5 --NewTestCasePath D:\pytest1\patch -m IncrementBuild --run

C:\Python37\Scripts\pytest.exe d_test.py --Target D:\pytest1\step\Whitely.toml --NewTestCaseNumber 1 --NewTestCasePath D:\pytest1\patch -m IncrementBuild --run --capture=sys
'''

    