import tushare as ts
import time

i = 0

print("请输入想要查询的代码：")

stock_ID = input()

df = ts.get_today_ticks(stock_ID)


counter = 0
for volume,type,price in zip(df['volume'],df['type'],df['price']):
    if volume >800:
        print("买卖性质为：",type)
        print("买卖数量（手）：",volume)
        print("买卖价格:",price)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        if type == "买盘":
            counter = counter + volume*100*price
        elif type == "卖盘":
            counter = counter - volume*100*price
#    if type == "买盘":
#
 #       counter = counter + volume*price*100
  #  elif type == "卖盘":
   #     counter = counter - volume*price*100


print(counter)

