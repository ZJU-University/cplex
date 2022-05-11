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
Page 198
案例6-2: 斯德特兰运输公司（物流管理）

    雷切尔是斯德特兰运输公司南大西洋办公处的经理。目前，她正和一家名叫化聚的业用化学品制造公司谈判一份新的这输合同。化聚公司想让斯德特兰公司
负责将其6个工厂的废物装载并这送到3个垃圾处理点。雷切尔非常担心化聚公司的这项提议。这些需要运输的化学成物一旦泄漏将会给人类和环境造成极大危害。
此外，这6个工厂所在地区的一些城镇和社区禁止在它们所管辖的区城中运输危险物质。因此，不但要谨慎处理每次的输并减速行驶，而且在很多情况下必须绕道而行。
    雷切尔估计出了从每个工厂造输一桶废物到每个垃圾处理点的运输成本，如下表所示：
    
    JSBT: 金斯波特 
    DWE: 丹维尔
    MK: 美肯
    SRM: 塞尔玛
    GLB: 哥伦布
    YLD: 亚兰墩
    
    BS: 白水
    LSKL: 罗斯堪洛
    DLS: 杜拉斯
    
    垃圾处理点，(成本, 美元)
    +---------+----+------+-----+
    | factory | BS | LSKL | DLS |
    +---------+----+------+-----+
    |   JSBT  | 12 |  15  |  17 |
    |   DWE   | 14 |  9   |  10 |
    |    MK   | 13 |  20  |  11 |
    |   SEM   | 17 |  16  |  19 |
    |   GLB   | 7  |  14  |  12 |
    |   YLD   | 22 |  16  |  18 |
    +---------+----+------+-----+
    
    6个工厂每周的产生的废物量如下：
    +---------+-------------------------------+
    | factory | Weekly Waste Volume (barrels) |
    +---------+-------------------------------+
    |   JSBT  |               35              |
    |   DWE   |               26              |
    |    MK   |               42              |
    |   SEM   |               53              |
    |   GLB   |               29              |
    |   YLD   |               38              |
    +---------+-------------------------------+
    
    往于白水、罗斯塔洛和杜拉新的3个拉级处理点每周最多可容纳的废物量分别为65桶、80桶和105桶。
    除了考虑将废物从每个工厂直接运到每个垃圾处理点之外，雷切尔还考虑使用将每个工厂和垃圾处理点当作中间运输点的运输方法。汽车可将废物卸到某个工厂
或垃圾处理点，然后再由另一辆汽车将废物装载上并运到目的地，反之亦然。斯德特兰公司不承担任何处理成本，因为化聚公司已同意承担废物在工厂和垃圾处理点
的所有处理成本。或换句话说，斯德特兰公司将只承担实际运输成本。因此，雷切尔希望能够发现在中间点卸货或装货而不是直接运输货物从而使运输成本降低的可能性。
    雷切尔估计了6个工厂之间每桶废物的运输成本，如下表所示:
    
    工厂（成本，美元）
    +---------+------+-----+----+-----+-----+-----+
    | factory | JSBT | DWE | MK | SEM | GLB | YLD |
    +---------+------+-----+----+-----+-----+-----+
    |   JSBT  |  0   |  6  | 4  |  9  |  7  |  8  |
    |   DWE   |  6   |  0  | 11 |  10 |  12 |  7  |
    |    MK   |  5   |  11 | 0  |  3  |  7  |  15 |
    |   SEM   |  9   |  10 | 3  |  0  |  3  |  16 |
    |   GLB   |  7   |  12 | 7  |  3  |  0  |  14 |
    |   YLD   |  8   |  7  | 15 |  16 |  14 |  0  |
    +---------+------+-----+----+-----+-----+-----+
    
    三个垃圾处理点两两之间每桶废物的运输成本估计值如下：
    垃圾处理点(美元)
    +-----------------------+----+------+-----+
    | Refuse disposal point | BS | LSKL | DLS |
    +-----------------------+----+------+-----+
    |           BS          | 0  |  12  |  10 |
    |          LSKL         | 12 |  0   |  15 |
    |          DLS          | 10 |  15  |  0  |
    +-----------------------+----+------+-----+

    雷切尔希望确定使斯德特兰公司的总成本最小的运输路线，以制定一份有关垃圾处理的合同提议提交给化聚公司。她特别想知道是直接从工厂运到垃圾处理点
