import bpy
import os

def print(*data):
    # create one string from multiple print parameters
    text = " ".join([str(item) for item in data]) + "\n"
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(text), type="OUTPUT")       


def main(context):
    for ob in context.scene.objects:
        print(ob)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


def change_retina_image(image_full_path, material_name="retina"):
    image_name = os.path.basename(image_full_path)
    bpy.ops.image.open(filepath=image_full_path, files=[{"name":image_name}], show_multiview=False)
    bpy.data.materials[material_name].node_tree.nodes["Image Texture"].image = bpy.data.images[image_name]




def render_scene(render_path):

    # Set the device_type
    bpy.context.preferences.addons[
        "cycles"
    ].preferences.compute_device_type = "CUDA" # or "OPENCL"

    # Set the device and feature set
    bpy.context.scene.cycles.device = "GPU"

    # get_devices() to let Blender detects GPU device
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1 # Using all devices, include GPU and CPU
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    
    render = scene.render
    render.use_file_extension = True
    render.filepath = render_path
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
    retina_plane = bpy.data.objects['retina']
    retina_bg = bpy.data.objects['retina_bg']
    retina_plane.rotation_euler[1] = 2
    
    
    
    
    rotations  = [0]
    distances = [90]
    testing = True

   
    
    src_directory = "C:\\Users\\hsr30\\Documents\\minor-project\\datasets\\disease-grading-custom\\cropped-testing-3500"
    target_directory = "C:\\Users\\hsr30\\Documents\\minor-project\\datasets\\disease-grading-custom\\rendered-testing-3500"
    print(f"Number of files: {len(os.listdir(src_directory))}")
  
    # get all the image names in the src directory
    for index, file in enumerate(os.listdir(src_directory)):
        if testing and index >= 1: break;
        if file.endswith(".jpg"):
            print("Processing: ", file)
            for rotation in rotations:
                for distance in distances:
                    retina_plane.rotation_euler[1] = rotation;
                    retina_plane.location[1] = distance;
                    retina_bg.location[1] = distance + 2;
                    # change the retina image
                    change_retina_image(os.path.join(src_directory, file))
                    # render the scene
                    # get file name without extension
                    file_name = file.split(".")[0] + f"-{rotation}-{distance}-3500.jpg"

                    render_scene(os.path.join(target_directory, file_name))