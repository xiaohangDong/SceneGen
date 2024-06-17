###bpy.ops.wm.read_homefile() 场景还原命令

# import bpy
# import os


# print("start:")
# # 创建一个空列表来存储模型
# models = []

# # 获取指定目录下的所有.blend文件
# blend_files = [f for f in os.listdir("C:\\CityGeneration\\replacement\\BuildingModels") if f.endswith('.blend')]

# # 文件路径列表
# file_paths = ["C://CityGeneration//replacement//BuildingModels//modernCity01.blend", "C://CityGeneration//replacement//BuildingModels//NeoTokyo.blend"]

# print("bian LI:")

# # 加载.blend文件
# # 遍历每个.blend文件
# for i, file_path in enumerate(file_paths):
#     with bpy.data.libraries.load(file_path) as (data_from, data_to):
#         data_to.objects = [name for name in data_from.objects if name in ['cityModel_' + str(i) for i in range(1, 87)]]
#         models.extend(data_to.objects)
#         print(data_to.objects)
#         print(f"Loaded {len(data_to.objects)} models from {file_path}, total models loaded: {len(models)}")

#         # 删除模型
#         for obj in data_to.objects:
#             bpy.data.objects.remove(obj, do_unlink=True)
#             # 删除模型
#             bpy.ops.object.delete()
#         # 清理孤立的数据块
#         bpy.ops.outliner.orphans_purge()
        
#         # 从列表中移除模型的引用
#         models = []


        
# print("bian LI end:")



# ==============================================================
# import bpy


# ## 设置导入类型为'APPEND'
# #bpy.context.space_data.params.import_type = 'APPEND'
    
# # 创建一个空列表来存储模型
# models = []

# # 加载.blend文件
# with bpy.data.libraries.load("C://CityGeneration//replacement//BuildingModels//morderCity.blend") as (data_from, data_to):
#      # 生成模型的名称，并将匹配的模型添加到列表中
#     data_to.objects = [name for name in data_from.objects if name in ['cityModel_' + str(i) for i in range(1, 87)]]
#     models.extend(data_to.objects)
    

# # 遍历'models'列表
# for model in models:
#     # 打印模型的名称
#     print(model.name)

# #for obj in data_to.objects:
# #    # 将对象链接到当前场景
# #    bpy.context.collection.objects.link(obj)


# ======================

# import bpy
# import os


# print("start:")
# # 创建一个空列表来存储模型
# models = []

# # 获取指定目录下的所有.blend文件
# blend_files = [f for f in os.listdir("C:\\CityGeneration\\replacement\\BuildingModels") if f.endswith('.blend')]

# # 文件路径列表
# file_paths = ["C://CityGeneration//replacement//BuildingModels//modernCity01.blend", "C://CityGeneration//replacement//BuildingModels//NeoTokyo.blend"]

# print("bian LI:")

# for i, file_path in enumerate(file_paths):
#     with bpy.data.libraries.load(file_path) as (data_from, data_to):
#         # 这里我们将需要的对象加载到data_to.objects
#         for obj_name in data_from.objects:
#             if obj_name in ['cityModel_' + str(i) for i in range(1, 86)]:
#                 obj = bpy.data.objects[obj_name]
#                 models.append(obj)
#                 print(obj.name)  # 打印对象的名字

# # 删除加载的对象
# for obj in models:
#     bpy.data.objects.remove(obj, do_unlink=True)

# # 清理内存
# bpy.ops.wm.memory_statistics()

###******************************************************************************************************************************

###加载单个文件

import bpy
import re
import random



def modelAssetList(n):
    #创建存储字典
    selected_objects ={}
    # 加载.blend文件
    with bpy.data.libraries.load("C://CityGeneration//replacement//BuildingModels//modernCity01.blend",link=False, assets_only=True) as (data_from, data_to):
        # Returns a context manager which exposes 2 library objects on entering. Each object has attributes matching bpy.data 
        data_to.objects = [name for name in data_from.objects if re.match(r'cityModel_\d+$', name)]
        # print(dir(data_to))
        # print(data_to.objects)
        # 随机选择n个对象
        selected_objects = random.sample(data_to.objects, n)
        print(selected_objects)
    return selected_objects
        
 

#Assestlist = modelAssetList(3)
## assets load method        
#obj_name = random.choice(Assestlist)
## 将对象链接到当前场景
#obj = bpy.data.objects.get(obj_name)
## 对对象进行缩放和位置变化操作
#obj.scale = (0.5, 0.5, 0.5)  # 缩放对象
#obj.location = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(0, 5))  # 设置对象位置
#    
#bpy.context.collection.objects.link(obj)
    
 

    

