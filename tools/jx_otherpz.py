#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import jx_common
import re

xjdf=0
totalitemnum=11
checkconfigbz=-1
notconfignum=0
configsuccessnum=0
jxitemsjcount=0

def Header_otherpz():
    printjg='''
****************************************************************************

               Linux基线规范检查和配置：8、其他配置要求

****************************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 


#No8.1、【配置要求】：检查是否设置ssh登录前警告Banner
def Warn_banner(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_1="★★★★★★★★★★No8.1、【配置要求】：检查是否设置ssh登录前警告Banner★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    banner_file='/etc/ssh_banner'
    cmdstr="cat /etc/ssh/sshd_config|grep -v '^#'|grep 'Banner /etc/ssh_banner'"
    cmdvalue=commands.getoutput(cmdstr).strip()
    if op=='--check':
       if cmdvalue=="":
          sbbzcount+=1
          exppzlist+="[%d]/etc/ssh/sshd_config未添加ssh_banner配置\n" %  linenum
       else:
          if not os.path.isfile(banner_file):
             sbbzcount+=1
             exppzlist+="[%d]%s配置文件不存在\n" %  (linenum,banner_file)
          else:
             cmdstr1="stat -c %%a %s" % banner_file
             cmdvalue1=(commands.getoutput(cmdstr1)).replace('\n','').strip()
             cmdstr2="stat -c %%U %s" % banner_file
             cmdvalue2=(commands.getoutput(cmdstr2)).replace('\n','').strip()
             cmdstr3="stat -c %%G %s" % banner_file
             cmdvalue3=(commands.getoutput(cmdstr3)).replace('\n','').strip()
             print 
             if cmdvalue1!='644':
                sbbzcount+=1
                exppzlist+="[%d]%s文件权限为%s,不符合标准权限644\n" %  (linenum,cmdvalue1,banner_file)
             elif cmdvalue2!='bin' or cmdvalue3!='bin':
                  sbbzcount+=1
                  exppzlist+="[%d]%s文件属主为%s属组为%s,不符合标准权限bin:bin\n" %  (linenum,cmdvalue2,cmdvalue3,banner_file)
             else:
                cmdstr="cat %s|grep -v '^#'|grep 'Authorized only. All activity will be monitored and reported'" % banner_file
                cmdvalue=commands.getoutput(cmdstr).strip()
                if cmdvalue=="":
                   sbbzcount+=1
                   exppzlist+="[%d]%s文件未添加配置\"Authorized only. All activity will be monitored and reported\"\n" %  (linenum,banner_file)
    elif op=='--config':
         if cmdvalue=="":
            cmdstr="echo 'Banner /etc/ssh_banner' >> /etc/ssh/sshd_config"
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[%d]/etc/ssh/sshd_config添加Banner /etc/ssh_banner配置失败\n" %  linenum
            else:
               successcount+=1
               successlist+="[%d]/etc/ssh/sshd_config添加Banner /etc/ssh_banner配置成功\n" %  linenum
               linenum+=1
               cmdstr="service sshd restart>/dev/null"
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]ssh服务重启失败\n" %  linenum
               else:
                  successcount+=1
                  successlist+="[%d]ssh服务重启成功！！\n" %  linenum
               linenum+=1
         if not os.path.isfile(banner_file):
            cmdstr="touch /etc/ssh_banner"
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[%d]%s配置文件创建失败\n" %  (linenum,banner_file)
            else:
               successcount+=1
               successlist+="[%d]%s配置文件创建成功\n" %  (linenum,banner_file)
            linenum+=1
         cmdstr1="stat -c %%a %s" % banner_file
         cmdvalue1=(commands.getoutput(cmdstr1)).replace('\n','').strip()
         cmdstr2="stat -c %%U %s" % banner_file
         cmdvalue2=(commands.getoutput(cmdstr2)).replace('\n','').strip()
         cmdstr3="stat -c %%G %s" % banner_file
         cmdvalue3=(commands.getoutput(cmdstr3)).replace('\n','').strip()
         if cmdvalue1!='644':
            cmdstr="chmod 644 %s"  % banner_file
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[%d]%s文件配置权限为644失败\n" %  (linenum,banner_file)
            else:
               successcount+=1
               successlist+="[%d]%s文件配置权限为644成功\n" %  (linenum,banner_file)
            linenum+=1
         if cmdvalue2!='bin' or cmdvalue3!='bin': 
              cmdstr="chown bin:bin %s"  % banner_file
              cmdstatus=os.system(cmdstr)
              if cmdstatus!=0:
                 sbbzcount+=1
                 exppzlist+="[%d]%s文件属主%s属组为%s,不符合标准bin:bin\n" %  (linenum,banner_file,cmdvalue2,cmdvalue3)
              else:
                 successcount+=1
                 successlist+="[%d]%s文件属主%s属组为%s,符合标准bin:bin\n" %  (linenum,banner_file,cmdvalue2,cmdvalue3)
              linenum+=1
         cmdstr="cat %s|grep -v '^#'|grep 'Authorized only. All activity will be monitored and reported'" % banner_file
         cmdvalue=commands.getoutput(cmdstr).strip()
         if cmdvalue=="":
            cmdstr="echo 'Authorized only. All activity will be monitored and reported' >>%s" % banner_file
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[%d]%s文件添加配置\"Authorized only. All activity will be monitored and reported\"失败！！\n" %  (linenum,banner_file)
            else:
               successcount+=1
               successlist+="[%d]%s文件添加配置\"Authorized only. All activity will be monitored and reported\"成功！！\n" %  (linenum,banner_file)
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照是否设置ssh登录前警告Banner检查,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_1,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照是否设置ssh登录前警告Banner检查，配置检查都符合基线配置规范。
                  ''' %  No8_1
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照是否设置ssh登录前警告Banner检查，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_1,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照是否设置ssh登录前警告Banner检查，%d项配置更新全部成功！！
需要过程如下：
%s             
               ''' % (No8_1,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照是否设置ssh登录前警告Banner检查,服务配置都符合基线配置规范。    
               ''' %  No8_1
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
#No8.2、【配置要求】：检查是否修改SNMP默认团体字
def SNMP_publicpz(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_2="★★★★★★★★★★No8.2、【配置要求】：检查是否修改SNMP默认团体字★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    snmp_summry=jx_common.snmp_summry
    banner_file='/etc/ssh_banner'
    cmdstr="rpm -qa|grep net-snmp"
    cmdvalue=commands.getoutput(cmdstr).strip()
    if op=='--check':
       if 'net-snmp-utils' not in cmdvalue and 'net-snmp-libs' not in cmdvalue and 'net-snmp' not in cmdvalue:
          sbbzcount+=1
          exppzlist+="[%d]当前系统未安装net-snmp相关rpm包\n" %  linenum
       else:
          cmdstr="ps -ef|grep 'snmpd'|grep -v 'grep'"
          cmdvalue=commands.getoutput(cmdstr).strip()
          if cmdvalue=="":
             sbbzcount+=1
             exppzlist+="[%d]snmp服务没启动,未找到snmpd相关进程\n" %  linenum
          else:
             cmdstr="cat /etc/snmp/snmpd.conf|grep -v  '^#'|grep '^com2sec'|grep 'public'"
             cmdvalue=commands.getoutput(cmdstr).strip()
             if cmdvalue!="":
                sbbzcount+=1
                exppzlist+="[%d]/etc/snmp/snmpd.conf中配置是默认团体字public\n" %  linenum
    elif op=='--config':
         if 'net-snmp-utils' not in cmdvalue or 'net-snmp-libs' not in cmdvalue or 'net-snmp' not in cmdvalue:
            yumstate=jx_common.PD_ISYUMSRC()
            if yumstate!=0:   
               sbbzcount+=1
               exppzlist+="[%d]当前系统YUM源配置异常，请检查配置\n" %  linenum
            else:
               cmdstr="yum install -y net-snmp net-snmp-libs net-snmp-utils >/dev/null"
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]net-snmp、net-snmp-libs、net-snmp-utils安装失败！！" %  linenum
               else:
                  successcount+=1
                  successlist="[%d]net-snmp、net-snmp-libs、net-snmp-utils安装成功！！" %  linenum
            linenum+=1
         cmdstr="ps -ef|grep 'snmpd'|grep -v 'grep'"
         cmdvalue=commands.getoutput(cmdstr).strip()
         if cmdvalue=="":
            cmdstr="service snmpd start >/dev/null 2>&1"
            cmdstatus=os.system(cmdstr)
            cmdstr="ps -ef|grep 'snmpd'|grep -v 'grep'"
            cmdvalue=commands.getoutput(cmdstr).strip()
            if cmdstatus!=0 and cmdvalue=="":
               sbbzcount+=1
               exppzlist+="[%d]snmp服务启动失败,未找到相关进程！！\n" %  linenum
            elif cmdstatus==0 and cmdvalue!="":
                 successcount+=1
                 successlist+="[%d]snmp服务启动成功,找到snmp相关进程！！\n" %  linenum
            linenum+=1
         cmdstr="cat /etc/snmp/snmpd.conf|grep -v  '^#'|grep '^com2sec'|grep 'public'"
         cmdvalue=commands.getoutput(cmdstr).strip()
         if cmdvalue!="":
            cmdstr="sed -i '/^com2sec/s/public/%s/g' /etc/snmp/snmpd.conf"  % snmp_summry
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[%d]/etc/snmp/snmpd.conf中默认团体字public修改为%s失败\n" %  (linenum,snmp_summry)
            else:
                successcount+=1
                successlist+="[%d]/etc/snmp/snmpd.conf中默认团体字public修改为%s成功！！\n" %  (linenum,snmp_summry)
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照检查是否修改SNMP默认团体字,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_2,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查是否修改SNMP默认团体字，配置检查都符合基线配置规范。
                  ''' %  No8_2
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照检查是否修改SNMP默认团体字，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_2,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照检查是否修改SNMP默认团体字，%d项配置更新全部成功！！
需要过程如下：
%s             
               ''' % (No8_2,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照检查是否修改SNMP默认团体字,服务配置都符合基线配置规范。    
               ''' %  No8_2
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    


#No8.3、【配置要求】：检查系统是否禁用Ctrl+Alt+Delete组合键
def Close_ctrl_alt_del(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_3="★★★★★★★★★★No8.3、【配置要求】：检查系统是否禁用Ctrl+Alt+Delete组合键★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    osversion=jx_common.get_osversion()
    Linux6_file='/etc/init/control-alt-delete.conf'
    Linux7_file='/usr/lib/systemd/system/ctrl-alt-del.target'
    Linux5_file='cat /etc/inittab'
    if op=='--check':
       if osversion==5:
          if os.path.isfile(Linux5_file):
             cmdstr="cat %s|grep -v '^#'|grep -E '^ca::ctrlaltdel:/sbin/shutdown -t3 -r now'" % Linux5_file
             cmdvalue=commands.getoutput(cmdstr).strip()
             if cmdvalue!="":
                sbbzcount+=1
                exppzlist+="[%d]Linux%s未禁用Ctrl+Alt+Delete配置\n" %  (linenum,osversion)
       elif osversion==6:
            if os.path.isfile(Linux6_file):
               cmdstr="cat %s|grep -v '^#'|grep -E '^exec /sbin/shutdown'|grep -E 'Control-Alt-Delete pressed'" % Linux6_file
               cmdvalue=commands.getoutput(cmdstr).strip()
               if cmdvalue!="":
                  sbbzcount+=1
                  exppzlist+="[%d]Linux%s未禁用Ctrl+Alt+Delete配置\n" %  (linenum,osversion)
       elif osversion==7:
            cmdstr="cat %s|grep -v '^#'" % Linux7_file
            cmdvalue=commands.getoutput(cmdstr).strip()
            if os.path.isfile(Linux7_file) and cmdvalue!="":
               sbbzcount+=1
               exppzlist+="[%d]Linux%s未禁用Ctrl+Alt+Delete配置\n" %  (linenum,osversion) 
       else:
            sbbzcount+=1
            exppzlist+="[%d]Linux版本获取失败\n" %  linenum       
    elif op=='--config':
         if osversion==5:
            if os.path.isfile(Linux5_file):
               cmdstr="cat %s|grep -v '^#'|grep -E '^ca::ctrlaltdel:/sbin/shutdown -t3 -r now'" % Linux5_file
               cmdvalue=commands.getoutput(cmdstr).strip()
               if cmdvalue!="":
                  cmdstr="sed -i '/^ca::ctrlaltdel:\/sbin\/shutdown/s/^/#/g' %s" % Linux5_file
                  cmdstatus=os.system(cmdstr)
                  if cmdstatus!=0:
                     sbbzcount+=1
                     exppzlist+="[%d]Linux%s禁用Ctrl+Alt+Delete配置过程失败\n" %  (linenum,osversion)
                  else:
                     successcount+=1
                     successlist+="[%d]Linux%s禁用Ctrl+Alt+Delete配置过程成功\n" %  (linenum,osversion)
         elif osversion==6:
              if os.path.isfile(Linux6_file):
                 cmdstr="cat %s|grep -v '^#'|grep -E '^exec /sbin/shutdown'|grep -E 'Control-Alt-Delete pressed'" % Linux6_file
                 cmdvalue=commands.getoutput(cmdstr).strip()
                 if cmdvalue!="":
                    cmdstr="sed -i '/^exec \/sbin\/shutdown/s/^/#/g' %s" % Linux6_file
                    cmdstatus=os.system(cmdstr)
                    if cmdstatus!=0:
                       sbbzcount+=1
                       exppzlist+="[%d]Linux%s禁用Ctrl+Alt+Delete配置过程失败\n" %  (linenum,osversion)
                    else:
                       successcount+=1
                       successlist+="[%d]Linux%s禁用Ctrl+Alt+Delete配置过程成功\n" %  (linenum,osversion)
         elif osversion==7:
              cmdstr="cat %s|grep -v '^#'" % Linux7_file
              cmdvalue=commands.getoutput(cmdstr).strip()
              if os.path.isfile(Linux7_file) and cmdvalue!="":
                 cmdstr="mv %s  %s.bak" % (Linux7_file,Linux7_file)
                 cmdstatus1=os.system(cmdstr)
                 cmdstr2="init q"
                 cmdstatus2=os.system(cmdstr2)
                 if cmdstatus1!=0 or cmdstatus2!=0:
                    sbbzcount+=1
                    exppzlist+="[%d]Linux%s禁用Ctrl+Alt+Delete配置过程失败\n" %  (linenum,osversion)
                 else:
                    successcount+=1
                    successlist+="[%d]Linux%s禁用Ctrl+Alt+Delete配置过程成功\n" %  (linenum,osversion)
         else:
              sbbzcount+=1
              exppzlist+="[%d]Linux版本获取失败\n" %  (linenum,osversion)  
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照检查系统是否禁用Ctrl+Alt+Delete组合键,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_3,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查系统是否禁用Ctrl+Alt+Delete组合键，配置检查都符合基线配置规范。
                  ''' %  No8_3
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照检查系统是否禁用Ctrl+Alt+Delete组合键，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_2,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照检查系统是否禁用Ctrl+Alt+Delete组合键，%d项配置更新全部成功！！
需要过程如下：
%s             
               ''' % (No8_3,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照检查系统是否禁用Ctrl+Alt+Delete组合键,服务配置都符合基线配置规范。    
               ''' %  No8_3
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    

    
    
    
#No8.4、【配置要求】：主机须启用时钟同步
def Host_ntppz(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_4="★★★★★★★★★★No8.4、【配置要求】：主机须启用时钟同步★★★★★★★★★★" 
    jxzt=0
    linenum=1
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    osversion=jx_common.get_osversion()
    IP=jx_common.JXGL_IP
    NTP_MAPGroups=jx_common.NTP_MAPGroups
    rpm_str="rpm -qa|grep -E  'ntp-'"
    is_install=commands.getoutput(rpm_str).strip()
    IP1w=IP.split('.')[0]
    IP2w=str(re.findall(r'(?<!\d)\d{1,3}\.\d{1,3}(?=\.\d)', IP)[0])
    IP3w=str(re.findall(r'(?<!\d)\d{1,3}\.\d{1,3}(?=\.\d).\d{1,3}(?=\.\d)', IP)[0])
    checkntpstate=0
    cmdstr="cat /etc/ntp.conf |grep '^server'|awk '{ print $2 }'"
    cmdgroups=(commands.getoutput(cmdstr)).replace('\n','').strip().split('\n')
    if op=='--check':
       if is_install=="":
          sbbzcount+=1
          exppzlist+="[%d]Linux%s未安装NTP包!!\n" %  (linenum,osversion)
       else:
          if len(cmdgroups)==0:
             sbbzcount+=1
             exppzlist+="[%d]Linux%s NTP未配置\n" %  (linenum,osversion)
          else:
             for k,v in NTP_MAPGroups.items():
                 fhd=0
                 if '>' in k:
                    IPstr=k.split('>')[0].strip('.*')
                    if IPstr.strip('.*')!=IP2w:
                       continue
                    else:
                       fhd+=1
                 elif '<' in k:
                    IPstr=k.split('<')[0].strip('.*')
                    if IPstr!=IP2w:
                       if IP3w not in k.split('<')[0].split('/'):
                          continue
                       else:
                          fhd+=1
                    else:
                       fhd+=1
                 elif '|' in k:
                    IPgroups=k.split('|')
                    for p in IPgroups:
                        IPstr=p.strip('.*')
                        if len(IPstr.split('.'))==1:
                           if IPstr!=IP1w:
                              continue
                           else:
                              fhd+=1
                        else:
                           if IPstr!=IP2w:
                              continue
                           else:
                              fhd+=1                
                 if fhd>=1:
                    for i in cmdgroups:
                        if i not in v.split('/'):
                           sbbzcount+=1
                           exppzlist+="[%d]Linux%s NTP未配置对应区域NTP（%s）\n" %  (linenum,osversion,k)
                           linenum+=1
                    break
          if sbbzcount==0:
             cmdstr="ps -fe|grep -v 'grep'|grep -E  'ntpd'"
             cmdvalue=commands.getoutput(cmdstr).strip()
             if cmdvalue=="":
                sbbzcount+=1
                exppzlist+="[%d]Linux%s NTP服务未启动\n" %  (linenum,osversion)
             else:
                if osversion==7:
                   cmdstr="systemctl list-unit-files|grep enabled|awk -F '.' '{ print $1}'|grep ntpd"
                   cmdvalue=commands.getoutput(cmdstr).strip()
                   if cmdvalue=="":
                      sbbzcount+=1
                      exppzlist+="[%d]Linux%s 开机自启动未设置\n" %  (linenum,osversion)
                elif osversion==6:
                     cmdstr="chkconfig --list |grep 3:on|grep ntpd >/dev/null"
                     cmdstatus=os.system(cmdstr)
                     if cmdstatus!=0:
                        sbbzcount+=1
                        exppzlist+="[%d]Linux%s 开机自启动未设置\n" %  (linenum,osversion) 
    elif op=='--config':
         if is_install=="":
            yumstate=jx_common.PD_ISYUMSRC()
            if yumstate!=0:   
               sbbzcount+=1
               exppzlist+="[%d]当前系统YUM源配置异常，请检查配置\n" %  linenum
            else:  
               cmdstr="yum install -y ntpd >/dev/null"
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]ntpd安装失败！！" %  linenum
               else:
                  successcount+=1
                  successlist="[%d]ntpd安装成功！！" %  linenum
               linenum+=1
         for k,v in NTP_MAPGroups.items():
             fhd=0
             if '>' in k:
                IPstr=k.split('>')[0].strip('.*')
                if IPstr.strip('.*')!=IP2w:
                   continue
                else:
                   fhd+=1
             elif '<' in k:
                IPstr=k.split('<')[0].strip('.*')
                if IPstr!=IP2w:
                   if IP3w not in k.split('<')[0].split('/'):
                      continue
                   else:
                      fhd+=1
                else:
                   fhd+=1
             elif '|' in k:
                IPgroups=k.split('|')
                for p in IPgroups:
                    IPstr=p.strip('.*')
                    if len(IPstr.split('.'))==1:
                       if IPstr!=IP1w:
                          continue
                       else:
                          fhd+=1
                    else:
                       if IPstr!=IP2w:
                          continue
                       else:
                          fhd+=1                      
             if fhd>=1:
                ntpsrcgroups=v.split('/')
                if len(cmdgroups)>0:             
                   for i in cmdgroups:
                       n=0
                       if i not in ntpsrcgroups:
                          cmdstr="sed -i '/^server/s/%s/%s/g' /etc/ntp.conf"  % (i,ntpsrcgroups[n])
                          cmdstatus=os.system(cmdstr)
                          if cmdstatus!=0:
                             sbbzcount+=1
                             exppzlist+="[%d]Linux%s NTP配置对应区域NTP IP（%s）失败\n" %  (linenum,osversion,ntpsrcgroups[n])
                          else:
                             successcount+=1
                             successlist+="[%d]Linux%s NTP配置对应区域NTP IP（%s）成功\n" %  (linenum,osversion,ntpsrcgroups[n])
                          linenum+=1
                       n+=1
                   break
                else:
                   for i in ntpsrcgroups:
                       n=0
                       cmdstr="echo 'server %s perfer'>>/etc/ntp.conf" % i
                       cmdstatus=os.system(cmdstr)
                       if cmdstatus!=0:
                          sbbzcount+=1
                          exppzlist+="[%d]Linux%s NTP配置对应区域NTP IP（%s）失败\n" %  (linenum,osversion,ntpsrcgroups[n])
                       else:
                          successcount+=1
                          successlist+="[%d]Linux%s NTP配置对应区域NTP IP（%s）成功\n" %  (linenum,osversion,ntpsrcgroups[n])
                       linenum+=1
                       n+=1                          
         cmdstr="ps -fe|grep -v 'grep'|grep -E  'ntpd'"
         cmdvalue=commands.getoutput(cmdstr).strip()
         if cmdvalue=="":
            cmdstr="service ntpd start >/dev/null"
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[%d]Linux%s NTP服务启动失败\n" %  (linenum,osversion)
            else:
               successcount+=1
               successlist+="[%d]Linux%s NTP服务启动成功\n" %  (linenum,osversion) 
            linenum+=1
         if osversion==7:
            cmdstr="systemctl list-unit-files|grep enabled|awk -F '.' '{ print $1}'|grep ntpd"
            cmdvalue=commands.getoutput(cmdstr).strip()
            if cmdvalue=="":
               cmdstr="systemctl enable ntpd >/dev/null"
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]Linux%s 开机自启动设置失败\n" %  (linenum,osversion)
               else:
                  successcount+=1
                  successlist+="[%d]Linux%s 开机自启动设置成功\n" %  (linenum,osversion)
         elif osversion==6:
              cmdstr="chkconfig --list |grep 3:on|grep ntpd >/dev/null"
              cmdstatus=os.system(cmdstr)
              if cmdstatus!=0:
                 cmdstr="chkconfig --level 12345 ntpd on >/dev/null"
                 cmdstatus=os.system(cmdstr)
                 if cmdstatus!=0:
                    sbbzcount+=1
                    exppzlist+="[%d]Linux%s 开机自启动设置失败\n" %  (linenum,osversion) 
                 else:
                    successcount+=1
                    successlist+="[%d]Linux%s 开机自启动设置成功\n" %  (linenum,osversion)
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照主机须启用时钟同步,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_4,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照主机须启用时钟同步，配置检查都符合基线配置规范。
                  ''' %  No8_4
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照主机须启用时钟同步，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_4,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照主机须启用时钟同步，%d项配置更新全部成功！！
需要过程如下：
%s             
               ''' % (No8_4,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照主机须启用时钟同步,服务配置都符合基线配置规范。    
               ''' %  No8_4
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
    
#No8.5、【配置要求】：禁用core dump
def Close_coredump(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_5="★★★★★★★★★★No8.5、【配置要求】：禁用core dump★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    corepzgroups=['* soft core 0','* hard core 0']
    if op=='--check':
       for c in corepzgroups:
           cmdstr="cat /etc/security/limits.conf|grep -E '%s'" % c
           cmdvalue=commands.getoutput(cmdstr).strip()
           if cmdvalue=="":
              sbbzcount+=1
              exppzlist+="[%d]/etc/security/limits.conf中未配置%s.\n" %  (linenum,c)
              linenum+=1
    elif op=='--config':
         for c in corepzgroups:
             cmdstr="cat /etc/security/limits.conf|grep -E '%s'" % c
             cmdvalue=commands.getoutput(cmdstr).strip()
             if cmdvalue=="":
                cmdstr="echo '%s' >>/etc/security/limits.conf" % c
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]/etc/security/limits.conf中添加%s配置失败.\n" %  (linenum,c)
                else:
                   successcount+=1
                   successlist+="[%d]/etc/security/limits.conf中添加%s配置成功.\n" %  (linenum,c)
             linenum+=1
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照检查禁用core dump,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_5,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查禁用core dump，配置检查都符合基线配置规范。
                  ''' %  No8_5
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照检查禁用core dump，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_5,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照检查禁用core dump，%d项配置更新全部成功！！
需要过程如下：
%s             
               ''' % (No8_5,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照检查禁用core dump,服务配置都符合基线配置规范。    
               ''' %  No8_5
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
    
#No8.6、【配置要求】：用户使用最大进程数及文件打开数配置
def User_ProcessFileNum(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_6="★★★★★★★★★★No8.6、【配置要求】：用户使用最大进程数及文件打开数配置★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    ProcessFileNumpzgroups=jx_common.ProcessFileNumpzgroups
    if op=='--check':
       for c in ProcessFileNumpzgroups:
           cmdstr="cat /etc/security/limits.conf|grep -v '^#'|grep '%s'" %  c
           cmdvalue=commands.getoutput(cmdstr).strip()
           if cmdvalue=="":
              sbbzcount+=1
              exppzlist+="[%d]/etc/security/limits.conf中%s未配置.\n" %  (linenum,c)
              linenum+=1
    elif op=='--config':
         for c in ProcessFileNumpzgroups:
             cmdstr="cat /etc/security/limits.conf|grep -v '^#'|grep '%s'" %  c
             cmdvalue=commands.getoutput(cmdstr).strip()
             if cmdvalue=="":
                cmdstr="echo '*  %s  65535' >>/etc/security/limits.conf" % c
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]/etc/security/limits.conf中添加*  %s  65535配置失败.\n" %  (linenum,c)
                else:
                   successcount+=1
                   successlist+="[%d]/etc/security/limits.conf中添加*  %s  65535配置成功.\n" %  (linenum,c)
             linenum+=1
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照用户使用最大进程数及文件打开数配置,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_6,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照用户使用最大进程数及文件打开数配置，配置检查都符合基线配置规范。
                  ''' %  No8_6
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if jxzt==2 :
            printjg='''
%s
配置结果：[失败]按照用户使用最大进程数及文件打开数配置，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_6,sbbzcount,exppzlist)
            checkconfigbz=2
         elif jxzt==1:
              printjg='''
%s
配置结果：[成功]按照用户使用最大进程数及文件打开数配置，%d项配置更新全部成功！！
需要过程如下：
%s             
            ''' % (No8_6,successcount,successlist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]按照用户使用最大进程数及文件打开数配置,服务配置都符合基线配置规范。    
               ''' %  No8_6
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
#No8.7、【配置要求】：系统服务优先级配置
def Service_priority(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_7="★★★★★★★★★★No8.7、【配置要求】：系统服务优先级配置★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    notesxitusercount=0
    ZJJ_USRgroups=jx_common.ZJJ_USER
    if op=='--check':
       cmdstr="cat /etc/sudoers|grep -v '^#'|grep 'NOPASSWD:/usr/bin/renice'"    
       cmdvalue=commands.getoutput(cmdstr).strip()
       if cmdvalue=="":
          sbbzcount+=1
          exppzlist+="[%d]/etc/sudoers中{%s} ALL=(ALL) NOPASSWD:/usr/bin/renice未配置.\n" %  (linenum,ZJJ_USRgroups)
    elif op=='--config':
         cmdstr="cat /etc/sudoers|grep -v '^#'|grep 'NOPASSWD:/usr/bin/renice'"    
         cmdvalue=commands.getoutput(cmdstr).strip()
         if cmdvalue=="":
            cmdstr1="stat -c %%a /etc/sudoers"
            cmdvalue1=commands.getoutput(cmdstr1).strip()
            if cmdvalue1!='640':
               cmdstr2="chmod 640 /etc/sudoers"
               cmdstatus2=os.system(cmdstr2)
               if cmdstatus2!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]/etc/sudoers修改为640权限失败.\n" %  linenum
               else:
                  successcount+=1
                  successlist+="[%d]/etc/sudoers修改为640权限成功.\n" %  linenum 
               linenum+=1
            if sbbzcount==0:            
               for u in ZJJ_USRgroups:
                   cmdstr3="id %s >/dev/null 2>&1" % u
                   cmdstatus3=os.system(cmdstr3)
                   if cmdstatus3!=0:
                      notesxitusercount+=1
                      continue
                   else:
                      cmdstr4="echo '%s ALL=(ALL) NOPASSWD:/usr/bin/renice' >>/etc/sudoers" % u
                      cmdstatus4=os.system(cmdstr4)
                      if cmdstatus4!=0:
                         sbbzcount+=1
                         exppzlist+="[%d]/etc/sudoers中添加%s ALL=(ALL) NOPASSWD:/usr/bin/renice失败\n" %  (linenum,u)
                      else:
                         successcount+=1
                         successlist+="[%d]/etc/sudoers中添加%s ALL=(ALL) NOPASSWD:/usr/bin/renice成功\n" %  (linenum,u)
                      linenum+=1
            if notesxitusercount==len(ZJJ_USRgroups):
               sbbzcount+=1
               exppzlist+="[%d]/etc/sudoers配置失败，由于系统中不存在%s里业务用户,请检查系统业务用户！！\n" %  (linenum,ZJJ_USRgroups)
               linenum+=1
            cmdstr11="stat -c %%a /etc/sudoers"
            cmdvalue11=commands.getoutput(cmdstr11).strip()
            if cmdvalue11!='440':
               cmdstr12="chmod 440 /etc/sudoers"
               cmdstatus12=os.system(cmdstr12)
               if cmdstatus12!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]/etc/sudoers权限恢复到440修改失败\n" %  linenum
               else:
                  successcount+=1
                  successlist+="[%d]/etc/sudoers权限恢复到440修改成功\n" %  linenum 
               linenum+=1
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照系统服务优先级配置,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_7,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照系统服务优先级配置，配置检查都符合基线配置规范。
                  ''' %  No8_7
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if jxzt==2 :
            printjg='''
%s
配置结果：[失败]按照系统服务优先级配置，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_7,sbbzcount,exppzlist)
            checkconfigbz=2
         elif jxzt==1:
              printjg='''
