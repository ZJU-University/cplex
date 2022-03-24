#!/usr/bin/env python
# encoding: utf-8

# the number of class: 1
# class time: 2022-02-26
# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-03-24

from utils.general import LOGGER
import cplex
from cplex.exceptions import CplexError

'''
Page 56 
案例2-2 可能性餐厅
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    # 参数定义
    max_dinner = 60  # 最多正餐数
    fish_time = 0.25  # 鱼肉套餐时间 / h
    beef_time = 2 * fish_time  # 牛肉套餐时间 / h
    max_labour_time = 20  # 劳动力 / h
    fish_profit = 12  # 鱼肉套餐利润 / $
    beef_profit = 16  # 牛肉套餐利润 / $

    # 决策变量定义
    # 即 X1: 鱼肉套餐数量 & X2: 牛肉套餐数量
    var_names = ['fish_num', 'beef_num']
    lbs = [0, 0]  # 下界
    ubs = [60, 60]  # 上界
    var_types = 'II'  # 数据类型
    # 'C': 连续的; 'B': 二元的; 'I': 整型; 'N': 半整型; 'S': 半连续

    # 目标函数
    # Z = fish_profit * fish_num + beef_profit * beef_num
    objective = [fish_profit, beef_profit]

    # 约束条件
    """
    最多卖出 max_dinner 份: fish_num + beef_num  <= max_dinner
    最大工时 max_labour_time :  fish_time * fish_num + beef_time * beef_num <= max_labour_time
    每卖出2份牛肉, 至少卖出3份鱼肉:  beef_num / fish_num <= 2/3
        -> 3 * beef_num <= 2 * fish_num
        -> 3 * beef_num - 2 * fish_num <= 0
    至少 10% 的客户会选择牛肉套餐: beef_num / (beef_num + fish_num) >= 10%
        -> beef_num >= 0.1 * beef_num + 0.1 * fish_num
        -> 0.1 * fish_num - 0.9 * beef_num <= 0
    
    """
    constraints_lefts = [
        [['fish_num', 'beef_num'], [1.0, 1.0]],
        [['fish_num', 'beef_num'], [fish_time, beef_time]],
        [['fish_num', 'beef_num'], [-2, 3]],
        [['fish_num', 'beef_num'], [0.1, -0.9]],
    ]  # 约束条件左边
    constraints_senses = 'LLLL'  # 约束条件关系
    # G: >=; L: <=; E: =; R: ranged constraints
    constraints_rights = [
        max_dinner,
        max_labour_time,
        0,
        0
    ]  # 约束条件右边
    constraints_names = ['c1', 'c2', 'c3', 'c4']  # 约束规则名

    try:
        cpx.objective.set_sense(cpx.objective.sense.maximize)  # 求解目标: 最小值
        cpx.variables.add(
            obj=objective,
            lb=lbs,
            ub=ubs,
            types=var_types,
            names=var_names
        )  # 设置变量
        cpx.linear_constraints.add(
            lin_expr=constraints_lefts,
            senses=constraints_senses,
            rhs=constraints_rights,
            names=constraints_names
        )  # 添加约束

        cpx.solve()  # 问题求解
        x = cpx.solution.get_values()  # 最优情况下的变量值
        objective_value = cpx.solution.get_objective_value()  # 最优情况下的目标值

        for i, var_name in enumerate(var_names):
            LOGGER.info(f'最优自变量 {var_name}: {x[i]}')
        LOGGER.info(f'最优结果: {objective_value}')

    except CplexError as e:
        LOGGER.error(e)





