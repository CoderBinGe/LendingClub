import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']


def analyze_data(data):
    # 选择列
    used_cols = ['loan_amnt', 'term', 'int_rate', 'grade', 'issue_d', 'addr_state', 'loan_status']
    used_data = data[used_cols]
    pd.set_option('display.max_columns', None)
    # print(used_data.head())

    # 1、查看不同借贷状态的数据量
    loan_status = used_data['loan_status'].value_counts()
    # print(loan_status)

    # 2、按月份统计借贷金额总量
    used_data['issue_d2'] = pd.to_datetime(used_data['issue_d'])
    # print(used_data['issue_d'])
    group_by_date = used_data.groupby(by='issue_d2').sum()
    group_by_date.reset_index(inplace=True)  # issue_d2设置为列索引，行索引变为默认的整型
    group_by_date['issue_month'] = group_by_date['issue_d2'].apply(lambda x: x.to_period('M'))
    group_by_month = group_by_date.groupby(by='issue_month')['loan_amnt'].sum()
    # 转换为dataframe
    group_by_month_df = pd.DataFrame(group_by_month).reset_index()
    print(group_by_month_df)
    # 保存结果
    group_by_month_df.to_csv('./output/group_by_month_df.csv', index=False)  # 不保留行索引

    # 方法2
    # used_data.set_index('issue_d2', inplace=True)
    # group_by_month = used_data.resample('M').sum()['loan_amnt']
    # print(group_by_month)

    # 可视化
    group_by_month_df.plot()
    plt.xlabel('日期')
    plt.ylabel('借贷总量')
    plt.title('日期 vs 借贷总量')
    plt.tight_layout()
    plt.savefig('./output/group_by_month_df.svg')
    plt.show()

    # 3. 按地区（州）统计借贷金额总量
    group_by_state = used_data.groupby(by='addr_state')['loan_amnt'].sum()
    # print(group_by_state)

    # 可视化
    group_by_state.plot(kind='bar')
    plt.xlabel('州')
    plt.ylabel('借贷总量')
    plt.title('州 vs 借贷总量')
    plt.tight_layout()
    plt.savefig('./output/group_by_state.png')
    plt.show()

    # 4、借贷评级、期限和利率的关系
    group_by_grade_term = used_data.groupby(['grade', 'term'])['int_rate'].mean()
    group_by_grade_term_df = pd.DataFrame(group_by_grade_term).reset_index()
    print(group_by_grade_term_df.head())
    group_by_grade_term_df.to_csv('./output/group_by_grade_term_df.csv', index=False)
    # 转换为透视表
    group_by_grade_term_pivot = group_by_grade_term_df.pivot(index='grade', columns='term', values='int_rate')
    group_by_grade_term_pivot.to_csv('./output/group_by_grade_term_pivot.csv')
