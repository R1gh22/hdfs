import time
from subprocess import getoutput as gout,getstatusoutput

gout("mkdir /root/Desktop/Cluster")

def hadoop():
	##----------------------------Slave's IP---------------------------------------#
	sl=int(input("How many slave you want:-"))
	sh1=open('/etc/ansible/hosts','w')
	sh1.write("[slave]")
	sh1.close()
	for j in range(0,sl):
		ip=input("Enter ip slave {} :-".format(j+1))
		usr=input("Enter username for ip slave {} :-".format(j+1))
		ps=input("Enter password for ip slave {} :-".format(j+1))
		sh2=open('/etc/ansible/hosts','a')
		sh2.write("\n{} ansible_ssh_user={} ansible_ssh_pass={}".format(ip,usr,ps))
		sh2.close()

	##-----------------------------Master's IP------------------------------------##

	mh1=open('/etc/ansible/hosts','a')
	mh1.write("\n\n[Master]")
	mh1.close()
	ip=input("Enter master's ip:-")
	usr=input("Enter master's username :-")
	ps=input("Enter master's password:-")
	mh2=open('/etc/ansible/hosts','a')
	mh2.write("\n{} ansible_ssh_user={} ansible_ssh_pass={}".format(ip,usr,ps))
	mh2.close()

	##----------------------------core-site.xml-----------------------------------##
	cs=open('/root/Desktop/Cluster/core.xml','w')
	cs.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>
</property>
</configuration>""".format(ip))
	cs.close()
	##----------------------------slave-hdfs-site.xml-----------------------------------##

	hd=open('/root/Desktop/Cluster/slave_hdfs.xml','w')
	hd.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/datanode</value>
</property>
</configuration>""")
	hd.close()

	##---------------------------master-hdfs-site.xml---------------------------------##

	md=open('/root/Desktop/Cluster/hdfs.xml','w')
	md.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/namenode</value>
</property>
</configuration>""")
	md.close()

	##-------------------------------run-yml-files------------------------------------##

	x=gout("ansible-playbook hadoop_install.yml")
	print(x)
	#time.sleep(60)
	y=gout("ansible-playbook hadoop_file.yml")
	print(y)

	##------------------------------configure-master & slave----------------------------------##

	gout(" sshpass -p {} ssh -o StrictHostKeyChecking=no -l {} {} iptables -F".format(ps,usr,ip))
	gout(" sshpass -p {} ssh -o StrictHostKeyChecking=no -l {} {}  echo Y | hadoop namenode -format ".format(ps,usr,ip))
	gout(" sshpass -p {} ssh -o StrictHostKeyChecking=no -l {} {} hadoop-daemon.sh start namenode".format(ps,usr,ip))
	c=gout(" sshpass -p {} ssh -o StrictHostKeyChecking=no -l {} {} jps | grep NameNode".format(ps,usr,ip))
	print(c)
	gout("ansible-playbook slave_config.yml")

##--------------------------------read-file---------------------------------##

def read():
	r=input("Enter The File Name:-")
	gout("hadoop fs -cat /{}".format(r))

##-------------------------------delete-file--------------------------------##

def delete():
	r=input("Give the file name which you want to remove")
	gout("hadoop fs -rm /{}".format(r))

##--------------------------------cluster-----------------------------------##
	
def cluster():
	print("""
	Press:1 Web Browser
	Press:2 On File
	Press:3 On Shell
	""")

	k=input("Enter Your Choise:-")
	if k==1:
		x=gout("ifconfig enp0s3") #use whatever your n/w card like enp0s3,etho,etc..
		ip=x.split(" ")
		gout("firefox {}:50070".format(ip[13]))
	elif k==2:
		fname=input("Enter file name:-\n")
		gout("hadoop dfsadmin -report > /root/Desktop/{}.txt".format(fname))
	elif k==3:
		f=gout("hadoop dfsadmin -report")
		print(f)

##----------------------------------------Program-starts-from-here------------------------------------------##

def start():

	print("""
	Press:1 For make hdfs-cluster
	Press:2 For read file
	Press:3 For delete file
	Press:4 For see hdfs cluster
	""")
	x=int(input("Enter your choise:-"))
	
	if x==1:
		hadoop()
	elif x==2:
		read()
	elif x==3:
		delete()
	elif x==4:
		cluster()
	else:
		print("Wrong choise\n____________\n")
		start()

start()
