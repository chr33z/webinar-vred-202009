from shutil import copy, copytree, copyfile
import errno
import subprocess
import string_utils
import os
import distutils.dir_util
import re
import sys
import hashlib

obfuscatePlugin = False
obfuscateModules = False
runVRED = True

# versions of vred for that the plugin should be installed
installVersions = ['13.0']

# version that is started after installation
startVersion = '13.0'


def vredInstallation():
    '''
    Return the path of the VRED installation on this machine. Change on every development machine
    '''
    return r'D:\Program Files\Autodesk\VREDPro-' + startVersion + r'\Bin\WIN64\VREDPro.exe'


def pluginPath(version):
    '''
    Return the path of the deploy plugin directory
    '''
    return os.path.join(os.path.expanduser('~'), "Documents", "Autodesk", "VRED-" + version, "ScriptPlugins", "example-plugin")


def modulesPath(version):
    '''
    Return the path of the deployed modules directory
    '''
    return os.path.join(os.path.expanduser('~'), "Documents", "Autodesk", "VRED-" + version, "modules")


def developmentPath():
    '''
    Return the path of the development directory
    '''
    filePath = os.path.realpath(__file__)
    fileDirectory, _ = os.path.split(filePath)
    return fileDirectory


def obfuscatePluginCode():
    print("[build] Obfuscate plugin code...")

    fileOrig = os.path.join(pluginPath(version), 'example_plugin.py')
    fileObf = os.path.join(pluginPath(version), 'example_plugin_obfuscated.py')

    os.system(
        r'pyminifier --obfuscate-import-methods --obfuscate-builtins --replacement-length=3 {0} >> {1}'.format(fileOrig, fileObf))
    os.system(r'del example_plugin.py')
    os.system(r'rename example_plugin_obfuscated.py example_plugin.py')

    with open("example_plugin.py", "rt") as fin:
        with open("example_plugin_obfuscated.py", "wt") as fout:
            for line in fin:
                # Remove single line comments
                if line.lstrip().startswith('#'):
                    continue

                # remove debug prints
                if r'[Debug]' in line:
                    continue

                fout.write(line)

    os.system(r'del example_plugin.py')
    os.system(r'rename example_plugin_obfuscated.py example_plugin.py')


def obfuscateModuleCode():
    print("[build] Obfuscate plugin modules...")
    moduleFiles = os.listdir(modulesPath(version))

    for file in moduleFiles:
        print("[build] Obfuscate plugin modules: " + str(file))

        if not file.startswith('example_plugin_') or not file.endswith('.py'):
            continue

        fileOrig = os.path.join(modulesPath(version), file)
        fileObf = fileOrig.replace('.py', '_obf.py')

        # run obfuscator
        os.system(
            'pyminifier --obfuscate-import-methods --obfuscate-builtins --replacement-length=3 %s >> %s' % (fileOrig, fileObf))
        os.system('del %s' % (fileOrig))
        os.rename(fileObf, fileOrig)

        with open(fileOrig, "rt") as fin:
            with open(fileObf, "wt") as fout:
                for line in fin:

                    # Remove single line comments
                    if line.lstrip().startswith('#'):
                        continue

                    # remove debug prints
                    if r'[Debug]' in line:
                        continue

                    fout.write(line)

        os.system(r'del %s' % (fileOrig))
        os.rename(fileObf, fileOrig)


# keep reference to script path
scriptPath = developmentPath()

print("[build] Start deploying python plugin...")

# Add more VRED versions to deploy to multiple installations
for version in installVersions:
    print("[build] Deploy version: " + str(version) + " ...")

    os.chdir(scriptPath)

    print("[build] Create plugin directories...")
    distutils.dir_util.mkpath(pluginPath(version))
    distutils.dir_util.mkpath(modulesPath(version))

    print("[build] Copy plugin...")
    pluginSrc = os.path.join(scriptPath, 'example_plugin.py')
    pluginDst = os.path.join(pluginPath(version), 'example_plugin.py')
    copyfile(pluginSrc, pluginDst)

    print("[build] Copy ui...")
    pluginUISrc = os.path.join(scriptPath, 'example_plugin.ui')
    pluginUIDst = os.path.join(pluginPath(version), 'example_plugin.ui')
    copyfile(pluginUISrc, pluginUIDst)

    print("[build] Copy modules...")
    pluginModulesSrc = os.path.join(scriptPath, 'modules')
    pluginModulesDst = modulesPath(version)
    distutils.dir_util.copy_tree(pluginModulesSrc, pluginModulesDst)

    if obfuscatePlugin:
        obfuscatePluginCode()

    if obfuscateModules:
        obfuscateModuleCode()

print("[build] Finished plugin deployment...")

if runVRED:
    print("[build] Run VRED...")
    subprocess.call(vredInstallation())

sys.exit()