%s
配置结果：[成功]按照系统服务优先级配置，%d项配置更新全部成功！！
需要过程如下：
%s             
            ''' % (No8_7,successcount,successlist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]按照用户使用最大进程数及文件打开数配置,服务配置都符合基线配置规范。    
               ''' %  No8_7
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
#No8.8、【配置要求】：检查/etc/aliases是否禁用不必要的别名
def Disable_alias(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_8="★★★★★★★★★★No8.8、【配置要求】：检查/etc/aliases是否禁用不必要的别名★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    DisableAliasGroups=jx_common.DisableAliasGroups
    if op=='--check':
       for k,v in DisableAliasGroups.items():
           cmdstr="cat /etc/aliases|grep -v '^#'|grep '^%s'|grep '%s'" % (k,v)
           cmdvalue=commands.getoutput(cmdstr).strip()
           if cmdvalue!="":
              sbbzcount+=1
              exppzlist+="[%d]/etc/aliases中存在%s: %s没有删除或注释\n" %  (linenum,k,v)
              linenum+=1
    elif op=='--config':
         for k,v in DisableAliasGroups.items():
             cmdstr="cat /etc/aliases|grep -v '^#'|grep '^%s'|grep '%s'" % (k,v)
             cmdvalue=commands.getoutput(cmdstr).strip()
             if cmdvalue!="":
                cmdstr="sed  -i '/^%s/s/^/#/g' /etc/aliases"  % k
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]/etc/aliases中删除或注释%s: %s失败\n" %  (linenum,k,v)
                else:
                   successcount+=1
                   successlist+="[%d]/etc/aliases中删除或注释%s: %s成功\n" %  (linenum,k,v)
                linenum+=1
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照检查/etc/aliases是否禁用不必要的别名,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_8,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查/etc/aliases是否禁用不必要的别名，配置检查都符合基线配置规范。
                  ''' %  No8_8
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if jxzt==2 :
            printjg='''
