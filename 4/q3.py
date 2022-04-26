#!/usr/bin/env python
# encoding: utf-8

# the number of class: 4
# class time: 2022-04-09
# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-04-26

from utils.general import LOGGER
import cplex
from cplex.exceptions import CplexError
import numpy as np

'''
Page 203
案例6-6: Tech的回馈周末（项⽬管理）

    
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

