import bpy


_mods_enum = bpy.types.Modifier.bl_rna.properties['type'].enum_items
# There's' a modifier called "Surface" which needs to be filtered out
# because it's not meant to be seen by users.
ALL_MODIFIERS = [(mod.name, mod.icon, mod.identifier) for mod in _mods_enum
                 if mod.name != "Surface"]


def get_favourite_modifiers_names():
    """List of the names of the favourite modifiers"""
    prefs = bpy.context.preferences.addons["modifier_list"].preferences
    # get correct class attributes and then their values
    attr_list = [attr for attr in dir(prefs) if attr.startswith("modifier_")]
    return [getattr(prefs, attr) for attr in attr_list]


def favourite_modifiers_names_icons_types():
    """Iterator of tuples of the names, icons and types of the favourite
    modifiers.
    """
    mods_enum = bpy.types.Modifier.bl_rna.properties['type'].enum_items
    all_mod_names = [modifier.name for modifier in mods_enum]
    all_mods_dict = dict(zip(all_mod_names, ALL_MODIFIERS))
    fav_mods_list = [all_mods_dict[mod] if mod in all_mods_dict else (None, None, None)
                     for mod in get_favourite_modifiers_names()]
    return iter(fav_mods_list)


# === Don't support show_in_editmode ===
DONT_SUPPORT_SHOW_IN_EDITMODE = {
    'MESH_SEQUENCE_CACHE',
    'BOOLEAN',
    'BUILD',
    'DECIMATE',
    'MULTIRES',
    'CLOTH',
    'COLLISION',
    'DYNAMIC_PAINT',
    'EXPLODE',
    'FLUID_SIMULATION',
    'PARTICLE_SYSTEM',
    'SMOKE',
    'SOFT_BODY'
}

# === Support show_on_cage ===
_deform_mods = {mod for _, _, mod in ALL_MODIFIERS[25:41]}
_other_show_on_cage_mods = {
    'DATA_TRANSFER',
    'NORMAL_EDIT',
    'WEIGHTED_NORMAL',
    'UV_PROJECT',
    'VERTEX_WEIGHT_EDIT',
    'VERTEX_WEIGHT_MIX',
    'VERTEX_WEIGHT_PROXIMITY',
    'ARRAY',
    'EDGE_SPLIT',
    'MASK',
    'MIRROR',
    'SOLIDIFY',
    'SUBSURF',
    'TRIANGULATE'
}
SUPPORT_SHOW_ON_CAGE = _deform_mods.union(_other_show_on_cage_mods)

# === Support use_apply_on_spline ===
SUPPORT_USE_APPLY_ON_SPLINE = {
    'ARMATURE',
    'CAST',
    'CURVE',
    'LATTICE',
    'SHRINKWRAP',
    'SIMPLE_DEFORM',
    'SMOOTH',
    'WARP',
    'WAVE',
}

# === Support apply_as_shape_key ===
_deform_mods = {mod for name, icon, mod in ALL_MODIFIERS[26:42]}
_other_shape_key_mods = {'CLOTH', 'SOFT_BODY', 'MESH_CACHE'}
SUPPORT_APPLY_AS_SHAPE_KEY = _deform_mods.union(_other_shape_key_mods)

# === Don't support copy ===
DONT_SUPPORT_COPY = {
    'CLOTH',
    'COLLISION',
    'DYNAMIC_PAINT',
    'FLUID_SIMULATION',
    'PARTICLE_SYSTEM',
    'SMOKE',
    'SOFT_BODY'
}

# === Have the ability to use an object to define the center of the effect ===
HAVE_GIZMO_PROPERTY = {
    'NORMAL_EDIT': "target",
    'VERTEX_WEIGHT_PROXIMITY': "target",
    'ARRAY': "offset_object",
    'MIRROR': "mirror_object",
    'SCREW': "object",
    'CAST': "object",
    'HOOK': "object",
    'LATTICE': "object",
    'SIMPLE_DEFORM': "origin",
    'WAVE': "start_position_object"
}

# === Mesh modifiers by categories ===
_mods = ALL_MODIFIERS

_modify_end = next(_mods.index(mod) + 1 for mod in _mods if mod[0] == "Vertex Weight Proximity")
_gen_start = next(_mods.index(mod) for mod in _mods if mod[0] == "Array")

# In Blender 2.82, the Weld modifier was added but it was incorrectly
# placed before Wireframe. That's been fixed in 2.83.
if bpy.app.version[1] == 82:
    _gen_end = next(_mods.index(mod) + 1 for mod in _mods if mod[0] == "Weld")
else:
    _gen_end = next(_mods.index(mod) + 1 for mod in _mods if mod[0] == "Wireframe")

_def_start = next(_mods.index(mod) for mod in _mods if mod[0] == "Armature")
_def_end = next(_mods.index(mod) + 1 for mod in _mods if mod[0] == "Wave")
_sim_start = next(_mods.index(mod) for mod in _mods if mod[0] == "Cloth")
_sim_end = next(_mods.index(mod) + 1 for mod in _mods if mod[0] == "Soft Body")

