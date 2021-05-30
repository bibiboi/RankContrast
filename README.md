# RankContrast

1.序列比较算法（全局序列比对及局部序列比对的python实现）

# 前言

阶段性地完成了DNA序列比较算法，还有很多不足和需要完善的地方有待日后改进。

## 算法思想介绍

[一个很详细完整的算法介绍](https://blog.csdn.net/weixin_43202635/article/details/82962032?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522160180045119195188342555%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=160180045119195188342555&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v28-1-82962032.pc_first_rank_v2_rank_v28&utm_term=%E5%BA%8F%E5%88%97%E6%AF%94%E5%AF%B9&spm=1018.2118.3001.4187)

***双序列全局比对及算法***
Needleman-Wunsch 算法：动态规划法
输入值：两条序列、替换记分矩阵以确定不同字母间的相似度得分，以及空位罚分

![全局比对计算公式](https://img-blog.csdnimg.cn/20201005020542766.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)

***双序列局部比对算法***
局部比对的计算公式在全局比对的基础上增加了第四个元素“0”。得分矩阵初始值仍是0，但第一行和第一列与全局比对不同，全是0。

![局部比对计算公式](https://img-blog.csdnimg.cn/20201005020631989.png#pic_center)

## 实现功能及实现方法

 1. 使用已定义的记分矩阵
 ![替换记分矩阵](https://img-blog.csdnimg.cn/2020100502071291.png#pic_center)
 2. 设置需比对的序列、gap大小及要进行的比对选择
 3. 打印最高得分的序列比对结果
 *方法：倒序查找最终路进行序列比对*
 4. 打印得分矩阵及比对路径
 *方法：使用递归和栈记录最终路径*

## 运行结果演示

 - 双序列全局比对
 
	 输入序列：atcggtac；aatcgta
   
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201005033414557.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
   
输入序列：atcggt；aacg

![全局比对](https://img-blog.csdnimg.cn/20201005022555153.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
 
 - 双序列局部比对
 
 输入序列：atccga；tcga
 
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201005033712855.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)
 
输入序列：acgtc；cg

 ![局部比对](https://img-blog.csdnimg.cn/20201005022651355.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpYmliaWJpYm9p,size_16,color_FFFFFF,t_70#pic_center)






## 遇到的问题及总结

 1. 思维误区： 最初在存储最终路径的问题上，认为在每次路径递归至初始结点时才将其入栈，导致遇到分岔路则无法记录前一条路的完整路径
 经过高人指点后解决：每次到达一个结点就将其入栈，递归结束后将其出栈
 2. 思维误区2：最初以采用存储每个点的前一点坐标为存储方式，导致所有得分矩阵只能存储一条路径
 再次经过高人指点后解决：改存储方式为存储每个点计算得来的方向

 
 4. 递归终止条件存储最终路径 -涉及问题：list的赋值、浅拷贝、深拷贝
 [Python List的赋值方法](https://blog.csdn.net/lovelyaiq/article/details/55102518)
 
 
 5. 画出路径矩阵表格 -涉及问题：表格与画布大小不一致且导致无法确定箭头坐标 
解决方式：使用bbox参数
 5. 获取得分矩阵中最大值的索引 - 涉及问题：获取where结果的索引值 
 6. 局部比对递归终止条件 - 涉及问题：列表比较 any() all()
 
 **总结**
 
 这次的作业因为拖延很晚才开始，遇到的问题也绝不仅仅只有以上几个，最深刻的还是最开始的思维误区，直接卡到崩溃，但其他问题也都耗费了或多或少的时间才解决，更有无数小问题调试了无数遍才得以做出这个半成品。其实还有很多待完善的地方，比如输入的字符判断，比如一致度和相似度的计算，比如图形化界面的编写，写出来的代码也还有很多不成熟的地方，但是因为时间问题，暂时就到这了，有时间再改进咯。
 
