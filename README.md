
options:
    --Target            tomlfile        Specify a platform target defined in a toml file
    --NewTestCaseNumber n               Creat a new TestCase, generate n patches and save it into directory specifed by --NewTestCasePath option
    -m                  IncrementBuild  Use it to only run incremental build test
    --run                               If not specify this option, no real test will be run
    --NewTestCasePath   directory       Specify where the patches and file recording patches are saved
    --capture=sys                       Print the build log
    --TestCasePath      picklefile      Specify the pickle file which records the patches status.
    --patch             patchfile       Specify a build tool patch for test

Command line example:

C:\Python37\Scripts\pytest.exe Incrementalbuild_test.py  --Target D:\pytest3\pytest3\step\Ovmf.toml --NewTestCaseNumber 2  -m IncrementBuild --run --capture=sys --patch E:\github\0001-Add-CpuDeadLoop.patch

C:\Python37\Scripts\pytest.exe Incrementalbuild_test.py --Target D:\pytest3\pytest3\step\Whitely.toml --TestCasePath D:\pytest1\patch\status.pickle
