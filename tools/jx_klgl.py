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

def Header_klgl():
    printjg='''
    *******************************************************************
    *                                                                 *
    *               Linux基线规范检查和配置：2、口令管理要求          *
    *                                                                 *
    *******************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 

#NO2.1、【配置要求】：密码复杂度要求
def Password_complexity(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No2_1="★★★★★★★★★★No2.1、【配置要求】：密码复杂度要求★★★★★★★★★★"
    jxzt=0
    minlen=0
    linenum=1
    filelinenum=0
    command="cat -n /etc/pam.d/system-auth|grep -v '#'|grep  -E 'password'|grep -E 'pam_pwquality.so|pam_cracklib.so'|sed -n '1p'"
    passwordcomplexstr=commands.getoutput(command).strip()
    addpz=0
    gxpz=0
    zzstrnr=""
    try:
       filelinenum=int(passwordcomplexstr.split()[0])
    except Exception:
       filelinenum=-1
    if op=='--check':
       if passwordcomplexstr=="":
          jxzt=3
       else:
          zzstr="echo %s|grep -E 'difok=3'|grep 'minlen'|grep 'ucredit=-1'|grep 'lcredit=-1'|grep 'dcredit=-1'" % passwordcomplexstr
          zzstrnr=commands.getoutput(zzstr)
          if zzstrnr!="":
             try:
                minlen=int(zzstr.split('minlen')[1].split()[0].lstrip('='))
             except Exception:
                minlen=0
             if minlen<8:
                jxzt=2
          else:
             jxzt=2
    elif op=='--config':
         if passwordcomplexstr!="":
            zzstr="echo %s|grep -E 'difok=3'|grep 'minlen'|grep 'ucredit=-1'|grep 'lcredit=-1'|grep 'dcredit=-1'|sed -n '1p'" % passwordcomplexstr
            zzstrnr=commands.getoutput(zzstr)
            if zzstrnr!="":
               try:
                  minlen=int(zzstr.split('minlen')[1].split()[0].lstrip('='))
               except Exception:
                  minlen=0
               gxpz=1
               if minlen<8:
                  if filelinenum!=-1:
                     cmd="sed -i '%ds/minlen=%d/minlen=%d/g' /etc/pam.d/system-auth" % (filelinenum,minlen,jx_common.JX_minlen)
                     cmdstatus=os.system(cmd)
                     if cmdstatus==0:
                        jxzt=1
                     else:
                        jxzt=2
               else:
                  jxzt=0
            else:
               cmd="sed -i '1i\password requisite pam_cracklib.so difok=3 minlen=8 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1' /etc/pam.d/system-auth"
               cmdstatus=os.system(cmd)
               addpz=1
               if  cmdstatus==0:                   
                   jxzt=1
               else:
                   jxzt=2
         else:
             cmd="sed -i '1i\password requisite pam_cracklib.so difok=3 minlen=8 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1' /etc/pam.d/system-auth"
             cmdstatus=os.system(cmd)
             addpz=1
             if  cmdstatus==0:                   
                 jxzt=1
             else:
                 jxzt=2
    else:
        jxzt=0

    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]扫描密码复杂度要求，基线配置不符合基线配置规范。
 不规范列表如下：
%s                
                  ''' % (No2_1,passwordcomplexstr)
          checkconfigbz=1
       elif jxzt==3:
            printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]扫描检查密码复杂度要求，此基线未配置。             
                  ''' % No2_1
            checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]扫描密码复杂度要求，符合基线配置规范。               
                  ''' % No2_1
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if gxpz==1:
            if jxzt==2:
               printjg='''
%s
配置结果：[失败]配置密码复杂度要求，更新部分配置失败。
修改配置如下：
%s                
               ''' % (No2_1,passwordcomplexstr)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]配置密码复杂度要求，更新部分配置成功。
