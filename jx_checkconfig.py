#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import time
import datetime
import hashlib
sys.path.append("tools")
import jx_zhgl
import jx_klgl
import jx_fwkzrzsq
import jx_common
import jx_zymlwjqxsz
import jx_rzshgl
import jx_aqgl
import jx_xtyh_ywgl
import jx_otherpz


RZWJ=['/var/log/cron','/var/log/secure','/var/log/messages','/var/log/maillog','/var/log/boot.log','/var/log/mail','/var/log/localmessages','/var/log/spooler']
sshd_configgroups=['UsePAM yes','PubkeyAuthentication yes','Protocol 2','LogLevel INFO','MaxAuthTries 5','IgnoreRhosts yes','RhostsAuthentication no','RhostsRSAAuthentication no','HostbasedAuthentication no','PermitEmptyPasswords no','PermitUserEnvironment no','ClientAliveInterval 60','ClientAliveCountMax 3','LoginGraceTime 60','X11Forwarding yes'] 
JXGL_Time=time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
CurrentUser=commands.getoutput("whoami")
JXGL_PATH=os.getcwd()
xxlb="##################################"
xxtb="******************"
xstb="xxxxxxxxxxxxxxxxxx"
PWD_MY=['1dAbcd@3edc4rfv','7d4r68ik,##@~','1mABC2wsx3edc@1','3mABC3edc4rfv@1234','6mABC3edc4rfv@1234','1yABC3edc4rfv@1234']
PWD_DICT={}
JBCreatedDate='2021-10-10 00:00:00'
YXDZ="暂无"
QQQSQM="暂无"
WXGZH="暂无"







    
#版权说明信息
def pqsm_help():
    print ('''
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@基线检查和配置工具v1.0版权和功能说明@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
       @@       ！！！严重警告说明：此脚本工具所有权由sansi所有，凡是未经授权，擅自抄袭、破解、售卖、使用等违法操作，必将追究其法律责任； @@
       @@ 本脚本工具仅供技术交流，请通过购买或授权的方式获取到密钥的同仁们，请在测试环境测试验证无问题之后，再用于其他重要关键环境，如因使@@
       @@ 用脚本工具而造成严重后果，后果自负。特此声明！！！                                                                              @@  
       @@ 本脚本工具功能：                                                                                                                @@
       @@             1、检查Linux基线符合度。                             2、按照标准配置Linux基线                                       @@
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
          ''')
          

#漏洞修复帮助提示信息
def ldxf_help(scriptsName,tsnr):
    print ('''温馨提示：%s
 --------------------------------------------------欢迎使用基线检查和配置工具（created by sansi）--------------------------------------------------------------------
 检查和配置说明：只针对Linux6/7的操作系统做基线检查和配置，脚本自动识别6或7的操作系统版本，请用root用户执行脚本,使用命令格式如下
 python %s [pwd] [mode]  [optional parameter]
                 [mode]可选择的如下：
                       --help  : 使用命令帮助;
                       --handbook:基线标准手册说明
                       --check:  检查基线是否符合;
                       --config: 按基线标准配置基线;
                 其中PWD{为脚本管理员授权的密钥};[optional parameter]可选参数如下：
                 {--skipiptables:跳过防火墙检查和配置;--skipyum:跳过yum检查和配置;--skipntp:跳过ntp检查和配置;--xtyw_pwd=[PWD]:指定xtyw密码{大写、小写、数字、特殊字符4选3；长度12位以上}}
                 举例如下：
                 >>检查Linux基线：python %s 'PWD' --check
                 >>配置Linux基线：python %s 'PWD' --config        
                 >>不检查防火墙基线检查
                   python %s 'PWD' --check  --skipiptables                                   
 -------------------------------------------------------------------------------------------------------------------------------------------------------------      
          ''' % (tsnr,scriptsName,scriptsName,scriptsName,scriptsName))
          
#漏洞修复报告标题          
def Report_Title(ReportName):
    Report_TIME=time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())) 
    reporttitle='''#########################################################《%s》###############################################################
                  【IP】:%s                                             
                  【当前扫描用户】:%s 
                  【当前扫描时间】:%s
                ''' % (ReportName,jx_common.JXGL_IP,CurrentUser,Report_TIME)
    jx_common.write_report(-1,jx_common.JXGL_Report,'a',reporttitle)

#密码初始化参数值
def PWD_CSH():
    for p in PWD_MY:
        md5_1=hashlib.md5("%s8866" % p).hexdigest()
        md5_2=hashlib.md5("%s9999" % md5_1).hexdigest()
        PWD_DICT[p]=md5_2
