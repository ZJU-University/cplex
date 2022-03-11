#!/usr/bin/env python
# encoding: utf-8

# created by JudeYin @yinjiahuidada@gmail.com
# create time: 2022-03-11
# course 工程决策方法与应用
# teacher Mr.Ma @hongma@foxmail.com
# the number of class: 1
# class time: 2022-02-26


from utils.general import LOGGER
import cplex
from cplex.exceptions import CplexError

'''
Page 54 
Q48: 
    泰克大学的招生办公室想决定在下一个秋季的新生班中招收多少本州和其他州的学生。本州学生的学费是每年7600美元，其他州的学生的学费是22500美元。
12800名本州学生和8100名其他州的学生申请了下一个秋季的新生班，泰克最多能招收3500名学生。然而由于泰克是一所州立大学，本州法律规定它只能招收最多
40%的其他州的学生。根据过去的经验，12%的本州学生和24%的其他州的学生会在第一年退学。泰克大学想找到一种方案使收取的学费最多，而且把第一年的退学
人数限制在600人
'''

if __name__ == '__main__':
    cpx = cplex.Cplex()

    # 参数定义
    max_stu_in = 3500  # 最大招收学生数量
    max_stu_out = 600  # 最大退学学生数量
    local_stu_tuition = 7600  # 本州学生学费
    nonlocal_stu_tuition = 22500  # 本州学生学费
    local_stu_drop_rt = 0.12  # 本州学生退学率
    nonlocal_stu_drop_rt = 0.24  # 他州学生退学率
    max_nonlocal_rt = 0.4  # 最大他州学生招生率

    # 决策变量定义
    # 即 X1: 招收的本州学生数量 & X2: 招收的他州学生数量
    var_names = ['local_stu', 'nonlocal_stu']  # 变量名
    lbs = [0, 0]  # 下界
    ubs = [max_stu_in, max_stu_in]  # 上界
    var_types = 'II'  # 数据类型
    # 'C': 连续的; 'B': 二元的; 'I': 整型; 'N': 半整型; 'S': 半连续

    # 目标函数
    # Z = local_stu_tuition * X1 + nonlocal_stu_tuition * X2
    objective = [local_stu_tuition, nonlocal_stu_tuition]

    # 约束条件
    """
    总招生人数限制: local_stu + nonlocal_stu <= max_stu_in
    总退学人数限制: local_stu * local_stu_drop_rt + nonlocal_stu * nonlocal_stu_drop_rt <= max_stu_out
    招生本/外州人数比例限制: nonlocal_stu / (local_stu + nonlocal_stu) <= max_nonlocal_rt
        => max_nonlocal_rt * local_stu + (max_nonlocal_rt - 1) * nonlocal_stu >= 0
    """
    constraints_lefts = [
        [['local_stu', 'nonlocal_stu'], [1.0, 1.0]],
        [['local_stu', 'nonlocal_stu'], [local_stu_drop_rt, nonlocal_stu_drop_rt]],
        [['local_stu', 'nonlocal_stu'], [max_nonlocal_rt, max_nonlocal_rt - 1]],
    ]  # 约束条件左边
    constraints_senses = 'LLG'  # 约束条件关系
    # G: >=; L: <=; E: =; R: ranged constraints
    constraints_rights = [
        max_stu_in,
        max_stu_out,
        0
    ]  # 约束条件右边
    constraints_names = ['c1', 'c2', 'c3']  # 约束规则名

    try:
        # 求解目标
        cpx.objective.set_sense(cpx.objective.sense.maximize)  # 最大值
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

        # 问题求解
        cpx.solve()

        # 最优情况下的变量值
        x = cpx.solution.get_values()
        for i, var_name in enumerate(var_names):
            LOGGER.info(f'最优 {var_name}: {x[i]}')

        # 最优情况下的目标值
        objective_value = cpx.solution.get_objective_value()
        LOGGER.info(f'最优结果: {objective_value}')

    except CplexError as e:
        LOGGER.error(e)