修改配置如下：
%s                
               ''' % (No2_1,passwordcomplexstr)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]检查密码复杂度要求，符合基线配置规范。
修改配置如下：
%s                
               ''' % (No2_1,passwordcomplexstr)
                notconfignum+=1
                checkconfigbz=0
         elif addpz==1:
              if jxzt==2:
                 printjg='''
%s
配置结果：[失败]按照密码复杂度要求，首行添加配置失败。
修改配置如下：
%s             
               ''' % (No2_1,passwordcomplexstr)
                 checkconfigbz=2
              elif jxzt==1:
                   printjg='''
%s
配置结果：[成功]按照密码复杂度要求，首行添加配置成功。              
               ''' % No2_1
                   xjdf+=1
                   checkconfigbz=0
              else:
                   printjg='''
%s
配置结果：[正常]按照密码复杂度要求，无需配置。              
               ''' % No2_1
                   notconfignum+=1
                   checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]按照密码复杂度要求，无需配置。              
               ''' % No2_1
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
    
#NO2.2、【配置要求】：禁止空口令登录    {删除用户密码：passwd -d root}
def Emptypassword_nologin(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No2_2="★★★★★★★★★★No2.2、【配置要求】：禁止空口令登录★★★★★★★★★★"
    jxzt=0
    command="awk -F ':' 'length($2)==0 { print $1 }' /etc/shadow"
    usergroupsstr=commands.getoutput(command).strip()
    totalblankpwdusernum=0
    usergroups=''
    if usergroupsstr!='':
       usergroups=usergroupsstr.split('\n')
       totalblankpwdusernum=len(usergroups)
    addpz=0
    gxpz=0
    zzstrnr=""
    userlist=""
    blankpwdunlockusernum=0
    pzsbbz=0
    if op=='--check':
       if totalblankpwdusernum!=0:
          for u in usergroups:
              cmd="passwd -S %s|awk '{ print $2 }'" % u
              pwdstatus=''.join(commands.getoutput(cmd)).replace('\n','')
              if 'L' in pwdstatus:
                 userlist+="[%s]用户密码为空且已锁定状态.\n" % u
                 jxzt=1
              else:
                 userlist+="[%s]用户密码为空且未锁定状态.\n" % u
                 blankpwdunlockusernum+=1
                 jxzt=2                 
    elif op=='--config':
         if totalblankpwdusernum!=0:
            for u in usergroups: 
                cmd="passwd -S %s|awk '{ print $2 }'" % u
                pwdstatus=''.join(commands.getoutput(cmd)).replace('\n','')
                if 'L' in pwdstatus:
                    userlist+="[%s]用户密码为空且为已锁定状态,跳过配置.\n"
                    print userlist
                else:
                    cmd="passwd -l %s >/dev/null" % u    
                    cmdstatus=os.system(cmd)
                    if  cmdstatus==0:
                        userlist+="[%s]用户密码为空,已处理从未锁定变为已锁定状态.\n" % u
                        jxzt=1
                    else:
                        userlist+="[%s]用户密码为空,处理从未锁定变为已锁定过程失败.\n"  % u
                        jxzt=2
                        pzsbbz=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照禁止空口令登录扫描，不符合基线配置规范{建议锁定或删除用户}。
 不规范列表如下：
%s                
                  ''' % (No2_2,userlist)
          checkconfigbz=1
       elif jxzt==1:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照禁止空口令登录扫描，%d个用户全部已锁定，符合基线配置规范。