#密码验证和密码期限函数        
def JB_BH_QXHS(jbpwd):
    i=0
    rqnr=""
    sflx=""
    for p  in PWD_DICT:
        if PWD_DICT[p]==jbpwd:
           jx_common.write_report(-1,jx_common.JXGL_Report,'w',"#####>>您的密码已经通过脚本认证!!")
           i=1
        #  rq=p[:2]
        #  if rq=='1d':
        #     rqnr="一天"
        #     sflx="青铜用户"
        #     rqdest=datetime.datetime.strptime(JBCreatedDate,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days=1)
        #  elif rq=='7d':
        #     rqnr="7天"
        #     sflx="特约测试用户"
        #     rqdest=datetime.datetime.strptime(JBCreatedDate,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days=7)
        #  elif rq=='1m':
        #     rqnr="一个月"
        #     sflx="白银用户"
        #     rqdest=datetime.datetime.strptime(JBCreatedDate,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days=30)
        #  elif rq=='3m':
        #     rqnr="三个月"
        #     sflx="黄金用户"
        #     rqdest=datetime.datetime.strptime(JBCreatedDate,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days=90)
        #  elif rq=='6m':
        #     rqnr="六个月"
        #     sflx="铂金用户"              
        #     rqdest=datetime.datetime.strptime(JBCreatedDate,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days=180)
        #  elif rq=='1y':
        #     rqnr="1年"
        #     sflx="钻石用户" 
        #     rqdest=datetime.datetime.strptime(JBCreatedDate,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days=365)
        #  else:           
        #     rqdest=""
        #  jx_common.write_report(-1,jx_common.JXGL_Report,'a',"获取您的套餐中,请等候...........")
        #  try:
        #     ntpsrc=''.join(commands.getoutput("cat /etc/ntp.conf|grep -vE '127.127.1.0|127.0.0.1|localhost'|grep -E '^server'|awk '{ print $2 }'|sed -n 1p")).replace('\n','')
        #     ntpstatus=os.system("ntpdate -d %s > /dev/null 2>&1" % ntpsrc)
        #     jx_common.write_report(-1,jx_common.JXGL_Report,'a',"获取您的套餐中,请等候..................")
        #     if ntpstatus!=0:
        #        jx_common.write_report(2,jx_common.JXGL_Report,'a',"当前Linux系统到您配置的ntp时间源不通，测试命令为ntpdate -d %s" % ntpsrc)
        #        exit(2)
        #     else:            
        #        ntpoffset=float(''.join(commands.getoutput("ntpdate -d %s|grep -E '^offset'" % ntpsrc)).replace('\n','').split()[-1])
        #  except Exception:
        #     jx_common.write_report(1,jx_common.JXGL_Report,'a',"请检查/etc/ntp.conf是否配置,ntpdate -d [时间源]检查offset值是否正常！！") 
        #     exit(2)
        #  jdzoffset=int(abs(ntpoffset))
        #  dayoffset=int(jdzoffset//86400)
        #  if ntpoffset<0 and jdzoffset!=0:
        #     currentrqsrc=datetime.datetime.now()-datetime.timedelta(days=dayoffset)
        #  else:
        #     currentrqsrc=datetime.datetime.now()+datetime.timedelta(days=dayoffset)
        #  sjczc=(rqdest - currentrqsrc).days     
        #  syts=(abs(sjczc)-1)
        #  if  sjczc>0:
        #      jx_common.write_report(-1,jx_common.JXGL_Report,'a',"#####>>尊敬的%s,该脚本创建时间为[%s],授权套餐为{%s}时间,剩余使用%s天.\n关于我们:【微信公众号】%s；%s；如有脚本相关问题请发送邮件:%s." % (sflx,JBCreatedDate,rqnr,syts,WXGZH,QQQSQM,YXDZ))
        #  elif sjczc==0:
        #      jx_common.write_report(1,jx_common.JXGL_Report,'a',"#####>>尊敬的%s,该脚本创建时间为[%s],授权套餐为{%s},到%s截止过期,请继续续期！！\n关于我们:【微信公众号】%s；%s；如有脚本相关问题请发送邮件:%s.)" % (sflx,JBCreatedDate,rqnr,rqdest,WXGZH,QQQSQM,YXDZ))
        #  else:
        #      jx_common.write_report(2,jx_common.JXGL_Report,'a',"#####>>尊敬的%s,该脚本创建时间为[%s],授权套餐为{%s},已经过期%s天,请继续续期！！\n关于我们:【微信公众号】%s；%s；如有脚本相关问题请发送邮件:%s." % (sflx,JBCreatedDate,rqnr,syts,WXGZH,QQQSQM,YXDZ))
        #      exit(2)
        #  break
    if i==0:
       jx_common.write_report(1,jx_common.JXGL_Report,'w',"#####>>密码认证未通过,请联系管理员授权！！")
       exit(2)
       
       
#1.账号管理(4)
def ZHGL(op):
    jx_common.jxdlcount+=1
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>>>>>1、账号管理<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       =========================================================================
       NO1.1、【配置要求】：删除或锁定无关的系统用户和用户组；
            基线符合性判断依据:判断是否为常规用户，具体系统无关用户，根据运维人员确定(脚本通过匹配系统用户和运维用户字典,对无关用户进行锁定。)
       
       NO1.2、【配置要求】：检查是否存在除root之外UID为0的用户
            基线符合性判断依据:执行命令awk -F ':'  '$3==0 { print $1 }' /etc/passwd 根据检查结果判断是否存在除root之外UID为0的用户，如存在锁定该用户passwd –l <username>    #锁定该用户
       
       NO1.3、【配置要求】：登录超时设置
            基线符合性判断依据：判断是否配置"TMOUT=",建议配置TMOUT=300,并且值不大于600
       
       NO1.4、【配置要求】：限制管理员root远程登录
            基线符合性判断依据：设置/etc/ssh/sshd_config文件中，第一次出现PermitRootLogin no为准; 如存在PermitRootLogin yes改为PermitRootLogin no，并且检查/etc/ssh/sshd_config，是否存在：
       ''')
    else:
        jx_zhgl.Header_zhgl()
        jx_zhgl.Unrelated_users(op)
        jx_zhgl.Exprootuid0_users(op)
        jx_zhgl.Login_timeout(op)
        jx_zhgl.Restrictroot_notlogin(op)
        try:
           pznum=int(jx_zhgl.jxitemsjcount-jx_zhgl.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_zhgl.totalitemnum,jx_zhgl.jxitemsjcount,op,jx_zhgl.xjdf,pznum)
    
#2.口令管理(4)    
def KLGL(op):
    jx_common.jxdlcount+=1
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>2、口令管理配置要求说明<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       ======================================================================
       NO2.1、【配置要求】：密码复杂度要求
               1）采用数字、字母、符号的无规律混排方式；
               2）口令的长度至少为8位，并且每90天至少更换1次
               3）如果系统长度不支持上述口令复杂度要求，应使用所支持的最长长度并适当缩小更换周期；也可以使用动态密码卡等一次性口令认证方式。
               4)修改操作系统账户的默认口令，系统无法实现的除外。
       		基线符合性判断依据：执行命令cat /etc/pam.d/system-auth|grep  "password requisite pam_cracklib.so difok=3 minlen=8 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1"是否存在。
       NO2.2、【配置要求】：禁止空口令登录
               检查方法：awk -F ':' 'length($2)==0 { print $1 }' /etc/shadow；[空]:表示无空口令登录的用户,否则存在空口令用户将它锁住或删除。
       NO2.3、【配置要求】：检查是否设置口令最小长度[标准值10,建议配置12及以上]
               检查方法：查看文件/etc/login.defs中设置 PASS_MIN_LEN 不小于标准值（10）     
       NO2.4、【配置要求】密码更新周期和口令更改最小天数要求
               检查方法：检查/etc/login.defs参数， 
                         PASS_MAX_DAYS 90
       				     PASS_WARN_AGE 30
                         PASS_MIN_DAYS 6
       				  [检查最长期限是否生效]passwd -S [USERNAME]|awk  '{ print $5 }'
                      [检查警告期限是否生效]passwd -S [USERNAME]|awk  '{ print $6}'
       ''')
    else:
        jx_klgl.Header_klgl()
        jx_klgl.Password_complexity(op)
        jx_klgl.Emptypassword_nologin(op)
        jx_klgl.Klminlen(op)
        jx_klgl.Password_lifeupdate(op)
        try:
           pznum=int(jx_klgl.jxitemsjcount-jx_klgl.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_klgl.totalitemnum,jx_klgl.jxitemsjcount,op,jx_klgl.xjdf,pznum)

