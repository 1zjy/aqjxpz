#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import jx_common

xjdf=0
totalitemnum=4
checkconfigbz=-1
notconfignum=0
configsuccessnum=0
jxitemsjcount=0

def Header_zhgl():
    printjg='''
    *******************************************************************
    *                                                                 *
    *               Linux基线规范检查和配置：1、账号管理要求          *
    *                                                                 *
    *******************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 

#No1.1、【配置要求】检查无关的系统用户和用户组
def Unrelated_users(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    command="cat /etc/passwd|cut -d ':' -f1"
    usergroups=commands.getoutput(command).split('\n')
    No1_1="★★★★★★★★★★No1.1、【配置要求】:删除或锁定无关的系统用户和用户组★★★★★★★★★★"
    unrelatedusergroups=''
    totalusernum=len(usergroups)
    expusers=0
    unlockusers=0
    lockusernum=0
    cl_unlockusernum=0
    pz_failednum=0
    for u in usergroups:
        if u  not in jx_common.XT_USER:
           if u not in jx_common.YW_USER:
              tempuser=''
              expusers+=1
              cmd="passwd -S %s|awk '{ print $2 }'" % u
              pwdstatus=''.join(commands.getoutput(cmd)).replace('\n','')
              cmd="passwd -S %s|awk '{ print $3 }'" % u
              pwdlastdate=''.join(commands.getoutput(cmd)).replace('\n','')
              if op=='--check':
                 if 'L' in pwdstatus:
                     tempuser="(已符合)[%s]:已锁定，最后一次密码修改时间为：%s\n" % (u,pwdlastdate)
                     lockusernum+=1
                 elif 'NP' in pwdstatus:
                     tempuser="(未符合)[%s]:未锁定且空密码,最后一次密码修改时间为：%s\n" % (u,pwdlastdate)
                     unlockusers+=1
                 elif 'P'==pwdstatus or 'PS'==pwdstatus:
                     tempuser="(未符合)[%s]:未锁定且密码状态正常，最后一次密码修改时间为：%s\n" % (u,pwdlastdate)
                     unlockusers+=1
                 else:
                     tempuser="(未符合)[%s]:未锁定且密码状态未知，最后一次密码修改时间为：%s\n" % (u,pwdlastdate)
                     unlockusers+=1
              elif op=='--config':
                   if 'L' not in pwdstatus:
                      cmd="passwd -l %s >/dev/null" % u
                      cmdstatus=os.system(cmd)
                      if cmdstatus==0:
                         tempuser="[%s]用户：由[未锁定]已配置为[已锁定];\n" % u
                         cl_unlockusernum+=1
                      else:
                         tempuser="[%s]用户：由[未锁定]配置[已锁定]过程失败！！;\n" % u
                         pz_failednum+=1
                   else:
                       tempuser="[%s]用户: 已为锁定状态;\n" % u
                       lockusernum+=1
              else:
                   tempuser="无"
              unrelatedusergroups+=tempuser
    if op=='--check':
       if unrelatedusergroups!='':
          if  unlockusers>0:
              printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]操作系统用户共%d个，扫描存在非常规用户或系统无关的用户共%d个，其中未锁定用户%d个。
用户列表如下：
%s                
                  ''' % (No1_1,totalusernum,expusers,unlockusers,unrelatedusergroups)
              checkconfigbz=1
          else:
              printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]操作系统用户共%d个，扫描存在非常规用户或系统无关的用户共%d个,其中已锁定用户%d个。
