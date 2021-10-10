#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import jx_common

xjdf=0
totalitemnum=2
checkconfigbz=-1
notconfignum=0
configsuccessnum=0
jxitemsjcount=0

def Header_xtyh_ywgl():
    printjg='''
****************************************************************************

               Linux基线规范检查和配置：7、系统优化与运维管理

****************************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 


#No7.1、【配置要求】：swappiness配置优化
def SwappinessPZ(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No7_1="★★★★★★★★★★No7.1、【配置要求】：swappiness配置优化★★★★★★★★★★" 
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    alarm_value=jx_common.swappiness_alarmvalue
    cmdstr="cat /proc/sys/vm/swappiness"
    cmdvalue=int(commands.getoutput(cmdstr).strip())
    if op=='--check':
       if cmdvalue>alarm_value:
          sbbzcount+=1
          exppzlist+="[%d]获取当前系统swappiness为%d.\n" %  (linenum,cmdvalue)
    elif op=='--config':
         if cmdvalue>alarm_value:
            cmdstr="cat /etc/sysctl.conf|grep -E '^vm.swappiness'|awk -F '=' '{ print $2 }'"
            cmdvalue=commands.getoutput(cmdstr).strip()
            if cmdvalue!="":
               cmdstr1="sed -i '/^vm.swappiness/s/%s/%s/g' /etc/sysctl.conf" % (cmdvalue,alarm_value)
               cmdstatus=os.system(cmdstr1)
               if cmdstatus!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]/etc/sysctl.conf中vm.swappiness=%s配置修改为%s失败！！\n" %  (linenum,cmdvalue,alarm_value)
               else:
                  successcount+=1
                  successlist+="[%d]/etc/sysctl.conf中vm.swappiness=%s配置修改为%s成功！！\n" % (linenum,cmdvalue,alarm_value)
            else:
               cmdstr2="echo 'vm.swappiness=%s' >> /etc/sysctl.conf" % alarm_value
               cmdstatus2=os.system(cmdstr2)
               if cmdstatus2!=0:
                  sbbzcount+=1
                  exppzlist+="[%d]/etc/sysctl.conf中添加vm.swappiness=%s配置失败\n" %  (linenum,alarm_value)
               else:
                  successcount+=1
                  successlist+="[%d]/etc/sysctl.conf中添加vm.swappiness=%s配置成功\n" % (linenum,alarm_value)
            status=os.system("sysctl -p >/dev/null")
            linenum+=1
            if status!=0:
               sbbzcount+=1
               exppzlist+="[%d]sysctl -p刷新配置失败\n" % linenum
            else:
               successcount+=1
               successlist+="[%d]sysctl -p刷新配置成功\n" % linenum
               cmdstr="cat /proc/sys/vm/swappiness"
               cmdvalue=int(commands.getoutput(cmdstr).strip())
               linenum+=1
               if cmdvalue>alarm_value:
                  sbbzcount+=1
                  exppzlist+="[%d]配置swappiness失败\n" % linenum
               else:
                  successcount+=1
                  successlist+="[%d]配置swappiness成功\n" % linenum     
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照swappiness配置优化检查,不符合基线规范。
不规范过程如下：
%s              
                  ''' % (No7_1,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照swappiness配置优化检查，配置检查都符合基线配置规范。
                  ''' %  No7_1
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照swappiness配置优化检查，存在%d项配置更新失败。
失败过程如下：
%s              
               ''' % (No7_1,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照swappiness配置优化检查，%d项配置更新全部成功！！
需要过程如下：
%s             
               ''' % (No7_1,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照swappiness配置优化检查,服务配置都符合基线配置规范。    
               ''' %  No7_1
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
#No7.2、【配置要求】：建立系统维护账号和建立互信
#def creatextyw_hxrz(op,xtyw_pwd):
#    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
#    jxitemsjcount+=1
#    No7_2="★★★★★★★★★★No7.2、【配置要求】：建立系统维护账号和建立互信★★★★★★★★★★" 
#    jxzt=0
#    linenum=1
#    filelinenum=0
#    umask=""
#    exppzlist=""
#    successlist=""
#    sbbzcount=0
#    successcount=0
#    usermaxexpiredate=jx_common.usermaxexpiredate
#    xtywmc=jx_common.xtyw_zhmc
#    publicmy=jx_common.xtyw_publicmy
#    xtyw_homeauthorized_keys=jx_common.xtyw_homeauthorized_keys
#    cmdstr="id %s >/dev/null 2>&1" % xtywmc
#    cmdstatus=os.system(cmdstr)
#    if op=='--check':
#       if cmdstatus!=0:
#          sbbzcount+=1
#          exppzlist+="[%d]%s用户不存在.\n" %  (linenum,xtywmc)
#       else:
#          cmdstr="passwd -S %s|awk '{ print $2 }'" % xtywmc
#          pwdstatus=''.join(commands.getoutput(cmdstr)).replace('\n','')
#          if 'P' !=pwdstatus and 'PS'!=pwdstatus:
#             sbbzcount+=1
#             exppzlist+="[%d]%s用户状态不符合要求（已锁定或空密码）.\n" %  (linenum,xtywmc)
#          else:
#             cmdstr="passwd -S %s|awk '{ print $5 }'" % xtywmc
#             cmdvalue=commands.getoutput(cmdstr).strip()
#             if usermaxexpiredate!=cmdvalue:
#                sbbzcount+=1
#                exppzlist+="[%d]%s用户未设置永不过期\n" %  (linenum,xtywmc)
#             else:
#                if not os.path.isfile(xtyw_homeauthorized_keys):
#                   sbbzcount+=1
#                   exppzlist+="[%d]%s用户文件%s不存在\n" %  (linenum,xtyw_homeauthorized_keys,xtywmc)
#                else:
#                   cmdstr="cat %s|grep '%s'" % (xtyw_homeauthorized_keys,publicmy)
#                   cmdvalue=commands.getoutput(cmdstr).strip()
#                   if cmdvalue=="":
#                      sbbzcount+=1
#                      exppzlist+="[%d]%s用户未建立互信\n" %  (linenum,xtywmc)
#                   else:
#                      cmdstr="grep -iE 'ALL=\(ALL\)  NOPASSWD:ALL' /etc/sudoers"
#                      cmdvalue=commands.getoutput(cmdstr).strip()
#                      if cmdvalue=="":
#                         sbbzcount+=1
#                         exppzlist+="[%d]%s用户未添加xtyw提权配置\n" %  (linenum,xtywmc)
#    elif op=='--config':
#         if cmdstatus!=0:
#            cmdstr="useradd %s" % xtywmc
#            cmdstatus=os.system(cmdstr)
#            if cmdstatus!=0:
#               sbbzcount+=1
#               exppzlist+="[%d]添加%s用户失败.\n" %  (linenum,xtywmc)
#            else:
#               successcount+=1
#               successlist+="[%d]添加%s用户成功.\n" %  (linenum,xtywmc)
#               linenum+=1
#         cmdstr="passwd -S %s|awk '{ print $2 }'" % xtywmc
#         pwdstatus=''.join(commands.getoutput(cmdstr)).replace('\n','')
#         if 'P' !=pwdstatus and 'PS'!=pwdstatus: 
#            cmdstr="cat /etc/shadow|grep -E '^%s:'|awk -F ':' '{ print $2 }'" % xtywmc
#            cmdvalue=commands.getoutput(cmdstr).strip()
#            if cmdvalue=="!!":
#               pwdvalue=''
#               if xtyw_pwd!='':
#                  cmdstr='''echo "%s"|passwd --stdin %s>/dev/null''' % (xtyw_pwd,xtywmc)
#               else:
#                  pwdvalue=jx_common.get_randompwd(16)
#                  cmdstr='''echo "%s"|passwd --stdin %s>/dev/null''' % (pwdvalue,xtywmc)
#               cmdstatus=os.system(cmdstr)
#               if cmdstatus!=0:                       
#                  sbbzcount+=1
#                  if pwdvalue!='':
#                     exppzlist+="[%d]%s用户密码,由于你未指定密码，按照密码要求设置为16位的随机密码失败,请排查原因或手工设置密码\n" %  (linenum,xtywmc)
#                  else:
#                     exppzlist+="[%d]%s用户密码已按您要求设置密码失败,请排查原因或手工设置密码.\n" %  (linenum,xtywmc)
#               else:
#                  successcount+=1
#                  if pwdvalue!='':
#                     successlist+="[%d]%s用户密码,由于你未指定密码，按照密码要求设置为16位的随机密码成功，其中密码为：%s，请妥善保管密码！！\n" %  (linenum,xtywmc,pwdvalue)
#                  else:
#                     successlist+="[%d]%s用户密码已按您要求设置密码成功,其中密码为:%s,请妥善保管密码！！\n" %  (linenum,xtywmc,xtyw_pwd)
#               linenum+=1
#         else:
#             if xtyw_pwd!='':
#                cmdstr='''echo "%s"|passwd --stdin %s>/dev/null''' % (xtyw_pwd,xtywmc)
#                cmdstatus=os.system(cmdstr)
#                if cmdstatus!=0:                       
#                   sbbzcount+=1
#                   exppzlist+="[%d]%s用户密码已按您要求设置密码失败,请排查原因或手工设置密码.\n" %  (linenum,xtywmc)
#                else:
#                   successcount+=1
#                   successlist+="[%d]%s用户密码已按您要求设置密码成功,其中密码为:%s,请妥善保管密码！！\n" %  (linenum,xtywmc,xtyw_pwd)
#                linenum+=1
#         cmdstr="passwd -S %s|awk '{ print $5 }'" % xtywmc
#         cmdvalue=commands.getoutput(cmdstr).strip()
#         if usermaxexpiredate!=cmdvalue:
#            cmdstr="chage -M 99999 xtyw"
#            cmdstatus=os.system(cmdstr)
#            if cmdstatus!=0:
#               sbbzcount+=1
#               exppzlist+="[%d]%s用户设置永不过期失败\n" %  (linenum,xtywmc)
#            else:
#               successcount+=1
#               successlist+="[%d]%s用户设置永不过期成功\n" %  (linenum,xtywmc)
#            linenum+=1
#         if not os.path.isfile(xtyw_homeauthorized_keys):
#            cmdstr="mkdir /home/%s/.ssh && chmod  700 /home/%s/.ssh && chown -R %s:%s /home/%s/.ssh && touch /home/%s/.ssh/authorized_keys && chmod 600 /home/%s/.ssh/authorized_keys" % (xtywmc,xtywmc,xtywmc,xtywmc,xtywmc,xtywmc,xtywmc)
#            cmdstatus=os.system(cmdstr)
#            if cmdstatus!=0:
#               sbbzcount+=1
#               exppzlist+="[%d]%s家目录中执行%s失败\n" %  (linenum,xtywmc,cmdstr)
#            else:
#               successcount+=1
#               successlist+="[%d]%s家目录中执行%s成功\n" %  (linenum,xtywmc,cmdstr)
#            linenum+=1
#         cmdstr="cat %s|grep '%s'" % (xtyw_homeauthorized_keys,publicmy)
#         cmdvalue=commands.getoutput(cmdstr).strip()
#         if cmdvalue=="":
#            cmdstr="echo '%s' >>%s" % (publicmy,xtyw_homeauthorized_keys)
#            cmdstatus=os.system(cmdstr)
#            if cmdstatus!=0: 
#               sbbzcount+=1
#               exppzlist+="[%d]%s用户添加互信失败，请检查%s\n" %  (linenum,xtywmc)
#            else:
#               successcount+=1
#               successlist+="[%d]%s用户添加互信成功。\n" %  (linenum,xtywmc)
#            linenum+=1
#         cmdstr="grep -iE 'ALL=\(ALL\)  NOPASSWD:ALL' /etc/sudoers"
#         cmdvalue=commands.getoutput(cmdstr).strip()
#         if cmdvalue=="":
#            cmdstr1="chmod u+w /etc/sudoers"
#            cmdstatus1=os.system(cmdstr1)
#            cmdstr2="sed -i '/^root/a xtyw    ALL=(ALL)  NOPASSWD:ALL'  /etc/sudoers"
#            cmdstatus2=os.system(cmdstr2)
#            cmdstr3="chmod u-w /etc/sudoers"
#            cmdstatus3=os.system(cmdstr3)
#            if cmdstatus1!=0 or cmdstatus2!=0 or cmdstatus3!=0:
#               sbbzcount+=1
#               exppzlist+="[%d]%s用户添加xtyw提权配置失败，请检查/etc/sudoers文件配置和权限\n" %  (linenum,xtywmc) 
#            else:
#               successcount+=1
#               successlist+="[%d]%s用户添加xtyw提权配置成功！！\n" %  (linenum,xtywmc)
#            linenum+=1
#    if exppzlist!="":
#       jxzt=2
#    if sbbzcount==0 and successcount>0:
#       jxzt=1
#    if op=='--check':
#       if jxzt==2:
#          printjg='''
#%s
#【符合度得分】： 0
#【扫描结果】：[异常]按照建立系统维护账号和建立互信检查,不符合基线规范。
#不规范过程如下：
#%s              
#                  ''' % (No7_2,exppzlist)
#          checkconfigbz=1
#       else:
#            printjg='''
#%s
#【符合度得分】：1
#【扫描结果】：[正常]按照建立系统维护账号和建立互信检查，配置检查都符合基线配置规范。
#                  ''' %  No7_2
#            xjdf+=1
#            jx_common.fhd_score+=1
#            checkconfigbz=0
#    elif op=='--config':
#            if jxzt==2 :
#               printjg='''
#%s
#配置结果：[失败]按照建立系统维护账号和建立互信检查，存在%d项配置更新失败。
#失败过程如下：
#%s              
#               ''' % (No7_2,sbbzcount,exppzlist)
#               checkconfigbz=2
#            elif jxzt==1:
#                 printjg='''
#%s
#配置结果：[成功]按照建立系统维护账号和建立互信检查，%d项配置更新全部成功！！
#需要过程如下：
#%s             
#               ''' % (No7_2,successcount,successlist)
#                 xjdf+=1
#                 checkconfigbz=0
#            else:
#                printjg='''
#%s
#配置结果：[正常]按照建立系统维护账号和建立互信检查,服务配置都符合基线配置规范。    
#               ''' %  No7_2
#                notconfignum+=1
#                checkconfigbz=0
#    else:
#        printjg="无"       
#    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
     