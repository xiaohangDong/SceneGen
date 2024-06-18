import bpy
import bmesh

import numpy as np
import math
from mathutils import Vector
import sys
sys.path.append('C:/CityGeneration/replacement/BlenderScene')



class Circumscribed_circle:

    @staticmethod
    def total_corner_angles(edges, n, r):
        sum = 0.0
        for i in range(n):
            sum += math.asin(edges[i] / (2 * r)) * 2
        return sum

    @staticmethod 
    def get_bounding_box_edges(model):
        obj = bpy.data.objects[model.name]
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        xs = [pt.x for pt in bbox_corners]
        ys = [pt.y for pt in bbox_corners]
        zs = [pt.z for pt in bbox_corners]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        return [width, height, width, height], (min(xs) + width / 2, min(ys) + height / 2, min(zs))

    @staticmethod
    def get_circumscribed_circle(model):
        edges, center = Circumscribed_circle.get_bounding_box_edges(model)  # 获取模型的边长
        N = len(edges)  # 边数

        max_edge = max(edges)  # 最长边

        # 以最长边为直径求圆心角之和，若为2π则直接返回
        sum = Circumscribed_circle.total_corner_angles(edges, N, max_edge / 2)
        if abs(sum - math.pi * 2) < 1e-5:
            return 
#            print("外接圆的最大半径是最大边的一半：%.2f" % (max_edge / 2))
#            print("圆心的世界坐标是：", center)
        #bpy.ops.mesh.primitive_circle_add(radius=max_edge / 2, location=center)
            #return (max_edge / 2)

        # 半径大于最大边的一半（即斜边大于直角边）
        left = max_edge / 2
        right = 10000000
        other = 0

        # 在误差范围内循环求解
        while right - left > 1e-5:
            mid = (right + left) / 2
            max_angle = math.asin(max_edge / (2 * mid)) * 2  # 求出最大边对应的圆心角
            sum = Circumscribed_circle.total_corner_angles(edges, N, mid)
            other = sum - max_angle
            # 如果除去最大圆心角的其他圆心角之和小于π，说明圆心在多边形外面
            if other < math.pi:
                sum = other + 2 * math.pi - max_angle
                if sum < 2 * math.pi:
                    left = mid
                else:
                    right = mid
            # 圆心在多边形里面
            else:
                if sum > 2 * math.pi:
                    left = mid
                else:
                    right = mid

#        print("外接圆的最大半径是：%.2f" % mid)
#        print("圆心的世界坐标是：", center)
        #返回多边形外接圆半径和圆心(x,y,z)坐标
        #bpy.ops.mesh.primitive_circle_add(radius=mid, location=center)
        return mid


