import bpy
import re
import random
# 获取场景中所有对象
filtered_models = []

# 获取当前的视图图层
view_layer = bpy.context.view_layer

# 获取所有对象
all_objects = bpy.context.scene.objects

# 遍历所有对象
for obj in all_objects:
    print(obj.name)
    print(obj.type)
    # 检查对象名称是否以"BasiccityModel_"开头并且对象类型为"资产"
    if (re.match(r'cityModel_\d+$', obj.name)):
        # 将符合条件的模型对象存储到字典中，以对象名称作为键，对象本身作为值
        filtered_models.append(obj.name)

# 打印筛选后的模型字典
print(filtered_models)


for i in range(10):
    
    tl_obname = random.choice(filtered_models)
    
    print( str(i) + 'round_name:'+ tl_obname)

    tl_obj = bpy.data.objects.get(tl_obname)

    tl_location = (- tl_obj.location[0], 0 - tl_obj.location[1], 0 - tl_obj.location[2])  # 新位置为(5, 0, 0)
    
    print(tl_location)
    
    # 清除之前选定的对象
    bpy.ops.object.select_all(action='DESELECT')
    
    # 确保对象在当前视图图层中可见
#    view_layer.active_layer_collection.collection.objects.link(tl_obj)
    tl_obj.select_set(True)
    
    
    bpy.ops.object.duplicate_move_linked(
        OBJECT_OT_duplicate={"linked": True},
        TRANSFORM_OT_translate={"value": tl_location}
    )
    
    # 将复制后的对象添加到当前视图图层
    duplicated_obj = bpy.context.selected_objects[0]
    view_layer.active_layer_collection.collection.objects.link(duplicated_obj)
    tl_obj.select_set(False)
 