%s
配置结果：[失败]按照检查/etc/aliases是否禁用不必要的别名，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_8,sbbzcount,exppzlist)
            checkconfigbz=2
         elif jxzt==1:
              printjg='''
%s
配置结果：[成功]按照检查/etc/aliases是否禁用不必要的别名，%d项配置更新全部成功！！
需要过程如下：
%s             
            ''' % (No8_8,successcount,successlist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]按照检查/etc/aliases是否禁用不必要的别名,服务配置都符合基线配置规范。    
               ''' %  No8_8
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
#No8.9、【配置要求】：检查是否配置定时自动屏幕锁定（适用于具备图形界面的设备）
def Timed_autoscreenlock(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_9="★★★★★★★★★★No8.9、【配置要求】：检查是否配置定时自动屏幕锁定（适用于具备图形界面的设备）★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    osversion=jx_common.get_osversion()
    gnomepz_dict6=jx_common.gnomepz_dict6
    gnomepz_dict7=jx_common.gnomepz_dict7
    cmdstr="rpm -qa|grep 'gnome-desktop'"
    cmdvalue=commands.getoutput(cmdstr).strip()
    if op=='--check':
       if cmdvalue!="":
          cmdstr="rpm -qa|grep GConf2"
          cmdvalue=commands.getoutput(cmdstr).strip()
          if cmdvalue=="":
             sbbzcount+=1
             exppzlist+="[%d]GConf2未配置安装\n" %  linenum
          else:
             if osversion==6 or osversion==7:
                cmdstr="ls /etc/gconf/gconf.xml.mandatory/apps 2>/dev/null"
                cmdinfo=commands.getoutput(cmdstr).strip()
                if cmdinfo!="":
                   for k1,v1 in gnomepz_dict6.item():
                       ktitle=k1.split('|')[1]
                       kmc=k1.split('|')[0]
                       if ktitle=='blank-only':
                          cmdstr="cat /etc/gconf/gconf.xml.mandatory/apps/gnome-screensaver/%gconf.xml|grep '%s'" % ktitle
                       else:
                          cmdstr="cat /etc/gconf/gconf.xml.mandatory/apps/gnome-screensaver/%gconf.xml|grep '%s'|grep '%s'" % (ktitle,v1)
                       cmdvalue=commands.getoutput(cmdstr).strip()
                       if cmdvalue=="":
                          sbbzcount+=1
                          exppzlist+="[%d]当前系统%s配置不为%s:%s\n" %  (linenum,kmc,ktitle,v1)
                          linenum+=1
             if osversion==7:
                for k2,v2 in gnomepz_dict7.item():
                    ktitle=k2.split('|')[1]
                    kmc=k2.split('|')[0]
                    if ktitle=='idle-delay':
                       cmdstr="gsettings get org.gnome.desktop.session %s" % ktitle
                    else:
                       cmdstr="gsettings get org.gnome.desktop.screensaver  %s" % ktitle
                    cmdvalue=commands.getoutput(cmdstr).strip()
                    if 'delay' in ktitle:
                       if not cmdvalue.isdigit():
                          sbbzcount+=1
                          exppzlist+="[%d]当前系统%s配置%s值不为%s\n" %  (linenum,kmc,ktitle,v2)
                          linenum+=1
                    else:
                       if cmdvalue!='true':
                          sbbzcount+=1
                          exppzlist+="[%d]当前系统%s配置%s状态不为%s\n" %  (linenum,kmc,ktitle,v2)
                          linenum+=1
       else:
           successcount+=1
           successlist+="未安装图形化界面，此基线检查跳过！！" 
    elif op=='--config':
         bz=0
         if cmdvalue!="":
            cmdstr="rpm -qa|grep GConf2"
            cmdvalue=commands.getoutput(cmdstr).strip()
            if cmdvalue=="":
               if jx_common.PD_ISYUMSRC()==2:
                  sbbzcount+=1
                  exppzlist+="[%d]YUM源异常,GConf2无法安装\n" %  linenum
               else:
                  cmdstr="yum install -y GConf2 >/dev/null 2>&1"
                  cmdstatus=os.system(cmdstr)
                  if cmdstatus!=0:
                     sbbzcount+=1
                     exppzlist+="[%d]GConf2安装失败\n" %  linenum
                  else:
                     successcount+=1
                     successlist+="[%d]GConf2安装成功\n" %  linenum 
                     if osversion==6 or osversion==7:
                        cmdstr="ls /etc/gconf/gconf.xml.mandatory/apps 2>/dev/null"
                        cmdinfo=commands.getoutput(cmdstr).strip()
                        if cmdinfo!="":
                           for k1,v1 in gnomepz_dict6.item():
                               ktitle=k1.split('|')[1]
                               kmc=k1.split('|')[0]
                               if ktitle=='blank-only':
                                  cmdstr="cat /etc/gconf/gconf.xml.mandatory/apps/gnome-screensaver/%gconf.xml|grep '%s'" % ktitle
                               else:
                                  cmdstr="cat /etc/gconf/gconf.xml.mandatory/apps/gnome-screensaver/%gconf.xml|grep '%s'|grep '%s'" % (ktitle,v1)
                               cmdvalue=commands.getoutput(cmdstr).strip()
                               if cmdvalue=="":
                                  if ktitle=='blank-only':
                                     cmdstr="gconftool-2 --direct --config-source  xml:readwrite:/etc/gconf/gconf.xml.mandatory --type string  --set /apps/gnome-screensaver/mode blank-only"
                                  else:
                                     cmdstr="gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory --type bool --set /apps/gnome-screensaver/%s %s"  % (ktitle,v1)           
                                  cmdstatus=os.system(cmdstr)
                                  if cmdstatus!=0:  
                                     sbbzcount+=1
                                     exppzlist+="[%d]当前系统%s配置为%s %s失败\n" %  (linenum,kmc,ktitle,v1)
                                  else:
                                     successcount+=1
                                     successlist+="[%d]当前系统%s配置为%s %s成功\n" %  (linenum,kmc,ktitle,v1)
                                  linenum+=1
                     if osversion==7:
                        for k2,v2 in gnomepz_dict7.item():
                            ktitle=k2.split('|')[1]
                            kmc=k2.split('|')[0]
                            if ktitle=='idle-delay':
                               cmdstr="gsettings get org.gnome.desktop.session %s" % ktitle
                            else:
                               cmdstr="gsettings get org.gnome.desktop.screensaver  %s" % ktitle
                            cmdvalue=commands.getoutput(cmdstr).strip()
                            if 'delay' in ktitle:
                               if not cmdvalue.isdigit():
                                  cmdstr="gsettings set org.gnome.desktop.screensaver %s %s" % (ktitle,v2) 
                                  cmdstatus=os.system(cmdstr)
                                  if cmdstatus!=0:
                                     sbbzcount+=1
                                     exppzlist+="[%d]当前Linux7系统%s配置%s设置为%s失败\n" %  (linenum,kmc,ktitle,v2)
                                  else:
                                     successcount+=1
                                     successlist+="[%d]当前Linux7系统%s配置%s设置为%s成功\n" %  (linenum,kmc,ktitle,v2)
                                     linenum+=1
                            else:
                               if cmdvalue!='true':
                                  cmdstr="gsettings set org.gnome.desktop.screensaver  %s true" % ktitle
                                  cmdstatus=os.system(cmdstr)
                                  if cmdstatus!=0:
                                     sbbzcount+=1
                                     exppzlist+="[%d]当前Linux7系统%s配置%s状态为%s失败\n" %  (linenum,kmc,ktitle,v2)
                                  else:
                                     successcount+=1
                                     successlist+="[%d]当前Linux7系统%s配置%s状态为%s成功\n" %  (linenum,kmc,ktitle,v2)
                                  linenum+=1
         else:
             bz=1
             successcount+=1
             successlist+="未安装图形化界面，此基线检查跳过！！" 

    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照检查是否配置定时自动屏幕锁定(适用于具备图形界面的设备),不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_9,exppzlist)
          checkconfigbz=1
          
       elif jxzt==1:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查是否配置定时自动屏幕锁定(适用于具备图形界面的设备)，由于没有图形化界面,所以检查都符合基线配置规范。
                  ''' %  No8_9
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查是否配置定时自动屏幕锁定(适用于具备图形界面的设备)，配置检查都符合基线配置规范。
                  ''' %  No8_9
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if jxzt==2 :
            printjg='''
