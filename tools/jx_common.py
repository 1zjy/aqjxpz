#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands
import socket
import re
import string,random
import os

XT_USER=['abrt','adm','amandabackup','avahi','avahi-autoipd','bin','chrony','cockpit-ws','colord','daemon','dbus','dirsrv','dovecot','dovenull','games','gdm','geoclue','gnome-initial-setup','gopher','haldaemon','halt','hsqldb','ipaapi','kdcproxy','lp','luci','mail','nfsnobody','nobody','ntp','ods','operator','oprofile','pcp','pegasus','piranha','pkiuser','polkitd','postfix','pulse','qemu','radvd','ricci','rpc','rpcuser','rtkit','saslauth','setroubleshoot','shutdown','sshd','sync','systemd-network','tcpdump','tss','unbound','usbmuxd','uucp','vcsa','webalizer']
YW_USER=['root','cqswj','oracle','grid','weblogic','nginx','redis','mysql','tomcat','apache','nagios','cqdzswjftp','dzzlkftp','ftp','xtyw','postgres','kluser','named']
SU_COMMONUser=['cqswj','weblogic','oracle','grid','nginx','apache','xtyw','tomcat']
HLWIPD=['10.116.100.*','10.116.101.*','10.116.102.*','10.116.103.*','10.116.104.*','10.116.105.*','10.116.107.*']
NTP_MAPGroups={'10.116.*>10.116.154/157':'10.116.123.25/10.116.123.26','98.11.*<10.116.154/10.116.157':'98.11.89.1/98.11.89.2','162.*.*|10.200.*':'162.30.53.100/162.30.53.101'}
NTPSJY={'紫光DMZ区时间源':'10.116.123.25/26','紫光核心区时间源':'98.11.89.1/2','华为核心区时间源':'162.12.88.1/3','西区核心区时间源':'162.30.53.100/101'}
try:
    JXGL_IP=socket.gethostbyname(socket.gethostname())
except Exception:
       JXGL_IP='127.0.0.1' 
JXGL_Report=""
fhd_score=0
ZHGL_MAXTMOUT=600 #登录超时时间最大值(s)
ZHGL_JYTMOUT=300  #建议登录超时时间(s)
jxdlcount=0  #基线检查大类数
jxitemtotalcount=50 #基线检查总数
jxitemsjtotalcount=0  #基线检查实际项目数
filedictgroups={'/etc':'755','/tmp':'750','/etc/rc.d/init.d':'750','/etc/passwd':'644','/etc/group':'644','/etc/shadow':'400','/etc/services':'644','/etc/security':'600','/etc/rc0.d/':'750','/etc/rc1.d/':'750','/etc/rc2.d/':'750','/etc/rc3.d/':'750','/etc/rc4.d/':'750','/etc/rc5.d/':'750','/etc/rc6.d/':'750','/etc/rc.d/init.d':'750'}
JX_minlen=8  #基线密码复杂度最小长度
KL_minlen=10 #口令最小长度10
KLJY_minlen=12 #口令建议设置12
KLGXZQ_MAX_DAYS=90 #密码最大更新周期
KLGXZQ_WRN_DAYS=30 #密码警告期限
SSHD_Config_FILE='/etc/ssh/sshd_config' #sshd配置文件
swappiness_alarmvalue=10
xtyw_zhmc='xtyw'
xtyw_homeauthorized_keys='/home/%s/.ssh/authorized_keys' % xtyw_zhmc
usermaxexpiredate='99999'
xtyw_publicmy='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1wYTh7cw1lUBcgr5kMKtLilh3CwbxhCJDITgZfYDlbNtPiURtrvpamBMHMYz9EuuBmXyXSF9D18oD/HmFiIXzgqobTGw2asNxwbpoPBY1YxvHJAZUV99ml/GrqdIFbLW2lgDsojIkXA0rnxZ1G/uHOaZBPuKKnvlaXyhtMV4NdZFK3UuzDyz82Bx8FLGVo+clkkZ9BeOWyOrTi5ihk/6ime24WdiSue2XwXxjrGCSu4oKBDNj778ytl31HSUz14gBrH4em1nLM22+P6ddVhrKp4oJgvY7IqAG1ibhuxUNXWkf3Q5EM5ZKdchK9TCKdKhiFqwGgiCmQAonjRD8Cx9H xtyw@hxq-poller21'
pwd_reg='^(?![A-Za-z0-9]+$)(?![a-z0-9\\W]+$)(?![A-Za-z\\W]+$)(?![A-Z0-9\\W]+$)^.{12,}$'
snmp_summry='cqsw'
ProcessFileNumpzgroups=['soft    nproc','hard    nproc','soft    nofile','hard    nofile']
ZJJ_USER=['weblogic','oracle','grid','nginx','apache','tomcat']
DisableAliasGroups={'games':'root','ingres':'root','system':'root','toor':'root','uucp':'root','manager':'root','dumper':'root','operator':'root','decode':'root','root':'marc'}
gnomepz_dict6={'启用屏保|blank-only':'','启用空闲激活时间|idle_delay':'15','启用空闲激活|idle_activation_enabled':'true','启用屏幕锁定|lock_enabled':'true'}
gnomepz_dict7={'启用激活空闲激活(centos 7 )|idle-activation-enabled':'true','启用屏幕锁定(centos 7)|lock-enabled':'true','黑屏至锁屏延迟时间（centos 7）|lock-delay':'300','启用空闲激活时间 （centos 7）|idle-delay':'300'}
NHCS_Dict={'accept_source_route':'0','accept_redirects':'0','accept_redirects':'0','send_redirects':'0','icmp_echo_ignore_broadcasts':'1','ip_forward':'0'}
Safedogkzzx=['10.116.124.65']
Safedog_permitclientipgroups=['98.11.*.*','10.116.*.*>10.116.154.*/10.116.157.*']



