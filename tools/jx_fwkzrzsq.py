#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import jx_common

xjdf=0
totalitemnum=5
checkconfigbz=-1
notconfignum=0
configsuccessnum=0
jxitemsjcount=0

def Header_fwkzrzsq():
    printjg='''
    *******************************************************************
    *                                                                 *
    *            Linux基线规范检查和配置：3、访问控制及认证授权       *
    *                                                                 *
    *******************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 


#No3.1、【配置要求】：用户缺省访问权限
def Userdefault_access(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    filegroups=['/etc/profile','/etc/csh.login','/etc/csh.cshrc','/etc/bashrc'] 
    No3_1="★★★★★★★★★★No3.1、【配置要求】：用户缺省访问权限★★★★★★★★★★"
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    sbbzcount=0
    ycbzcount=0
    for f in filegroups:
        command="cat -n %s|grep -v '#'|grep 'umask'|sed -n '$p'" % f
        umaskstr=commands.getoutput(command).strip()
        if umaskstr!="":
           try:
              umask=umaskstr.split()[-1]
           except Exception:
              umask="-1"
           try:
              filelinenum=int(umaskstr.split()[0])
           except Exception:
              filelinenum=-1
           if umask!="-1" and filelinenum!=-1:
              if f=='/etc/profile':
                 if umask!='027':
                    exppzlist+="%d [/etc/profile]:umask %s.\n" % (filelinenum,umask)
              else:
                 if umask!='077':
                    exppzlist+="%d [%s]:umask %s.\n" % (filelinenum,f,umask)
           else:
               ycbzcount+=1
        else:
           exppzlist+="  [%s] 未配置umask" % f
    if op=='--check':
       if exppzlist!="":
             jxzt=2
       else:
           jxzt=0
    elif op=='--config':
         exppzlistgroups=exppzlist.strip('\n').split('\n')
         if exppzlist!="":
            for e in exppzlistgroups:
                try:
                   tmp_linenum=int(e.split()[0])
                except Exception:
                   tmp_linenum=-1
                tmp_umaskvalue=e.split()[-1].strip('.')
                tmp_filename=e.split('/')[-1].split(']')[0]
                cmdstr="cat /etc/%s|grep -E '^umask'" % tmp_filename
                cmdvalue=commands.getoutput(cmdstr).strip()
                if tmp_filename=='profile':
                   if cmdvalue!="":
                      cmdstr="sed -i '%ds/%s/027/g'  /etc/profile" % (tmp_linenum,tmp_umaskvalue)
                   else:
                      cmdstr="echo 'umask 027' >> /etc/profile"
                else:
                   if cmdvalue!="":
                      cmdstr="sed -i '%ds/%s/077/g'  /etc/%s" % (tmp_linenum,tmp_umaskvalue,tmp_filename)
                   else:
                      cmdstr="echo 'umask 077' >> /etc/%s" % tmp_filename 
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   sbbzcount+=1
            if sbbzcount>0:
               jxzt=2
            else:
               jxzt=1
         else:
            jxzt=0  
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照用户缺省访问权限检查,不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No3_1,exppzlist)
          checkconfigbz=1
       elif jxzt==3:
            printjg='''