#3.访问控制及认证授权(5)
def FWKZ_RZSQ(op):
    jx_common.jxdlcount+=1
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>3、访问控制及认证授权<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       ======================================================================
       NO3.1、【配置要求】：用户缺省访问权限
               控制用户缺省访问权限，当在创建新文件或目录时应屏蔽掉新文件或目录不应有的访问允许权限。防止同属于该组的其它用户及别的组的用户修改该用户的文件或更高限制。
       		   基线符合性判断依据：
                          1）执行：more /etc/profile检查是否包含 umask 值且 umask=027(同理/etc/csh.login、/etc/csh.cshrc、/etc/bashrc中查看umask 077)
                          2）如果没有执行：echo "umask 027" >> /etc/profile 或 echo "umask 077" >> /etc/csh.login等
       NO3.2、【配置要求】：授权账户SSH访问控制
               >>对于使用IP 协议进行远程维护的系统，应配置使用SSH 等加密协议，并安全配置SSHD 的设置。
               检查方法：在/etc/ssh/sshd_config配置文件中确认如下配置是否存在：
                         Protocol 2
                         LogLevel INFO
                         MaxAuthTries 5
                         IgnoreRhosts yes
                         RhostsAuthentication no
                         RhostsRSAAuthentication no
                         HostbasedAuthentication no
                         PermitEmptyPasswords no
                         PermitUserEnvironment no
                         ClientAliveInterval 60
                         ClientAliveCountMax 3
                         LoginGraceTime 60
                         X11Forwarding yes
                         配置之后,重启服务：service sshd restart
       NO3.3、【配置要求】:允许和限制SSH远程访问主机
               >>对物理主机/虚拟机进行IP地址访问限制，防止异常陌生IP地址访问攻击。
               1）第一种方法（废弃）：
               配置 /etc/hosts.deny 与 /etc/hosts.allow文件
               配置 /etc/hosts.deny 文件
               # no sshd 
               sshd:ALL  //禁止所有IP地址ssh访问
               配置 /etc/hosts.allow 文件
               根据业务需求配置相关IP地址
               例如：sshd:192.168.220.   //允许192.168.220.0  IP段访问
               2）第二种方法（推荐）:
               /etc/ssh/sshd_config
               allowusers [username]@[IP或IP段]
               特殊说明：第一种方法不一定完全生效，脚本只对第二种配置进行检查，第一种配置是不符合规范的。               
       NO3.4、【配置要求】登录失败处理功能策略(不做检查，此方法存在争议)
               设置登录失败功能，建议设置5次，防止恶意攻击者可以对系统口令进行反复暴力破解(设置登录失败功能策略，通过PAM限制用户登录失败次数，如果次数达到设置的阈值，则锁定用户)
               检查方法：
               1)vim /etc/pam.d/sshd （远程ssh）
               在文件首行#%PAM-1.0下增加：
               auth required pam_tally2.so deny=5 unlock_time=600 even_deny_root root_unlock_time=600
               2)vim /etc/pam.d/login （终端）
               在文件首行#%PAM-1.0下增加：
               auth required pam_tally2.so deny=5 unlock_time=600 even_deny_root root_unlock_time=600
               3)vim /etc/pam.d/system-auth (服务器终端)
               在文件首行#%PAM-1.0下增加：
               auth required pam_tally2.so onerr=fail deny=5 unlock_time=600 even_deny_root root_unlock_time=600
        NO3.5、【配置要求】检查是否使用PAM认证模块禁止wheel组之外的用户su为root
               为了安全性，只允许部分普通用户能切换到root，其他用户做限制不能切换
               [检查方法]
               默认检查cqswj是否设置wheel组:id cqswj，如果在此{%s}组用户全部设置合规，没设置则不合规。
               /etc/pam.d/su取消注释:#auth		required	pam_wheel.so use_uid                
               Linux6:
                 /etc/pam.d/su中是否存在：auth required pam_wheel.so group=wheel
               Linux7:
                 /etc/login.defs中是否存在：SU_WHEEL_ONLY yes 
               [加固方法]
                usermod -G wheel cqswj或[%s]
                sed -i '/pam_wheel.so use_uid/s/^#//g' /etc/pam.d/su
                Linux6:
                echo "auth required pam_wheel.so group=wheel">> /etc/pam.d/su
                Linux7:
                echo "SU_WHEEL_ONLY yes" >> /etc/login.defs
       ''' % jx_common.SU_COMMONUser)
    else:
        jx_fwkzrzsq.Header_fwkzrzsq()
        jx_fwkzrzsq.Userdefault_access(op)
        jx_fwkzrzsq.Sshaccess_control(op)
        #Sshpermit_restriction(op)
        #Loginfailed_policy(op)
        jx_fwkzrzsq.Restrictroot_Pam_directlogin(op)
        try:
           pznum=int(jx_fwkzrzsq.jxitemsjcount-jx_fwkzrzsq.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_fwkzrzsq.totalitemnum,jx_fwkzrzsq.jxitemsjcount,op,jx_fwkzrzsq.xjdf,pznum)

#4.重要目录和文件权限设置(3)
def ZYML_WJQX(op):
    jx_common.jxdlcount+=1
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>4、重要目录和文件权限设置<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       ======================================================================
       NO4.1、【配置要求】：配置重要目录和文件的权限
               控制用户对有敏感标记重要信息资源的操作。
               检查方法：
               ls –l /etc/  [不做检查，配置之后存在异常]
               ls -l /etc/passwd
               ls -l /etc/group 
               ls -l /etc/shadow 
               ls -l /etc/services 
               ls -l /etc/security 
               ls -l /etc/rc*.d/ 
               ls -l /etc/rc.d/init.d/
               按照如下建议修改
               chmod 750 /etc  (由于会影响普通用户家目录[chmod 755 /etc/])
               chmod 750 /tmp  (如果安装图形界面 chmod 777 /tmp，否则会报错"服务器有错/usr/libexec/gconf-sanity-check-2的退出状态为256")
               chmod 750 /etc/rc.d/init.d
               chmod 644 /etc/passwd
               chmod 644 /etc/group 
               chmod 400 /etc/shadow 
               chmod 644 /etc/services 
               chmod 600 /etc/security 
               chmod 750 /etc/rc*.d/ 
               chmod 750 /etc/rc.d/init.d

               对于重要目录，建议执行如下类似操作：chmod  750 /etc/rc.d/init.d/*；只有 root 可以读、写和执行这个目录下的脚本
       NO4.2、【配置要求】：检查重要文件是否存在suid和sgid权限
               为降低风险，防止未授权用户通过sudo执行相关重要文件命令
               检查方法：
               执行命令: 
               find /usr/bin/chage /usr/bin/gpasswd /usr/bin/wall /usr/bin/chfn /usr/bin/chsh /usr/bin/newgrp /usr/bin/write /usr/sbin/usernetctl /usr/sbin/traceroute /bin/mount /bin/umount /bin/ping /sbin/netreport -type f -perm +6000 2>/dev/null 
               如果存在输出结果，则使用chmod 755 文件名 命令修改文件的权限。 
               例如：chmod a-s /usr/bin/chage
       NO4.3、【配置要求】：检查系统引导器配置文件权限
               为降低风险，检查系统引导器配置文件权限
               检查方法：
               查看如下文件权限是否为600
               #Linux6
               chmod 600 /etc/grub.conf [非链接文件]
               chmod 600 /boot/grub/grub.conf
               chmod 600 /etc/lilo.conf
               #Linux7
               chmod 600 /etc/grub2.cfg [非链接文件]
               chmod 600 /boot/grub2/grub.cfg
       ''')
    else:
        jx_zymlwjqxsz.Header_zymlwjqxsz()
        jx_zymlwjqxsz.Importantdirectory_fileright(op)
        jx_zymlwjqxsz.Checksuid_sgid_file(op)
        jx_zymlwjqxsz.Checkbootfileright(op)
        try:
           pznum=int(jx_zymlwjqxsz.jxitemsjcount-jx_zymlwjqxsz.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_zymlwjqxsz.totalitemnum,jx_zymlwjqxsz.jxitemsjcount,op,jx_zymlwjqxsz.xjdf,pznum)