MESH_MODIFY_NAMES_ICONS_TYPES = [mod for mod in ALL_MODIFIERS[0:_modify_end]]
MESH_GENERATE_NAMES_ICONS_TYPES = [mod for mod in ALL_MODIFIERS[_gen_start:_gen_end]]
MESH_DEFORM_NAMES_ICONS_TYPES = [mod for mod in ALL_MODIFIERS[_def_start:_def_end]]
MESH_SIMULATE_NAMES_ICONS_TYPES = [mod for mod in ALL_MODIFIERS[_sim_start:_sim_end]]

# === Curve, surface and text modifiers by categories ===
CURVE_MODIFY_NAMES_ICONS_TYPES = [
    ('Mesh Cache', 'MOD_MESHDEFORM', 'MESH_CACHE'),
    ('Mesh Sequence Cache', 'MOD_MESHDEFORM', 'MESH_SEQUENCE_CACHE')
]

CURVE_GENERATE_NAMES_ICONS_TYPES = [
    ('Array', 'MOD_ARRAY', 'ARRAY'),
    ('Bevel', 'MOD_BEVEL', 'BEVEL'),
    ('Build', 'MOD_BUILD', 'BUILD'),
    ('Decimate', 'MOD_DECIM', 'DECIMATE'),
    ('Edge Split', 'MOD_EDGESPLIT', 'EDGE_SPLIT'),
    ('Mirror', 'MOD_MIRROR', 'MIRROR'),
    ('Remesh', 'MOD_REMESH', 'REMESH'),
    ('Screw', 'MOD_SCREW', 'SCREW'),
    ('Solidify', 'MOD_SOLIDIFY', 'SOLIDIFY'),
    ('Subdivision Surface', 'MOD_SUBSURF', 'SUBSURF'),
    ('Triangulate', 'MOD_TRIANGULATE', 'TRIANGULATE')
]

if bpy.app.version[1] >= 82:
    CURVE_GENERATE_NAMES_ICONS_TYPES.append(('Weld', 'AUTOMERGE_OFF', 'WELD'))

CURVE_DEFORM_NAMES_ICONS_TYPES = [
    ('Armature', 'MOD_ARMATURE', 'ARMATURE'),
    ('Cast', 'MOD_CAST', 'CAST'),
    ('Curve', 'MOD_CURVE', 'CURVE'),
    ('Hook', 'HOOK', 'HOOK'),
    ('Lattice', 'MOD_LATTICE', 'LATTICE'),
    ('Mesh Deform', 'MOD_MESHDEFORM', 'MESH_DEFORM'),
    ('Shrinkwrap', 'MOD_SHRINKWRAP', 'SHRINKWRAP'),
    ('Simple Deform', 'MOD_SIMPLEDEFORM', 'SIMPLE_DEFORM'),
    ('Smooth', 'MOD_SMOOTH', 'SMOOTH'),
    ('Warp', 'MOD_WARP', 'WARP'),
    ('Wave', 'MOD_WAVE', 'WAVE')
]

CURVE_SIMULATE_NAMES_ICONS_TYPES = [
    ('Soft Body', 'MOD_SOFT', 'SOFT_BODY')
]

CURVE_ALL_NAMES_ICONS_TYPES = (
    CURVE_MODIFY_NAMES_ICONS_TYPES
    + CURVE_GENERATE_NAMES_ICONS_TYPES
    + CURVE_DEFORM_NAMES_ICONS_TYPES
    + CURVE_SIMULATE_NAMES_ICONS_TYPES
)

# === Lattice modifiers by categories ===
LATTICE_MODIFY_NAMES_ICONS_TYPES = (
    ('Mesh Cache', 'MOD_MESHDEFORM', 'MESH_CACHE'),
)

LATTICE_DEFORM_NAMES_ICONS_TYPES = (
    ('Armature', 'MOD_ARMATURE', 'ARMATURE'),
    ('Cast', 'MOD_CAST', 'CAST'),
    ('Curve', 'MOD_CURVE', 'CURVE'),
    ('Hook', 'HOOK', 'HOOK'),
    ('Lattice', 'MOD_LATTICE', 'LATTICE'),
    ('Mesh Deform', 'MOD_MESHDEFORM', 'MESH_DEFORM'),
    ('Shrinkwrap', 'MOD_SHRINKWRAP', 'SHRINKWRAP'),
    ('Simple Deform', 'MOD_SIMPLEDEFORM', 'SIMPLE_DEFORM'),
    ('Warp', 'MOD_WARP', 'WARP'),
    ('Wave', 'MOD_WAVE', 'WAVE'),
)

LATTICE_SIMULATE_NAMES_ICONS_TYPES = (
    ('Soft Body', 'MOD_SOFT', 'SOFT_BODY'),
)

LATTICE_ALL_NAMES_ICONS_TYPES = (
    LATTICE_MODIFY_NAMES_ICONS_TYPES
    + LATTICE_DEFORM_NAMES_ICONS_TYPES
    + LATTICE_SIMULATE_NAMES_ICONS_TYPES
)
