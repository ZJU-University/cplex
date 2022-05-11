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
import pandas as pd

'''
Page 203
案例6-6: Tech的回馈周末（项⽬管理）
    Tech学生会(SGA)每年春天都组织一个名为“回馈周末”的活动。SGA要求学生组队在4月份连续4个星期六为大学社区的居民开展项目工作。
学生团队一般由3~5名学生组成，来自各个宿舍、兄弟会、姐妹会、学生俱乐部和组织。SGA通过居民在城镇水电费账单上以及报纸广告和互联网网站上填写的表格选择项目。
居民简要填写了他们想要完成的项目的表格，主要是院子清理工作，另外还有窗户清洗、绘画，把不需要的物品拖到Goodwill或垃圾场等杂项工作。一旦表格被提交，
SGA的协调员与团队组长一起到居民家中评估所涉及的项目，团队组长提供他们团队完成该项目所需时间的估计。大部分项目都涉及体力劳动，因为团员的数量、
团队的技能以及团队的实际构成不同，完成项目的时间将因团队而异。以下是6支队伍提交的第一个周六的12个项目的时间估计(小时)。

    +------+------+------+------+------+------+------+------+------+------+------+------+------+
    | team | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   |
    +------+------+------+------+------+------+------+------+------+------+------+------+------+
    | A    | 5    | 1.5  | 6    | 4    | 3.5  | 3    | 6    | 1.5  | 5    | 1    | 3    | 3.5  |
    | B    | 4    | 2    | 5    | 5    | 3    | 3    | 5.5  | 2    | 4    | 1.5  | 4    | 2.5  |
    | C    | 5    | 1.5  | 6.5  | 3.5  | 2.5  | 4    | 4.5  | 3    | 3.5  | 1    | 3.5  | 4    |
    | D    | 3.5  | 2    | 5.5  | 4    | 3.5  | 2.5  | 5    | 2.5  | 4    | 1.5  | 2.5  | 4    |
    | E    | 3.5  | 3    | 5    | 3    | 2    | 4    | 5    | 2    | 5    | 2    | 4    | 3    |
    | F    | 4    | 2.5  | 6    | 5    | 3    | 3    | 6    | 3    | 3    | 2    | 3    | 3.5  |
    +------+------+------+------+------+------+------+------+------+------+------+------+------+
    
    SGA的主要目标是在可能的情况下完成所有12个项目，每个团队可以参与多个项目但不能工作超过8小时。SGA希望每个团队至少参与一个项目。
    a.确定最佳的项目分配，以使完成的项目数量最大化。
    b.如果SGA希望完成所有12个项目，同时使所有6个团队所需的总时间最小化，请确定项目团队的分配。
    如果有的话，两种解决方案之间的区别是什么?每个团队的平均工作时间是多少?
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    # 问题 a or b
    question = 'a'

    teams = {
        'A': {
            '1': 5, '2': 1.5, '3': 6, '4': 4, '5': 3.5, '6': 3,
            '7': 6, '8': 1.5, '9': 5, '10': 1, '11': 3, '12': 3.5
        },
        'B': {
            '1': 4, '2': 2, '3': 5, '4': 5, '5': 3, '6': 3,
            '7': 5.5, '8': 2, '9': 4, '10': 1.5, '11': 4, '12': 2.5
        },
        'C': {
            '1': 5, '2': 1.5, '3': 6.5, '4': 3.5, '5': 2.5, '6': 4,
            '7': 4.5, '8': 3, '9': 3.5, '10': 1, '11': 3.5, '12': 4
        },
        'D': {
            '1': 3.5, '2': 2, '3': 5.5, '4': 4, '5': 3.5, '6': 2.5,
            '7': 5, '8': 2.5, '9': 4, '10': 1.5, '11': 2.5, '12': 4
        },
        'E': {
            '1': 3.5, '2': 3, '3': 5, '4': 3, '5': 2, '6': 4,
            '7': 5, '8': 2, '9': 5, '10': 2, '11': 4, '12': 3
        },
        'F': {
            '1': 4, '2': 2.5, '3': 6, '4': 5, '5': 3, '6': 3,
            '7': 6, '8': 3, '9': 3, '10': 2, '11': 3, '12': 3.5
        },
    }

    var_names = [f'{team}_{work}' for team in teams for work in teams[team]]

    # 要么选择, 要么不选择
    lbs = np.zeros(len(var_names))  # 下界
    ubs = np.ones(len(var_names))  # 上界
    var_types = 'I' * len(var_names)  # 数据类型

    # 约束条件
    constraints_lefts = []  # 约束条件左边
    constraints_senses = ''  # 约束条件场景
    constraints_rights = []  # 约束条件右边

    # 每个团队至少参加一个项目
    for team in teams:
        _constraint = []
        __constraint = []
        for var_name in var_names:
            if var_name.split('_')[0] == team:
                _constraint.append(var_name)
                __constraint.append(1)
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'G'
        constraints_rights.append(1)

    # 每个团队的工作时间不能超过8个小时
    for team in teams:
        _constraint = []
        __constraint = []
        for var_name in var_names:
            if var_name.split('_')[0] == team:
                _constraint.append(var_name)
                __constraint.append(teams[team][var_name.split('_')[-1]])
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'L'
        constraints_rights.append(8)

    # 每个项目至少被选择一次
    for work in range(1, 13):
        _constraint = []
        __constraint = []
        for var_name in var_names:
            if var_name.split('_')[-1] == str(work):
                _constraint.append(var_name)
                __constraint.append(1)
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'G'
        constraints_rights.append(1)

    if question == 'a':
        # 确定最佳的项目分配，以使完成的项目数量最大化
        objective = np.ones(len(var_names))  # 完成项目的数量
        cpx.objective.set_sense(cpx.objective.sense.maximize)  # 求解目标: 最大值
    elif question == 'b':
        # 如果SGA希望完成所有12个项目，同时使所有6个团队所需的总时间最小化，请确定项目团队的分配
        objective = [teams[var_name.split('_')[0]][var_name.split('_')[-1]]for var_name in var_names]  # 完成项目的总时间
        cpx.objective.set_sense(cpx.objective.sense.minimize)  # 求解目标: 最小值

    constraints_names = [f'c{i}' for i in range(len(constraints_lefts))]  # 约束规则名

    try:
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

        df = pd.DataFrame(columns=[
                'var_names', 'objective_value'
            ])
        for i, var_name in enumerate(var_names):
            if x[i] != 0:
                df.loc[i] = [var_name, x[i]]
        LOGGER.info(f'All variables\n{df}')
        LOGGER.info(f'Best result: {objective_value}')

    except CplexError as e:
        LOGGER.error(e)
