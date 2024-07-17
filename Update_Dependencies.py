bl_info = {
    "name": "Update Drivers",
    "author": "WPC",
    "version": (1, 2),
    "blender": (4, 1, 0),
    "location": "",
    "description": "Executes code when active camera changes",
    "category": "Development",
}

import bpy
from bpy.app.handlers import persistent

prev_camera = None

def change_target(obj, target):
    try:
        obj.constraints["Track Camera"].target = target
    except KeyError:
        return

def update_driver(d):
        # https://blender.stackexchange.com/questions/118350/how-to-update-the-dependencies-of-a-driver-via-python-script
        d.driver.expression += " "
        d.driver.expression = d.driver.expression[:-1]

def update_dependencies_for(item):
    try:
        drivers = item.animation_data.drivers
        for d in drivers:
            update_driver(d)
    except AttributeError:
        return

@persistent
def update_all_dependencies(scene):
    global prev_camera
    scene_camera = bpy.context.scene.camera
    
    try:
        if scene_camera == prev_camera:
            return
            
        prev_camera = scene_camera
    
        for obj in bpy.data.objects:
            update_dependencies_for(obj)
            change_target(obj, scene_camera)
    
        for node in bpy.data.node_groups:
            update_dependencies_for(node)
    except:
        return

def register():
    bpy.app.handlers.depsgraph_update_post.append(update_all_dependencies)
    
    bpy.app.handlers.load_post.append(update_all_dependencies)  #?
    
    bpy.app.handlers.render_pre.append(update_all_dependencies)
    
    bpy.app.handlers.frame_change_pre.append(update_all_dependencies)
    
def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(update_all_dependencies)
    
    bpy.app.handlers.load_post.remove(update_all_dependencies)
    
    bpy.app.handlers.render_pre.remove(update_all_dependencies)    
    
    bpy.app.handlers.frame_change_pre.remove(update_all_dependencies)
    
if __name__ == "__main__":
    register()
    #unregister()