用户列表如下：
%s                
                  ''' % (No1_1,totalusernum,expusers,lockusernum,unrelatedusergroups)
              xjdf+=1
              jx_common.fhd_score+=1
              checkconfigbz=0
       else:
           printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]操作系统用户共%d个，经过扫描不存在非常规用户或系统无关的用户。
%s                
                  ''' % (No1_1,totalusernum,unrelatedusergroups)
           xjdf+=1
           jx_common.fhd_score+=1
           checkconfigbz=0
    elif op=='--config':
         if unrelatedusergroups!='':
            if pz_failednum>0:
               printjg='''
%s
配置结果：[失败]操作系统用户共%d个，配置存在非常规用户或系统无关的用户共%d个,处理成功未锁定用户%d个,配置失败%d个。
用户列表如下：
%s                
               ''' % (No1_1,totalusernum,expusers,unrelatedusergroups,cl_unlockusernum,pz_failednum)
               checkconfigbz=2
            elif cl_unlockusernum>0:
                 printjg='''
%s
配置结果：[成功]操作系统用户共%d个，配置存在非常规用户或系统无关的用户共%d个,全部处理成功未锁定用户%d个。
用户列表如下：
%s                
               ''' % (No1_1,totalusernum,expusers,cl_unlockusernum,unrelatedusergroups)
                 xjdf+=1
                 checkconfigbz=0
            else:
                 printjg='''
%s
配置结果：[正常]操作系统用户共%d个，配置存在非常规用户或系统无关的用户共%d个,%d个用户全部为已锁定状态。
用户列表如下：
%s                
               ''' % (No1_1,totalusernum,expusers,lockusernum,unrelatedusergroups)
                 notconfignum+=1
                 checkconfigbz=0
         else:
            printjg='''
%s
配置结果：[正常]操作系统用户共%d个，配置不存在非常规用户或系统无关的用户。
用户列表如下：
%s                
               ''' % (No1_1,totalusernum,"无")  
            notconfignum+=1
            checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  



#No1.2、【配置要求】检查是否存在除root之外UID为0的用户
def Exprootuid0_users(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    command="awk -F ':'  '$3==0 { print $1 }' /etc/passwd"
    usergroups=commands.getoutput(command).split('\n')
    No1_2="★★★★★★★★★★No1.2、【配置要求】:检查是否存在除root之外UID为0的用户★★★★★★★★★★"
    expusergroups=""
    expnum=0
    unlockusernum=0
    cl_unlockusernum=0
    pz_failednum=0
    for u in usergroups:
        tempuser=""
        if u!='root':
           cmd="passwd -S %s|awk '{ print $2 }'" % u
           pwdstatus=''.join(commands.getoutput(cmd)).replace('\n','')
           cmd="passwd -S %s|awk '{ print $3 }'" % u
           pwdlastdate=''.join(commands.getoutput(cmd)).replace('\n','')
           if op=='--check':
              if 'L' not in pwdstatus:
                  tempuser="(未符合)[%s]未锁定，最后一次密码修改时间为：%s;\n" % (u,pwdlastdate)
                  unlockusernum+=1
              else:
                  tempuser="(已符合)[%s]已锁定，最后一次密码修改时间为：%s;\n" % (u,pwdlastdate)
              expnum+=1
           elif op=='--config':
                if 'L' not in pwdstatus:
                   cmd="passwd -l %s >/dev/null" % u
                   cmdstatus=os.system(cmd)
                   if cmdstatus==0:
                      tempuser="[%s]用户：由[未锁定]已配置为[已锁定];\n" % u
                      cl_unlockusernum+=1
                   else:
                      tempuser="[%s]用户：由[未锁定]配置[已锁定]过程失败！！;\n" % u
                      pz_failednum+=1
                else:
                    tempuser="[%s]用户: 已为锁定状态;\n" % u
           expusergroups+=tempuser
    if op=='--check':
       if unlockusernum!=0:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]操作系统用户扫描存在除root之外UID为0的用户共%d个,未锁定%d个
