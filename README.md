#PyAuto
###自动化UI操作
1
自动模拟点击UI窗口
####解决需求：
1.模拟人工点击操作进行自动化。

这个开发项目的针对一款windows的桌面软件。
此桌面软件是用一个webkit写的浏览器。外部无法获取控件hwnd等任何信息。
所以只能根据UI反馈的颜色信息进行每步自动化的操作。

#####步骤器：
1.点击器
2.输入器
3.颜色检查器

Machine为一个管理器
加入所需的步骤器即可
然后start

######如何取消自动化操作？
鼠标动一下就可以。每次步骤前会检查上一次的步骤坐标。如果用户干预了鼠标。就会终止所有步骤的执行

##GitHub：
https://github.com/zhangliganggm/PyAuto

##Coding项目代码管理：
https://coding.net/u/acee/p/PyAuto/git

##Makedown在线编辑器
https://maxiang.io/#

######作者
QQ:394452216
Email:Acee-Studio@qq.com
Blog:http://cgace.blogbus.com/