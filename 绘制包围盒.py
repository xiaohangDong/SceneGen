import bpy
from mathutils import Vector

def get_bounding_box_world_coordinates(object):
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

    return min_vertex, max_vertex


def draw_model_bounding_box(object):

    min_vertex, max_vertex = get_bounding_box_world_coordinates(object)
    min_x, min_y, min_z = min_vertex
    max_x, max_y, max_z = max_vertex

    # 创建边界线的顶点坐标
    verts = [(min_x, min_y, min_z), 
             (max_x, min_y, min_z), 
             (max_x, max_y, min_z), 
             (min_x, max_y, min_z), 
             (min_x, min_y, max_z), 
             (max_x, min_y, max_z), 
             (max_x, max_y, max_z), 
             (min_x, max_y, max_z)]

    edges = [(0, 1), (1, 2), (2, 3), (3, 0), 
             (4, 5), (5, 6), (6, 7), (4, 7), 
             (0, 4), (1, 5), (2, 6), (3, 7)]

    faces = []

    mesh = bpy.data.meshes.new(name=object.name + "Bounding Box")
    obj = bpy.data.objects.new(name=object.name + "Bounding Box Object", object_data=mesh)



    mesh.from_pydata(verts, edges, faces)
    mesh.update()

    scene = bpy.context.scene
    scene.collection.objects.link(obj)

    print("Bounding box created successfully.")

# 获取模型对象
building = bpy.data.objects['plane']

# 绘制包围盒
draw_model_bounding_box(building)



# 获取模型的包围盒顶点坐标
#bound_box = plane.bound_box

# 应用世界变换矩阵到包围盒顶点坐标
#world_coords = [plane_matrix_world @ mathutils.Vector(v[:]) for v in bound_box]

# 提取包围盒顶点中的Z轴坐标
#z_coords = [v.z for v in world_coords]

# 计算包围盒在Z轴上的最小和最大坐标
#min_z = min(z_coords)

#print("plane Min Z Coordinate:", min_z)




# 获取模型的全局坐标
#global_location = building.matrix_world.translation

# 打印模型的全局坐标
#print("=============================")
#print("Model Name: ", building.name)
#print("Global Location: ", global_location)
#print("=============================")


# 获取平面对象的尺寸
#plane_dimensions = plane.dimensions
#plane_width = plane_dimensions.x
#plane_length = plane_dimensions.y

# 获取楼房模型的底部高度
#building_lowest_z = min((vertex.co.z for vertex in building.data.vertices))
#building_hightst_z =  max((vertex.co.z for vertex in building.data.vertices))

#print("=============================")
#print("building_lowest_z:", building_lowest_z)
#print("building_hightst_z:", building_hightst_z)
#print("=============================")


#building_height = building_hightst_z - building_lowest_z




# 获取建筑模型的尺寸和世界转换矩阵
#building_dimensions = building.dimensions
#building_matrix_world = building.matrix_world

#print("building.dimensions: ", building.dimensions)

# 将建筑模型的尺寸向量转换为全局坐标系中的表示
#global_dimensions = building_matrix_world.to_scale() @ building_dimensions

#print("Global Dimensions_world: ", global_dimensions)

#print("building_lowest_z:", building_lowest_z)

## 计算楼房底部尺寸
#building_dimensions = building.dimensions
#building_width = building_dimensions.x
#building_length = building_dimensions.y

## 按照平面大小和楼房底部尺寸比例进行缩放
#scale_x = plane_width / building_width
#scale_y = plane_length / building_length
#scale_z = 1.0  # 不对高度进行缩放

## 缩放楼房模型
#building.scale = (scale_x, scale_y, scale_z)

## 移动楼房模型至平面上
#building.location.x = plane.location.x
#building.location.y = plane.location.y
#building.location.z = plane.location.z 




# 更新场景
bpy.context.view_layer.update()