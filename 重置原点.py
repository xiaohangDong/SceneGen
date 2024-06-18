import bpy
from mathutils import Vector

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
    

object = bpy.data.objects['4']
Reset_model_origin(object)
