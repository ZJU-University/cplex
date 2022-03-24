#!/usr/bin/env python
# encoding: utf-8

# the number of class: 1
# class time: 2022-02-26
# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-03-24

from utils.general import LOGGER
import cplex
from cplex.exceptions import CplexError
from cplex._internal._constants import CPX_MINBOUND

'''
Page 55～56 
案例2-1 大都市警察巡逻
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    # 参数定义
    perimeter = (5, 12)  # 周长范围
    avg_dis_den = 3  # 平均巡逻距离分母
    x_v = 20  # 水平方向行驶速度
    y_v = 15  # 垂直方向行驶速度
    avg_v = (x_v + y_v) / 2
    min_yx_rt = 0.5  # 垂直方向最少比水平方向多的比率

    # 决策变量定义
    # 即 X1: 水平距离 & X2: 垂直距离
    var_names = ['coordinate_x', 'coordinate_y']
    # >>> 界限可以加在约束条件中 >>>
    # because 2*(x+(1+min_yx_rt)*x)<=max(perimeter)
    # because min(perimeter)<=2*y<=max(perimeter)
    lbs = [CPX_MINBOUND, min(perimeter)/2]  # 下界
    ubs = [max(perimeter)/((min_yx_rt+1+1)*2), max(perimeter)/2]  # 上界
    # <<< 界限可以加在约束条件中 <<<
    var_types = 'CC'  # 数据类型
    # 'C': 连续的; 'B': 二元的; 'I': 整型; 'N': 半整型; 'S': 半连续

    # 目标函数
    # Z = ( 1 / avg_dis_den * coordinate_x + 1 / avg_dis_den * coordinate_y ) / ( x_v + y_v )
    objective = [1/avg_dis_den/(x_v + y_v), 1/avg_dis_den/(x_v + y_v)]

    # 约束条件
    """
    周长范围: 5 <= 2(coordinate_x + coordinate_x) <= 12 
    垂直方向至少比水平方向的距离多 50%: y >= (1+min_yx_rt)x => 1.5x - y <=0
    """
    constraints_lefts = [
        [['coordinate_x', 'coordinate_y'], [2.0, 2.0]],
        [['coordinate_x', 'coordinate_y'], [2.0, 2.0]],
        [['coordinate_x', 'coordinate_y'], [1+min_yx_rt, -1]],
    ]  # 约束条件左边
    constraints_senses = 'GLL'  # 约束条件关系
    # G: >=; L: <=; E: =; R: ranged constraints
    constraints_rights = [
        min(perimeter),
        max(perimeter),
        0
    ]  # 约束条件右边
    constraints_names = ['c1', 'c2', 'c3']  # 约束规则名

    try:
        cpx.objective.set_sense(cpx.objective.sense.minimize)  # 求解目标: 最小值
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





