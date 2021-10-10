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

def Header_zymlwjqxsz():
    printjg='''
    *******************************************************************
    *                                                                 *
    *         Linux基线规范检查和配置：4、重要目录和文件权限设置      *
    *                                                                 *
    *******************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 


#No4.1、【配置要求】：配置重要目录和文件的权限{查看权限值:stat -c %a [filename/dir]}
def Importantdirectory_fileright(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    filedictgroups=jx_common.filedictgroups
    No4_1="★★★★★★★★★★No4.1、【配置要求】：配置重要目录和文件的权限★★★★★★★★★★"
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    for f in filedictgroups:
        command="stat -c %%a %s" % f
        qxvalue=commands.getoutput(command).strip()
        if op=='--check':
           if qxvalue!=filedictgroups[f]:
              sbbzcount+=1
              exppzlist+="[%d]{%s}==>%s  建议值：%s.\n" % (linenum,f,qxvalue,filedictgroups[f])
           else:
              successlist+="[%d]{%s}==>%s\n" % (linenum,f,filedictgroups[f])
              successcount+=1
        elif op=='--config':
             if qxvalue!=filedictgroups[f]:
                cmd="chmod %s %s" % (filedictgroups[f],f)
                cmdstatus=os.system(cmd)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]{%s}==>%s 更新%s过程失败.\n" % (linenum,f,qxvalue,filedictgroups[f])
                else:
                   successcount+=1
                   successlist+="[%d]{%s}==>%s 更新为%s成功.\n" % (linenum,f,qxvalue,filedictgroups[f]) 
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
【扫描结果】：[异常]按照配置重要目录和文件的权限检查,不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No4_1,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照配置重要目录和文件的权限检查，%d项重要文件都符合基线配置规范。
 列表如下：
%s 
                  ''' %  (No4_1,successcount,successlist)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照配置重要目录和文件的权限检查，存在%d项重要文件权限更新失败。
