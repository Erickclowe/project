import pandas as pd  
import os  
  
# 设置CSV文件所在的文件夹路径和结果Excel文件的名称 yjy 
csv_folder = input("请输入.csv文件夹的路径,例如（双斜线）,D:\\test\\nback3（240926）: ")  # 替换为您的CSV文件夹路径  
output_excel =input("请输入,输出路径,例如（双斜线）,D:\\test\\nback3.xlsx：") # 替换为您想要的输出Excel文件名  
# 初始化一个列表来存储每个文件的和  
sums_list = []  
  
# 遍历文件夹中的所有CSV文件  
for filename in os.listdir(csv_folder):  
    if filename.endswith('.csv'):  
        file_path = os.path.join(csv_folder, filename)  
          
        # 读取CSV文件的第13列（索引为12），并跳过前17行，然后取第18到第90行  
        df = pd.read_csv(file_path, usecols=[12])  
        df = df.iloc[19:89]  # 注意：iloc是基于0的索引，所以17表示第18行  
        print(df)  
        # 计算该列的和，并将结果添加到列表中  
        column_sum = df.iloc[:, 0].sum()  # 使用iloc[:, 0]来选择第一列（即我们的第13列）  
        sums_list.append(column_sum)  
  
# 将结果写入新的Excel文件  
result_df = pd.DataFrame({'File Sums': sums_list})  
result_df.to_excel(output_excel, index=False)  
  
print(f"算好了 {output_excel}")