#5.日志审核(3)
def RZSH(op):
    jx_common.jxdlcount+=1
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>5、日志审核<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       ======================================================================
       NO5.1、【配置要求】：开启系统日志记录
               应开启主机操作系统审核功能，审核内容包括但不限于运行状态日志、系统事件、账户管理、登录事件、操作事件、配置文件的修改，日志保存期限至少6个月。
               检查方法：
               1)查看日志服务是否安装并且进程是否已启动：
               rpm -qa|grep rsyslog
               ps -elf |grep rsyslogd
               2)开启日志审核：
                 /etc/init.d/rsyslog start
                 或service rsyslog start
               3)日志加固，确保已配置rsyslog默认文件权限：
                 vim /etc/rsyslog.conf
                 在#### GLOBAL DIRECTIVES ####段中添加：
                 $FileCreateMode 0640
       NO5.2、【配置要求】：开启操作日志记录，记录用户的操作日志。
               应开启主机操作系统审核功能，审核内容包括但不限于运行状态日志、系统事件、账户管理、登录事件、操作事件、配置文件的修改，日志保存期限至少6个月。
               检查方法：在/etc/profile中检查是否存在如下配置
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
        NO5.3、【配置要求】：检查日志文件权限设置
　　　　　　　　设备应配置权限，控制对日志文件读取、修改和删除等操作(权限小于等于775)
　　　     　　［检查方法］
                %s 文件权限权限小于等于775,建议设置600
                [加固建议]
                chmod 600 /var/log/cron 
                chmod 600 /var/log/secure 
                chmod 600 /var/log/messages 
                chmod 600 /var/log/maillog 
                chmod 600 /var/log/boot.log 
                chmod 600 /var/log/mail 
                chmod 600 /var/log/localmessages 
                chmod 600 /var/log/spooler               
       ''' % RZWJ)
       
    else:
        jx_rzshgl.Header_rzshgl()
        jx_rzshgl.Opensystem_log(op)
        jx_rzshgl.Openopration_log(op)
        jx_rzshgl.Checklogqx_gl(op)
        try:
           pznum=int(jx_rzshgl.jxitemsjcount-jx_rzshgl.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_rzshgl.totalitemnum,jx_rzshgl.jxitemsjcount,op,jx_rzshgl.xjdf,pznum)


#6.安全管理(2)        
def AQGL(op):
    jx_common.jxdlcount+=1
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>6、安全管理<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       ======================================================================
       NO6.1、【配置要求】：关闭不必要的服务和端口
               关闭telnet、autofs、acpid、cpus、ipsec、ip6tables、rpcbind、postfix等服务
               检查方法：
               chkconfig --list |grep 3:on 查看哪些正运行的服务
               Linux6:
               使用下面命令关闭无关的服务：
               chkconfig --level 12345 autofs off
               chkconfig --level 12345 acpid off
               chkconfig --level 12345 cups off 
               chkconfig --level 12345 cups-config-daemon off
               chkconfig --level 12345 ipsec off
               chkconfig --level 12345 ip6tables off
               chkconfig --level 12345 rpcbind off
               chkconfig --level 12345 postfix off
               chkconfig --level 12345 pppoe-server off
               chkconfig --level 12345 sendmail off
               chkconfig --level 12345 isdn off
               chkconfig --level 12345 mdmonitor off
               chkconfig --level 12345 rhnsd off
               chkconfig --level 12345 smartd off
               chkconfig --level 12345 gpm off
               chkconfig --level 12345 telnet off
               chkconfig --level 12345 nfslock off
               Linux7:
               systemctl list-unit-files|grep enabled|awk -F '.' '{ print $1}'
               关闭以上服务 systemctl disable [服务名称]
       NO6.2、【配置要求】：互联网DMZ区服务器开启iptables服务
               对于检查互联网服务器IP为%s进行防火墙状态和规则检查
               检查方法：
               1)检查iptables是否安装或firewalld服务状态。
                  rpm –qa|grep iptables 或 rpm –qa|grep firewalld
               2)安装完成后查询iptables或firewalld服务是否运行：
                  service iptables status  或 systemctl status firewalld          
       NO6.3、【配置要求】：按安全组检查安全狗软件是否安装
               对操作系统操作审计。
               检查方法：
               1)检查safedog服务状态。
                 service safedog status
               2)查看到控制中心端口80端口是否能通：
                  telnet 10.116.124.65 80   
               配置方法：
              【紫光云(不包含横向联网区)】 curl -sk https://10.116.124.65/safe/soft/sdserver-installer.sh | bash -s -- 10.116.124.65 cloud NF-7400L
                             
       ''' % HLWIPD)
    else:
        jx_aqgl.Header_aqgl()
        jx_aqgl.Closeservice_nouse(op)
        jx_aqgl.Openhlwiptables(op)
        #jx_aqgl.SafeDog_InstallPZ(op)
        try:
           pznum=int(jx_aqgl.jxitemsjcount-jx_aqgl.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_aqgl.totalitemnum,jx_aqgl.jxitemsjcount,op,jx_aqgl.xjdf,pznum)

       
