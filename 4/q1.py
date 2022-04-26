#!/usr/bin/env python
# encoding: utf-8

# the number of class: 4
# class time: 2022-04-09
# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-04-26

from utils.general import LOGGER
import cplex
import numpy as np
from cplex.exceptions import CplexError

'''
Page 165
案例5-4: 联合⼴播⽹络的电视⼴告时段安排（销售计划）


'''

if __name__ == '__main__':
    cpx = cplex.Cplex()


