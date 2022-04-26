#!/usr/bin/env python
# encoding: utf-8

# the number of class: 3
# class time: 2022-03-26
# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-04-26

from utils.general import LOGGER
import cplex
import numpy as np
from cplex.exceptions import CplexError

'''
Page 127
Q48:                                                                                                                     
    潮水城市银行有4家分行，其输入和输出如下：
    
    输入1=柜员工时（单位：100小时）
    输入2=营业面积（单位：100平方英尺）
    输入3=费用（单位：1000美元）
    输出1=存取款和支票业务处理（单位：1000笔）
    输出2=贷款申请
    输出3=新账户开立（单位：100笔）
    
    每个分行每个月的输入和输出值如下：
    ------------------------------------------
    |     |       输出       |       输入      |
    | 分行 ------------------------------------
    |     |  1  |  2  |  3  |  1  |  2  |  3 |
    ------------------------------------------
    |  A  | 76  | 125 |  12 | 16  | 22 |  12 |
    |  B  | 82  | 105 |   8 | 12  | 19 |  10 |
    |  C  | 69  |  98 |   9 | 17  | 26 |  16 |
    |  D  | 72  | 117 |  14 | 14  | 18 |  14 |
    ------------------------------------------
    
    使用数据包络分析（DEA）评估哪家分行效率较差。

'''

if __name__ == '__main__':
    cpx = cplex.Cplex()