用户列表如下：
%s                
                  ''' % (No1_2,expnum,unlockusernum,expusergroups)
          checkconfigbz=1
       else:
          printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]操作系统用户扫描不存在除root之外UID为0的用户。           
                  ''' % No1_2
          xjdf+=1
          jx_common.fhd_score+=1
          checkconfigbz=0
    elif op=='--config':
         if  expusergroups!='':
             if pz_failednum>0:
                printjg='''
%s
配置结果：[失败]存在除root之外UID为0的用户共%d个,处理成功未锁定用户%d个,配置失败%d个。
用户列表如下：
%s                
               ''' % (No1_2,expnum,cl_unlockusernum,pz_failednum,expusergroups)
                checkconfigbz=2
             else:
                printjg='''
%s
配置结果：[成功]存在除root之外UID为0的用户共%d个,处理全部成功未锁定用户%d个。
用户列表如下：
%s                
               ''' % (No1_2,expnum,cl_unlockusernum,pz_failednum,expusergroups)
                xjdf+=1
                checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]存在除root之外UID为0的用户共0个。             
               ''' % No1_2
             notconfignum+=1
             checkconfigbz=0             
    else:
        printjg="无"
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)    


#No1.3、【配置要求】登录超时设置
def Login_timeout(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    command="cat -n /etc/profile|grep -v '#'|grep TMOUT"
    Timeoutpz_groups=commands.getoutput(command).split('\n')
    No1_3="★★★★★★★★★★No1.3、【配置要求】:登录超时设置★★★★★★★★★★"
    jxzt=0
    linenum=1
    pznum=len(Timeoutpz_groups)
    pzlist=""
    qdvalue=0
    if pznum==0:
       jxzt=3
    for t in Timeoutpz_groups: 
        try:
           value=int(t.split('=')[1])
        except Exception:
            value=-1
        try:
           filelinenum=int(t.split()[0])
        except Exception:
            filelinenum=-1   
        pzlist+="[%d]%s\n" % (linenum,t)
        if op=='--check':       
           if linenum==pznum:
              qdvalue=value
              if value>jx_common.ZHGL_MAXTMOUT:
                 jxzt=2
              elif value>jx_common.ZHGL_JYTMOUT and value<=jx_common.ZHGL_MAXTMOUT:
                 jxzt=1
              else:
                 jxzt=0
        elif op=='--config':
             if linenum==pznum:
                qdvalue=value
                if value!=jx_common.ZHGL_JYTMOUT:
                   cmd="sed -i '%ds/%s/%s/g' /etc/profile" % (filelinenum,value,jx_common.ZHGL_JYTMOUT)
                   cmdstatus=os.system(cmd)
                   if cmdstatus==0:
                      jxzt=1
                   else:
                      jxzt=2
                else:
                    jxzt=0
             else:
                 if filelinenum!=-1:
                    cmd="sed -i '%ds/^/#/g' /etc/profile" % filelinenum
                    cmdstatus=os.system(cmd)
        linenum+=1      
    if op=='--check':
       if  qdvalue==-1:
           printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]登录超时时间获取参数失败,请排查！！。             
                     ''' % No1_3
           checkconfigbz=1 
       else:
           if jxzt==2:
              if pznum>1:
                 printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]登录超时时间为%ds已超过600s(以最后一个配置为判断依据),不符合基线规范。
%s                
                     ''' % (No1_3,qdvalue,"配置列表如下:\n"+pzlist)
                 checkconfigbz=1 
              else:
                 printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]登录超时时间设置为%ds已超过600s,不符合基线规范。             
                     ''' % (No1_3,qdvalue)
                 checkconfigbz=1                     
           elif  jxzt==1:    
                 printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]登录超时时间设置为%ds已超过建议值300s低于最大值600s,符合基线规范。       
                  ''' % (No1_3,qdvalue)
                 xjdf+=1
                 jx_common.fhd_score+=1
                 checkconfigbz=0
           else:
               printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]登录超时时间设置为%ds小于或等于300s,符合基线规范。             
                  ''' % (No1_3,qdvalue)
               xjdf+=1
               jx_common.fhd_score+=1
               checkconfigbz=0
    elif op=='--config':
         if  qdvalue==-1:
             printjg='''
%s
【配置结果】：[异常]登录超时时间配置参数失败,请排查！！。             
                     ''' % No1_3
             checkconfigbz=1
         else:
             if jxzt==2:
                printjg='''
%s
配置结果：[失败]登录超时时间修改失败从%ds到300s,请排查异常。
               ''' % (No1_3,qdvalue)
                checkconfigbz=2
             elif jxzt==3:
                  cmd="echo 'export TMOUT=300'>>/etc/profile"
                  cmdstatus=os.system(cmd)
                  if cmdstatus==0:
                     printjg='''
%s
配置结果：[成功]检查之前未配置,已添加登录超时时间已配置为300s。
               ''' % No1_3
                     xjdf+=1
                     checkconfigbz=0
                  else:       
                     printjg='''
%s
配置结果：[失败]检查之前未配置,添加登录超时时间配置过程失败，请排查异常。
                       ''' % No1_3
                     checkconfigbz=2                       
             elif jxzt==1:   
                printjg='''
%s
配置结果：[成功]登录超时时间已重新设置从%ds配置为300s。               
               ''' % (No1_3,qdvalue)
                xjdf+=1
                checkconfigbz=0
             else:  
                printjg='''
%s
配置结果：[正常]登录超时时间已为300s。               
               ''' % No1_3 
                notconfignum+=1
                checkconfigbz=0                
    else:
        printjg="无"
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)          

