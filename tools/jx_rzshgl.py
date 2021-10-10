#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import jx_common

xjdf=0
totalitemnum=3
checkconfigbz=-1
notconfignum=0
configsuccessnum=0
jxitemsjcount=0

def Header_rzshgl():
    printjg='''
************************************************************************

               Linux基线规范检查和配置：5、日志审核

************************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 


#No5.1、【配置要求】：开启系统日志记录
def Opensystem_log(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No5_1="★★★★★★★★★★No5.1、【配置要求】：开启系统日志记录★★★★★★★★★★"
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    cmdstr="rpm -qa|grep rsyslog"
    rpminstallstr=commands.getoutput(cmdstr).strip()
    if op=='--check':
       if rpminstallstr=="":
          sbbzcount+=1
          exppzlist+="[%d]rsyslog包未安装.\n" %  linenum
       else:
          successcount+=1
          successlist+="[%d]rsyslog包检查已安装\n" %  linenum
          cmdstr="ps -elf |grep rsyslogd|grep -v 'grep'"
          fwstr=commands.getoutput(cmdstr).strip()
          linenum+=1
          if fwstr=="":
             exppzlist+="[%d]rsyslog服务未启动.\n" %  linenum
             sbbzcount+=1
          else:
             successcount+=1
             successlist+="[%d]rsyslog服务检查已启动.\n" %  linenum
             cmdstr="cat /etc/rsyslog.conf|grep -v '^#'|grep 'FileCreateMode 0640'"
             pzstr=commands.getoutput(cmdstr).strip()
             linenum+=1
             if pzstr=="":
                exppzlist+="[%d]/etc/rsyslog.conf中未配置$FileCreateMode 0640.\n" %  linenum
                sbbzcount+=1
             else:
                successlist+="[%d]/etc/rsyslog.conf中检查$FileCreateMode 0640参数已存在\n" %  linenum
                successcount+=1
    elif op=='--config': 
         if rpminstallstr=="":
            yumstate=jx_common.PD_ISYUMSRC()
            if yumstate==2:
               sbbzcount+=1
               exppzlist+="[%d]检查未安装rsyslog,开始配置安装前检查yum源不正常,请检查！！\n" %  linenum
            else:
               cmdstr="yum install -y rsyslog >/dev/null"
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]配置安装rsyslog失败，请检查！！\n" %  linenum
               else:
                   successcount+=1
                   successlist+="[%d]执行安装配置rsyslog服务成功\n" %  linenum
                   cmdstr="service rsyslog start"
                   cmdstatus=os.system(cmdstr)
                   linenum+=1
                   if cmdstatus!=0:
                      sbbzcount+=1
                      exppzlist+="[%d]执行启动rsyslog服务失败，请检查！！\n" %  linenum
                   else:
                      successlist+="[%d]执行启动rsyslog服务成功，请检查！！\n" %  linenum
                      successcount+=1 
                      cmdstr="sed -i  '/GLOBAL DIRECTIVES/a $FileCreateMode 0640' /etc/rsyslog.conf"
                      cmdstatus=os.system(cmdstr)
                      linenum+=1
                      if cmdstatus!=0:
                         sbbzcount+=1
                         exppzlist+="[%d]执行rsyslog配置文件中添加$FileCreateMode 0640失败，请检查！！\n" %  linenum
                      else:
                         successcount+=1
                         successlist+="[%d]执行配置rsyslog配置文件中添加$FileCreateMode 0640成功！！\n" %  linenum
         else: 
             cmdstr="ps -elf |grep rsyslogd|grep -v 'grep'"
             fwstr=commands.getoutput(cmdstr).strip()
             if fwstr=="":
                cmdstr="service rsyslog start"
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]执行启动rsyslog服务失败，请检查！！\n" %  linenum
                else:
                   successlist+="[%d]执行启动rsyslog服务成功\n" %  linenum
                   successcount+=1                    
             cmdstr="cat /etc/rsyslog.conf|grep -v '^#'|grep 'FileCreateMode 0640'"
             pzstr=commands.getoutput(cmdstr).strip()
             linenum+=1
             if pzstr=="":
                cmdstr="sed -i  '/GLOBAL DIRECTIVES/a $FileCreateMode 0640' /etc/rsyslog.conf"
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]执行rsyslog配置文件中添加$FileCreateMode 0640失败，请检查！！\n" %  linenum
                else:
                   successcount+=1
                   successlist+="[%d]执行配置rsyslog配置文件中添加$FileCreateMode 0640成功！！\n" %  linenum
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照开启系统日志记录检查,不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No5_1,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照开启系统日志记录检查，%d项配置检查都符合基线配置规范。
 列表如下：
%s 
                  ''' %  (No5_1,successcount,successlist)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照开启系统日志记录检查，存在%d项配置更新失败。
