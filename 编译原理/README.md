
# 编译原理
这是我的编译原理课程设计程序,使用了python语言编写
限制条件如下！！！
+ 除了需要安装要用到的python库之外，还需要安装graphviz并配置好环境变量才能画图
+ 递归分析和lr0分析并不完整，只支持一些文法。
+ 预测分析能识别大部分的C语言代码，可以查看语法分析/static/C文法2来查看
+ 词法分析主要是状态转换图和lex正则匹配，状态转换图写的很少，lex的话，大部分的token和错误能识别
+ 中间代码生成，目前只支持算式表达式、for、while、if、简单的bool表达式（a>b这种）。可以进行嵌套。
+ NFA、DNA、minDFA 三个已经实现完成。minDFA那点可能有点小问题但不是很严重。
+ 代码尽量严格加上空格，否则语法分析会报错

## 注意：可供参考之用但不允许使用我的代码拿来完成任务！！！
我的代码已经上传到学校保存了，查重出来就没了！！！
整体界面
### 词法分析
![image](https://user-images.githubusercontent.com/64669137/171987269-330223a1-23e5-455b-b2ea-b7147844f106.png)
### 语法树
![image](https://user-images.githubusercontent.com/64669137/171987298-0c1309b1-3827-4691-aa18-71021c381281.png)
### 中间代码
![image](https://user-images.githubusercontent.com/64669137/171987319-ab534f83-3bc3-41df-b832-65eaf18478b7.png)
### 目标代码
![image](https://user-images.githubusercontent.com/64669137/171987357-76ecc8c8-e335-4477-b6a6-2ec9bf0f8247.png)