更便宜，还是在这些工厂和垃圾处理点卸下和装载一些废物更便宜。请建立一个模型帮雷切尔解决此问题，并求解该模型以确定最优路线。
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    factory_wastes = {
        'JSBT': 35, 'DWE': 26, 'MK': 42, 'SEM': 53, 'GLB': 29, 'YLD': 38,
    }  # 工厂产生的废物
    plant_capacities = {'BS': 65, 'LSKL': 80, 'DLS': 105}  # 处理厂最大处理能力
    transport_costs = {
        'JSBT': {'JSBT': 0, 'DWE': 6, 'MK': 4, 'SEM': 9, 'GLB': 7, 'YLD': 8, 'BS': 12, 'LSKL': 15, 'DLS': 17},
        'DWE': {'JSBT': 6, 'DWE': 0, 'MK': 11, 'SEM': 10, 'GLB': 12, 'YLD': 7, 'BS': 14, 'LSKL': 9, 'DLS': 10},
        'MK': {'JSBT': 5, 'DWE': 11, 'MK': 0, 'SEM': 3, 'GLB': 7, 'YLD': 15, 'BS': 13, 'LSKL': 20, 'DLS': 11},
        'SEM': {'JSBT': 9, 'DWE': 10, 'MK': 3, 'SEM': 0, 'GLB': 3, 'YLD': 16, 'BS': 17, 'LSKL': 16, 'DLS': 19},
        'GLB': {'JSBT': 7, 'DWE': 12, 'MK': 7, 'SEM': 3, 'GLB': 0, 'YLD': 14, 'BS': 7, 'LSKL': 14, 'DLS': 12},
        'YLD': {'JSBT': 8, 'DWE': 7, 'MK': 15, 'SEM': 16, 'GLB': 14, 'YLD': 0, 'BS': 22, 'LSKL': 16, 'DLS': 18},
        'BS': {'BS': 0, 'LSKL': 12, 'DLS': 10},
        'LSKL': {'BS': 12, 'LSKL': 0, 'DLS': 15},
        'DLS': {'BS': 10, 'LSKL': 15, 'DLS': 0},
    }  # 运输成本

    var_names = [
        f'{from_situation}_{to_situation}'
        for from_situation in transport_costs for to_situation in transport_costs[from_situation]
        if from_situation != to_situation
    ]

    lbs = np.zeros(len(var_names))  # 下界
    ubs = [cplex.infinity] * len(var_names)  # 上界
    var_types = 'I' * len(var_names)  # 数据类型

    # 目标函数
    objective = []
    for var_name in var_names:
        objective.append(transport_costs[var_name.split('_')[0]][var_name.split('_')[1]])

    # 约束条件
    constraints_lefts = []  # 约束条件左边
    constraints_senses = ''  # 约束条件场景
    constraints_rights = []  # 约束条件右边

    # 不能超过处理厂最大处理能力
    for plant in plant_capacities:
        _constraint = []
        __constraint = []
        for var_name in var_names:
            if var_name.split('_')[0] == plant:
                _constraint.append(var_name)
                __constraint.append(-1)
            elif var_name.split('_')[-1] == plant:
                _constraint.append(var_name)
                __constraint.append(1)
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'L'
        constraints_rights.append(plant_capacities[plant])

    # 工厂需要运输出去的废物等于工厂产生的废物
    for factory in factory_wastes:
        _constraint = []
        __constraint = []
        for var_name in var_names:
            if var_name.split('_')[0] == factory:
                _constraint.append(var_name)
                __constraint.append(-1)
            elif var_name.split('_')[-1] == factory:
                _constraint.append(var_name)
                __constraint.append(1)
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'E'
        constraints_rights.append(-factory_wastes[factory])

    constraints_names = [f'c{i}' for i in range(len(constraints_lefts))]  # 约束规则名
    # for i in range(len(constraints_lefts)):
    #     print(i, constraints_lefts[i], constraints_senses[i], constraints_rights[i])

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