失败列表如下：
%s              
               ''' % (No5_1,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照开启系统日志记录检查，%d项配置全部成功！！
需要更新列表如下：
%s             
               ''' % (No5_1,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照开启系统日志记录检查,rsyslog服务和配置都符合基线配置规范。    
               ''' % No5_1
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    



#No5.2、【配置要求】：开启操作日志记录，记录用户的操作日志。
def Openopration_log(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No5_2="★★★★★★★★★★No5.2、【配置要求】：开启操作日志记录，记录用户的操作日志。★★★★★★★★★★"
    logfilegroups=["USER=`whoami`","USER_IP=`hostname`","mkdir /var/log/history","chmod 777 /var/log/history","mkdir /var/log/history/${LOGNAME}","chmod 300 /var/log/history/${LOGNAME}","export HISTSIZE=4096","export HISTFILESIZE=5"]
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    for l in logfilegroups:
        cmdstr="cat /etc/profile|grep '%s'" % l
        tempstr=commands.getoutput(cmdstr).strip()
        if op=='--check':
           if tempstr=="":
              if sbbzcount>1:
                 exppzlist="操作日志记录配置未配置或未按照规范配置"
                 break
              else:
                 sbbzcount+=1
                 exppzlist+="[%d]配置项:%s未配置.\n" %  (linenum,l)
                 linenum+=1
        elif op=='--config':
             if tempstr=="":
                if sbbzcount>1:
                   cmdstr='''
tee -a /etc/profile <<-'EOF'
USER=`whoami`
USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'`
if [ "$USER_IP" = "" ]; then
   USER_IP=`hostname`
fi
if [ ! -d /var/log/history ]; then
   mkdir /var/log/history
   chmod 777 /var/log/history
fi
if [ ! -d /var/log/history/${LOGNAME} ]; then
   mkdir /var/log/history/${LOGNAME}
   chmod 300 /var/log/history/${LOGNAME}
fi
export HISTSIZE=4096
export HISTFILESIZE=5
DT=`date +"%Y%m%d_%H:%M:%S"`
export HISTFILE="/var/log/history/${LOGNAME}/${USER}@${USER_IP}_$DT"
chmod 600 /var/log/history/${LOGNAME}/*history* 2>/dev/null
EOF'''
                   cmdstatus=os.system(cmdstr)
                   if cmdstatus!=0:
                      sbbzcount+=1
                      exppzlist="操作日志记录配置失败！！"
                   else:   
                      successcount+=1
                      successlist="操作日志记录配置成功！！"
                   break
                else:
                    sbbzcount+=1
    if exppzlist!="":
       jxzt=2
    if sbbzcount==2 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照开启操作日志记录，记录用户的操作日志检查,不符合基线规范。
不规范说明如下：
%s              
                  ''' % (No5_2,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照开启操作日志记录，记录用户的操作日志检查，检查都符合基线配置规范。
                  ''' %  No5_2
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照开启操作日志记录，记录用户的操作日志检查，存在配置更新失败。            
               ''' % No5_2
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照开启操作日志记录，记录用户的操作日志检查，全部配置成功！！          
               ''' % No5_2
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照开启操作日志记录，记录用户的操作日志检查,配置都符合基线配置规范。    
               ''' % No5_2
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
    
#No5.3、【配置要求】：检查日志文件权限设置
def Checklogqx_gl(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    check_logfile_groups=['/var/log/cron','/var/log/secure','/var/log/messages','/var/log/maillog','/var/log/boot.log','/var/log/mail','/var/log/localmessages','/var/log/spooler']
    No5_3="★★★★★★★★★★No5.3、【配置要求】：检查日志文件权限设置★★★★★★★★★★"
    jxzt=0
    linenum=1
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    bzqxm=755
    jybzm='600'
    if op=='--check':
       for  f in check_logfile_groups:
            if os.path.exists(f):
               cmd="stat %s|grep 'symbolic link'" % f
               cmdjg=commands.getoutput(cmd).strip()
               if cmdjg=="":
                  command="stat -c %%a %s" % f
                  try:
                     jcqxm=int(commands.getoutput(command).strip())
                  except Exception:
                     jcqxm=777
                  if jcqxm>bzqxm:
                     exppzlist+="[%d]{%s}==>%d  建议值：小于或等于%d.\n" % (linenum,f,jcqxm,bzqxm)
                     sbbzcount+=1
                  else:
                     successcount+=1
                     successlist+="[%d]{%s}==>%d 正常.\n" % (linenum,f,jcqxm)
               else:
                  successcount+=1
                  successlist+="[%d]{%s}为链接文件,正常跳过检查.\n" % (linenum,f)
            else:
                successcount+=1
                successlist+="[%d]{%s}文件不存在,正常跳过检查.\n" % (linenum,f)
            linenum+=1
    elif op=='--config':
         for  f in check_logfile_groups:
            if os.path.exists(f):
               cmd="stat %s|grep 'symbolic link'" % f
               cmdjg=commands.getoutput(cmd).strip()
               if cmdjg=="":
                  command="stat -c %%a %s" % f
                  jcqxm=commands.getoutput(command).strip()
                  if jcqxm!=jybzm:
                     cmdstr="chmod %s %s" % (jybzm,f)
                     cmdstatus=os.system(cmdstr)
                     if cmdstatus!=0:  
                        exppzlist+="[%d]{%s}==>%s 更新%s过程失败.\n" % (linenum,f,jcqxm,bzqxm)
                        sbbzcount+=1
                     else:
                        successcount+=1
                        successlist+="[%d]{%s}==>%s 按推荐建议更新%s过程成功.\n" % (linenum,f,jcqxm,bzqxm)
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
【扫描结果】：[异常]检查日志文件权限设置,存在%d个文件不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No5_3,sbbzcount,exppzlist)
          checkconfigbz=1
       else:
          printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]检查日志文件权限设置，所有文件都符合基线配置规范。
 文件如下：
%s 
                  ''' %  (No5_3,successlist)
          xjdf+=1
          jx_common.fhd_score+=1
          checkconfigbz=0
    elif op=='--config':
         if jxzt==2:
            printjg='''
%s
配置结果：[失败]检查日志文件权限设置，存在%d个文件权限更新失败。
失败列表如下：
%s              
               ''' % (No5_3,sbbzcount,exppzlist)
            checkconfigbz=2
         elif jxzt==1:
              printjg='''
%s
配置结果：[成功]检查日志文件权限设置，%d个文件权限全部成功！！
需要更新列表如下：
%s             
               ''' % (No5_3,successcount,successlist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]检查日志文件权限设置,所有文件权限都符合基线配置规范。              
               ''' %  No5_3
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    