%s
配置结果：[失败]按照检查是否配置定时自动屏幕锁定(适用于具备图形界面的设备)，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_9,sbbzcount,exppzlist)
            checkconfigbz=2
         elif jxzt==1 and bz==0:
              printjg='''
%s
配置结果：[成功]按照检查是否配置定时自动屏幕锁定(适用于具备图形界面的设备)，%d项配置更新全部成功！！
需要过程如下：
%s             
            ''' % (No8_9,successcount,successlist)
              xjdf+=1
              checkconfigbz=0
         elif jxzt==1 and bz==1:
              printjg='''
%s
配置结果：[正常]按照检查是否配置定时自动屏幕锁定(适用于具备图形界面的设备)，由于没有图形化界面,无需基线配置！！
需要过程如下：
%s             
            ''' % (No8_9,successlist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]按照检查是否配置定时自动屏幕锁定(适用于具备图形界面的设备),服务配置都符合基线配置规范。    
               ''' %  No8_9
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
#No8.10、【配置要求】：检查密码重复使用次数限制
def Password_Repeatlimit(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_10="★★★★★★★★★★No8.10、【配置要求】：检查密码重复使用次数限制★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    cmdbzstr="password    sufficient    pam_unix.so md5 shadow nullok try_first_pass use_authtok remember="
    str="cat /etc/pam.d/system-auth|grep '^%s'|grep '%s'|grep '%s'|grep '%s'" % (cmdbzstr.split()[0],cmdbzstr.split()[3],cmdbzstr.split()[-2],cmdbzstr.split()[-1])
    cmdvalue=commands.getoutput(str).strip()
    if op=='--check':
       if cmdvalue=="":
          sbbzcount+=1
          exppzlist+="[%d]%s未配置请检查\n" %  (linenum,cmdbzstr)
       else:
          if 'remember' in cmdvalue:
              remembernum=cmdvalue.split('=')[1]
              if not remembernum.isdigit():
                 sbbzcount+=1
                 exppzlist+="[%d]%s中remember值不符合规范！！\n" %  (linenum,cmdbzstr)
    elif op=='--config':
         cmdcxstr="cat -n /etc/pam.d/system-auth|grep -v '^#'|grep password|grep sufficient|grep use_authtok"
         cmdcxvalue=commands.getoutput(cmdcxstr).strip()
         if cmdvalue=="":
            if cmdcxvalue!="":
               jmstr=cmdcxvalue.split()[4]
               num=cmdcxvalue.split()[0]
               if jmstr!='md5':
                  cmdstr="sed -i '%ss/%s/md5/g' /etc/pam.d/system-auth" % (num,jmstr)
                  cmdstatus=os.system(cmdstr)
                  if cmdstatus!=0:
                     sbbzcount+=1
                     exppzlist+="[%d]%s中%s替换md5失败\n" %  (linenum,cmdbzstr,jmstr)
                  else:
                     successcount+=1
                     successlist+="[%d]%s中%s替换md5成功\n" %  (linenum,cmdbzstr,jmstr)
                  linenum+=1
               if 'remember=' not in cmdcxvalue.split()[-1]:                    
                  cmdstr="sed -i '%ss/$/ remember=5/g' /etc/pam.d/system-auth" % num
                  cmdstatus=os.system(cmdstr)
                  if cmdstatus!=0:
                     sbbzcount+=1
                     exppzlist+="[%d]%s中添加remember=5失败\n" %  (linenum,cmdbzstr.strip('remember='))
                  else:
                     successcount+=1
                     successlist+="[%d]%s中添加remember=5成功\n" %  (linenum,cmdbzstr.strip('remember='))                
            else:
               cmdtempstr="password    sufficient    pam_unix.so md5 shadow nullok try_first_pass use_authtok remember=5"
               cmdstr="sed -i '1i\%s' /etc/pam.d/system-auth" % cmdtempstr
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]%s\n重复使用次数限制添加到文件首行失败\n" %  (linenum,cmdtempstr)
               else:
                  successcount+=1
                  successlist+="[%d]%s\n重复使用次数限制配置添加文件到首行成功\n" %  (linenum,cmdtempstr)
         else:
            num=cmdcxvalue.split()[0]
            remembernum=cmdvalue.split('=')[1]
            if not remembernum.isdigit():
               cmdstr="sed -i '%ss/%s/5/g' /etc/pam.d/system-auth" % (num,remembernum)
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]%s中remember值修改失败！！\n" %  (linenum,cmdbzstr)
               else:
                  successcount+=1
                  successlist+="[%d]%s中remember值修改成功！！\n" %  (linenum,cmdbzstr)
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照检查密码重复使用次数限制，不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_10,exppzlist)
          checkconfigbz=1
          
       elif jxzt==1:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查密码重复使用次数限制，所以检查都符合基线配置规范。
                  ''' %  No8_10
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查密码重复使用次数限制，配置检查都符合基线配置规范。
                  ''' %  No8_10
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if jxzt==2 :
            printjg='''