class Inscribed_circle:
    N_CELLS = 5
    M_CELLS = 5

    # polygon为传入参数
    @staticmethod
    def FindInscribedCircleCenter(polygon):
        if len(polygon) <= 1:
            return 0
        bounds = [10000, -10000, 100000, -10000]
        for pt in polygon:
            if pt[0] < bounds[0]: bounds[0] = pt[0]
            if pt[0] > bounds[1]: bounds[1] = pt[0]
            if pt[1] < bounds[2]: bounds[2] = pt[1]
            if pt[1] > bounds[3]: bounds[3] = pt[1]

        point_pia = [0, 0, 0]
        flt_tmp = np.finfo(float).max
        count = 1
        while True:
            count += 1
            # find new candidate PIA
            point_tmp = Inscribed_circle.GeometryFindPIA(polygon, bounds)
            # update current PIA
            point_pia[0] = point_tmp[0]
            point_pia[1] = point_tmp[1]
            # update the bounds
            flt_tmp = (bounds[1] - bounds[0]) / (np.sqrt(2) * 2)
            bounds[0] = point_pia[0] - flt_tmp
            bounds[1] = point_pia[0] + flt_tmp
            flt_tmp = (bounds[3] - bounds[2]) / (np.sqrt(2) * 2)
            bounds[2] = point_pia[1] - flt_tmp
            bounds[3] = point_pia[1] + flt_tmp

            
            if bounds[1] - bounds[0] < 0.01 or bounds[3] - bounds[2] < 0.01:
                break

        tmp_distance = Inscribed_circle.DistancePointAPolygon(polygon, point_pia)
        output = [point_pia[0], point_pia[1], polygon[0][2], tmp_distance]
        return output
    @staticmethod
    def GeometryFindPIA(polygon, bounds):
        pia = [0, 0, 0]
        pia[0] = (bounds[0] + bounds[1]) / 2
        pia[1] = (bounds[2] + bounds[3]) / 2
        tmp = [0, 0, 0]
        increment_x = (bounds[1] - bounds[0]) / Inscribed_circle.N_CELLS
        increment_y = (bounds[3] - bounds[2]) / Inscribed_circle.M_CELLS
        max_distance = 0
        tmp_distance = np.finfo(float).max
        for i in range(Inscribed_circle.N_CELLS + 1):
            tmp[0] = bounds[0] + i * increment_x
            for j in range(Inscribed_circle.M_CELLS + 1):
                tmp[1] = bounds[2] + j * increment_y
                # compare with candidate PIA if point is in polygon
                if Inscribed_circle.IsPointInPolygon(polygon, tmp):
                    tmp_distance = Inscribed_circle.DistancePointAPolygon(polygon, tmp)
                    if tmp_distance > max_distance:
                        max_distance = tmp_distance
                        pia[0] = tmp[0]
                        pia[1] = tmp[1]
        return pia

    @staticmethod
    def IsPointInPolygon(polyline, pt):
        count = 0
        mark1 = [1000, 1000, 0]
        for i in range(len(polyline)):
            id = (i + 1) % len(polyline)
            if Inscribed_circle.get_line_intersection(polyline[i], polyline[id], pt, mark1) == 1:
                count += 1
        if count % 2 == 1:
            return True
        else:
            return False

    @staticmethod
    def get_line_intersection(p0, p1, p2, p3):
        s_numer, t_numer, denom, t = 0, 0, 0, 0
        s10 = [p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]]
        s32 = [p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]]

        denom = s10[0] * s32[1] - s32[0] * s10[1]
        if denom == 0:  # 平行或共线
            return 0  # Collinear
        denomPositive = denom > 0

        s02 = [p0[0] - p2[0], p0[1] - p2[1], p0[2] - p2[2]]

        s_numer = s10[0] * s02[1] - s10[1] * s02[0]
        if (s_numer < 0) == denomPositive:  # 参数是大于等于0且小于等于1的，分子分母必须同号且分子小于等于分母
            return 0  # No collision

        t_numer = s32[0] * s02[1] - s32[1] * s02[0]
        if (t_numer < 0) == denomPositive:
            return 0  # No collision

        if abs(s_numer) > abs(denom) or abs(t_numer) > abs(denom):
            return 0  # No collision

        return 1
    @staticmethod
    def DistancePointAPolygon(polyline, pt):
        mark = [0, 0, 0]
        max_dist = 10000
        for i in range(len(polyline)):
            id = (i + 1) % len(polyline)
            diff = [polyline[id][0] - polyline[i][0], polyline[id][1] - polyline[i][1], polyline[id][2] - polyline[i][2]]
            mark[0] = -diff[1] * 10000 + pt[0]
            mark[1] = diff[0] * 10000 + pt[1]
            dist = 0
            if Inscribed_circle.get_line_intersection(polyline[i], polyline[id], pt, mark) == 1:  # 有交点
                pt_edge = [pt[0] - polyline[i][0], pt[1] - polyline[i][1], pt[2] - polyline[i][2]]
                val = pt_edge[0]*diff[0] + pt_edge[1]*diff[1]
                val1 = pt_edge[0]*pt_edge[0] + pt_edge[1]*pt_edge[1]
                if val1 < 0.00001:
                    dist = 0
                else:
                    val1 = math.sqrt(val1)
                    val2 = diff[0]*diff[0] + diff[1]*diff[1]
                    val2 = math.sqrt(val2)
                    temp = val / (val1*val2)
                    if temp > 1: temp = 1.0
                    if temp < -1: temp = -1.0
                    dist = val1*math.sin(math.acos(temp))
            else:
                dist1 = [pt[0] - polyline[i][0], pt[1] - polyline[i][1], pt[2] - polyline[i][2]]
                dist2 = [pt[0] - polyline[id][0], pt[1] - polyline[id][1], pt[2] - polyline[id][2]]
                val1 = dist1[0]*dist1[0] + dist1[1]*dist1[1]
                val2 = dist2[0]*dist2[0] + dist2[1]*dist2[1]
                if val1 > val2:
                    val2 = math.sqrt(val2)
                    dist = val2
                else:
                    val1 = math.sqrt(val1)
                    dist = val1
            if dist < max_dist:
                max_dist = dist
        return max_dist

    # # 指定你的.blender文件的路径
    # filepath = "C:/CityGeneration/replacement/BlenderScene/onlyRoad.blend"

    # # 使用bpy.ops.wm.open_mainfile()函数打开文件
    # bpy.ops.wm.open_mainfile(filepath=filepath)
    @staticmethod
    def scene_setup(obj):
        # Get the object by name
        #obj = bpy.data.objects['lot.009']
        print(f"scene_setup parameters :{obj}")
        # Get a BMesh from the object's mesh data
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        # Find the face that is facing upwards
        for face in bm.faces:
            if face.normal.z > 0:
                # This is the face we want
                break

        # Get the vertices of the face in world coordinates
        verts = [obj.matrix_world @ v.co for v in face.verts]

        # Print the vertices
        for i, v in enumerate(verts):
            print(obj.name+f"Vertex {i}: {v.x}, {v.y}, {v.z}")
            
            
        # Convert the vertices to cv::Point3f vector
        polygon = [(v.x, v.y, v.z) for v in verts]
        print(f"polygon :{polygon}")

        # Create the output array
        output = np.zeros(4)


        # Call the function
        output = Inscribed_circle.FindInscribedCircleCenter(polygon)

        # Convert the center of the inscribed circle back to world coordinates
        center = obj.matrix_world @ Vector((output[0], output[1], 0))

        # Print the result
        print("多边形内接圆圆心 ", center.x, center.y)
        print("内接圆半径 ", output[3])
        

        # Create a new circle mesh object at the center of the inscribed circle 
        # bpy.ops.mesh.primitive_circle_add(
        #     radius=output[3], 
        #     #location=(center.x, center.y, verts[0].z)
        #     location=(center.x, center.y, 0)
        # )



        
        #返回多边形内接圆的半径和世界坐标
        '''
        radius, coordinates = inscribed_circle.scene_setup(obj)
        print("Radius: ", radius)
        print("Coordinates: ", coordinates)
        '''
        del bm, face, polygon  # 清理所有临时变量
        
        return output[3], (center.x, center.y, verts[0].z)



