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
import pandas as pd

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

    # 创建dataframe
    data = [
        [76, 125, 12, 16, 22, 12],
        [82, 105, 8, 12, 19, 10],
        [69, 98, 9, 17, 26, 16],
        [72, 117, 14, 14, 18, 14]
    ]
    column_nm = [f'{tp}_{i}' for tp in ['output', 'input'] for i in range(1, 4)]
    idx = ['A', 'B', 'C', 'D']
    df = pd.DataFrame(data=data, index=idx, columns=column_nm)

    # 判断四家的是否处于效率前沿
    var_names = column_nm
    lbs = np.zeros(len(var_names))  # 下界
    ubs = [cplex.infinity] * len(var_names)  # 上界
    var_types = 'C' * len(var_names)  # 数据类型

    # 约束条件
    constraints_lefts = []  # 约束条件左边
    constraints_senses = ''  # 约束条件场景
    constraints_rights = []  # 约束条件右边

    # out - in <= 0
    _constraint = [var_name for var_name in var_names]
    for bank in df.index:
        __constraint = []
        for _ in _constraint:
            if 'output' in _:
                __constraint.append(float(df.loc[bank, _]))
            else:
                __constraint.append(-float(df.loc[bank, _]))

        # 约束条件
        constraints_lefts.append([_constraint, __constraint])
        constraints_senses += 'L'
        constraints_rights.append(0)

    # 求解
    df_result = pd.DataFrame(columns=['value'])
    for bank in df.index:
        if len(constraints_senses) > 4:
            constraints_lefts = constraints_lefts[:-1]
            constraints_senses = constraints_senses[:-1]
            constraints_rights = constraints_rights[:-1]

        # 单个银行归一化
        _constraint = [var_name for var_name in var_names if 'input' in var_name]
        __constraint = [float(df.loc[bank, '_'.join(_.split('_')[-2:])]) for _ in _constraint]

        # 约束条件
        constraints_lefts.append([_constraint.copy(), __constraint.copy()])
        constraints_senses += 'E'
        constraints_rights.append(1)

        # 目标函数
        objective = []
        for var_name in var_names:
            if 'output' in var_name:
                objective.append(float(df.loc[bank, '_'.join(var_name.split('_')[-2:])]))
            else:
                objective.append(0)
        constraints_names = [f'c{i}' for i in range(len(constraints_lefts))]  # 约束规则名

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

            # 获取结果
            df_result.loc[bank, 'value'] = objective_value

        except CplexError as e:
            LOGGER.error(e)

    df_result['value'] = (df_result['value'] - df_result['value'].shift(periods=1, axis=0, fill_value=0))
    LOGGER.info(f'result\n {df_result}')