%s
配置结果：[失败]按照检查密码重复使用次数限制，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_10,sbbzcount,exppzlist)
            checkconfigbz=2
         elif jxzt==1:
              printjg='''
%s
配置结果：[成功]按照检查密码重复使用次数限制，%d项配置更新全部成功！！
需要过程如下：
%s             
            ''' % (No8_10,successcount,successlist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]按照检查密码重复使用次数限制,服务配置都符合基线配置规范。    
               ''' %  No8_10
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
#No8.11、【配置要求】：检查系统内核参数配置
def Kernel_parameterPZ(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No8_11="★★★★★★★★★★No8.11、【配置要求】：检查系统内核参数配置★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    NHCS_dictgroup=jx_common.NHCS_Dict
    if op=='--check':
       for k,v in NHCS_dictgroup.items():
           if k=='icmp_echo_ignore_broadcasts' or k=='ip_forward':
              cmdstr="cat /proc/sys/net/ipv4/%s" % k
           else:
              cmdstr="cat /proc/sys/net/ipv4/conf/all/%s" % k
           cmdvalue=commands.getoutput(cmdstr).strip()
           if cmdvalue!=v:
              sbbzcount+=1
              exppzlist+="[%d]%s值%s未满足标准值%s\n" %  (linenum,cmdstr,cmdvalue,v)
              linenum+=1
    elif op=='--config':
         for k,v in NHCS_dictgroup.items():
             if k=='icmp_echo_ignore_broadcasts' or k=='ip_forward':
                cmdcheckstr="cat /proc/sys/net/ipv4/%s" % k
                cmdstr="echo 'net.ipv4.%s=%s'>>/etc/sysctl.conf" % (k,v)
             else:
                cmdcheckstr="cat /proc/sys/net/ipv4/conf/all/%s" % k
                cmdstr="echo 'net.ipv4.conf.all.%s=%s'>>/etc/sysctl.conf" % (k,v)
             cmdvalue=commands.getoutput(cmdcheckstr).strip()
             if cmdvalue!=v:
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]%s执行添加操作失败\n" %  (linenum,cmdstr)
                else:
                   successcount+=1
                   successlist+="[%d]%s执行添加操作成功\n" %  (linenum,cmdstr)
                linenum+=1
         if linenum>1:
            cmdstr="sysctl -p>/dev/null"
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[%d]%s执行失败\n" %  (linenum,cmdstr)
            else:
               successcount+=1
               successlist+="[%d]%s执行成功\n" %  (linenum,cmdstr)
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]检查系统内核参数配置，不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No8_11,exppzlist)
          checkconfigbz=1
          
       elif jxzt==1:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]检查系统内核参数配置，所以检查都符合基线配置规范。
                  ''' %  No8_11
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]检查系统内核参数配置，配置检查都符合基线配置规范。
                  ''' %  No8_11
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if jxzt==2 :
            printjg='''
%s
配置结果：[失败]检查系统内核参数配置，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No8_11,sbbzcount,exppzlist)
            checkconfigbz=2
         elif jxzt==1:
              printjg='''
%s
配置结果：[成功]检查系统内核参数配置，%d项配置更新全部成功！！
需要过程如下：
%s             
            ''' % (No8_11,successcount,successlist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]检查系统内核参数配置,服务配置都符合基线配置规范。    
               ''' %  No8_11
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  