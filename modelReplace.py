import bpy
import bmesh
import numpy as np
import math
import gc
from mathutils import Vector
import os
import random
import time
import sys
sys.path.append('C:/CityGeneration/replacement/BlenderScene/memoryMinor')

import modeAsset

# 记录程序开始时间
start_time = time.time()

import onlyLot as ol
import Circle_Tool as ct




##模型文件路径
#fbx_filepath = "C:/CityGeneration/replacement/BuildingModels/high_01.fbx"


class modelReplace:
    """
    
    实现模型在地块上的放置
    
    """
    @staticmethod
    def load_model():
        """
        读取本地3D模型，并加载到场景中
        """

        
        # 获取场景中的所有对象
        all_objects = bpy.data.objects

        # 检查是否已经存在同名模型
        for obj in all_objects:
            if obj.name == "tall":  
                instance = obj.copy()
                instance.data = obj.data.copy()
                instance.name="tall"+ str(len(bpy.data.objects))  # 设置实例名称
                modelReplace.Reset__model_origin(instance)
                return [instance]  # 如果模型已经存在，返回实例


        # 获取导入的对象
        imported_objects = bpy.context.selected_objects
        
        print(type(imported_objects[0]))  # 打印出对象的类型

        # 设置模型的初始名称
        imported_objects[0].name = "tall"+ str(len(bpy.data.objects))  # 设置你想要的模型名称
        # bpy.context.view_layer.objects.active = imported_objects[0]
        #bpy.ops.object.transform_apply(location=True)
        # 重新设置原点
        for obj in imported_objects:
            modelReplace.Reset__model_origin(obj)
        return imported_objects

    @staticmethod
    def Scaling_ratio(lot, BuildingModel):
        """
        确定地块与楼房之间的缩放比例，并返回比例
        """
        # 创建Circumscribed_circle的实例
        #cc = ct.Circumscribed_circle() 
        
        #模型的地面外接圆半径
        model_z_radius = ct.Circumscribed_circle.get_circumscribed_circle(BuildingModel)

        print("model_z_radius:",model_z_radius)
        #ci = ct.Inscribed_circle()
        
        #地块多边形的内接圆半径
        lot_inCircle, lot_inCircle_coordinates = ct.Inscribed_circle.scene_setup(lot)

        print("lot_inCircle:",lot_inCircle)
        #缩放比例确定
        scale_ratio = lot_inCircle / model_z_radius
        print(lot.name+"scale_ratio:",scale_ratio)
        
       
        return scale_ratio,lot_inCircle_coordinates
    
    @staticmethod
    def Reset_model_origin(object):
        # 获取模型的边界框顶点坐标
        bounding_box = object.bound_box

        # 初始化最小和最大坐标值
        min_x, min_y, min_z = bounding_box[0]
        max_x, max_y, max_z = bounding_box[0]

        # 计算包围盒在各轴上的坐标范围
        for vertex in bounding_box:
            min_x = min(min_x, vertex[0])
            min_y = min(min_y, vertex[1])
            min_z = min(min_z, vertex[2])
            max_x = max(max_x, vertex[0])
            max_y = max(max_y, vertex[1])
            max_z = max(max_z, vertex[2])

        # 转换包围盒顶点坐标到世界坐标系
        min_vertex = object.matrix_world @ Vector((min_x, min_y, min_z))
        max_vertex = object.matrix_world @ Vector((max_x, max_y, max_z))

        # 计算包围盒底面的中心点
        center_x = (min_vertex.x + max_vertex.x) / 2
        center_y = (min_vertex.y + max_vertex.y) / 2
        center_z = min_vertex.z  # 底面的z坐标就是最小的z坐标

        # 创建一个新的中心点向量
        center = Vector((center_x, center_y, center_z))

        # 将模型的原点设置为新的中心点
        bpy.context.scene.cursor.location = center
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    



#加载后的资产模型，需要在场景中隐藏掉
def model_hide(obj_name):
    view_layer = bpy.context.view_layer
    if obj_name in view_layer.objects:
        obj = bpy.data.objects.get(obj_name)
        obj.hide_set(True)
        obj.hide_render = True
        obj.hide_viewport = True
        return obj
    else:
        return None


Assestlist = modeAsset.modelAssetList(15)


lots = ol.lot_loads()
# assets load method 
       

for lot_name in lots:
    lot = bpy.data.objects[lot_name]
    
    # assets load method        
    tl_obname = random.choice(Assestlist)
    
    
    # 将对象链接到当前场景
#    obj = bpy.data.objects.get(obj_name)
    
    tl_obj = bpy.data.objects.get(tl_obname)
   
    # 将对象添加到当前视图图层
    view_layer = bpy.context.view_layer
    

    
    if tl_obname not in view_layer.objects:  
        # 将复制后的对象添加到当前视图图层
        view_layer.active_layer_collection.collection.objects.link(tl_obj)

        
    
    if tl_obj:
        #计算多边形地块内接圆      
        lot_inCircle, tl_location = ct.Inscribed_circle.scene_setup(lot)
        
        
        ac_location = (tl_location[0] - tl_obj.location[0], tl_location[1] - tl_obj.location[1], tl_location[2] - tl_obj.location[2])
        
        #print('tl_location:',tl_location)
        
        # 清除之前选定的对象
        bpy.ops.object.select_all(action='DESELECT')
        

        tl_obj.select_set(True)
                
        bpy.ops.object.duplicate_move_linked(
            OBJECT_OT_duplicate={"linked": True},
            TRANSFORM_OT_translate={"value": ac_location}
        )
        
        
        # 将复制后的对象添加到当前视图图层
        duplicated_obj = bpy.context.selected_objects[0]
                      
        #缩放楼房模型大小
        scal_ratio,x = modelReplace.Scaling_ratio(lot, tl_obj)
        
    
        #scale duplicated_obj models
        duplicated_obj.scale = (scal_ratio, scal_ratio, scal_ratio)
        

        tl_obj.select_set(False)


for obj_name in Assestlist:
    model_hide(obj_name)
# 记录程序结束时间
end_time = time.time()
# 计算程序运行时间，并打印出来
total_time = end_time - start_time
print("程序运行时间：{:.2f} 秒".format(total_time))

#bpy.ops.wm.read_homefile() 恢复为带有用户设置的初始状态 


            

