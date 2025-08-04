# TouchDesigner Parameter Reference Guide

This comprehensive reference documents all parameter types, ranges, and valid values for TouchDesigner operators. This guide serves as a technical reference for the TD Network Creator mode to ensure valid parameter configurations.

## Table of Contents

1. [TOP (Texture Operators) Parameters](#top-texture-operators-parameters)
2. [CHOP (Channel Operators) Parameters](#chop-channel-operators-parameters)
3. [SOP (Surface Operators) Parameters](#sop-surface-operators-parameters)
4. [DAT (Data Operators) Parameters](#dat-data-operators-parameters)
5. [MAT (Material Operators) Parameters](#mat-material-operators-parameters)
6. [COMP (Component Operators) Parameters](#comp-component-operators-parameters)
7. [Parameter Types Reference](#parameter-types-reference)
8. [Parameter Modes](#parameter-modes)

---

## TOP (Texture Operators) Parameters

### Common TOP Parameters

All TOPs share these fundamental parameters:

#### Resolution
- **Parameter**: `resolution`
- **Type**: Menu
- **Options**: 
  - `'256'`, `'512'`, `'1024'`, `'2048'`, `'4096'`
  - `'1920x1080'`, `'1280x720'`, `'3840x2160'`
  - `'custom'` (uses resolutionw/resolutionh)
  - `'inputfit'` (matches input resolution)
- **Default**: `'256'`

#### Custom Resolution
- **Parameters**: `resolutionw`, `resolutionh`
- **Type**: Integer
- **Range**: 1 to 16384
- **Default**: 256

#### Pixel Format
- **Parameter**: `format`
- **Type**: Menu
- **Options**:
  - `'rgba8fixed'` - 8-bit RGBA (0-1 range)
  - `'rgba16float'` - 16-bit float RGBA
  - `'rgba32float'` - 32-bit float RGBA
  - `'r8fixed'` - 8-bit single channel
  - `'r16float'` - 16-bit float single channel
  - `'r32float'` - 32-bit float single channel
  - `'rg8fixed'` - 8-bit RG channels
  - `'rg16float'` - 16-bit float RG channels
  - `'rg32float'` - 32-bit float RG channels
- **Default**: `'rgba8fixed'`

#### Filter Mode
- **Parameter**: `filtertype`
- **Type**: Menu
- **Options**:
  - `'nearest'` - No interpolation
  - `'linear'` - Linear interpolation
  - `'mipmap'` - Mipmapped filtering
- **Default**: `'linear'`

#### Extend Mode
- **Parameter**: `extendmode`
- **Type**: Menu
- **Options**:
  - `'hold'` - Clamp to edge
  - `'zero'` - Black outside bounds
  - `'repeat'` - Tile texture
  - `'mirror'` - Mirror at edges
- **Default**: `'hold'`

### Noise TOP Parameters

```python
# Example parameter configuration
noise_params = {
    'type': 'sparse',  # Options: 'sparse', 'hermite', 'hardsparse', 'random', 'alligator', 'perlin'
    'seed': 1,         # Integer: 0-65535
    'period': 1.0,     # Float: 0.001-1000
    'amplitude': 1.0,  # Float: -10 to 10
    'offset': 0.0,     # Float: -10 to 10
    'monochrome': 0,   # Toggle: 0 or 1
    'outputaspect': 1  # Toggle: 0 or 1
}
```

### Blur TOP Parameters

```python
blur_params = {
    'size': 1.0,       # Float: 0-100
    'sizex': 1.0,      # Float: 0-100
    'sizey': 1.0,      # Float: 0-100
    'filter': 'gauss', # Options: 'gauss', 'box', 'bartlett', 'radial'
    'extend': 'hold',  # Options: 'hold', 'zero', 'repeat', 'mirror'
    'passes': 1        # Integer: 1-10
}
```

### Composite TOP Parameters

```python
composite_params = {
    'operand': 'over',     # Options: 'over', 'under', 'add', 'subtract', 'multiply', 'screen', 'difference'
    'preaddmult': 1.0,     # Float: -10 to 10
    'postaddmult': 1.0,    # Float: -10 to 10
    'alignpixels': 0,      # Toggle: 0 or 1
    'operand1alpha': 1.0,  # Float: 0-1
    'operand2alpha': 1.0   # Float: 0-1
}
```

### Transform TOP Parameters

```python
transform_params = {
    'tx': 0.0,         # Float: -10 to 10
    'ty': 0.0,         # Float: -10 to 10
    'sx': 1.0,         # Float: 0.001 to 10
    'sy': 1.0,         # Float: 0.001 to 10
    'rotate': 0.0,     # Float: -360 to 360
    'pivotx': 0.5,     # Float: 0 to 1
    'pivoty': 0.5,     # Float: 0 to 1
    'extend': 'hold'   # Options: 'hold', 'zero', 'repeat', 'mirror'
}
```

---

## CHOP (Channel Operators) Parameters

### Common CHOP Parameters

#### Time Slice
- **Parameter**: `timeslice`
- **Type**: Toggle
- **Values**: 0 (Off), 1 (On)
- **Default**: 0

#### Sample Rate
- **Parameter**: `rate`
- **Type**: Float
- **Range**: 0.001 to 1000000
- **Default**: 60

#### Start/End
- **Parameters**: `start`, `end`
- **Type**: Float
- **Range**: -1000000 to 1000000
- **Default**: 0, 1

#### Extend Conditions
- **Parameters**: `left`, `right`
- **Type**: Menu
- **Options**:
  - `'hold'` - Hold first/last value
  - `'slope'` - Continue slope
  - `'cycle'` - Loop values
  - `'mirror'` - Mirror values
  - `'default'` - Use default value
- **Default**: `'hold'`

### Audio Device In CHOP Parameters

```python
audio_in_params = {
    'device': 0,           # Integer: Device index
    'channels': 2,         # Integer: 1-32
    'queuesize': 0.02,     # Float: 0.001-1 (seconds)
    'buffersize': 256,     # Integer: 64-4096
    'rate': 44100          # Integer: 8000, 11025, 22050, 44100, 48000, 96000
}
```

### LFO CHOP Parameters

```python
lfo_params = {
    'type': 'sin',         # Options: 'sin', 'square', 'ramp', 'triangle', 'pulse', 'random'
    'frequency': 1.0,      # Float: 0.001-1000
    'amplitude': 1.0,      # Float: -10 to 10
    'offset': 0.0,         # Float: -10 to 10
    'phase': 0.0,          # Float: 0-1
    'pulsewidth': 0.5,     # Float: 0-1 (for pulse type)
    'seed': 1              # Integer: 0-65535 (for random type)
}
```

### Pattern CHOP Parameters

```python
pattern_params = {
    'type': 'ramp',        # Options: 'ramp', 'step', 'random', 'sine', 'cosine', 'triangle'
    'length': 600,         # Integer: 1-100000 (samples)
    'cycles': 1,           # Integer: 1-1000
    'step': 1,             # Integer: 1-1000 (for step type)
    'amplitude': 1.0,      # Float: -10 to 10
    'offset': 0.0,         # Float: -10 to 10
    'seed': 1              # Integer: 0-65535 (for random)
}
```

### Math CHOP Parameters

```python
math_chop_params = {
    'preoff': 0.0,         # Float: -10 to 10
    'gain': 1.0,           # Float: -10 to 10
    'postoff': 0.0,        # Float: -10 to 10
    'chopop': 'add',       # Options: 'add', 'subtract', 'multiply', 'divide', 'average', 'maximum', 'minimum'
    'matchby': 'channel',  # Options: 'channel', 'index'
    'align': 'start'       # Options: 'start', 'end', 'stretch'
}
```

---

## SOP (Surface Operators) Parameters

### Common SOP Parameters

#### Transform Parameters
- **Position**: `tx`, `ty`, `tz` (Float: -1000 to 1000)
- **Rotation**: `rx`, `ry`, `rz` (Float: -360 to 360)
- **Scale**: `sx`, `sy`, `sz` (Float: 0.001 to 100)
- **Uniform Scale**: `scale` (Float: 0.001 to 100)
- **Pivot**: `px`, `py`, `pz` (Float: -1000 to 1000)

### Geometry Attributes

```python
# Common attributes that can be created/modified
attributes = {
    'P': 'position',       # vec3: vertex position
    'N': 'normal',         # vec3: vertex normal
    'uv': 'texture',       # vec3: texture coordinates
    'Cd': 'color',         # vec4: vertex color
    'Alpha': 'alpha',      # float: vertex alpha
    'pscale': 'scale'      # float: point scale for instancing
}
```

### Box SOP Parameters

```python
box_params = {
    'sizex': 1.0,          # Float: 0.001-100
    'sizey': 1.0,          # Float: 0.001-100
    'sizez': 1.0,          # Float: 0.001-100
    'divsx': 1,            # Integer: 1-100
    'divsy': 1,            # Integer: 1-100
    'divsz': 1,            # Integer: 1-100
    'consolidatecorners': 1 # Toggle: 0 or 1
}
```

### Sphere SOP Parameters

```python
sphere_params = {
    'type': 'polygon',     # Options: 'polygon', 'mesh', 'bezier', 'primitive'
    'radx': 1.0,           # Float: 0.001-100
    'rady': 1.0,           # Float: 0.001-100
    'radz': 1.0,           # Float: 0.001-100
    'rows': 13,            # Integer: 3-100
    'cols': 24,            # Integer: 3-100
    'imperfect': 0         # Toggle: 0 or 1
}
```

### Noise SOP Parameters

```python
noise_sop_params = {
    'type': 'sparse',      # Options: 'sparse', 'hermite', 'hardsparse', 'simplex'
    'amplitude': 0.5,      # Float: 0-10
    'elementsize': 1.0,    # Float: 0.001-100
    'offset': 0.0,         # Float: -100 to 100
    'harmonics': 1,        # Integer: 1-10
    'roughness': 0.5,      # Float: 0-1
    'exponent': 1.0        # Float: 0.1-10
}
```

---

## DAT (Data Operators) Parameters

### Common DAT Parameters

#### Language Settings
- **Parameter**: `language`
- **Type**: Menu
- **Options**: `'python'`, `'tscript'`
- **Default**: `'python'`

#### Execution Mode
- **Parameter**: `executemode`
- **Type**: Menu
- **Options**:
  - `'automatic'` - Execute on input change
  - `'manual'` - Execute on pulse
  - `'eachframe'` - Execute every frame
- **Default**: `'automatic'`

### Table DAT Parameters

```python
table_params = {
    'rows': 10,            # Integer: 0-10000
    'cols': 10,            # Integer: 0-10000
    'rownames': 0,         # Toggle: 0 or 1
    'colnames': 0,         # Toggle: 0 or 1
    'clear': 0,            # Pulse parameter
    'appendrow': 0,        # Pulse parameter
    'appendcol': 0         # Pulse parameter
}
```

### Text DAT Parameters

```python
text_params = {
    'text': '',            # String: multiline text
    'wordwrap': 0,         # Toggle: 0 or 1
    'fontsize': 12,        # Integer: 6-200
    'fontalpha': 1.0,      # Float: 0-1
    'fontcolorr': 1.0,     # Float: 0-1
    'fontcolorg': 1.0,     # Float: 0-1
    'fontcolorb': 1.0      # Float: 0-1
}
```

### Execute DAT Parameters

```python
execute_params = {
    'active': 1,           # Toggle: 0 or 1
    'executemode': 'automatic',  # See execution modes above
    'startscript': '',     # Python code string
    'createscript': '',    # Python code string
    'exitscript': '',      # Python code string
    'framestart': '',      # Python code string
    'frameend': ''         # Python code string
}
```

### Callback Types

```python
# Common callbacks for DATs
callbacks = {
    'onTableChange': 'def onTableChange(dat): pass',
    'onRowChange': 'def onRowChange(dat, rows): pass',
    'onColChange': 'def onColChange(dat, cols): pass',
    'onCellChange': 'def onCellChange(dat, cells, prev): pass',
    'onCreate': 'def onCreate(dat): pass',
    'onRemove': 'def onRemove(dat): pass'
}
```

---

## MAT (Material Operators) Parameters

### Common MAT Parameters

#### Shader Model
- **Parameter**: `shadermodel`
- **Type**: Menu
- **Options**: `'phong'`, `'pbr'`, `'constant'`, `'wireframe'`
- **Default**: `'phong'`

### Phong MAT Parameters

```python
phong_params = {
    # Diffuse
    'diffuser': 1.0,       # Float: 0-1
    'diffuseg': 1.0,       # Float: 0-1
    'diffuseb': 1.0,       # Float: 0-1
    
    # Specular
    'specularr': 1.0,      # Float: 0-1
    'specularg': 1.0,      # Float: 0-1
    'specularb': 1.0,      # Float: 0-1
    'shininess': 40.0,     # Float: 0-128
    
    # Ambient
    'ambientr': 0.0,       # Float: 0-1
    'ambientg': 0.0,       # Float: 0-1
    'ambientb': 0.0,       # Float: 0-1
    
    # Emission
    'emitr': 0.0,          # Float: 0-10
    'emitg': 0.0,          # Float: 0-10
    'emitb': 0.0,          # Float: 0-10
    
    # Maps
    'diffusemap': '',      # TOP path
    'specularmap': '',     # TOP path
    'normalmap': '',       # TOP path
    'bumpmap': '',         # TOP path
    
    # Settings
    'shadeless': 0,        # Toggle: 0 or 1
    'wireframe': 0,        # Toggle: 0 or 1
    'cullface': 1          # Toggle: 0 or 1
}
```

### PBR MAT Parameters

```python
pbr_params = {
    # Base Color
    'basecolorr': 1.0,     # Float: 0-1
    'basecolorg': 1.0,     # Float: 0-1
    'basecolorb': 1.0,     # Float: 0-1
    
    # Material Properties
    'metallic': 0.0,       # Float: 0-1
    'roughness': 0.5,      # Float: 0-1
    'ambientocclusion': 1.0, # Float: 0-1
    
    # Maps
    'basecolormap': '',    # TOP path
    'metallicmap': '',     # TOP path
    'roughnessmap': '',    # TOP path
    'normalmap': '',       # TOP path
    'heightmap': '',       # TOP path
    'aomap': '',           # TOP path
    
    # Advanced
    'ior': 1.5,            # Float: 1-3 (Index of Refraction)
    'subsurface': 0.0,     # Float: 0-1
    'clearcoat': 0.0,      # Float: 0-1
    'clearcoatroughness': 0.0  # Float: 0-1
}
```

### GLSL MAT Parameters

```python
glsl_mat_params = {
    'vertexshader': '',    # DAT path to vertex shader
    'pixelshader': '',     # DAT path to pixel shader
    'outputshader': '',    # DAT path to output shader
    'numsamplers': 0,      # Integer: 0-16
    'nummatrices': 0,      # Integer: 0-16
    'numvectors': 0        # Integer: 0-32
}
```

---

## COMP (Component Operators) Parameters

### Common COMP Parameters

#### Panel Settings
- **Parameter**: `panelw`, `panelh`
- **Type**: Integer
- **Range**: 1 to 16384
- **Default**: 100

#### Display
- **Parameter**: `display`
- **Type**: Toggle
- **Values**: 0 (Off), 1 (On)
- **Default**: 1

### Container COMP Parameters

```python
container_params = {
    # Size
    'w': 100,              # Integer: 1-16384
    'h': 100,              # Integer: 1-16384
    
    # Position
    'alignorder': 0,       # Integer: 0-10
    'sidealign': 0,        # Menu: 0=left, 1=center, 2=right
    'topalign': 0,         # Menu: 0=top, 1=middle, 2=bottom
    
    # Appearance
    'bgcolorr': 0.1,       # Float: 0-1
    'bgcolorg': 0.1,       # Float: 0-1
    'bgcolorb': 0.1,       # Float: 0-1
    'bgalpha': 1.0,        # Float: 0-1
    
    # Border
    'bordercolorr': 0.7,   # Float: 0-1
    'bordercolorg': 0.7,   # Float: 0-1
    'bordercolorb': 0.7,   # Float: 0-1
    'borderalpha': 1.0,    # Float: 0-1
    'borderwidth': 1,      # Integer: 0-10
    
    # Children
    'children': 1,         # Toggle: 0 or 1
    'display': 1           # Toggle: 0 or 1
}
```

### Window COMP Parameters

```python
window_params = {
    # Window Settings
    'winoffsetu': 0,       # Integer: -10000 to 10000
    'winoffsetv': 0,       # Integer: -10000 to 10000
    'winsizeu': 1280,      # Integer: 1-16384
    'winsizev': 720,       # Integer: 1-16384
    
    # Display
    'fullscreen': 0,       # Toggle: 0 or 1
    'borders': 1,          # Toggle: 0 or 1
    'ontop': 0,            # Toggle: 0 or 1
    'winclose': 1,         # Toggle: 0 or 1
    
    # Performance
    'fps': 60,             # Float: 1-1000
    'vsync': 1,            # Toggle: 0 or 1
    'gpumemclear': 1       # Toggle: 0 or 1
}
```

### Geo COMP Parameters

```python
geo_params = {
    # Render Settings
    'material': '',        # MAT path
    'render': 1,           # Toggle: 0 or 1
    'drawpriority': 0,     # Integer: -100 to 100
    
    # Transform (inherited from common SOP params)
    'tx': 0.0,             # Float: -1000 to 1000
    'ty': 0.0,             # Float: -1000 to 1000
    'tz': 0.0,             # Float: -1000 to 1000
    'rx': 0.0,             # Float: -360 to 360
    'ry': 0.0,             # Float: -360 to 360
    'rz': 0.0,             # Float: -360 to 360
    'sx': 1.0,             # Float: 0.001 to 100
    'sy': 1.0,             # Float: 0.001 to 100
    'sz': 1.0,             # Float: 0.001 to 100
    
    # Instancing
    'instanceop': '',      # CHOP/DAT/SOP path
    'instancetx': 'tx',    # String: channel name
    'instancety': 'ty',    # String: channel name
    'instancetz': 'tz',    # String: channel name
    'instancerx': 'rx',    # String: channel name
    'instancery': 'ry',    # String: channel name
    'instancerz': 'rz',    # String: channel name
    'instancesx': 'sx',    # String: channel name
    'instancesy': 'sy',    # String: channel name
    'instancesz': 'sz'     # String: channel name
}
```

### Camera COMP Parameters

```python
camera_params = {
    # Position
    'tx': 0.0,             # Float: -1000 to 1000
    'ty': 0.0,             # Float: -1000 to 1000
    'tz': 2.0,             # Float: -1000 to 1000
    
    # Rotation
    'rx': 0.0,             # Float: -360 to 360
    'ry': 0.0,             # Float: -360 to 360
    'rz': 0.0,             # Float: -360 to 360
    
    # Projection
    'projection': 'perspective',  # Options: 'perspective', 'orthographic'
    'fov': 45.0,           # Float: 1-170 (Field of View)
    'near': 0.001,         # Float: 0.0001-1000
    'far': 10.0,           # Float: 0.1-10000
    
    # Look At
    'lookat': '',          # COMP path
    'lookatx': 0.0,        # Float: -1000 to 1000
    'lookaty': 0.0,        # Float: -1000 to 1000
    'lookatz': 0.0,        # Float: -1000 to 1000
    'lookup': 0.0,         # Float: -1 to 1
    'lookupx': 0.0,        # Float: -1 to 1
    'lookupy': 1.0,        # Float: -1 to 1
    'lookupz': 0.0         # Float: -1 to 1
}
```

### Light COMP Parameters

```python
light_params = {
    # Light Type
    'lighttype': 'point',  # Options: 'point', 'cone', 'distant'
    
    # Color
    'dimmer': 1.0,         # Float: 0-10
    'colorr': 1.0,         # Float: 0-1
    'colorg': 1.0,         # Float: 0-1
    'colorb': 1.0,         # Float: 0-1
    
    # Cone Light Specific
    'coneangle': 45.0,     # Float: 0-90
    'conedelta': 10.0,     # Float: 0-90
    'coneroll': 0.0,       # Float: -360 to 360
    
    # Attenuation
    'attenuated': 1,       # Toggle: 0 or 1
    'attenuationstart': 1.0, # Float: 0-1000
    'attenuationend': 10.0,  # Float: 0-1000
    
    # Shadows
    'shadowtype': 0,       # Menu: 0=off, 1=hard, 2=soft
    'shadowblur': 1.0,     # Float: 0-10
    'shadowbias': 0.001    # Float: 0-1
}
```

---

## Parameter Types Reference

### Basic Parameter Types

#### Float Parameters
```python
float_param = {
    'type': 'float',
    'default': 0.0,
    'range': [-10.0, 10.0],  # [min, max]
    'clamp': True,            # Clamp to range
    'normMin': 0.0,           # Normalized slider min
    'normMax': 1.0            # Normalized slider max
}
```

#### Integer Parameters
```python
int_param = {
    'type': 'int',
    'default': 0,
    'range': [0, 100],        # [min, max]
    'clamp': True             # Clamp to range
}
```

#### String Parameters
```python
string_param = {
    'type': 'str',
    'default': '',
    'multiline': False        # Single or multiline
}
```

#### Toggle Parameters
```python
toggle_param = {
    'type': 'toggle',
    'default': 0,             # 0 or 1
    'onLabel': 'On',          # Custom label when on
    'offLabel': 'Off'         # Custom label when off
}
```

#### Menu Parameters
```python
menu_param = {
    'type': 'menu',
    'default': 'option1',
    'menuNames': ['Option 1', 'Option 2', 'Option 3'],
    'menuLabels': ['option1', 'option2', 'option3']
}
```

### Compound Parameter Types

#### XY Parameters
```python
xy_param = {
    'type': 'xy',
    'default': [0.0, 0.0],
    'range': [[-1.0, -1.0], [1.0, 1.0]]
}
```

#### XYZ Parameters
```python
xyz_param = {
    'type': 'xyz',
    'default': [0.0, 0.0, 0.0],
    'range': [[-10.0, -10.0, -10.0], [10.0, 10.0, 10.0]]
}
```

#### RGB Parameters
```python
rgb_param = {
    'type': 'rgb',
    'default': [1.0, 1.0, 1.0],
    'range': [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]
}
```

#### RGBA Parameters
```python
rgba_param = {
    'type': 'rgba',
    'default': [1.0, 1.0, 1.0, 1.0],
    'range': [[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0]]
}
```

### Special Parameter Types

#### File Parameters
```python
file_param = {
    'type': 'file',
    'default': '',
    'fileTypes': ['tox', 'toe', 'jpg', 'png', 'mov'],
    'folder': False           # True for folder selection
}
```

#### OP Parameters
```python
op_param = {
    'type': 'op',
    'default': '',
    'opType': 'TOP',          # Filter by operator type
    'opFilter': '*'           # Wildcard filter
}
```

#### Pulse Parameters
```python
pulse_param = {
    'type': 'pulse',
    'default': 0,             # Always 0
    'momentary': True         # Auto-reset after pulse
}
```

### Python Expressions in Parameters

Parameters can contain Python expressions when in expression mode:

```python
# Time-based expressions
'absTime.frame'           # Current frame number
'absTime.seconds'         # Time in seconds
'me.time.frame'          # Local time frame
'me.time.seconds'        # Local time seconds

# Operator references
'op("noise1").par.amplitude'  # Reference another op's parameter
'parent().par.w'              # Parent's parameter
'me.par.tx'                   # Self parameter reference

# Channel references
'op("pattern1")[0]'           # First sample of channel 0
'op("pattern1")["chan1"][5]'  # Sample 5 of named channel

# Math expressions
'sin(absTime.seconds * 2)'    # Sine wave over time
'noise(me.time.seconds, 0.5)' # Noise function
'fit(op("lfo1")[0], -1, 1, 0, 100)'  # Remap range

# Conditional expressions
'1 if me.par.toggle else 0'   # Conditional value
```

---

## Parameter Modes

### Constant Mode
- Default mode for all parameters
- Fixed value entered directly
- No evaluation or cooking required
- Most efficient for static values

### Expression Mode
- Python expressions evaluated every cook
- Access to TD expression functions
- Can reference other operators
- Updates automatically when dependencies change

```python
# Enable expression mode
op('myop').par.tx.mode = ParMode.EXPRESSION
op('myop').par.tx.expr = 'sin(absTime.seconds)'
```

### Export Mode
- Parameter driven by CHOP channel
- Real-time updates from channel data
- Useful for animation and control

```python
# Set up export
op('myop').par.tx.mode = ParMode.EXPORT
op('myop').par.tx.export = op('lfo1')
```

### Bind Mode
- Two-way connection between parameters
- Changes in one update the other
- Useful for UI controls and synchronized parameters

```python
# Set up bind
op('slider1').par.value.mode = ParMode.BIND
op('slider1').par.value.bindExpr = 'op("constant1").par.value'
```

### Sequence Mode
- Parameter controlled by animation curves
- Keyframe-based animation
- Used primarily in Animation COMP

---

## Parameter Validation Examples

### Validating Parameter Values

```python
def validate_resolution(value):
    """Validate resolution parameter value"""
    valid_resolutions = ['256', '512', '1024', '2048', '4096',
                        '1920x1080', '1280x720', '3840x2160',
                        'custom', 'inputfit']
    return value in valid_resolutions

def validate_pixel_format(value):
    """Validate pixel format parameter value"""
    valid_formats = ['rgba8fixed', 'rgba16float', 'rgba32float',
                    'r8fixed', 'r16float', 'r32float',
                    'rg8fixed', 'rg16float', 'rg32float']
    return value in valid_formats

def validate_range(value, min_val, max_val, param_type='float'):
    """Validate parameter is within range"""
    if param_type == 'float':
        return min_val <= float(value) <= max_val
    elif param_type == 'int':
        return min_val <= int(value) <= max_val
    return False

def validate_menu_option(value, valid_options):
    """Validate menu parameter value"""
    return value in valid_options
```

### Common Parameter Patterns

```python
# Time-based animation
time_params = {
    'speed': 1.0,          # Animation speed multiplier
    'offset': 0.0,         # Time offset
    'loop': 1,             # Enable looping
    'palindrome': 0        # Ping-pong animation
}

# Color parameters with alpha
color_params = {
    'colorr': 1.0,         # Red component (0-1)
    'colorg': 1.0,         # Green component (0-1)
    'colorb': 1.0,         # Blue component (0-1)
    'alpha': 1.0           # Alpha component (0-1)
}

# Transform parameter group
transform_group = {
    'translate': ['tx', 'ty', 'tz'],
    'rotate': ['rx', 'ry', 'rz'],
    'scale': ['sx', 'sy', 'sz'],
    'pivot': ['px', 'py', 'pz'],
    'uniformscale': 'scale'
}

# Input/Output configuration
io_params = {
    'input': '',           # Input operator path
    'input2': '',          # Secondary input
    'output': '',          # Output operator path
    'bypass': 0,           # Bypass processing
    'cache': 0             # Enable caching
}
```

### Parameter Dependencies

Some parameters only apply when others have specific values:

```python
# Example: Noise TOP dependencies
noise_dependencies = {
    'monochrome': {
        'enabled_when': {'type': ['sparse', 'hermite', 'perlin']},
        'disabled_when': {'type': ['random']}
    },
    'harmonics': {
        'enabled_when': {'type': ['sparse', 'hermite', 'perlin']},
        'range_when': {
            'type=sparse': [1, 10],
            'type=perlin': [1, 8]
        }
    }
}

# Example: Resolution dependencies
resolution_dependencies = {
    'resolutionw': {
        'enabled_when': {'resolution': 'custom'}
    },
    'resolutionh': {
        'enabled_when': {'resolution': 'custom'}
    }
}
```

### Performance Considerations

```python
# GPU-friendly parameter ranges
gpu_optimal = {
    'resolution': [256, 512, 1024, 2048],  # Powers of 2
    'format': 'rgba16float',               # Good balance
    'samples': [1, 2, 4, 8, 16],          # Power of 2 samples
    'blur_passes': [1, 2, 3],             # Limit passes
    'instance_count': 10000                # Reasonable limit
}

# CPU-intensive parameters to watch
cpu_intensive = {
    'python_cooking': 'Avoid per-frame Python execution',
    'table_size': 'Large tables (>10000 cells) impact performance',
    'file_io': 'Minimize file reads/writes per frame',
    'resolution_changes': 'Changing resolution causes reallocation'
}
```

## Quick Reference Tables

### TOP Resolution Presets
| Preset | Width | Height | Aspect Ratio |
|--------|-------|--------|--------------|
| 256 | 256 | 256 | 1:1 |
| 512 | 512 | 512 | 1:1 |
| 1024 | 1024 | 1024 | 1:1 |
| 2048 | 2048 | 2048 | 1:1 |
| 4096 | 4096 | 4096 | 1:1 |
| 1280x720 | 1280 | 720 | 16:9 |
| 1920x1080 | 1920 | 1080 | 16:9 |
| 3840x2160 | 3840 | 2160 | 16:9 |

### CHOP Sample Rates
| Rate | Use Case |
|------|----------|
| 24 | Film frame rate |
| 30 | NTSC video |
| 60 | Real-time graphics |
| 120 | High-speed tracking |
| 44100 | CD-quality audio |
| 48000 | Professional audio |
| 96000 | High-resolution audio |

### Common Parameter Expressions
| Expression | Description | Example |
|------------|-------------|---------|
| `absTime.seconds` | Absolute time in seconds | `sin(absTime.seconds * 2)` |
| `me.time.frame` | Local frame number | `me.time.frame % 100` |
| `op('name')[0]` | CHOP channel value | `op('lfo1')[0]` |
| `parent().par.name` | Parent parameter | `parent().par.w` |
| `fit(val, inMin, inMax, outMin, outMax)` | Remap range | `fit(op('lfo1')[0], -1, 1, 0, 100)` |
| `noise(x, y, z)` | Perlin noise | `noise(me.time.seconds, 0, 0)` |
| `project.cookRate` | Project frame rate | `me.time.seconds * project.cookRate` |

## Best Practices

1. **Parameter Naming**
   - Use lowercase for parameter names
   - Use underscores for multi-word parameters
   - Be consistent with TouchDesigner conventions

2. **Default Values**
   - Always provide sensible defaults
   - Consider the most common use case
   - Ensure defaults produce visible results

3. **Range Selection**
   - Use normalized ranges (0-1) when possible
   - Provide adequate headroom for values
   - Consider both artistic and technical needs

4. **Expression Safety**
   - Validate expressions before setting
   - Handle division by zero
   - Provide fallback values

5. **Performance**
   - Minimize parameter changes per frame
   - Use constants for static values
   - Batch parameter updates when possible

## Common Pitfalls

1. **String Parameters**
   - Empty strings can cause errors
   - Path parameters need validation
   - Case sensitivity in operator names

2. **Float Precision**
   - Rounding errors in calculations
   - Display vs actual precision
   - Comparison tolerance needed

3. **Menu Parameters**
   - Menu options are case-sensitive
   - Invalid options revert to default
   - Menu indices vs menu names

4. **Expression Mode**
   - Syntax errors stop cooking
   - Circular dependencies cause errors
   - Performance impact of complex expressions

## Parameter Access in Python

```python
# Reading parameters
value = op('noise1').par.amplitude.eval()
raw_value = op('noise1').par.amplitude.val

# Setting parameters
op('noise1').par.amplitude = 2.0
op('noise1').par.amplitude.val = 2.0

# Setting expressions
op('noise1').par.amplitude.expr = 'sin(absTime.seconds)'
op('noise1').par.amplitude.mode = ParMode.EXPRESSION

# Pulsing parameters
op('moviefilein1').par.reload.pulse()

# Accessing all parameters
for par in op('noise1').pars():
    print(f"{par.name}: {par.eval()}")

# Parameter groups
transform_pars = op('geo1').pars('t*')  # All translate params
color_pars = op('constant1').pars('color*')  # All color params

# Custom parameters
page = op('base1').appendCustomPage('Custom')
page.appendFloat('Customfloat', label='Custom Float', size=1)
page.appendToggle('Customtoggle', label='Custom Toggle')
page.appendMenu('Custommenu', label='Custom Menu',
                menuNames=['Option1', 'Option2'],
                menuLabels=['option1', 'option2'])
```

## Conclusion

This parameter reference provides comprehensive coverage of TouchDesigner's parameter system. Use it as a guide when creating networks programmatically to ensure valid parameter values and optimal performance. Remember that parameters can interact in complex ways, so always test your parameter configurations in the actual TouchDesigner environment.

For the most up-to-date parameter information, consult the TouchDesigner documentation or use the TD MCP Server's operator information tools.