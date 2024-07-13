# armature-link
Link one armature to match the other armature pose.

The addon will go through all bones in the source armature and add a copy transforms constrain to each bone in the target armature with the same name.

Unlink will just remove all copy transforms constrains from all bones on the target armature. This can be destructive if you use copy transforms apart from the addon usage.

If you like the addon, feel free to [send a drink](https://buymeacoffee.com/nuemedia).

## Install
1. Download the file armature-link.py.
2. Go to Blender addon settings and Install new addon.
3. Select the file and enable the addon.

## How to use
1. Select the source armature
2. Select the target armature
3. Press Link