失败列表如下：
%s              
               ''' % (No4_1,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照配置重要目录和文件的权限检查，%d项重要文件权限全部成功！！
需要更新列表如下：
%s             
               ''' % (No4_1,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照用户缺省访问权限检查,所有重要文件权限都符合基线配置规范。 
列表如下：
%s              
               ''' % (No4_1,filedictgroups)
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    

#No4.2、【配置要求】：检查重要文件是否存在suid和sgid权限
def Checksuid_sgid_file(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    checkfilestr="/usr/bin/chage /usr/bin/gpasswd /usr/bin/wall /usr/bin/chfn /usr/bin/chsh /usr/bin/newgrp /usr/bin/write /usr/sbin/usernetctl /usr/sbin/traceroute /bin/mount /bin/umount /bin/ping /sbin/netreport"
    No4_2="★★★★★★★★★★No4.2、【配置要求】：检查重要文件是否存在suid和sgid权限★★★★★★★★★★"
    jxzt=0
    linenum=1
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    bzqxm=755
    jcqxm=6000
    command="find  %s -type f -perm +6000 2>/dev/null" % checkfilestr
    filegroups=commands.getoutput(command).strip()
    if op=='--check':
       if filegroups!="":
          for f in filegroups.split('\n'):
              exppzlist+="[%d]{%s}==>%s  建议值：%s.\n" % (linenum,f,jcqxm,bzqxm)
              sbbzcount+=1
              linenum+=1
    elif op=='--config':
         if filegroups!="":
            for f in filegroups.split('\n'):
                cmd="chmod %s %s" % (bzqxm,f)
                cmdstatus=os.system(cmd)
                if cmdstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]{%s}==>%s 更新%s过程失败.\n" % (linenum,f,jcqxm,bzqxm)
                else:
                   successcount+=1
                   successlist+="[%d]{%s}==>%s 更新为%s成功.\n" % (linenum,f,jcqxm,bzqxm) 
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
【扫描结果】：[异常]按照检查重要文件是否存在suid和sgid权限检查,存在%d个文件不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No4_2,sbbzcount,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查重要文件是否存在suid和sgid权限检查，所有文件都符合基线配置规范。
 文件如下：
%s 
                  ''' %  (No4_2,checkfilestr)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照检查重要文件是否存在suid和sgid权限检查，存在%d个文件权限更新失败。
失败列表如下：
%s              
               ''' % (No4_2,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照检查重要文件是否存在suid和sgid权限检查，%d个文件权限全部成功！！
需要更新列表如下：
%s             
               ''' % (No4_2,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照检查重要文件是否存在suid和sgid权限检查,所有文件权限都符合基线配置规范。              
               ''' %  No4_2
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  

#No4.3、【配置要求】：检查系统引导器配置文件权限
def Checkbootfileright(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    check_bootfileLinux6=['/etc/grub.conf','/boot/grub/grub.conf','/etc/lilo.conf']
    check_bootfileLinux7=['/etc/grub2.cfg','/boot/grub2/grub.cfg']
    No4_3="★★★★★★★★★★No4.3、【配置要求】：检查系统引导器配置文件权限★★★★★★★★★★"
    jxzt=0
    linenum=1
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    bzqxm='600'
    osversion=jx_common.get_osversion()
    bootfilegroups=[]
    if osversion==6:
       bootfilegroups=check_bootfileLinux6
    elif osversion==7:
       bootfilegroups=check_bootfileLinux7
    if op=='--check':
       for  b in bootfilegroups:
            if os.path.exists(b):
               cmd="stat %s|grep 'symbolic link'" % b
               cmdjg=commands.getoutput(cmd).strip()
               if cmdjg=="":
                  command="stat -c %%a %s" % b
                  jcqxm=commands.getoutput(command).strip()
                  if jcqxm!=bzqxm:
                     exppzlist+="[%d]{%s}==>%s  建议值：%s.\n" % (linenum,b,jcqxm,bzqxm)
                     sbbzcount+=1
                  else:
                     successcount+=1
                     successlist+="[%d]{%s}==>%s 正常.\n" % (linenum,b,jcqxm)
               else:
                  successcount+=1
                  successlist+="[%d]{%s}为链接文件,正常跳过检查.\n" % (linenum,b)
            else:
                successcount+=1
                successlist+="[%d]{%s}文件不存在,正常跳过检查.\n" % (linenum,b)
            linenum+=1
    elif op=='--config':
         for  b in bootfilegroups:
            if os.path.exists(b):
               cmd="stat %s|grep 'symbolic link'" % b
               cmdjg=commands.getoutput(cmd).strip()
               if cmdjg=="":
                  command="stat -c %%a %s" % b
                  jcqxm=commands.getoutput(command).strip()
                  if jcqxm!=bzqxm:
                     cmdstr="chmod %s %s" % (bzqxm,b)
                     cmdstatus=os.system(cmdstr)
                     if cmdstatus!=0:  
                        exppzlist+="[%d]{%s}==>%s 更新%s过程失败.\n" % (linenum,b,jcqxm,bzqxm)
                        sbbzcount+=1
                     else:
                        successcount+=1
                        successlist+="[%d]{%s}==>%s 更新%s过程成功.\n" % (linenum,b,jcqxm,bzqxm)
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
【扫描结果】：[异常]检查Linux%d系统引导器配置文件权限,存在%d个文件不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No4_3,osversion,sbbzcount,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]检查Linux%d系统引导器配置文件权限，所有文件都符合基线配置规范。
 文件如下：
%s 
                  ''' %  (No4_3,osversion,successlist)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]检查Linux%d系统引导器配置文件权限，存在%d个文件权限更新失败。
失败列表如下：
%s              
               ''' % (No4_3,osversion,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]检查Linux%d系统引导器配置文件权限，%d个文件权限全部成功！！
需要更新列表如下：
%s             
               ''' % (No4_3,osversion,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]检查Linux%d系统引导器配置文件权限,所有文件权限都符合基线配置规范。              
               ''' %  (No4_3,osversion)
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  