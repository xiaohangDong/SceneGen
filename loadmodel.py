import bpy
import sys
sys.path.append('C:/CityGeneration/replacement/BlenderScene')

import modelReplace
import onlyLot as ol
#模型文件路径
fbx_filepath = "C:/CityGeneration/replacement/BuildingModels/high_01.fbx"
def load_model(n):
    """
    读取本地3D模型，并加载到场景中
    """

    # 获取场景中的所有对象
    all_objects = bpy.data.objects

    loaded_objects = []

    for i in range(n):
        model_name = "tall" + str(i)
        model_exists = False

        # 检查是否已经存在同名模型
        for obj in all_objects:
            if obj.name == model_name:
                instance = obj.copy()
                instance.data = obj.data.copy()
                instance.name = model_name + str(len(bpy.data.objects))  # 设置实例名称
                modelReplace.modelReplace.Reset_model_origin(instance)
               
                loaded_objects.append(instance)
                model_exists = True
                break

        if not model_exists:
            # 导入模型
            bpy.ops.import_scene.fbx(filepath=fbx_filepath)

            # 获取导入的对象
            imported_objects = bpy.context.selected_objects

            # 设置模型的初始名称
            imported_objects[0].name = model_name + str(len(bpy.data.objects))  # 设置你想要的模型名称

            # 重新设置原点
            for obj in imported_objects:
                modelReplace.modelReplace.Reset_model_origin(obj)
    
            loaded_objects.extend(imported_objects)
    print(loaded_objects)
    return loaded_objects

#load_model(3)