%s
【符合度得分】：0
【扫描结果】：[异常]按照用户缺省访问权限检查，检查%s文件中umask出现异常，不符合基线规范。              
                  ''' % (No3_1,filegroups)
            checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照用户缺省访问权限检查，umask值都符合基线配置规范。              
                  ''' %  No3_1
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照用户缺省访问权限检查，存在更新umask配置失败。
失败列表如下：
%s              
               ''' % (No3_1,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照用户缺省访问权限检查，配置需更新umask都全部成功！！
需要更新列表如下：
%s             
               ''' % (No3_1,exppzlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照用户缺省访问权限检查,%s中umask值都符合基线配置规范。              
               ''' % (No3_1,filegroups)
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  


#No3.2、【配置要求】：授权账户SSH访问控制
def Sshaccess_control(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    sshdconfiggroups=['Protocol 2','LogLevel INFO','MaxAuthTries 5','IgnoreRhosts yes','RhostsAuthentication no','RhostsRSAAuthentication no','HostbasedAuthentication no','PermitEmptyPasswords no','PermitUserEnvironment no','ClientAliveInterval 60','ClientAliveCountMax 3','LoginGraceTime 60','X11Forwarding yes']
    sshconfigfile=jx_common.SSHD_Config_FILE
    No3_2="★★★★★★★★★★No3.2、【配置要求】：授权账户SSH访问控制★★★★★★★★★★"
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    gxcgcount=0
    sbbzcount=0
    for s in sshdconfiggroups:
        command="cat -n %s|grep -v '#'|grep '%s'" % (sshconfigfile,s) 
        pzgroupsstr=commands.getoutput(command).strip()
        if pzgroupsstr!="":
           pzgroups=pzgroupsstr.strip('\n').split('\n')
           pznum=len(pzgroups)
           n=1
           if pznum>1:
              if op=='--check':
                 sbbzcount+=1
                 exppzlist+="%d [%s] 配置重复.\n" % (linenum,s)
                 linenum+=1
              elif op=='--config':
                   for p in pzgroups:
                       try:
                          filelinenum=int(p.split()[0])
                       except Exception:
                          filelinenum=-1
                       if n!=pznum:
                          cmdstr="sed -i '%ds/^/#/g' %s" % (filelinenum,sshconfigfile)
                          status=os.system(cmdstr)
                          if status!=0:
                             exppzlist+="%d <%d> [%s] 删除重复配置失败\n" % (linenum,filelinenum,s)
                             linenum+=1
                             sbbzcount+=1
                          else:
                             successlist+="%d <%d> [%s] 重复配置更新成功\n" % (gxcgcount,filelinenum,s)
                             gxcgcount+=1
                       n+=1                     
        else:
           if op=='--check':
              exppzlist+="%d [%s] 未配置.\n" % (linenum,s)
              linenum+=1
              sbbzcount+=1
           elif op=='--config':
                cmdstr="echo '%s' >> %s" % (s,sshconfigfile)
                cmdstatus=os.system(cmdstr)
                if cmdstatus!=0:
                   exppzlist+="%d [%s] 添加配置失败\n" % (linenum,s)
                   linenum+=1
                   sbbzcount+=1
                else:
                   successlist+="%d [%s] 未配置已添加成功.\n" % (gxcgcount,s)
                   gxcgcount+=1
    if exppzlist!="":
       jxzt=2
    if op=='--config':
       if sbbzcount==0 and gxcgcount>0:
          jxzt=1
     
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照授权账户SSH访问控制检查,%d项配置均不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No3_2,sbbzcount,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照授权账户SSH访问控制检查，ssh相关配置都符合基线配置规范。              
                  ''' %  No3_2
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照授权账户SSH访问控制检查，存在%d项更新SSH配置失败。
配置失败列表如下：
%s              
               ''' % (No3_2,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照授权账户SSH访问控制检查，%d项配置更新ssh都全部成功！！
配置列表如下：
%s             
               ''' % (No3_2,gxcgcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照授权账户SSH访问控制检查，ssh配置全部符合基线配置规范。              
               ''' % No3_2
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  


#No3.5、【配置要求】:检查是否使用PAM认证模块禁止wheel组之外的用户su为root
def Restrictroot_Pam_directlogin(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    sshdconfiggroups=['Protocol 2','LogLevel INFO','MaxAuthTries 5','IgnoreRhosts yes','RhostsAuthentication no','RhostsRSAAuthentication no','HostbasedAuthentication no','PermitEmptyPasswords no','PermitUserEnvironment no','ClientAliveInterval 60','ClientAliveCountMax 3','LoginGraceTime 60','X11Forwarding yes']
    osversion=int(jx_common.get_osversion())
    No3_5="★★★★★★★★★★No3.5、【配置要求】：检查是否使用PAM认证模块禁止wheel组之外的用户su为root★★★★★★★★★★"
    jxzt=0
    exppzlist=""
    successlist=""
    gxcgcount=0
    sbbzcount=0
    linenum=1
    xquserbz=0
    SU_COMMONUser=jx_common.SU_COMMONUser
    cmdstr="cat -n /etc/pam.d/su|grep -v '#'|grep 'pam_wheel.so use_uid'"
    cmd_use_uidvalue=commands.getoutput(cmdstr).strip()
    cmdstr1="cat /etc/group|grep '^wheel'|awk -F ':' '{ print $NF }'"
    wheelusers=commands.getoutput(cmdstr1).strip()
    if op=='--check':
       if osversion==6:
          cmdstr="cat -n /etc/pam.d/su|grep -v '#'|grep 'pam_wheel.so'|grep 'group=wheel'"
          pamwheelvalue=commands.getoutput(cmdstr).strip()
          if pamwheelvalue=="":
             exppzlist+="[%d][/etc/pam.d/su]中auth required pam_wheel.so group=wheel未配置.\n" % linenum
             sbbzcount+=1           
       elif osversion==7:
            cmdstr="cat /etc/login.defs|grep -v '#'|grep 'SU_WHEEL_ONLY'|grep 'yes'"
            suwheelvalue=commands.getoutput(cmdstr).strip()
            if suwheelvalue=="":
               exppzlist+="[%d][/etc/login.defs]中SU_WHEEL_ONLY yes未配置.\n" % linenum
               sbbzcount+=1 
       if cmd_use_uidvalue=="":
          exppzlist+="[%d][/etc/pam.d/su]中auth		required	pam_wheel.so use_uid未配置.\n" % linenum
          sbbzcount+=1
       for u in SU_COMMONUser:
           cmdstr="id %s >/dev/null 2>&1" % u
           cmdstatus=os.system(cmdstr)
           cmdstr1="passwd -S %s|awk '{ print $2 }'" % u
           pwdstatus=''.join(commands.getoutput(cmdstr1)).replace('\n','')
           if cmdstatus!=0 or 'L' in pwdstatus:
              continue
           else:
              if u not in wheelusers.split(','): 
                 exppzlist+="[%d]%s用户未添加到wheel组.\n" % (linenum,u)
                 sbbzcount+=1
                 linenum+=1                 
    elif op=='--config':
         if osversion==6:
            cmdstr="cat -n /etc/pam.d/su|grep -v '#'|grep 'pam_wheel.so'|grep 'group=wheel'"
            pamwheelvalue=commands.getoutput(cmdstr).strip()
            if pamwheelvalue=="":
               cmdstr="echo 'auth required pam_wheel.so group=wheel' >> /etc/pam.d/su"
               cmdstatus=os.system(cmdstr)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[/etc/pam.d/su]中添加auth required pam_wheel.so group=wheel配置失败.\n"
               else:
                  gxcgcount+=1
                  successlist+="[/etc/pam.d/su]中添加auth required pam_wheel.so group=wheel]配置成功.\n"
         elif osversion==7:
              cmdstr1="cat /etc/login.defs|grep -v '#'|grep 'SU_WHEEL_ONLY'|grep 'yes'"
              suwheelvalue=commands.getoutput(cmdstr1).strip()
              if suwheelvalue=="":
                 cmdstr="echo 'SU_WHEEL_ONLY yes' >> /etc/login.defs"
                 cmdstatus=os.system(cmdstr)
                 if cmdstatus!=0:
                    sbbzcount+=1
                    exppzlist+="[/etc/login.defs]中添加SU_WHEEL_ONLY yes配置失败.\n"
                 else:
                    gxcgcount+=1
                    successlist+="[/etc/login.defs]中添加SU_WHEEL_ONLY yes配置成功.\n"
         if cmd_use_uidvalue=="":
            cmdstr="echo 'auth		required	pam_wheel.so use_uid' >> /etc/pam.d/su"
            cmdstatus=os.system(cmdstr)
            if cmdstatus!=0:
               sbbzcount+=1
               exppzlist+="[/etc/pam.d/su]中添加auth		required	pam_wheel.so use_uid配置失败.\n"
            else:
               gxcgcount+=1
               successlist+="[/etc/pam.d/su]中添加auth		required	pam_wheel.so use_uid配置成功.\n"    
         for u in SU_COMMONUser:
             cmdstr="cat /etc/passwd|grep '%s'" % u
             cmdvalue=commands.getoutput(cmdstr).strip()
             if cmdvalue!="":
                cmd="passwd -S %s|awk '{ print $2 }'" % u
                pwdstatus=''.join(commands.getoutput(cmd)).replace('\n','')
                if 'L' not in pwdstatus:
                    cmdstr="usermod -G wheel %s" % u
                    cmdstatus=os.system(cmdstr)
                    if cmdstatus!=0:
                       exppzlist+="选取未锁定普通用户[%s],加入wheel组失败.\n" % u
                       sbbzcount+=1
                    else:
                       gxcgcount+=1
                       successlist+="选取未锁定普通业务用户[%s],加入wheel组成功.\n" % u
    if exppzlist!="":
       jxzt=2
    if op=='--config':
       if sbbzcount==0 and gxcgcount>0:
          jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]检查是否使用PAM认证模块禁止wheel组之外的用户su为root,%d项配置均不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No3_5,sbbzcount,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]检查是否使用PAM认证模块禁止wheel组之外的用户su为root，相关配置都符合基线配置规范。              
                  ''' %  No3_5
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]检查是否使用PAM认证模块禁止wheel组之外的用户su为root，存在%d项更新配置失败。
配置失败列表如下：
%s              
               ''' % (No3_5,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]检查是否使用PAM认证模块禁止wheel组之外的用户su为root，%d项配置更新都全部成功！！
配置列表如下：
%s             
               ''' % (No3_5,gxcgcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]检查是否使用PAM认证模块禁止wheel组之外的用户su为root，配置全部符合基线配置规范。              
               ''' % No3_5
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  