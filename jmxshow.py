#!/usr/bin/python
import jpype
import sys
URL="service:jmx:jmxmp://10.0.0.2:12345"
JMXREMOTEPATH="/home/undefine/.java/"
def showName(connection,name):
    info=connection.getMBeanInfo(name)
    for attribute in info.getAttributes():
        if attribute.isReadable() == 1:
            try:
                print " ", attribute.getName(),':', connection.getAttribute(name,attribute.getName())
            except:
                print " ", attribute.getName(),': FAIL'

def main():
    jpype.startJVM("/usr/lib/jvm/java-6-sun/jre/lib/i386/server/libjvm.so","-Djava.endorsed.dirs=" + JMXREMOTEPATH)
    jmxurl = jpype.javax.management.remote.JMXServiceURL(URL)
    jhash = jpype.java.util.HashMap()
    jmxsoc = jpype.javax.management.remote.JMXConnectorFactory.connect(jmxurl,jhash)
    connection = jmxsoc.getMBeanServerConnection()

    if len(sys.argv) == 1:
        for name in connection.queryNames(None,None):
            print str(name)
    #        showName(connection,name)
    elif len(sys.argv) == 2:
        name=jpype.javax.management.ObjectName(sys.argv[1])
        showName(connection,name)

    jpype.shutdownJVM()


if __name__ == "__main__":
    main()