#7.系统优化与运维管理(2)        
def XTYH_YWGL(op,xtyw_pwd):
    jx_common.jxdlcount+=1
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>7、系统优化与运维管理<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       ======================================================================
       NO7.1、【配置要求】：swappiness配置优化
               [检查方法]
               cat /proc/sys/vm/swappiness值是否<=10，建议配置为10。
               [加固建议]
               echo "vm.swappiness=10" >> /etc/sysctl.conf
               sysctl -p
               cat /proc/sys/vm/swappiness
       NO7.2、【配置要求】：建立系统维护账号和建立互信
               用于普通用户或root无法登录出现异常时候，通过此账号进行维护处理。
               [检查方法]
               检查是否存在xtyw账号，过期时间是否设置为永不过期，互信密钥是否添加，sudoer配置文件是否添加
               检查用户是否存在：id xtyw
               检查用户是否设置密码：passwd -S xtyw|awk '{ print $2 }'" [P或PS:正常状态,L或LK：为锁定状态,NP:用户密码未空的状态]
               检查是否设置为永不过期：passwd -S xtyw
               检查是否设置为互信：首先判断：/home/xtyw/.ssh/authorized_keys文件是否存在，然后检查cat /home/xtyw/.ssh/authorized_keys|grep 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1wYTh7cw1lUBcgr5kMKtLilh3CwbxhCJDITgZfYDlbNtPiURtrvpamBMHMYz9EuuBmXyXSF9D18oD/HmFiIXzgqobTGw2asNxwbpoPBY1YxvHJAZUV99ml/GrqdIFbLW2lgDsojIkXA0rnxZ1G/uHOaZBPuKKnvlaXyhtMV4NdZFK3UuzDyz82Bx8FLGVo+clkkZ9BeOWyOrTi5ihk/6ime24WdiSue2XwXxjrGCSu4oKBDNj778ytl31HSUz14gBrH4em1nLM22+P6ddVhrKp4oJgvY7IqAG1ibhuxUNXWkf3Q5EM5ZKdchK9TCKdKhiFqwGgiCmQAonjRD8Cx9H xtyw@hxq-poller21'
               检查是否设置sudoers：grep -iE 'xtyw    ALL=\(ALL\)  NOPASSWD:ALL' /etc/sudoers
               [加固建议]
               useradd  xtyw
               echo `< /dev/urandom tr -dc 0-9-A-Z-a-z-/|head -c ${1:-16};echo`|passwd --stdin xtyw
               chage -M 99999 xtyw
               mkdir /home/xtyw/.ssh
               chmod  700 /home/xtyw/.ssh
               echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1wYTh7cw1lUBcgr5kMKtLilh3CwbxhCJDITgZfYDlbNtPiURtrvpamBMHMYz9EuuBmXyXSF9D18oD/HmFiIXzgqobTGw2asNxwbpoPBY1YxvHJAZUV99ml/GrqdIFbLW2lgDsojIkXA0rnxZ1G/uHOaZBPuKKnvlaXyhtMV4NdZFK3UuzDyz82Bx8FLGVo+clkkZ9BeOWyOrTi5ihk/6ime24WdiSue2XwXxjrGCSu4oKBDNj778ytl31HSUz14gBrH4em1nLM22+P6ddVhrKp4oJgvY7IqAG1ibhuxUNXWkf3Q5EM5ZKdchK9TCKdKhiFqwGgiCmQAonjRD8Cx9H xtyw@hxq-poller21" >>/home/xtyw/.ssh/authorized_keys
               chmod 600 /home/xtyw/.ssh/authorized_keys
               chown -R xtyw:xtyw /home/xtyw/.ssh
               chmod u+w /etc/sudoers
               sed -i '/^root/a xtyw    ALL=(ALL)  NOPASSWD:ALL'  /etc/sudoers
               chmod u-w /etc/sudoers    
       ''')
    else:
        jx_xtyh_ywgl.Header_xtyh_ywgl()
        jx_xtyh_ywgl.SwappinessPZ(op)
        #jx_xtyh_ywgl.creatextyw_hxrz(op,xtyw_pwd)
        try:
           pznum=int(jx_xtyh_ywgl.jxitemsjcount-jx_xtyh_ywgl.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_xtyh_ywgl.totalitemnum,jx_xtyh_ywgl.jxitemsjcount,op,jx_xtyh_ywgl.xjdf,pznum)


#8.其他配置要求(10)  
def QTPZYQ(op):
    if op=='--handbook':
       print (
       '''
       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>8、其他配置要求<<<<<<<<<<<<<<<<<<<<<<<<<<<<
       ======================================================================
       NO8.1、【配置要求】：检查是否设置ssh登录前警告Banner
       　　　　SSH登录时显示警告信息，在登录成功前不泄漏服务器信息。
              ［检查方法］
               查看文件/etc/ssh/sshd_config，检查是否存在如下配置:banner <file_path>，且<file_path>内容不为空
