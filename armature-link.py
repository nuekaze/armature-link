# Copyright (C) 2024  Nuekaze, NueMedia
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name": "Armature link",
    "author": "Nuekaze",
    "blender": (4, 1, 0),
    "category": "Animation",
    "location": "View3D > Sidebar"
}

from bpy.types import PropertyGroup, Operator, Panel, Object, Scene
from bpy.props import IntProperty, PointerProperty
from bpy.utils import register_class, unregister_class

class Settings(PropertyGroup):
    source: PointerProperty(name='Source',  type=Object, description='Link bones from this armature.')
    target: PointerProperty(name='Target',  type=Object, description='Appliy link to this armature.')
    ad_counter: IntProperty(name='ad', default=0)

def get_armatures(self, context):
    armatures = []

    for o in context.scene.objects:
        if o.type == 'ARMATURE':
            armatures.append((o.name, o.name, o.name))

    return armatures

class ANIM_OT_armature_link(Operator):
    bl_idname = 'armature_link.link'
    bl_label = 'Link'
    bl_description = 'Go through all bones and make links.'

    @classmethod
    def poll(self, context):
        if context.scene.armature_link.source and context.scene.armature_link.target:
            return True
        return False

    def execute(self, context):
        source = context.scene.armature_link.source
        target = context.scene.armature_link.target

        for b in source.pose.bones:
            skip = False

            try:
                t = target.pose.bones[b.name]
                for c in t.constraints:
                    # Make sure we do not add doubles
                    if c.type == 'COPY_TRANSFORMS':
                        skip = True

                if not skip:
                    m = t.constraints.new('COPY_TRANSFORMS')
                    m.target = source
                    m.subtarget = b.name

            except KeyError:
                pass

        context.scene.armature_link.ad_counter += 1
        return {'FINISHED'}

class ANIM_OT_armature_unlink(Operator):
    bl_idname = 'armature_link.unlink'
    bl_label = 'Unlink'
    bl_description = 'Remove all copy transform modifiers.'

    @classmethod
    def poll(self, context):
        if context.scene.armature_link.source and context.scene.armature_link.target:
            return True
        return False

    def execute(self, context):
        source = context.scene.armature_link.source
        target = context.scene.armature_link.target

        for b in target.pose.bones:
            t = target.pose.bones[b.name]
            for c in t.constraints:
                # Make sure we do not add doubles
                if c.type == 'COPY_TRANSFORMS':
                    t.constraints.remove(c)

        return {'FINISHED'}

class ANIM_PT_armature_link(Panel):
    bl_label = 'Armature link'
    bl_category = 'Armature link'
    bl_idname = 'ANIM_PT_armature_link'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout.column()
        layout.prop(context.scene.armature_link, 'source', icon='ARMATURE_DATA')
        layout.prop(context.scene.armature_link, 'target', icon='ARMATURE_DATA')
        layout.operator('armature_link.link')
        layout.operator('armature_link.unlink')
        
        # Show donation link once.
        if context.scene.armature_link.ad_counter == 10:
            layout.separator()
            layout.label(text='Like the addon?')
            layout.operator("wm.url_open", text="Send a drink!").url = "https://buymeacoffee.com/nuemedia"

def register():
    register_class(ANIM_OT_armature_link)
    register_class(ANIM_OT_armature_unlink)
    register_class(ANIM_PT_armature_link)
    register_class(Settings)
    Scene.armature_link = PointerProperty(type=Settings)

def unregister():
    unregister_class(ANIM_OT_armature_link)
    unregister_class(ANIM_OT_armature_unlink)
    unregister_class(ANIM_PT_armature_link)
    unregister_class(Settings)

if __name__ == '__main__':
    register()
