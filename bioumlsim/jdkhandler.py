import jpype
import os
from os import path as ospath
from platform import system
import subprocess

class JDKHandler:

    @staticmethod
    def installJDK():
        import jdk
        path = jdk.install(11)

    def getJVMVersion(self):
        return '.'.join(map(str, jpype.getJVMVersion()))
     
    def checkJavaVersion(self, release):
        if not ospath.isfile(release):
            return False
        f = open(release, 'r')
        lines = f.readlines()
        for line in lines:
            if line.startswith('JAVA_VERSION=\"11'):
                return True
        return False

    def isMac(self):
        systemName = system()
        if systemName == 'Windows' or systemName == 'Linux':
            return False
        return True

    def findJDK(self, verbose=False):
        jdkBasePath = ospath.join(ospath.expanduser("~"), ".jdk")
        if not ospath.isdir(jdkBasePath):
            self.log('Can not find appropriate JDK in ' + jdkBasePath)
            return ''              
        for name in os.listdir(jdkBasePath):
            jdkPath = ospath.join(jdkBasePath, name)
            if self.isMac():
                jdkPath = ospath.join(jdkPath, 'Contents', 'Home')
            self.log('Checking ' + ospath.join(jdkPath, 'release'), verbose)
            if self.checkJavaVersion(ospath.join(jdkPath, 'release')):
                self.log('Appropriate version detected', verbose)
                return jdkPath
        self.log('Can not find appropriate JDK in ' + jdkBasePath)
        return '' 

    def findJVM(self, jdkLocation='', verbose=False):
        jdk = jdkLocation
        if jdk == '':
            jdk = self.findJDK(verbose=verbose)
        if jdk == '':
            return ''
        self.log('JDK found at ' + jdk, verbose)
        possiblePaths = self.guessJVMLocations()
        javaFile = self.guessJVMFile() 
        for possiblePath in possiblePaths:
            jvm = ospath.join(jdk, possiblePath, javaFile)
            self.log('Check JVM location: ' + jvm, verbose)
            if ospath.isfile(jvm):
                self.log ('JVM Found', verbose)
                return jvm;
        jvm = self.find(javaFile, jdk)
        if jvm == '':
            print('Can not find appropriate JVM. Please install Java 11 or use bioumlsim.installJDK()')
        return jvm 
    
    def guessJVMLocations(self):
        systemName = system()
        if systemName == 'Windows':
            return ['jre/bin/server', 'bin/server']
        elif systemName == 'Linux':
            return ['lib/server', 'jre/lib/amd64/server']
        else:
            return ['jre/lib/server', 'lib/server', 'jre/lib/jli']

    def guessJVMFile(self):
        systemName = system()
        if systemName == 'Windows':
            return 'jvm.dll'
        elif systemName == 'Linux':
            return 'libjvm.so'
        else:
            return 'libjvm.dylib'

    def log(self, message, verbose=True):
        if verbose:
            print(message)  

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return ospath.join(root, name)
        return ''

    def isJavaSet(self):
         try:
             p = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
             version = str(p.splitlines()[0].split()[-1])[3:]
             return version.startswith('1.8') or version.startswith('11')
         except FileNotFoundError:
             return False 

    def isJavaHomeSet(self, verbose=False):
        try:
            os.environ['JAVA_HOME']
            self.log('Java home: ' + os.environ['JAVA_HOME'], verbose)
            return True
        except KeyError:
            return False

    def startJVM(self, path, jdk='', verbose=False):
        if jdk != '':
            self.log('Provided path to jdk: ' + jdk, verbose)
            jvmPath = self.findJVM(jdkLocation=jdk, verbose=verbose)
        elif self.isJavaSet() and self.isJavaHomeSet(verbose=verbose): 
            jvmPath = ''
        else:
            jvmPath = self.findJVM(verbose=verbose)
        if jvmPath == '':
           self.log('Will try to find jvm automatically', verbose) 
           jpype.startJVM(classpath=[path + '/*'], convertStrings=True)
        else:
           self.log ('JVM is located at ' + jvmPath, verbose)
           jpype.startJVM(jvmPath, classpath=[path + '/*'], convertStrings=True)
        print("JVM version: " + self.getJVMVersion())
        return True