　　　　　　　［加固方法］
              touch /etc/ssh_banner
　　　　　　　chown bin:bin /etc/ssh_banner
　　　　　　　chmod 644 /etc/ssh_banner
　　　　　　　echo " Authorized only. All activity will be monitored and reported " > /etc/ssh_banner
　　　　　　　echo "Banner /etc/ssh_banner" >> /etc/ssh/sshd_config
　　　　　　　service sshd restart
       NO8.2、【配置要求】：检查是否修改SNMP默认团体字.
               SNMP服务未开启或者修改了默认的团体名则合规,否则不合规。
               ［检查方法］
　　　　　　　　1）查看snmpd进程是否存在。
　　　　　　　　#ps -ef|grep "snmpd"|grep -v "grep"
　　　　　　　  2）查看文件/etc/snmp/snmpd.conf,检查SNMP团体名配置。
　　　　　　　［加固建议］
　　　　　　　１）修改snmp配置文件/etc/snmp/snmpd.conf找到类似如下配置,修改默认团体名public为其他用户自己可识别的字符串。
	　　　　　　　com2sec notConfigUser  default  public   #<notConfigUser>为连接snmp的用户名 <default>为可以连接snmp的地址范围 <public>为团体名
	　　　　　２）、重启snmp服务
	　　　　　　　#service snmpd restart
       NO8.3、【配置要求】：检查系统是否禁用Ctrl+Alt+Delete组合键
               　禁止Ctrl+Alt+Delete，防止非法重新启动服务器。禁用了使用组合键Ctrl+Alt+Delete重启系统则合规,否则不合规
               ［检查方法］
　　　　　　　　Linux７：
　　　　　　　　检查是否存在这个文件/usr/lib/systemd/system/ctrl-alt-del.target
　　　　　　　　Linux６
　　　　　　　　查看文件/etc/init/control-alt-delete.conf,是否存在使用组合键control+alt+delete控制系统重启的配置。
		　　　　　exec /sbin/shutdown -r now "Control-Alt-Delete pressed"
                Linux5
                查看/etc/inittab文件  
                ca::ctrlaltdel:/sbin/shutdown -t3 -r now   //默认为启用，在前面加上#号进行关闭
　　　　　　　　［加固建议］
　　　　　　　　Linux７：
　　　　　　　　　ｍｖ　/usr/lib/systemd/system/ctrl-alt-del.target /usr/lib/systemd/system/ctrl-alt-del.target.bak
　　　　　　　　　init　q　重新加载配置文件使配置生效
                  或 注释掉/usr/lib/systemd/system/ctrl-alt-del.target所有内容
　　　　　　　　Linux 6
　　　　　　　　编辑文件/etc/init/control-alt-delete.conf,将如下行删除或注释:
　　　　　　　  exec /sbin/shutdown -r now "Control-Alt-Delete pressed"
　　　　　　　　Linux 5
　　　　　　　　编辑文件cat /etc/inittab,将如下行删除或注释:
　　　　　　　  ca::ctrlaltdel:/sbin/shutdown -t3 -r now
　　　 NO8.4、【配置要求】：主机须启用时钟同步
　　　　　　　　对应区域配置对应NTP时间源：｛%s｝
　　　     　　［检查方法］
　　　　　　　　1.确认是否安装NTP组件
                  rpm -qa|grep -E  'ntp-'
                2.检查是否配置对应区域的时间源
                  server XXX.XXX.XXX.XXX
                3、是否运行，然后是否自动启动
                  ps -fe|grep ntpd
                Linux6
                  chkconfig --list ntpd 
                Linux7 
                   systemctl list-unit-files|grep enabled|awk -F '.' '{ print $1}'|grep ntpd是否存在
                [加固建议]
　　　　　　　　编辑/etc/ntp.conf文件，对NTP服务进行配置，可在文件中加一行：
　　　　　　　　server XXX.XXX.XXX.XXX     #将时钟源指定为已设好的时钟同步服务器
　　　　　　　　service ntpd start        #启用服务
　　　　　　　　chkconfig ntpd on          #设置自动运行
　　　 NO8.5、【配置要求】：禁用core dump 
　　　　　　　　core dump 中可能包括系统信息，易被入侵者利用。
　　　     　　［检查方法］
　　　　　　　　1)执行：more /etc/security/limits.conf 检查是否包含下列项：
                 * soft core 0
                 * hard core 0
                 2)若没有，执行：vi /etc/security/limits.conf 添加
                 * soft core 0
                 * hard core 0 
                [加固建议]
                 echo "* soft core 0" >> /etc/security/limits.conf
                 echo "* hard core 0" >> /etc/security/limits.conf