#NO1.4、【配置要求】：限制管理员root远程登录
def Restrictroot_notlogin(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    command="cat -n /etc/ssh/sshd_config|grep -v '#'|grep 'PermitRootLogin'"
    norestrictrootstr=commands.getoutput(command).strip()
    No1_4="★★★★★★★★★★No1.4、【配置要求】:限制管理员root远程登录★★★★★★★★★★"
    jxzt=0
    linenum=1
    pznum=0
    if norestrictrootstr!="":
       norestrictrootgroups=norestrictrootstr.split('\n')
       pznum=len(norestrictrootgroups)
    pzlist=""
    qdvalue=""
    value=""
    filelinenum=0
    if pznum==0:
       if op=='--check':
          jxzt=2
       else:
           cmd="echo 'PermitRootLogin no' >> /etc/ssh/sshd_config"
           cmdstatus=os.system(cmd)
           if cmdstatus==0:
              jxzt=1
           else:
              jxzt=2
    else:
        for t in norestrictrootgroups: 
            try:
               value=t.split()[-1]
            except Exception:
                value="异常"
            try:
               filelinenum=int(t.split()[0])
            except Exception:
                filelinenum=-1   
            pzlist+="[%d]%s\n" % (linenum,t)
            if op=='--check':      
               if linenum==1: 
                  qdvalue=value           
                  if value=='no':
                     jxzt=0
                  else:
                     jxzt=2
            elif op=='--config':         
                 if linenum==1:
                    qdvalue=value 
                    if value!='no':
                       cmd="sed -i '%ds/%s/no/g' /etc/ssh/sshd_config" % (filelinenum,value)
                       cmdstatus=os.system(cmd)
                       if cmdstatus==0:
                          jxzt=1
                       else:
                          jxzt=2
                 else:
                     if filelinenum!=-1:
                        cmd="sed -i '%ds/^/#/g' /etc/ssh/sshd_config" % filelinenum
                        cmdstatus=os.system(cmd)
            linenum+=1
    if op=='--check':
       if jxzt==2:
          if pznum>0:
             printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]检查操作系统限制管理员root远程登录参数为{PermitRootLogin %s}(以第一次出现PermitRootLogin配置为准),不符合基线规范。
%s                
                     ''' % (No1_4,qdvalue,"配置列表如下:\n"+pzlist)
          else:
              printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]检查操作系统限制管理员root远程登录参数不存在,不符合基线规范。             
                     ''' % No1_4
          checkconfigbz=1
       else:
           printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]检查操作系统限制管理员root远程登录参数为{PermitRootLogin %s},符合基线规范。             
                  ''' % (No1_4,qdvalue)
           xjdf+=1
           jx_common.fhd_score+=1
           checkconfigbz=0
    elif op=='--config':
         if  qdvalue=="异常":
             printjg='''
%s
【配置结果】：[异常]获取限制管理员root远程登录参数异常,请排查！！。             
                     ''' % No1_4
             checkconfigbz=1
         else:
             if jxzt==2:
                printjg='''
%s
配置结果：[失败]操作系统限制管理员root远程登录参数为PermitRootLogin %s中%s修改为no失败,请排查异常。
               ''' % (No1_4,qdvalue,qdvalue)
                checkconfigbz=2
             elif jxzt==3:
                  cmd="echo 'PermitRootLogin no'>>/etc/ssh/sshd_config"
                  cmdstatus=os.system(cmd)
                  if cmdstatus==0:
                     printjg='''
%s
配置结果：[成功]检查之前未配置,已添加限制管理员root远程登录。
               ''' % No1_4
                     xjdf+=1
                     checkconfigbz=0
                  else:       
                     printjg='''
%s
配置结果：[失败]检查之前未配置,添加限制管理员root远程登录失败，请排查异常。
                       ''' % No1_4 
                     checkconfigbz=2
             elif jxzt==1:
                  if pznum!=0:             
                     printjg='''
%s
配置结果：[成功]限制管理员root远程登录PermitRootLogin %s中%s成功修改为no。               
               ''' % (No1_4,qdvalue,qdvalue)
                  else:
                     printjg='''
%s
配置结果：[成功]限制管理员root远程登录配置PermitRootLogin no成功添加。               
               ''' % No1_4
                  xjdf+=1
                  checkconfigbz=0 
             else:  
                printjg='''
%s
配置结果：[正常]限制管理员root远程登录配置已为PermitRootLogin no。               
               ''' % No1_4
                notconfignum+=1
                checkconfigbz=0                
    else:
        printjg="无"
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)         