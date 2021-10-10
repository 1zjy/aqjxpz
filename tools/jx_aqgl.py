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

def Header_aqgl():
    printjg='''
************************************************************************

               Linux基线规范检查和配置：6、安全管理

************************************************************************
            '''
    jx_common.write_report(3,jx_common.JXGL_Report,'a',printjg) 


#No6.1、【配置要求】：关闭不必要的服务和端口
def Closeservice_nouse(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No6_1="★★★★★★★★★★No6.1、【配置要求】：关闭不必要的服务和端口★★★★★★★★★★"
    fwgroups=['autofs','acpid','cups', 'cups-config-daemon','ipsec','ip6tables','rpcbind','postfix','pppoe-server','sendmail','isdn','mdmonitor','rhnsd','smartd','gpm','telnet','nfslock']
    jxzt=0
    linenum=1
    filelinenum=0
    umask=""
    exppzlist=""
    successlist=""
    sbbzcount=0
    successcount=0
    osversion=jx_common.get_osversion()
    checksvrgroupsstr=""
    configsvrgroupsstr=""
    if osversion==6:
       checksvrgroupsstr="chkconfig --list |grep 3:on|awk '{ print $1 }'"   
    elif osversion==7:
         checksvrgroupsstr="systemctl list-unit-files|grep enabled|awk -F '.' '{ print $1}'"
    checksvrgroups=commands.getoutput(checksvrgroupsstr).strip().split('\n')
    for s in checksvrgroups: 
        if op=='--check':
           if s in fwgroups:
              sbbzcount+=1
              exppzlist+="[%d]%s服务未关闭.\n" %  (linenum,s)
        elif op=='--config':
             if s in fwgroups:
                if osversion==6:
                   fwstr="chkconfig --level 12345 %s off  >/dev/null 2>&1" % s
                elif osversion==7:
                     fwstr="systemctl disable  %s >/dev/null 2>&1" % s
                fwstatus=os.system(fwstr)
                if fwstatus!=0:
                   sbbzcount+=1
                   exppzlist+="[%d]%s服务关闭失败！！\n" %  (linenum,s)
                else:
                   successcount+=1
                   successlist+="[%d]%s服务关闭成功！！\n" % (linenum,s)
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照Linux%d关闭不必要的服务和端口检查,不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No6_1,osversion,exppzlist)
          checkconfigbz=1
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照Linux%d关闭不必要的服务和端口检查，配置检查都符合基线配置规范。
                  ''' %  (No6_1,osversion)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照Linux%d关闭不必要的服务和端口检查，存在%d项配置更新失败。
失败列表如下：
%s              
               ''' % (No6_1,osversion,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照Linux%d关闭不必要的服务和端口检查，%d项配置全部成功！！
需要更新列表如下：
%s             
               ''' % (No6_1,osversion,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            else:
                printjg='''
%s
配置结果：[正常]按照Linux%d关闭不必要的服务和端口检查,服务配置都符合基线配置规范。    
               ''' % (No6_1,osversion)
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
#No6.2、【配置要求】：互联网DMZ区服务器开启iptables服务
def Openhlwiptables(op):
    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
    jxitemsjcount+=1
    No6_2="★★★★★★★★★★No6.2、【配置要求】：互联网DMZ区服务器开启iptables服务★★★★★★★★★★"
    IP=jx_common.JXGL_IP
    osversion=jx_common.get_osversion()
    sbbzcount=0
    exppzlist=""
    successcount=0
    successlist=""
    linenum=1
    jxzt=0
    cgppvalue=0
    for i in jx_common.HLWIPD:
        if op=='--check':
           if IP!='127.0.0.1':
              if i.strip('.*') in IP:
                 cgppvalue+=1
                 if osversion==6:
                    cmdstr0="service iptables status"
                    state=os.system(cmdstr0)
                    if state!=0:
                       sbbzcount+=1
                       exppzlist+="[%d]Linux6服务器IP：%s,未开启防火墙\n" %  (linenum,IP)
                 elif osversion==7:
                      cmdstr1="systemctl status firewalld|grep Active|awk  '{ print $3 }'"
                      cmdstr2="systemctl status iptables|grep Active|awk  '{ print $3 }'"
                      state1=commands.getoutput(cmdstr1).strip()
                      state2=commands.getoutput(cmdstr2).strip()
                      if state1!='(running)' and state2!='(exited)':
                         sbbzcount+=1
                         exppzlist+="[%d]Linux7服务器IP：%s,未开启防火墙\n" %  (linenum,IP)     
           else:
              sbbzcount+=1
              exppzlist+="[%d]此服务器IP为127.0.0.1无法判断是否为互联网地址，请检查系统配置\n" %  linenum
              break
        elif op=='--config':
             if IP!='127.0.0.1':
                if i.strip('.*') in IP:
                   cgppvalue+=1
                   if osversion==6:
                      cmdstr0="service iptables start>/dev/null"
                      state=os.system(cmdstr0)
                      if state!=0:
                         sbbzcount+=1
                         exppzlist+="[%d]Linux6服务器IP：%s,防火墙开启失败\n" %  (linenum,IP)
                      else:
                         successcount+=1
                         successlist+="[%d]Linux6服务器IP：%s,防火墙开启成功\n" %  (linenum,IP)
                   elif osversion==7:
                        cmdstr="systemctl status firewalld|grep Active|awk  '{ print $3 }'"
                        state=commands.getoutput(cmdstr).strip()
                        if state!='(running)':
                           cmdstr1="systemctl start firewalld" 
                           state1=os.system(cmdstr1)
                           if state1!=0:
                              cmdstr2="systemctl|grep iptbales"
                              str2=commands.getoutput(cmdstr2).strip()
                              cmdstr4="systemctl status iptables|grep Active|awk  '{ print $3 }'"
                              str4=commands.getoutput(cmdstr4).strip()
                              if str2!="":
                                 if str4!='(exited)':
                                    cmdstr3="service start iptables>/dev/null"
                                    state3=os.system(cmdstr3)
                                    if state3!=0:
                                       sbbzcount+=1
                                       exppzlist+="[%d]Linux7服务器IP：%s,防火墙开启失败\n" %  (linenum,IP)
                                    else:
                                       successcount+=1
                                       successlist+="[%d]Linux7服务器IP：%s,防火墙开启成功\n" %  (linenum,IP)
                           else:
                               successcount+=1
                               successlist+="[%d]Linux7服务器IP：%s,防火墙开启成功\n" %  (linenum,IP)                       
             else:
                sbbzcount+=1
                exppzlist+="[%d]此服务器IP为127.0.0.1无法判断是否为互联网地址，请检查系统配置\n" %  linenum
    if exppzlist!="":
       jxzt=2
    if sbbzcount==0 and successcount>0:
       jxzt=1
    if op=='--check':
       if jxzt==2:
          printjg='''
%s
【符合度得分】： 0
【扫描结果】：[异常]按照互联网DMZ区服务器开启iptables服务检查,Linux%s检查不符合基线规范。
不规范列表如下：
%s              
                  ''' % (No6_2,osversion,exppzlist)
          checkconfigbz=1
       elif cgppvalue==0:   
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照互联网DMZ区服务器开启iptables服务检查，此服务器%s未在要求%s列表中,不强制要求配置防火墙，因此符合基线配置规范。
                  ''' %  (No6_2,IP,str(jx_common.HLWIPD))
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0 
       else:
            printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照互联网DMZ区服务器开启iptables服务检查，Linux%s配置检查都符合基线配置规范。
                  ''' %  (No6_2,osversion)
            xjdf+=1
            jx_common.fhd_score+=1
            checkconfigbz=0
    elif op=='--config':
            if jxzt==2 :
               printjg='''
%s
配置结果：[失败]按照互联网DMZ区服务器开启iptables服务检查，Linux%s中存在%d项配置更新失败。
失败列表如下：
%s              
               ''' % (No6_2,osversion,sbbzcount,exppzlist)
               checkconfigbz=2
            elif jxzt==1:
                 printjg='''
%s
配置结果：[成功]按照互联网DMZ区服务器开启iptables服务检查，Linux%s中%d项配置全部成功！！
需要更新列表如下：
%s             
               ''' % (No6_2,osversion,successcount,successlist)
                 xjdf+=1
                 checkconfigbz=0
            elif cgppvalue==0:   
                 printjg='''
%s
【符合度得分】：1
【扫描结果】：[正常]按照互联网DMZ区服务器开启iptables服务检查，此服务器%s未在要求%s列表中,不强制要求配置防火墙，因此符合基线配置规范。
                  ''' %  (No6_2,IP,str(jx_common.HLWIPD))
                 notconfignum+=1
                 checkconfigbz=0 
            else:
                printjg='''
%s
配置结果：[正常]按照互联网DMZ区服务器开启iptables服务检查,Linux%s中服务配置都符合基线配置规范。    
               ''' % (No6_2,osversion)
                notconfignum+=1
                checkconfigbz=0
    else:
        printjg="无"       
    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
    
    
##No6.3、【配置要求】：按安全组检查安全狗软件是否安装
#def SafeDog_InstallPZ(op):
#    global xjdf,totalitemnum,jxitemsjcount,notconfignum,configsuccessnum,checkconfigbz
#    jxitemsjcount+=1
#    No6_3="★★★★★★★★★★No6.3、【配置要求】：按安全组检查安全狗软件是否安装★★★★★★★★★★"
#    IP=jx_common.JXGL_IP
#    osversion=jx_common.get_osversion()
#    sbbzcount=0
#    exppzlist=""
#    successcount=0
#    successlist=""
#    linenum=1
#    jxzt=0
#    Safedog_kzzx=jx_common.Safedogkzzx[0]
#    permitIPgroups=jx_common.Safedog_permitclientipgroups
#    ipcheck=0
#    ipnopermitpz=0
#    isinstallsafedog=0
#    for j in permitIPgroups:
#        if j.strip('.*') in IP:
#           ipcheck=1
#        if '>' in j:
#           IPP=j.split('>')[0]
#           IPN=j.split('>')[1]
#           if IPP.strip('.*') in IP:
#              for n in IPN.split('/'):
#                  if n.strip('.*') in IP:
#                     ipnopermitpz=1
#              if ipnopermitpz==0:
#                 ipcheck==1
#    if op=='--check':
#       if ipcheck==0 or ipnopermitpz==1:
#          isinstallsafedog=1
#       else:
#          cmdstr0="service safedog status|grep 'safedog service is running'"
#          cmdvalue=commands.getoutput(cmdstr0).strip()
#          if cmdvalue=="":
#             sbbzcount+=1
#             exppzlist+="[%d]当前服务器IP：%s,查询服务%s运行异常\n" %  (linenum,cmdstr0)
#          else:    
#             if IP!='127.0.0.1':
#                cmdstr="nc -vz %s 80>/dev/null" %  Safedog_kzzx
#                cmdstatus=os.system(cmdstr)
#                if cmdstatus!=0:
#                   sbbzcount+=1
#                   exppzlist+="[%d]此服务器IP为%s,到控制中心%s不通\n" %  (linenum,IP,kzzxip)     
#             else:
#                sbbzcount+=1
#                exppzlist+="[%d]此服务器IP为127.0.0.1无法判断是否为互联网地址，请检查系统配置\n" %  linenum
#    elif op=='--config':
#         if ipcheck==0 or ipnopermitpz==1:
#            isinstallsafedog=1
#         else:
#            cmdstr0="service safedog status|grep 'safedog service is running'"
#            cmdvalue=commands.getoutput(cmdstr0).strip()
#            if cmdvalue=="":
#               cmdstr1="service safedog status|grep 'safedog serivce is not running'"
#               cmdvalue1=commands.getoutput(cmdstr1).strip()
#               if cmdvalue1!="":
#                  cmdstr2="service safedog start"
#                  cmdstatus=os.system(cmdstr2)
#                  if cmdstatus!=0:
#                     sbbzcount+=1
#                     exppzlist+="[%d]当前服务器IP：%s,安全狗服务启动失败！！\n" %  linenum
#                  else:
#                     successcount+=1
#                     successlist+="[%d]当前服务器IP：%s,安全狗服务启动成功！！\n" %  linenum
#               else:
#                  kzzxip=""
#                  for i in HLWIPGROUPS:
#                      if i.strip('.*') in IP:
#                         kzzxip=WW_Safedog_kzzx
#                  if kzzxip=="":
#                     kzzxip=NW_Safedog_kzzx
#                  cmdstr="curl -sk https://%s/safe/soft/sdserver-installer.sh | bash -s -- %s cloud NF-7400L" % (kzzxip,kzzxip)
#                  cmdstatus=os.system(cmdstr)
#                  if cmdstatus!=0:
#                     sbbzcount+=1
#                     exppzlist+="[%d]安全狗安装失败\n" %  linenum
#                  else:
#                     successcount+=1
#                     successlist+="[%d]安全狗安装成功\n" %  linenum
#    if exppzlist!="":
#       jxzt=2
#    if sbbzcount==0 and successcount>0:
#       jxzt=1
#    if op=='--check':
#       if jxzt==2:
#          printjg='''
#%s
#【符合度得分】： 0
#【扫描结果】：[异常]按安全组检查安全狗软件是否安装检查,检查安全狗未安装或运行异常不符合基线规范。
#不规范列表如下：
#%s              
#                  ''' % (No6_3,exppzlist)
#          checkconfigbz=1
#       elif isinstallsafedog==1:   
#            printjg='''
#%s
#【符合度得分】：1
#【扫描结果】：[正常]按安全组检查安全狗软件是否安装检查，%s未在列表中%s,按安全组不要求安装安装狗，跳过检查,因此符合基线配置规范。
#                  ''' %  (No6_3,IP,permitIPgroups)
#            xjdf+=1
#            jx_common.fhd_score+=1
#            checkconfigbz=0 
#       else:
#            printjg='''
#%s
#【符合度得分】：1
#【扫描结果】：[正常]按安全组检查安全狗软件是否安装检查，已安装安全狗检查都符合基线配置规范。
#                  ''' %  No6_3
#            xjdf+=1
#            jx_common.fhd_score+=1
#            checkconfigbz=0
#    elif op=='--config':
#            if jxzt==2 :
#               printjg='''
#%s
#配置结果：[失败]按安全组检查安全狗软件是否安装检查，安装安全狗过程中存在%d项配置失败。
#失败列表如下：
#%s              
#               ''' % (No6_3,sbbzcount,exppzlist)
#               checkconfigbz=2
#            elif jxzt==1:
#                 printjg='''
#%s
#配置结果：[成功]按安全组检查安全狗软件是否安装检查，安装安全狗过程%d项配置全部成功！！
#需要更新列表如下：
#%s             
#               ''' % (No6_3,successcount,successlist)
#                 xjdf+=1
#                 checkconfigbz=0
#            elif isinstallsafedog==1:   
#                 printjg='''
#%s
#【符合度得分】：1
#【扫描结果】：[正常]按安全组检查安全狗软件是否安装检查，%s未在列表中%s,按安全组不要求安装安装狗，跳过配置,因此符合基线配置规范。
#                  ''' %  (No6_3,IP,permitIPgroups)
#                 notconfignum+=1
#                 checkconfigbz=0 
#            else:
#                printjg='''
#%s
#配置结果：[正常]按安全组检查安全狗软件是否安装检查,已安装安全狗检查都符合基线配置规范。    
#               ''' % No6_3
#                notconfignum+=1
#                checkconfigbz=0
#    else:
#        printjg="无"       
#    jx_common.write_report(checkconfigbz,jx_common.JXGL_Report,'a',printjg)  
#     
#     