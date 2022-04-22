#!/usr/bin/env python
# encoding: utf-8

# the number of class: 2
# class time: 2022-03-12
# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-04-07

from utils.general import LOGGER
import cplex
from cplex.exceptions import CplexError
import numpy as np

'''
Page 132
案例4-2: 泉水园艺工具  
    泉水家族从1952年开始经营一家园艺工具和设备制造公司。公司把园艺工具销售给分销商，同时也会直接出售给工具商店和家庭用品折扣连锁店。
    泉水公司最著名的4种小型园艺工具是泥刀、锄头、耙子和铁铲。每种工具由优质钢材和木柄组成。泉水家族以他们高质量的工具为傲。
    加工过程包括两步。第一步包括两道工序，冲压出金属工具头并钻出螺丝孔。完整的工具头将进入第二部，包括组装程序，在这里木柄和工具头会被组装在
一起，然后是完工和包装程序，下面的表格显示了每种工具每道工序的加工时间。

    泥刀: trowel      锄头: hoe      耙子: rake      铁铲: shovel
    --------------------------------------------------------------
    | 工序 |               工具(小时/单位)       |  每月可用时间(小时) |
    | 工序 |-----------------------------------|  每月可用时间(小时) |
    | 工序 | trowel |  hoe   |  rake  | shovel |  每月可用时间(小时) |
    --------------------------------------------------------------
    | 冲压 |  0.04  |  0.17  |  0.06  |  0.12  |       500        |
    | 钻孔 |  0.05  |  0.14  |   --   |  0.14  |       400        |
    --------------------------------------------------------------
    | 组装 |  0.06  |  0.13  |  0.05  |  0.10  |       600        |
    | 完工 |  0.05  |  0.21  |  0.02  |  0.10  |       550        |
    | 包装 |  0.03  |  0.15  |  0.04  |  0.15  |       500        |
    --------------------------------------------------------------

    公司使用的钢材由日本的一家钢铁厂提供。厂家每个月可提供10000平方英尺的铁片。每种工具需要的钢材以及每种工具的月合同销售量如下表所示：    
    泥刀: trowel      锄头: hoe      耙子: rake      铁铲: shovel
    --------------------------------------
    |          | 铁片(平方英尺) | 月合同销量 |
    --------------------------------------
    |  trowel  |      1.2     |   1800   |
    |  hoe     |      1.6     |   1400   |
    |  rake    |      2.1     |   1600   |
    |  shovel  |      2.4     |   1800   |
    --------------------------------------

    公司可以一直生存和繁荣的首要原因是，总可以按时满足顾客的需求和生产高质量的产品。因此，公司会采取加班生产的方式以满足销售需求，同时公司与
当地的工具和模具公司有长期的合同生产工具头。公司愿意把第一步加工过程外包，因为这样在组装和完工之前进行质检比较容易。基于同样的原因，公司不会外包
整个工具，因为工具完工和包装之后不容易进行质检。公司每个月有100小时的加班时长，可用于每个加工过程的每道工序。
    每种工具的两个加工过程的常规和加班生产成本如下表所示：

    泥刀: trowel      锄头: hoe      耙子: rake      铁铲: shovel
    -------------------------------------------------------------------------------------
    |          |              加工过程1              |              加工过程2              |
    |          --------------------------------------------------------------------------
    |          | 常规成产成本(美元) | 加班成产成本(美元) | 常规成产成本(美元) | 加班成产成本(美元) |
    -------------------------------------------------------------------------------------
    |  trowel  |       6.00      |       6.20      |       3.00      |       3.10      |
    |  hoe     |      10.00      |      10.70      |       5.00      |       5.40      |
    |  rake    |       8.00      |       8.50      |       4.00      |       4.30      |
    |  shovel  |      10.00      |      10.70      |       5.00      |       5.40      |
    -------------------------------------------------------------------------------------
    
    外包加工过程I的成本比常规生产成本多20%
    泉水公司想制定一个生产计划，包括每个加工过程的常规和加班生产计划，以及外包的工具头数量，以使生产成本最低。为这个问题建立一个线性规划模型
并用计算机求解。
    
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    # 参数定义
    # 产品
    products = {
        'trowel': {
            'fe': 1.2,  # 铁皮
            'sale': 1800,  # 合同
            'process_cy': 0.04,  # 冲压
            'process_zk': 0.05,  # 钻孔
            'process_zz': 0.06,  # 组装
            'process_wg': 0.05,  # 完工
            'process_bz': 0.03,  # 包装
        },
        'hoe':  {
            'fe': 1.6,
            'sale': 1400,
            'process_cy': 0.17,
            'process_zk': 0.13,
            'process_zz': 0.13,
            'process_wg': 0.21,
            'process_bz': 0.15,
        },
        'rake': {
            'fe': 2.1,
            'sale': 1600,
            'process_cy': 0.06,
            'process_zk': 0,
            'process_zz': 0.05,
            'process_wg': 0.02,
            'process_bz': 0.04,
        },
        'shovel': {
            'fe': 2.4,
            'sale': 1800,
            'process_cy': 0.12,
            'process_zk': 0.14,
            'process_zz': 0.10,
            'process_wg': 0.10,
            'process_bz': 0.15,
        },
    }

    processes = {
        'cy': {
            'time': 500,
            'trowel': {
                'normal': 6,
                'plus': 6.2,
            },
            'hoe': {
                'normal': 10,
                'plus': 10.7,
            },
            'rake': {
                'normal': 8,
                'plus': 8.5,
            },
            'shovel': {
                'normal': 10,
                'plus': 10.7,
            },
        },
        'zk': {
            'time': 400,
            'trowel': {
                'normal': 6,
                'plus': 6.2,
            },
            'hoe': {
                'normal': 10,
                'plus': 10.7,
            },
            'rake': {
                'normal': 8,
                'plus': 8.5,
            },
            'shovel': {
                'normal': 10,
                'plus': 10.7,
            },
        },
        'zz': {
            'time': 600,
            'trowel': {
                'normal': 3,
                'plus': 3.1,
            },
            'hoe': {
                'normal': 5,
                'plus': 5.4,
            },
            'rake': {
                'normal': 4,
                'plus': 4.3,
            },
            'shovel': {
                'normal': 5,
                'plus': 5.4,
            },
        },
        'wg': {
            'time': 550,
            'trowel': {
                'normal': 3,
                'plus': 3.1,
            },
            'hoe': {
                'normal': 5,
                'plus': 5.4,
            },
            'rake': {
                'normal': 4,
                'plus': 4.3,
            },
            'shovel': {
                'normal': 5,
                'plus': 5.4,
            },
        },
        'bz': {
            'time': 500,
            'trowel': {
                'normal': 3,
                'plus': 3.1,
            },
            'hoe': {
                'normal': 5,
                'plus': 5.4,
            },
            'rake': {
                'normal': 4,
                'plus': 4.3,
            },
            'shovel': {
                'normal': 5,
                'plus': 5.4,
            },
        },
    }

    work_stats = ['normal', 'plus']
    sans = ['yes', 'no']
    # 决策变量定义
    var_names = []
    for work_stat in work_stats:
        for process in processes:
            for product in products:
                if process in ['cy', 'zk']:
                    for san in sans:
                        if work_stat != 'plus':
                            var_names.append(f'{work_stat}_{process}_{product}_{san}')
                        else:
                            if f'{work_stat}_{process}_{product}_no' not in var_names:
                                var_names.append(f'{work_stat}_{process}_{product}_no')
                else:
                    var_names.append(f'{work_stat}_{process}_{product}_no')
    print(var_names)
    lbs = np.zeros(len(var_names))  # 下界
    ubs = []
    for var_name in var_names:
        if var_name.split('_')[0] == 'normal':
            if var_name.split('_')[-1] == 'no':
                ubs.append(processes[var_name.split('_')[1]]['time'])
            else:
                ubs.append(cplex.infinity)
        else:
            ubs.append(100)
    var_types = 'I' * len(var_names)  # 数据类型
    # 'C': 连续的; 'B': 二元的; 'I': 整型; 'N': 半整型; 'S': 半连续

    # 目标函数
    objective = []
    for var_name in var_names:
        if var_name.split('_')[-1] == 'yes':
            objective.append(round(processes[var_name.split('_')[1]][var_name.split('_')[2]][var_name.split('_')[0]] * 1.2, 1))
        else:
            objective.append(processes[var_name.split('_')[1]][var_name.split('_')[2]][var_name.split('_')[0]])

    # 约束条件
    constraints_lefts = []  # 约束条件左边
    constraints_rights = []  # 约束条件右边
    num = 0
    for process in processes:  # 总普通时常限制
        _constraint = []
        for var_name in var_names:
            if var_name.split('_')[0] == 'normal' and var_name.split('_')[1] == process and var_name.split('_')[-1] != 'yes':
                _constraint.append(var_name)
        constraint = [_constraint, np.ones(len(_constraint))]
        constraints_lefts.append(constraint)
        constraints_rights.append(processes[process]['time'])
        num += 1
    constraints_senses = 'L' * num  # 约束条件关系

    num = 0
    for process in processes:  # 总加班时常限制
        _constraint = []
        for var_name in var_names:
            if var_name.split('_')[0] == 'plus' and var_name.split('_')[1] == process and var_name.split('_')[-1] != 'yes':
                _constraint.append(var_name)
        constraint = [_constraint, np.ones(len(_constraint))]
        constraints_lefts.append(constraint)
        constraints_rights.append(100)
        num += 1
    constraints_senses = constraints_senses + 'L' * num  # 约束条件关系

    # 销售数量限制
    num = 0
    for product in products:
        for process in processes:
            _constraint = []
            for var_name in var_names:
                if var_name.split('_')[2] == product and var_name.split('_')[1] == process:
                    _constraint.append(var_name)
            constraint = [_constraint, np.ones(len(_constraint))]
            num += 1
            constraints_lefts.append(constraint)
            constraints_rights.append(int(products[product]['sale'] * products[product][f'process_{process}']))
    constraints_senses = constraints_senses + 'G' * num  # 约束条件关系
    # G: >=; L: <=; E: =; R: ranged constraints
    constraints_names = [f'c{i}' for i in range(len(constraints_lefts))]  # 约束规则名

    print(constraints_lefts)
    print(constraints_senses)
    print(constraints_rights)

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