列表如下：
%s                 
                  ''' % (No2_2,totalblankpwdusernum,userlist)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照禁止空口令登录扫描，不存在空口令用户，符合基线配置规范。              
                  ''' %  No2_2
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 or pzsbbz==1:
               printjg='''
%s
配置结果：[失败]按照禁止空口令登录要求，配置存在空口令用户更新配置失败。
修改配置列表如下：
%s                
               ''' % (No2_2,userlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照禁止空口令登录要求，配置存在空口令用户更新配置全部成功。
修改配置列表如下：
%s                
               ''' % (No2_2,userlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照禁止空口令登录要求，符合基线配置规范。              
               ''' % No2_2
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  


#NO2.3、【配置要求】：检查是否设置口令最小长度[标准值10,建议配置12及以上]
def Klminlen(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No2_3="★★★★★★★★★★No2.3、【配置要求】：检查是否设置口令最小长度[标准值10,建议配置12及以上]★★★★★★★★★★"
    jxzt=0
    minlen=0
    linenum=1
    filelinenum=0
    command=" cat -n /etc/login.defs|grep -v '#'|grep -E 'PASS_MIN_LEN'|sed -n '1p'"
    cmdstr=commands.getoutput(command).strip()
    try:
       minkllenth=int(cmdstr.split()[-1])
    except Exception:
       minkllenth=-1
    try:
       filelinenum=int(cmdstr.split()[0])
    except Exception:
       filelinenum=-1
    if minkllenth!=-1 and filelinenum!=-1:
       if op=='--check':
          if minkllenth<jx_common.KL_minlen:
             jxzt=2               
       elif op=='--config':
            if minkllenth<jx_common.KLJY_minlen:
               cmdstr="sed -i '%ds/%d/%d/g' /etc/login.defs" % (filelinenum,minkllenth,jx_common.KLJY_minlen)
               cmdstatus=os.system(cmdstr)
               if cmdstatus==0:
                  jxzt=1
               else:
                  jxzt=2
    else:
        jxzt=3
               
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照检查是否设置口令最小长度[标准值10,建议配置12及以上]，PASS_MIN_LEN=%d,不符合基线规范。              
                  ''' % (No2_3,minkllenth)
          checkconfigbz=1
       elif jxzt==3:
            printjg='''
%s
【符合度得分】：0
【扫描结果】：[异常]按照检查是否设置口令最小长度[标准值10,建议配置12及以上]，检查PASS_MIN_LEN值出现异常，不符合基线规范。              
                  ''' % No2_3
            checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照检查是否设置口令最小长度[标准值10,建议配置12及以上]，PASS_MIN_LEN=%d,符合基线配置规范。              
                  ''' %  (No2_3,minkllenth)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照检查是否设置口令最小长度[标准值10,建议配置12及以上]，PASS_MIN_LEN=%d,配置更新失败,请检查！！。              
               ''' % (No2_3,minkllenth)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照检查是否设置口令最小长度[标准值10,建议配置12及以上]，PASS_MIN_LEN=%d,配置更新为建议值:PASS_MIN_LEN 12成功！！               
               ''' % (No2_3,minkllenth)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照检查是否设置口令最小长度[标准值10,建议配置12及以上],PASS_MIN_LEN=%d,符合基线配置规范。              
               ''' % (No2_3,minkllenth)
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  


#   PASS_MAX_DAYS 90
#   PASS_WARN_AGE 30
#[检查最长期限是否生效]passwd -S [USERNAME]|awk  '{ print $5 }'
#[检查警告期限是否生效]passwd -S [USERNAME]|awk  '{ print $6}'

#No2.4、【配置要求】密码更新周期要求{配置文件和未锁定的业务用户检查}
def Password_lifeupdate(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No2_4="★★★★★★★★★★No2.4、【配置要求】密码更新周期要求★★★★★★★★★"
    jxzt=0
    minlen=0
    linenum=1
    filelinenum1=0
    filelinenum2=0
    cmdstatus1=-1
    cmdstatus2=-1
    cmdstatus3=0
    sbbzcount=0
    cgbzcount=0
    expect_user=jx_common.xtyw_zhmc
    jxzt1=0    
    PWDGX_MAX_DAYS=jx_common.KLGXZQ_MAX_DAYS
    PWDGX_WRAN_DAYS=jx_common.KLGXZQ_WRN_DAYS
    usergxsuccesslist="" #成功更新列表
    expuser_pwdgxzq=""  #异常列表
    #获取操作系统所有用户列表
    command="cat /etc/passwd|cut -d ':' -f1"
    usergroups=commands.getoutput(command).split('\n')
    #获取PASS_MAX_DAYS值
    command=" cat -n /etc/login.defs|grep -v '#'|grep -E 'PASS_MAX_DAYS'|sed -n '1p'"
    cmdmaxdayssstr=commands.getoutput(command).strip()
    try:
       maxdays=long(cmdmaxdayssstr.split()[-1])
    except Exception:
       maxdays=-9999
    try:
       filelinenum1=int(cmdmaxdayssstr.split()[0])
    except Exception:
       filelinenum1=-9999
    #获取PASS_WARN_AGE值
    command=" cat -n /etc/login.defs|grep -v '#'|grep -E 'PASS_WARN_AGE'|sed -n '1p'"
    cmdwarnagesstr=commands.getoutput(command).strip()
    try:
       warnages=long(cmdwarnagesstr.split()[-1])
    except Exception:
       warnages=-9999
    try:
       filelinenum2=int(cmdwarnagesstr.split()[0])
    except Exception:
       filelinenum2=-9999
    if maxdays!=-9999 and warnages!=-9999 and filelinenum1!=-9999 and filelinenum2!=-9999:
       if op=='--check':
          for u in usergroups:
              if u in jx_common.YW_USER:
                 if u!=expect_user:
                    cmd="passwd -S %s|awk '{ print $2 }'" % u
                    pwdstatus=''.join(commands.getoutput(cmd)).replace('\n','')
                    if 'L' not in pwdstatus:
                        try:
                           cmd1="passwd -S %s|awk '{ print $5 }'" % u
                           temp_maxdays=long(commands.getoutput(cmd1).strip())
                        except Exception:
                           temp_maxdays=-9999
                        try:                    
                           cmd2="passwd -S %s|awk '{ print $6 }'" % u
                           temp_warndays=long(commands.getoutput(cmd2).strip())
                        except Exception:
                           temp_warndays=-9999
                        if temp_warndays!=-9999 and temp_maxdays!=-9999:
                           if temp_maxdays!=PWDGX_MAX_DAYS or temp_warndays!=PWDGX_WRAN_DAYS:
                              expuser_pwdgxzq+="[%s]用户最长期限为%d,警告期限为%d.\n" % (u,temp_maxdays,temp_warndays)
                              sbbzcount+=1
                        else:
                            jxzt=3
          if jxzt!=3:
             if maxdays!=PWDGX_MAX_DAYS or warnages!=PWDGX_WRAN_DAYS:
                jxzt1=2
             if jxzt1==2 or sbbzcount>0:
                jxzt=2                       
       elif op=='--config':
            if maxdays!=PWDGX_MAX_DAYS:
               command1="sed -i '%ds/%d/%d/g' /etc/login.defs" % (filelinenum1,maxdays,PWDGX_MAX_DAYS)
               cmdstatus1=os.system(command1)
            if warnages!=PWDGX_WRAN_DAYS:
               command2="sed -i '%ds/%d/%d/g' /etc/login.defs" % (filelinenum2,warnages,PWDGX_WRAN_DAYS)
               cmdstatus2=os.system(command2)
            for u in usergroups:
                if u in jx_common.YW_USER:
                   if u!=expect_user:
                      cmd="passwd -S %s|awk '{ print $2 }'" % u
                      pwdstatus=''.join(commands.getoutput(cmd)).replace('\n','')
                      if 'L' not in pwdstatus:
                         try:
                            cmd1="passwd -S %s|awk '{ print $5 }'" % u
                            temp_maxdays=long(''.join(commands.getoutput(cmd1)).replace('\n',''))
                         except Exception:
                            temp_maxdays=-9999
                         try:                    
                            cmd2="passwd -S %s|awk '{ print $6 }'" % u
                            temp_warndays=long(''.join(commands.getoutput(cmd2)).replace('\n',''))
                         except Exception:
                            temp_warndays=-9999
                         if temp_warndays!=-9999 and temp_maxdays!=-9999:
                            if temp_maxdays!=PWDGX_MAX_DAYS  or temp_warndays!=PWDGX_WRAN_DAYS:
                               cmdstr="passwd -x %d -w %d %s>/dev/null" % (PWDGX_MAX_DAYS,PWDGX_WRAN_DAYS,u)
                               cmdstatus=os.system(cmdstr)
                               if cmdstatus!=0:
                                  sbbzcount+=1
                                  expuser_pwdgxzq+="[%s]用户最长期限失败更新为%d 或警告期限失败更新为%d" % (u,PWDGX_MAX_DAYS,PWDGX_WRAN_DAYS)
                               else:
                                  usergxsuccesslist+="[%s]用户最长期限成功更新为%d 或警告期限成功更新为%d" % (u,PWDGX_MAX_DAYS,PWDGX_WRAN_DAYS)
                                  cgbzcount+=1    
                         else:
                             jxzt=3
            if jxzt!=3:
               if cmdstatus1==-1 and cmdstatus2==-1:
                  jxzt1=0
               elif cmdstatus1==0 and cmdstatus2==-1:
                  jxzt1=1
               elif cmdstatus1==-1 and cmdstatus2==0:
                  jxzt1=1
               else:
                  jxzt1=2               
               if jxzt1==2 or sbbzcount>0:
                  jxzt=2
               elif jxzt1==1 or cgbzcount>0:
                  jxzt=1
               else:
                  jxzt=0
    else:
        jxzt=3
    if usergxsuccesslist=="":
       usergxsuccesslist="无"
    if op=='--check':
       if jxzt==2:
          if sbbzcount==0:
             printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照密码更新周期要求，不符合基线规范。
[1]/etc/login.defs异常配置如下：
%d PASS_MAX_DAYS %d
%d PASS_WARN_AGE %d
                  ''' % (No2_4,filelinenum1,maxdays,filelinenum2,warnages)
          elif jxzt1==0:
               printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照密码更新周期要求，不符合基线规范。
[1]未锁定业务用户异常配置列表如下：
%s
                  ''' % (No2_4,expuser_pwdgxzq)
          else:
               printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照密码更新周期要求，不符合基线规范。
[1]/etc/login.defs异常配置如下：
%d PASS_MAX_DAYS %d
%d PASS_WARN_AGE %d
[2]未锁定业务用户异常配置列表如下：
%s
                  ''' % (No2_4,filelinenum1,maxdays,filelinenum2,warnages,expuser_pwdgxzq)
             
          checkconfigbz=1
       elif jxzt==3:
            printjg='''
%s
【符合度得分】：0
【扫描结果】：[异常]按照密码更新周期要求，检查/etc/login.defs或未锁定的业务用户密码更新周期出现异常，不符合基线规范。              
                  ''' % No2_4
            checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照密码更新周期要求检查，所有未锁定的业务用户和/etc/login.defs中密码更新周期配置都符合基线配置规范。              
                  ''' %  No2_4
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
         if jxzt==2:
            if sbbzcount==0:
               printjg='''
%s
配置结果：[失败]按照密码更新周期要求检查，/etc/login.defs中PASS_MAX_DAYS或PASS_WARN_AGE,配置更新失败,请检查！！。              
               ''' % No2_4
            elif jxzt1==0:
                 printjg='''
%s
配置结果：[失败]按照密码更新周期要求检查，未锁定的业务用户设置更新失败,请检查！！
异常用户列表如下：
%s            
               ''' % (No2_4,expuser_pwdgxzq)
            else:
                printjg='''
%s
配置结果：[失败]按照密码更新周期要求检查，/etc/login.defs中配置和未锁定的业务用户设置都存在更新失败,请检查！！
[1]/etc/login.defs异常配置如下：
%d PASS_MAX_DAYS %d
%d PASS_WARN_AGE %d
[2]异常用户列表如下：
%s           
               ''' % (No2_4,filelinenum1,maxdays,filelinenum2,warnages,expuser_pwdgxzq)
                checkconfigbz=2
         elif jxzt==1:
              printjg='''
%s
配置结果：[成功]按照密码更新周期要求检查，/etc/login.defs中配置或未锁定的业务用户设置更新成功,请检查！！
[1]/etc/login.defs配置如下：
%d PASS_MAX_DAYS %d
%d PASS_WARN_AGE %d
[2]用户列表如下：
%s           
               ''' % (No2_4,filelinenum1,PWDGX_MAX_DAYS,filelinenum2,PWDGX_WRAN_DAYS,usergxsuccesslist)
              xjdf+=1
              checkconfigbz=0
         else:
             printjg='''
%s
配置结果：[正常]按照密码更新周期要求检查,/etc/login.defs中配置和未锁定的业务用户设置,都符合基线配置规范。              
               ''' % No2_4
             notconfignum+=1
             checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