#字体色     |       背景色     |      颜色描述
#-------------------------------------------
#30        |        40       |       黑色
#31        |        41       |       红色
#32        |        42       |       绿色
#33        |        43       |       黃色
#34        |        44       |       蓝色
#35        |        45       |       紫红色
#36        |        46       |       青蓝色
#37        |        47       |       白色
#-------------------------------------------
#-------------------------------
#显示方式     |      效果
#-------------------------------
#0           |     终端默认设置
#1           |     高亮显示
#4           |     使用下划线
#5           |     闪烁
#7           |     反白显示
#8           |     不可见
#-------------------------------


#正常输出信息函数
def write_report(level,filename,lx,str):
    f=open(filename,lx)
    if level==2:
       f.write("\033[1;35m %s \033[0m\n" % str)
       print('\033[1;35m %s \033[0m' % str)
    elif level==1:
       f.write("\033[1;33m %s \033[0m\n" % str)
       print('\033[1;33m %s \033[0m' % str)
    elif level==3:
       f.write("\033[1;32m %s \033[0m\n" % str)
       print('\033[1;32m %s \033[0m' % str)
    else:
       f.write(str+"\n")
       print str
    f.close()
    
#检查操作系统版本    
def get_osversion():
    cmdstr="uname -r|awk -F '.' '{ print $(NF-1) }'| tr -cd '[0-9]'"
    try:
       osversion=int(commands.getoutput(cmdstr))
    except Exception:
       osversion=-1
    return osversion
    
def check_pwd(string):
    pattern = r'%s' % pwd_reg
    res = re.search(pattern, string)
    if res:
        return 0
    else:
        return 2
        
def get_randompwd(length):
    cmdstr="openssl rand -base64 50|tr -dc A-Z-a-z-0-9|head -c${1:-%s}" % length
    pwd=commands.getoutput(cmdstr).strip()
    return  pwd


 

#检测yum源是否正常
def PD_ISYUMSRC():
    cleanstr="yum clean all >/dev/null"
    liststr="yum list >/dev/null"
    cleanstatus=os.system(cleanstr)
    liststatus=os.system(liststr)
    if cleanstatus==0 and liststatus==0:
       return 0
    else:
       return 2 
    
#小结得分函数
def Summary_score(dlnum,totalitemnum,jxitemsjcount,op,jxdf,pznum):
    global jxitemsjtotalcount
    if op=='--check':
       printjg='''
☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

   【基线检查[%d]】共%d项,实际扫描%d项,小计得%d分,累计得%d分.

☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
               ''' % (dlnum,totalitemnum,jxitemsjcount,jxdf,fhd_score)
    elif op=='--config':
         if pznum==0:
            pzbfb=100
         elif pznum!=-1:
            pzbfb=jxdf/pznum*100
         else:
            pzbfb=0
         printjg='''
☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

 【基线检查[%d]】共%d项,实际扫描%d项，实际配置%d项，配置成功率%d%%.

☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
                 ''' % (dlnum,totalitemnum,jxitemsjcount,pznum,pzbfb)  
    
    else:
        printjg="无"
    jxitemsjtotalcount+=jxitemsjcount        
    write_report(-1,JXGL_Report,'a',printjg) 