　　　 NO8.6、【配置要求】：用户使用最大进程数及文件打开数配置
　　　　　　　　建议根据业务需求对单个用户使用的进程数、文件打开数等进行设置。
　　　     　　［检查方法］
                脚本通过检查操作系统是否存在%s,对用户是否全部配置 /etc/security/limits.conf进行检查。
                [加固建议]
                 vi /etc/security/limits.conf 添加
                 *   soft    nproc     65535(后面值根据业务情设定)
                 *   hard    nproc     65535
                 *   soft    nofile    65535
                 *   hard    nofile    65535 
                 重新ssh连接建立会话ulimit -a检查是否生效。
        NO8.7、【配置要求】：系统服务优先级配置
　　　　　　　　当系统服务水平降低时，通过renice命令修改已经存在进程的NI值
　　　     　　［检查方法］
                检查/etc/sudoers中是否存在[%s]  ALL=(ALL) NOPASSWD:/usr/bin/renice 
                检查方式：cat /etc/sudoers|grep -v '^#'|grep 'NOPASSWD:/usr/bin/renice'
                [加固建议]
                1)、配置以weblogic用户为例能够sudo执行renice 命令，在/etc/sudoers 文件中添加
                    例如：weblogic  ALL=(ALL) NOPASSWD:/usr/bin/renice
                    
                2)、用top和ps aux 命令查看存在进程的NI值和进程号 
                3)、手动修改已经存在进程的NI值
                    renice -n -15  -p {weblogic pid}  -n后面是优先级的值，-p后面是进程号
        NO8.8、【配置要求】：检查/etc/aliases是否禁用不必要的别名
　　　　　　　　检查/etc/aliases是否禁用不必要的别名
　　　     　　［检查方法］
                编辑别名文件vi /etc/aliases，删除或注释掉下面的行
                #games: root
                #ingres: root
                #system: root
                #toor: root
                #uucp: root
                #manager: root
                #dumper: root
                #operator: root
                #decode: root
                #root: marc
                补充操作说明
                更新后运行/usr/bin/newaliases，使改变生效 
                [加固建议]
                sed  -i '/^games/s/^/#/g' /etc/aliases
                sed  -i '/^ingres/s/^/#/g' /etc/aliases
                sed  -i '/^system/s/^/#/g' /etc/aliases
                sed  -i '/^toor/s/^/#/g' /etc/aliases
                sed  -i '/^uucp/s/^/#/g' /etc/aliases
                sed  -i '/^manager/s/^/#/g' /etc/aliases
                sed  -i '/^dumper/s/^/#/g' /etc/aliases
                sed  -i '/^operator/s/^/#/g' /etc/aliases
                sed  -i '/^decode/s/^/#/g' /etc/aliases
                sed  -i '/^root/s/^/#/g' /etc/aliases
                /usr/bin/newaliases     
        NO8.9、【配置要求】：检查是否配置定时自动屏幕锁定（适用于具备图形界面的设备）
　　　　　　　　检查是否配置定时自动屏幕锁定（只对安装了图形界面系统生效）
　　　     　　［检查方法］
                检查是否安装GConf2
                rpm -qa|grep GConf2
                [加固建议]
                gconftool-2 --direct --config-source  xml:readwrite:/etc/gconf/gconf.xml.mandatory --type string  --set /apps/gnome-screensaver/mode blank-only
                gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory  --type int --set /apps/gnome-screensaver/idle_delay 15
                gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory --type bool --set /apps/gnome-screensaver/idle_activation_enabled true
                gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory --type bool --set /apps/gnome-screensaver/lock_enabled true
                gsettings set org.gnome.desktop.screensaver idle-activation-enabled true
                gsettings set org.gnome.desktop.screensaver lock-enabled true
                gsettings set org.gnome.desktop.screensaver lock-delay 300 
                gsettings set org.gnome.desktop.session idle-delay 300 
        NO8.10、【配置要求】：检查密码重复使用次数限制
