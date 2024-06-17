import bpy
import bmesh
import numpy as np
import math
import gc
from mathutils import Vector
import os
import random

import sys
sys.path.append('C:/CityGeneration/replacement/BlenderScene')

import modeAsset

import Circle_tool_old as ct
import onlyLot as ol


#模型文件路径
fbx_filepath = "C:/CityGeneration/replacement/BuildingModels/high_01.fbx"


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

        # 导入模型
        bpy.ops.import_scene.fbx(filepath=fbx_filepath)

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
        print("Scaling_ratio_lot:",lot.type)
        print("Scaling_ratio_BuildingModel:",BuildingModel.type)
        
        #模型的地面外接圆半径
        model_z_radius = ct.Circumscribed_circle.get_circumscribed_circle(BuildingModel)

        print("model_z_radius:",model_z_radius)
        #ci = ct.Inscribed_circle()
        
        #地块多边形的内接圆半径
        lot_inCircle, lot_inCircle_coordinates = ct.Inscribed_circle.scene_setup(lot)

        
        #缩放比例确定
        scale_ratio = lot_inCircle / model_z_radius
        
       
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
    


import loadmodel





Assestlist = modeAsset.modelAssetList(10)
lots = ol.lot_Count()
# assets load method 
       

for lot_name in lots:
    lot=bpy.data.objects[lot_name]
    # assets load method        
    obj_name = random.choice(Assestlist)
    
    # 将对象链接到当前场景
    obj = bpy.data.objects.get(obj_name)
    if obj:
        obj_copy = obj.copy()
        obj_copy.data = obj.data.copy()
        
    #缩放楼房模型大小
    scal_ratio,lot_inCircle_coordinates = modelReplace.Scaling_ratio(lot, obj_copy)

    obj_copy.scale *= scal_ratio
    #移动楼房模型
    obj_copy.location = lot_inCircle_coordinates
    # 链接到当前场景
    bpy.context.collection.objects.link(obj_copy)



    

    gc.collect()


            

