import bpy

def deleteUnusedAssets():
    # 获取当前场景中显示的对象名称集合
    displayed_objects = set(obj.name for obj in bpy.context.scene.objects if not obj.hide_get())

    # 遍历所有资产类型
    for asset_type in dir(bpy.data):
        if hasattr(getattr(bpy.data, asset_type), "remove"):
            asset_data = getattr(bpy.data, asset_type)
            for asset in asset_data:
                if asset.users == 0 and asset.name not in displayed_objects:
                    # 删除未显示且未使用的资产
                    asset_data.remove(asset)

deleteUnusedAssets()