　　　　　　　　对于采用静态口令认证技术的设备，应配置设备，使用户不能重复使用最近5次（含5次）内已使用的口令。
　　　     　　［检查方法］
                检查/etc/pam.d/system-auth中是否存在password sufficient pam_unix.so md5 shadow nullok try_first_pass use_authtok remember=5
                [加固建议]
                 sed -i '/try_first_pass use_authtok/s/sha512/md5/g' /etc/pam.d/system-auth
                 sed -i '/try_first_pass use_authtok/s/$/ remember=5/g' /etc/pam.d/system-auth
        NO8.11、【配置要求】：检查系统内核参数配置
                 检查系统内核参数配置
                 [检查方法]
                 检查是否禁止icmp源路由(0):cat /proc/sys/net/ipv4/conf/all/accept_source_route
                 检查是否禁止icmp重定向报文(0):cat /proc/sys/net/ipv4/conf/all/accept_redirects
                 检查send_redirects配置(0):cat /proc/sys/net/ipv4/conf/all/send_redirects
                 检查icmp_echo_ignore_broadcasts配置(1):cat /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts
                 检查ip_forward配置(0):cat /proc/sys/net/ipv4/ip_forward
                 [加固建议]
                 echo "net.ipv4.conf.all.accept_source_route=0" >> /etc/sysctl.conf
                 echo "net.ipv4.conf.all.accept_redirects=0" >> /etc/sysctl.conf
                 echo "net.ipv4.conf.all.send_redirects=0" >> /etc/sysctl.conf
                 echo "net.ipv4.icmp_echo_ignore_broadcasts=1" >> /etc/sysctl.conf
                 echo "net.ipv4.ip_forward=0" >> /etc/sysctl.conf
                 sysctl -p
       ''' %  (jx_common.NTPSJY,jx_common.ProcessFileNumpzgroups,jx_common.ZJJ_USER))
    else:
        jx_otherpz.Header_otherpz()
        jx_otherpz.Warn_banner(op)
        jx_otherpz.SNMP_publicpz(op)
        jx_otherpz.Close_ctrl_alt_del(op)
        jx_otherpz.Host_ntppz(op)
        jx_otherpz.Close_coredump(op)
        jx_otherpz.User_ProcessFileNum(op)
        jx_otherpz.Service_priority(op)
        jx_otherpz.Disable_alias(op)
        jx_otherpz.Timed_autoscreenlock(op)
        jx_otherpz.Password_Repeatlimit(op)
        jx_otherpz.Kernel_parameterPZ(op)
        try:
           pznum=int(jx_otherpz.jxitemsjcount-jx_otherpz.notconfignum)
        except Exception:
           pznum=-1
        jx_common.Summary_score(jx_common.jxdlcount,jx_otherpz.totalitemnum,jx_otherpz.jxitemsjcount,op,jx_otherpz.xjdf,pznum)
        #Openhlwiptables(op)





   




 
#一、基线检查或配置
def JXGL_check_config(selectmode,skipyumbz,skipntpbz,skipiptables,xtyw_pwd):
    op=selectmode
    ZHGL(op)
    KLGL(op)
    FWKZ_RZSQ(op)
    ZYML_WJQX(op)
    RZSH(op)
    AQGL(op)
    XTYH_YWGL(op,xtyw_pwd)
    QTPZYQ(op)
    
    
#二、基线标准手册
def JXGL_handbook(selectmode):
    op=selectmode
    ZHGL(op)
    KLGL(op)
    #FWKZ_RZSQ(op)
    #ZYML_WJQX(op)
    #RZSH(op)
    #AQGL(op)
    #XTYH_YWGL(op)
    #QTPZYQ(op)
    
def main():  
    jxjcpzargs=sys.argv
    scriptsName=jxjcpzargs[0]
    Modes=['--help','--check','--handbook','--config']
    optionalparams=['--skipiptables','--skipyum','--skipntp','--xtyw_pwd']
    skipyumbz=0
    skipntpbz=0
    skipiptables=0
    xtyw_pwd=''
    optionalargs01=''
    optionalargs02=''
    optionalargs03=''
    pqsm_help()   
    try:
        jbpwd=jxjcpzargs[1]
    except Exception:
        jbpwd=''
    if jbpwd=='' or jbpwd in Modes:
       tsnr="请仔细查看如下帮助!!"
       ldxf_help(scriptsName,tsnr)
       exit(0)
    try:
        selectmode=jxjcpzargs[2]
    except Exception:
        selectmode=''
    if selectmode not in Modes:
       tsnr="您输入mode不符合要求!!"
       ldxf_help(scriptsName,tsnr)
       exit(2)
    elif selectmode==Modes[0]:
       tsnr="请仔细查看如下帮助!!"
       ldxf_help(scriptsName,tsnr)
       exit(0)
    try:
       optionalargs01=jxjcpzargs[3]
    except Exception:
           optionalargs01=''
    try:
       optionalargs02=jxjcpzargs[4]
    except Exception:
           optionalargs02=''
    try:
       optionalargs03=jxjcpzargs[5]
    except Exception:
           optionalargs03=''
    try:
       optionalargs04=jxjcpzargs[6]
    except Exception:
           optionalargs04=''
    optionalgroups=[optionalargs01,optionalargs02,optionalargs03,optionalargs04]
    for op in  optionalgroups:
        op_zd=''
        if '=' in op:
           op_zd=op.split('=')[0]
           op_value=op.split('=')[1]
        if op!='':
           if optionalparams[0]==op:
              skipiptables=1
           elif optionalparams[1]==op:
                skipyumbz=1
           elif optionalparams[2]==op:
                skipntpbz=1
           elif optionalparams[3]==op_zd:
                if jx_common.check_pwd(op_value)==0:
                   xtyw_pwd=op_value
                else:
                   ldxf_help(scriptsName,"可选参数输入没满足密码要求（大写字母，小写字母，数字，特殊字符 四项中的至少三项，长度12位以上)，请查看如下[optional parameter]")
                   exit(0)
           else:
               ldxf_help(scriptsName,"可选参数输入有误，请查看如下[optional parameter]")
               exit(0)
    if selectmode==Modes[1]:
       ReportName="Linux基线检查报告"
       jx_common.JXGL_Report=JXGL_PATH+"/jxreport/JXGLReport_check_"+jx_common.JXGL_IP+"_"+JXGL_Time+".txt"
    elif selectmode==Modes[3]:
       ReportName="Linux基线配置报告"
       jx_common.JXGL_Report=JXGL_PATH+"/jxreport/JXGLReport_config_"+jx_common.JXGL_IP+"_"+JXGL_Time+".txt"
    elif selectmode==Modes[2]:
       ReportName="Linux基线标准手册"
       jx_common.JXGL_Report=JXGL_PATH+"/jxreport/JXGLReport_handbook_"+jx_common.JXGL_IP+"_"+JXGL_Time+".txt"
    else:
       ReportName=""
       jx_common.JXGL_Report="无"      
    PWD_CSH()
    JB_BH_QXHS(jbpwd)
    Report_Title(ReportName)
    if selectmode==Modes[1] or selectmode==Modes[3]:
       JXGL_check_config(selectmode,skipyumbz,skipntpbz,skipiptables,xtyw_pwd)
       jx_common.write_report('-1',jx_common.JXGL_Report,'a',"基线检查最终得分为%d" % jx_common.fhd_score)
    elif selectmode==Modes[2]:
       JXGL_handbook(selectmode)
    else:
        tsnr="您输入mode不符合要求!!"
        ldxf_help(scriptsName,tsnr)
        exit(0)
    
        
#main
if __name__ == '__main__':
    main()
