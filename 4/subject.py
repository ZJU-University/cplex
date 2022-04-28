from prettytable import PrettyTable

# table = PrettyTable(['垃圾处理点', '白水', '罗斯堪洛', '杜拉斯'])
# table.add_row(['金斯波特', 12, 15, 17])
# table.add_row(['丹维尔', 14, 9, 10])
# table.add_row(['美肯', 13, 20, 11])
# table.add_row(['塞尔玛', 17, 16, 19])
# table.add_row(['哥伦布', 7, 14, 12])
# table.add_row(['亚兰墩', 22, 16, 18])

# table = PrettyTable(['垃圾处理点', '白水', '罗斯堪洛', '杜拉斯'])
# table.add_row(['白水', 0, 12, 10])
# table.add_row(['罗斯堪洛', 12, 0, 15])
# table.add_row(['杜拉斯', 10, 15, 0])

# table = PrettyTable(['工厂', '每周的废物量（桶）'])
# table.add_row(['金斯波特', 35])
# table.add_row(['丹维尔', 26])
# table.add_row(['美肯', 42])
# table.add_row(['塞尔玛', 53])
# table.add_row(['哥伦布', 29])
# table.add_row(['亚兰墩', 38])

table = PrettyTable(['工厂', '金斯波特', '丹维尔', '美肯', '塞尔玛', '哥伦布', '亚兰墩'])
table.add_row(['金斯波特', 0, 6, 4, 9, 7, 8])
table.add_row(['丹维尔', 6, 0, 11, 10, 12, 7])
table.add_row(['美肯', 5, 11, 3, 0, 7, 15])
table.add_row(['塞尔玛', 9, 10, 3, 0, 3, 16])
table.add_row(['哥伦布', 7, 12, 7, 3, 0, 14])
table.add_row(['亚兰墩', 8, 7, 15, 16, 14, 0])

print(table)
