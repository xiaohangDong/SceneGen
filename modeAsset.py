
import bpy
import re
import random



def modelAssetList(n):
    #创建存储字典
    selected_objects ={}
    # 加载.blend文件
    with bpy.data.libraries.load("C://CityGeneration//replacement//BuildingModels//moderncity01.blend",link=False, assets_only=True) as (data_from, data_to):
        #moderncity01 ,NeoTokyo.blend,
        # Returns a context manager which exposes 2 library objects on entering. Each object has attributes matching bpy.data 
        data_to.objects = [name for name in data_from.objects if re.match(r'cityModel_\d+$', name)]
                
        # print(dir(data_to))
        # print(data_to.objects)
        
        # 随机选择n个对象
        selected_objects = random.sample(data_to.objects, n)
        print(selected_objects)
    return selected_objects
        
 

#Assestlist = modelAssetList(10)


### 实例化集合
##bpy.ops.object.collection_instance_add(collection=collection_name)

## 获取新创建的实例
#instance = bpy.context.active_object

## 修改实例的scale属性
#instance.scale = (random_scale, random_scale, random_scale)

## 获取集合
#collection = bpy.data.collections[collection_name]

#for i in range(10):
#    obj_name = random.choice(Assestlist)    
#    
#    obj = bpy.data.objects.get(obj_name)
#    if obj:
#        # collection instance to scene
#        
#        # 集合的名称
#        collection_name = obj_name
#        # 实例化集合
#        bpy.ops.object.collection_instance_add(collection=collection_name)
#        # 获取新创建的实例
#        instance = bpy.context.active_object
#         # 修改实例的scale属性
#        #instance.scale = (random_scale, random_scale, random_scale)
#        
#        random_location = random.uniform(-20, 20)
#        instance.location = (random_location, random_location, random_location)
 

    

