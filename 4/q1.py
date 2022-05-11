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
from decimal import Decimal
import pandas as pd

'''
Page 165
案例5-4: 联合⼴播⽹络的电视⼴告时段安排（销售计划）
    联合广播网络(UBN)向广告客户销售自己电视节目中的商业广告时段。它在春季就会公布自己秋季的电视安排，随后开始向客户销售广告时段。
长期客户会给予优先购买广告时段的机会。新的秋季时段在9月的第3周开始。广告时段主要有15秒和30秒两种。公司制定了全年的详细销售计划，
主要是基于每月制、双月制、6周制或3月制。为了使广告能有效覆盖其营销的目标群体，广告客户一般会有一些较偏好的节目，同时他们也要考虑具体的
广告预算问题。UBN基于节目的收视率对广告时段进行收费，主要是由节目的受众人群种类和规模决定的。
    Nanocom是一家商业软件开发公司，公司希望这个秋季在几个节目中购买30秒和15秒的广告时段。Nanocom希望拥有年长、较成熟、高收入的观众群，
这类人群中可能包括从事高科技行业的商业人士。公司有广告预算600000美元，它已经通知UBN广告人员，它比较倾向购买广告时段的节目是: 
Bayside, NewsLine, The Hour, Cops and Lawyers. The Judge, Friday Night Football 和ER Doctor。NewsLine 和The Hour是
新闻类节目，其他的除了Friday Night Football 是专业的足球节目外，都是成人剧。Nanocom希望它购买的广告时段中至少有50%是节目NewsLine, 
The Hour和Friday Night Football中的。Nanocom希望UBN为自己制定一个从10月第3周开始到11月(自括整个11月)的为期6周的销售计划。
    UBN的销售计划是基于它不同节目的表现积分的。UBN和广告客户的主要目标是制作一份可以达到最高表现积分的计划。表现积分基于几个因素，
包括该节目与目标受众的吻合程度、该节目的观众密集度、该时间段的历史收视率、同时间段其他竞争性节目以及与之相关的节目的表现。UBN根据节目的表现积分
来为广告设定收费水平。表现积分和收费都乘以一个基于节目播放周的权重因素和这周的预期总观众，因为总观众会随的不同周而变化。下面的表格显示了成本、
表现积分和每个节目可出售的15秒和30秒商业广告的广告时段:

    program: 节目 
    time: 商业广告长度(秒)
    cost: 成本(1000美元)
    integration: 表现积分
    ava_time: 可用时段
    +-----------------------+------+------+-------------+----------+
    | program               | time | cost | integration | ava_time |
    +-----------------------+------+------+-------------+----------+
    | Bayside               | 30   | 50   | 115.2       | 3        |
    | Bayside               | 15   | 25   | 72          | 3        |
    | Newsline              | 30   | 41   | 160         | 4        |
    | Newsline              | 15   | 20.5 | 100         | 1        |
    | The Hour              | 30   | 36   | 57.6        | 3        |
    | The Hour              | 15   | 18   | 36          | 3        |
    | Cops and Lawyers      | 30   | 45   | 136         | 4        |
    | Cops and Lawyers      | 15   | 27.5 | 85          | 2        |
    | The Judge             | 30   | 52   | 100.8       | 2        |
    | The Judge             | 15   | 26   | 63          | 2        |
    | Friday Night Football | 30   | 25   | 60.8        | 4        |
    | Friday Night Football | 15   | 12.5 | 38          | 2        |
    | ER Docker             | 30   | 46   | 129.6       | 3        |
    | ER Docker             | 15   | 23   | 81          | 1        |
    +-----------------------+------+------+-------------+----------+
    
    UBN提出了一个Nanocom也同意的建议，即在6周的每一周都有广告时段的一个最大和最小数量，并且Nanocom在每周每个节目中最多只有一个广告时段
(15秒的或30秒的)。下面的表格显示的是每周的权重因素和每周广告时段的最大数量、最小数量。

    +--------+------+------+------+------+------+------+
    | week   | 10-3 | 10-4 | 11-1 | 11-2 | 11-3 | 11-4 |
    +--------+------+------+------+------+------+------+
    | weight | 1.1  | 1.2  | 1.2  | 1.4  | 1.4  | 1.6  |
    | min    | 1    | 1    | 2    | 2    | 2    | 3    |
    | max    | 4    | 5    | 5    | 5    | 5    | 5    |
    +--------+------+------+------+------+------+------+

    帮助UBN为Nanocom公司制定一个6周的销售计划来使总的表现积分最大化。
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    programs = {
        'Bayside': {
            '30': {'cost': 50, 'integration': 115.2, 'ava_time': 3},
            '15': {'cost': 25, 'integration': 72, 'ava_time': 3}
        },
        'NewsLine': {
            '30': {'cost': 41, 'integration': 160, 'ava_time': 4},
            '15': {'cost': 20.5, 'integration': 100, 'ava_time': 1}
        },
        'TheHour': {
            '30': {'cost': 36, 'integration': 57.6, 'ava_time': 3},
            '15': {'cost': 18, 'integration': 36, 'ava_time': 3}
        },
        'CopsAndLawyers': {
            '30': {'cost': 45, 'integration': 136, 'ava_time': 4},
            '15': {'cost': 27.5, 'integration': 85, 'ava_time': 2}
        },
        'TheJudge': {
            '30': {'cost': 52, 'integration': 100.8, 'ava_time': 2},
            '15': {'cost': 26, 'integration': 63, 'ava_time': 2}
        },
        'FridayNightFootball': {
            '30': {'cost': 25, 'integration': 60.8, 'ava_time': 4},
            '15': {'cost': 12.5, 'integration': 38, 'ava_time': 2}
        },
        'ERDocker': {
            '30': {'cost': 46, 'integration': 129.6, 'ava_time': 3},
            '15': {'cost': 23, 'integration': 81, 'ava_time': 1}
        },
    }
    weeks = {
        '103': {'weight': 1.1, 'range': (1, 4)},
        '104': {'weight': 1.2, 'range': (1, 5)},
        '111': {'weight': 1.2, 'range': (2, 5)},
        '112': {'weight': 1.4, 'range': (2, 5)},
        '113': {'weight': 1.4, 'range': (2, 5)},
        '114': {'weight': 1.6, 'range': (3, 5)},
    }  # 10月第三周 - 11月第四周

    total_cost = 600
    var_names = [f"{program}_{i}_{week}" for program in programs for i in programs[program] for week in weeks]

    # 要么选择, 要么不选择
    lbs = np.zeros(len(var_names))  # 下界
    ubs = np.ones(len(var_names))  # 上界
    var_types = 'I' * len(var_names)  # 数据类型

    # 约束条件
    constraints_lefts = []  # 约束条件左边
    constraints_senses = ''  # 约束条件场景
    constraints_rights = []  # 约束条件右边

    # 目标函数
    objective = [
        float(
            Decimal(str(programs[var_name.split('_')[0]][var_name.split('_')[1]]['integration'])) *
            Decimal(str(weeks[var_name.split('_')[-1]]['weight']))
        )
        for var_name in var_names
    ]  # 表现积分最高

    # 每周每个节目中最多治选择一个, 30s or 15s
    for week in weeks:
        for program in programs:
            _constraint = []
            for var_name in var_names:
                if var_name.split('_')[0] == program and var_name.split('_')[-1] == week:
                    _constraint.append(var_name)
            constraints_lefts.append([_constraint, [1] * len(_constraint)])
            constraints_senses += 'L'
            constraints_rights.append(1)

    # 时间段符合要求
    for week in weeks:
        _constraint = []
        __constraint = []
        for var_name in var_names:
            if var_name.split('_')[-1] == week:
                _constraint.append(var_name)
                __constraint.append(programs[var_name.split('_')[0]][var_name.split('_')[1]]['ava_time'])
        # 大于最小值
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'G'
        constraints_rights.append(min(weeks[week]['range']))
        # 小于最大值
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'L'
        constraints_rights.append(max(weeks[week]['range']))

    # 费用符合要求
    _constraint = []
    __constraint = []
    for var_name in var_names:
        _constraint.append(var_name)
        __constraint.append(
            float(
                Decimal(str(programs[var_name.split('_')[0]][var_name.split('_')[1]]['cost'])) *
                Decimal(str(weeks[var_name.split('_')[-1]]['weight']))
            )
        )
    constraints_lefts.append([_constraint, __constraint])
    constraints_senses += 'L'
    constraints_rights.append(total_cost)

    # 占比 超过 50%
    _constraint = []
    __constraint = []
    for var_name in var_names:
        _constraint.append(var_name)
        if var_name.split('_')[0] in ['NewsLine', 'TheHour', 'FridayNightFootball']:
            __constraint.append(int(var_name.split('_')[1]))
        else:
            __constraint.append(-int(var_name.split('_')[1]))
    constraints_lefts.append([_constraint, __constraint])
    constraints_senses += 'G'
    constraints_rights.append(0)

    constraints_names = [f'c{i}' for i in range(len(constraints_lefts))]  # 约束规则名
    # for i in range(len(constraints_lefts)):
    #     print(i, constraints_lefts[i], constraints_senses[i], constraints_rights[i])

    try:
        cpx.objective.set_sense(cpx.objective.sense.maximize)  # 求解目标: 最大值
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
