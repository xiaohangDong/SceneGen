import bpy
import pickle
import os, time, pathlib
import bmesh
import sys


sys.path.append('C:/CityGeneration/Procedural-City-Generation-master')

from procedural_city_generation import *






def lot_loads():
    
    
    #打开地块文件 
    filepath = "C:/CityGeneration/replacement/polys/s150150_polygons.txt" 
    #filepath = "C:/CityGeneration/Procedural-City-Generation-master_GPT_Replacement/procedural_city_generation/temp/radical2020_polygons.txt"
    with open(filepath, "rb") as f:
            polygons = pickle.load(f)
            
    #####################################################
    # get the grass material

    grassMaterial = None

    filepath = "C://CityGeneration//replacement//BuildingModels//草1_1709392872132-788513644.blend"
    with bpy.data.libraries.load(filepath,link=False) as (data_from, data_to):
            # Returns a context manager which exposes 2 library objects on entering. Each object has attributes matching bpy.data 
            data_to.materials = [name for name in data_from.materials if name.startswith("草")]
            

    for material in data_to.materials:
        if material is not None:
            grassMaterial = material
        
    #############################################
    
    
    
    '''draw the lot segment in the blender, and return the counts of the lot'''
    lot_names=[]
    lot_count = 1  # 初始地块编号
    
    # 新建一个lot collection
    lots_collection = bpy.data.collections.new("lot")
    # 获取当前场景
    scene = bpy.context.scene
    # 将新建的collection添加到场景中
    scene.collection.children.link(lots_collection)
    
    # 遍历每个Polygon2D对象
    for polygon in polygons:
        # 如果poly_type属性为"road"，则舍弃
        if polygon.poly_type == "road":
            continue

        # 如果poly_type属性为"lot"，在Blender中进行绘制
        if polygon.poly_type == "lot":
#            print("Drawing lot...")
            
            
            # 创建一个Mesh对象
            mesh = bpy.data.meshes.new("lot_mesh")
            
            # 创建一个bmesh
            bm = bmesh.new()
                        

            # 获取多边形的顶点数据并创建面的顶点索引列表
            vertices = [(v[0], v[1], 0) for v in polygon.vertices]
            for v in vertices:
                bm.verts.new(v)
                
            # 确保索引表已更新
            bm.verts.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            
            
            # 创建面
            face_verts = [bm.verts[i] for i in range(len(vertices))]
            bm.faces.new(face_verts) 
            
            
            # 计算法线方向
            bm.normal_update()

     # 将面的法线方向指向Z轴正方向
            # for f in bm.faces:
            #     f.normal_update()
            #     f.normal_flip()

            # 转换bmesh到mesh
            bm.to_mesh(mesh)
            mesh.update()

            # 创建一个新的面材质
            #mat = bpy.data.materials.new(name="polygon_material")

            # 创建一个新的材质槽
            mat_slot = mesh.materials.append(grassMaterial)
    ##########################################################################
    # uv set:
            uv_layer = mesh.uv_layers.new()
            # 设置UV坐标以覆盖整个UV空间
            min_x = min([v[0] for v in polygon.vertices])
            min_y = min([v[1] for v in polygon.vertices])
            max_x = max([v[0] for v in polygon.vertices])
            max_y = max([v[1] for v in polygon.vertices])
            
            for loop in mesh.loops:
                vertex = mesh.vertices[loop.vertex_index]
                u = (vertex.co[0] - min_x) / (max_x - min_x)
                v = (vertex.co[1] - min_y) / (max_y - min_y)
                uv_layer.data[loop.index].uv = (u, v)
    #####################################
    
             # 将材质槽分配给所有面
            for polygon_face in mesh.polygons:
                if mat_slot is not None:
                    polygon_face.material_index = mat_slot       
                    # 获取分配给面的材质
                    material = mesh.materials[mat_slot]

                            
            mesh.update()

            # 创建一个对象，并将网格绑定到对象上
            obj = bpy.data.objects.new("lot_" + str(lot_count), mesh)
            
            lot_names.append(obj.name)
            lot_count += 1  # 更新地块编号
            # 将对象添加到场景中
            bpy.context.collection.objects.link(obj)
    
    print("Total lot count:", len(lot_names))
    print("Lot names:", lot_names)
    return lot_names
  

# lots_name=lot_Count()