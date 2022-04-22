#!/usr/bin/env python
# encoding: utf-8

# the number of class: 2
# class time: 2022-03-12
# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-04-07

from utils.general import LOGGER
import cplex
import numpy as np
from cplex.exceptions import CplexError

'''
Page 128
Q62: 
    蓝山电力和照明公司在位于美国东海岸的弗吉尼亚州、北卡罗来纳州、马里兰州和特拉华州的4个火力发电厂发电。公司从弗吉尼亚西南部、南部和肯塔基的
6个生产厂商处购买煤炭。蓝山和以下3个生产商有供煤的固定合同。
    
    安科: AK      布恩小溪: BN      世纪: SJ
    ------------------------------------------------------------
    | 煤炭生产商 |    吨    |   每吨成本(美元)   ｜   每吨百万 BTU   |
    ------------------------------------------------------------
    |    AK    |  190000  |        23        |      26.2       |
    |    BN    |  305000  |        28        |      27.1       |
    |    SJ    |  310000  |        24        |      25.6       |
    ------------------------------------------------------------

    这些生产商生产的煤炭的发电能力因为煤炭的质量而有所不同。例如：安科生产的煤炭每吨可以产生26.2百万BTU的热量，而布恩小溪生产的煤炭每吨可以
产生27.1百万BTU的热量。蓝山也从3家后备生产商按需购买煤炭(与这些生产商没有固定合同)。通常情况下，这些生产商提供的煤炭质次价高:

    戴克: DK      伊顿: YD      富兰克林: FK
    ------------------------------------------------------------
    | 煤炭生产商 |    吨    |   每吨成本(美元)   ｜   每吨百万 BTU   |
    ------------------------------------------------------------
    |    DK    |  125000  |        31        |      21.4       |
    |    YD    |   95000  |        29        |      19.2       |
    |    FK    |  190000  |        34        |      23.6       |
    ------------------------------------------------------------

    蓝山4家工厂的供电需求如下所示(注意，大约需要1000万BTU产生100万瓦.小时的电量):

    亚峰: 1      萨日: 2      皮德蒙特: 3      切萨皮克: 4 
    ----------------------------------
    | 发电厂 |    供电需求量(百万BTU)    |
    ----------------------------------
    |   1   |       4600000          |
    |   2   |       6100000          |
    |   3   |       5700000          |
    |   4   |       7300000          |
    ---------------------------------- 

    例如: 亚峰发电厂明年至少需要生产4600000百万BTU，大约460000百万瓦.小时的电量。
    煤炭首先通过铁路从生产厂家运到发电厂，每个发电厂处理煤炭的成本是不同的。下表显示了从每个生产商向每个发电厂供应煤炭的运输和处理成本的总和。

    亚峰: 1      萨日: 2      皮德蒙特: 3      切萨皮克: 4 
    安科: AK      布恩小溪: BN      世纪: SJ
    戴克: DK      伊顿: YD      富兰克林: FK
    ----------------------------------------------------
    | 煤炭生产商 |               发电厂(美元)             |
    | 煤炭生产商 |----------------------------------------
    | 煤炭生产商 |    1    |    2    |    3    |    4    |
    ----------------------------------------------------
    |    AK    |  12.20  |  14.25  |  11.15  |  15.00  |
    |    BN    |  10.75  |  13.70  |  11.75  |  14.45  |
    |    SJ    |  15.10  |  16.65  |  12.90  |  12.00  |
    |    DK    |  14.30  |  11.90  |  16.35  |  11.65  |
    |    YD    |  12.65  |   9.35  |  10.20  |   9.55  |
    |    FK    |  16.45  |  14.75  |  13.80  |  14.90  |
    ----------------------------------------------------
    
    建立并求解线性规划模型，计算从每个煤炭生产商到每个发电厂需要运送多少吨煤以使成本最小。

'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    # 参数定义
    # 所需电量
    power_stations = {
        1: {  # 亚峰
            'ele': 4600000,
            'ak': 12.20, 'bn': 10.75, 'sj': 15.10, 'dk': 14.30, 'yd': 12.65, 'fk': 16.45  # 处理费用
        },
        2: {  # 萨日
            'ele': 6100000,
            'ak': 14.25, 'bn': 13.70, 'sj': 16.65, 'dk': 11.90, 'yd': 9.35, 'fk': 14.75
        },
        3: {  # 皮德蒙特
            'ele': 5700000,
            'ak': 11.15, 'bn': 11.75, 'sj': 12.90, 'dk': 16.35, 'yd': 10.20, 'fk': 13.80
        },
        4: {  # 切萨皮克
            'ele': 7300000,
            'ak': 15.00, 'bn': 14.45, 'sj': 12.00, 'dk': 11.65, 'yd': 9.55, 'fk': 14.90
        }
    }

    providers = {
        'ak': {
            'total': 190000,
            'price': 23,
            'btu': 26.2
        },
        'bn': {
            'total': 305000,
            'price': 28,
            'btu': 27.1
        },
        'sj': {
            'total': 310000,
            'price': 24,
            'btu': 25.6
        },
        'dk': {
            'total': 125000,
            'price': 31,
            'btu': 21.4
        },
        'yd': {
            'total': 95000,
            'price': 29,
            'btu': 19.2
        },
        'fk': {
            'total': 190000,
            'price': 34,
            'btu': 23.6
        }
    }

    # 决策变量定义
    var_names = [f'{power_station}_from_{provider}' for provider in providers for power_station in power_stations]
    lbs = np.zeros(len(var_names))  # 下界
    ubs = [providers[var_name.split('_')[-1]]['total'] for var_name in var_names]  # 上界
    var_types = 'I' * len(var_names)  # 数据类型
    # 'C': 连续的; 'B': 二元的; 'I': 整型; 'N': 半整型; 'S': 半连续

    # 目标函数
    objective_1 = [providers[var_name.split('_')[-1]]['price'] for var_name in var_names]  # 购买煤的费用
    objective_2 = [power_stations[int(var_name.split('_')[0])][var_name.split('_')[-1]] for var_name in var_names]  # 处理费用
    objective = []
    for i, value in enumerate(objective_1):
        objective.append(objective_1[i] + objective_2[i])

    # 约束条件
    constraints_lefts = []  # 约束条件左边
    constraints_rights = []  # 约束条件右边
    num = 0
    for provider in providers:  # 总量限制
        _constraint = []
        for var_name in var_names:
            if var_name.split('_')[-1] == provider:
                _constraint.append(var_name)
        constraint = [_constraint, np.ones(len(_constraint))]
        constraints_lefts.append(constraint)
        constraints_rights.append(providers[provider]['total'])
        num += 1
    constraints_senses = 'L' * num  # 约束条件关系
    # G: >=; L: <=; E: =; R: ranged constraints

    num = 0
    for power_station in power_stations:  # 电量限制
        _constraint = []
        __constraint = []
        for var_name in var_names:
            if int(var_name.split('_')[0]) == power_station:
                _constraint.append(var_name)
        for _ in _constraint:
            __constraint.append(providers[_.split('_')[-1]]['btu'])
        constraint = [_constraint, __constraint]
        constraints_lefts.append(constraint)
        constraints_rights.append(power_stations[power_station]['ele'])
        num += 1
    constraints_senses = constraints_senses + 'G' * num  # 约束条件关系
    constraints_names = [f'c{i}' for i in range(len(constraints_lefts))]  # 约束规则名

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

