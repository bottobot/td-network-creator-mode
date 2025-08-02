"""
Color Gradient GLSL Shader Network for TouchDesigner
Creates various gradient types with customizable color palettes
"""

# The GLSL shader code for gradient generation
COLOR_GRADIENT_GLSL = '''
// Multi-type Color Gradient Generator for TouchDesigner
// Supports linear, radial, angular, and diamond gradients

// Gradient type selection
uniform int uGradientType;     // 0=Linear, 1=Radial, 2=Angular, 3=Diamond, 4=Spiral
uniform vec2 uCenter;          // Center point for radial/angular gradients
uniform float uAngle;          // Angle for linear gradient (in radians)
uniform float uScale;          // Scale factor for the gradient
uniform float uOffset;         // Offset/phase for the gradient
uniform float uPower;          // Power curve for gradient falloff
uniform int uRepeat;           // Number of repetitions
uniform int uMirror;           // 0=No mirror, 1=Mirror gradient

// Color palette uniforms (up to 5 colors)
uniform vec4 uColor0;          // First color (RGBA)
uniform vec4 uColor1;          // Second color
uniform vec4 uColor2;          // Third color
uniform vec4 uColor3;          // Fourth color
uniform vec4 uColor4;          // Fifth color
uniform int uColorCount;       // Number of active colors (2-5)

// Blending parameters
uniform float uSmoothness;     // Smoothness of color transitions
uniform int uInterpolation;    // 0=Linear, 1=Smooth, 2=Cubic

// Output
out vec4 fragColor;

// Smooth interpolation function
float smoothInterpolate(float t) {
    return t * t * (3.0 - 2.0 * t);
}

// Cubic interpolation function
float cubicInterpolate(float t) {
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}

// Apply interpolation based on mode
float applyInterpolation(float t, int mode) {
    if (mode == 1) return smoothInterpolate(t);
    else if (mode == 2) return cubicInterpolate(t);
    return t; // Linear
}

// Calculate gradient value based on type
float calculateGradient(vec2 uv) {
    float value = 0.0;
    
    if (uGradientType == 0) {
        // Linear gradient
        vec2 dir = vec2(cos(uAngle), sin(uAngle));
        value = dot(uv - vec2(0.5), dir) + 0.5;
    }
    else if (uGradientType == 1) {
        // Radial gradient
        value = length(uv - uCenter) * 2.0;
    }
    else if (uGradientType == 2) {
        // Angular gradient
        vec2 delta = uv - uCenter;
        value = atan(delta.y, delta.x) / (2.0 * 3.14159265359) + 0.5;
    }
    else if (uGradientType == 3) {
        // Diamond gradient
        vec2 delta = abs(uv - uCenter);
        value = max(delta.x, delta.y) * 2.0;
    }
    else if (uGradientType == 4) {
        // Spiral gradient
        vec2 delta = uv - uCenter;
        float angle = atan(delta.y, delta.x);
        float radius = length(delta);
        value = fract(angle / (2.0 * 3.14159265359) + radius * 2.0);
    }
    
    // Apply scale and offset
    value = value * uScale + uOffset;
    
    // Apply repetition
    if (uRepeat > 1) {
        value = fract(value * float(uRepeat));
    }
    
    // Apply mirroring
    if (uMirror == 1) {
        value = 1.0 - abs(1.0 - 2.0 * value);
    }
    
    // Apply power curve
    value = pow(clamp(value, 0.0, 1.0), uPower);
    
    return value;
}

// Multi-color gradient mixing
vec4 mixColors(float t) {
    // Ensure t is in valid range
    t = clamp(t, 0.0, 1.0);
    
    // Array of colors
    vec4 colors[5];
    colors[0] = uColor0;
    colors[1] = uColor1;
    colors[2] = uColor2;
    colors[3] = uColor3;
    colors[4] = uColor4;
    
    // Calculate position in gradient
    float scaledT = t * float(uColorCount - 1);
    int index = int(floor(scaledT));
    float localT = fract(scaledT);
    
    // Apply smoothness
    localT = mix(localT, applyInterpolation(localT, uInterpolation), uSmoothness);
    
    // Clamp index to valid range
    index = clamp(index, 0, uColorCount - 2);
    
    // Mix between adjacent colors
    return mix(colors[index], colors[index + 1], localT);
}

void main() {
    vec2 uv = vUV.st;
    
    // Calculate gradient value
    float gradientValue = calculateGradient(uv);
    
    // Get color from palette
    vec4 color = mixColors(gradientValue);
    
    // Output final color
    fragColor = color;
}
'''

def create_color_gradient_network():
    """
    Creates a color gradient network with multiple gradient types and controls
    Returns the main container COMP
    """
    
    # Create main container
    container = op('/project1').create(containerCOMP, 'color_gradient')
    container.nodeX = 0
    container.nodeY = -400
    container.nodeWidth = 250
    container.nodeHeight = 200
    
    # Create GLSL TOP for gradient generation
    glsl_top = container.create(glslTOP, 'gradient_glsl')
    glsl_top.nodeX = 0
    glsl_top.nodeY = 0
    glsl_top.par.resolution1 = 1920
    glsl_top.par.resolution2 = 1080
    glsl_top.par.pixelformat = 'rgba16float'
    
    # Set GLSL code
    glsl_top.par.fragmentshader = COLOR_GRADIENT_GLSL
    
    # Create parameter controls container
    params_container = container.create(containerCOMP, 'parameters')
    params_container.nodeX = 300
    params_container.nodeY = 0
    params_container.nodeWidth = 200
    params_container.nodeHeight = 400
    
    # Gradient type menu
    menu_comp = params_container.create(menuCOMP, 'gradient_type')
    menu_comp.nodeX = 0
    menu_comp.nodeY = 350
    menu_comp.par.menunames = 'Linear Radial Angular Diamond Spiral'
    menu_comp.par.default = 'Linear'
    menu_comp.par.label = 'Gradient Type'
    
    # Center point XY slider
    xy_slider = params_container.create(xySliderCOMP, 'center')
    xy_slider.nodeX = 0
    xy_slider.nodeY = 280
    xy_slider.par.default1 = 0.5
    xy_slider.par.default2 = 0.5
    xy_slider.par.min1 = 0
    xy_slider.par.max1 = 1
    xy_slider.par.min2 = 0
    xy_slider.par.max2 = 1
    xy_slider.par.label = 'Center'
    
    # Angle slider
    angle_slider = params_container.create(sliderCOMP, 'angle')
    angle_slider.nodeX = 0
    angle_slider.nodeY = 210
    angle_slider.par.default1 = 0
    angle_slider.par.min1 = -180
    angle_slider.par.max1 = 180
    angle_slider.par.label = 'Angle'
    
    # Scale slider
    scale_slider = params_container.create(sliderCOMP, 'scale')
    scale_slider.nodeX = 0
    scale_slider.nodeY = 160
    scale_slider.par.default1 = 1
    scale_slider.par.min1 = 0.1
    scale_slider.par.max1 = 5
    scale_slider.par.label = 'Scale'
    
    # Offset slider
    offset_slider = params_container.create(sliderCOMP, 'offset')
    offset_slider.nodeX = 0
    offset_slider.nodeY = 110
    offset_slider.par.default1 = 0
    offset_slider.par.min1 = -1
    offset_slider.par.max1 = 1
    offset_slider.par.label = 'Offset'
    
    # Power slider
    power_slider = params_container.create(sliderCOMP, 'power')
    power_slider.nodeX = 0
    power_slider.nodeY = 60
    power_slider.par.default1 = 1
    power_slider.par.min1 = 0.1
    power_slider.par.max1 = 4
    power_slider.par.label = 'Power'
    
    # Repeat slider
    repeat_slider = params_container.create(sliderCOMP, 'repeat')
    repeat_slider.nodeX = 0
    repeat_slider.nodeY = 10
    repeat_slider.par.default1 = 1
    repeat_slider.par.min1 = 1
    repeat_slider.par.max1 = 10
    repeat_slider.par.slidertype = 'int'
    repeat_slider.par.label = 'Repeat'
    
    # Mirror toggle
    toggle_comp = params_container.create(toggleCOMP, 'mirror')
    toggle_comp.nodeX = 0
    toggle_comp.nodeY = -40
    toggle_comp.par.label = 'Mirror'
    
    # Smoothness slider
    smooth_slider = params_container.create(sliderCOMP, 'smoothness')
    smooth_slider.nodeX = 0
    smooth_slider.nodeY = -90
    smooth_slider.par.default1 = 0.5
    smooth_slider.par.min1 = 0
    smooth_slider.par.max1 = 1
    smooth_slider.par.label = 'Smoothness'
    
    # Interpolation menu
    interp_menu = params_container.create(menuCOMP, 'interpolation')
    interp_menu.nodeX = 0
    interp_menu.nodeY = -140
    interp_menu.par.menunames = 'Linear Smooth Cubic'
    interp_menu.par.default = 'Linear'
    interp_menu.par.label = 'Interpolation'
    
    # Create color palette container
    colors_container = container.create(containerCOMP, 'color_palette')
    colors_container.nodeX = 550
    colors_container.nodeY = 0
    colors_container.nodeWidth = 150
    colors_container.nodeHeight = 300
    
    # Create 5 color pickers
    color_pickers = []
    for i in range(5):
        picker = colors_container.create(colorpickerCOMP, f'color{i}')
        picker.nodeX = 0
        picker.nodeY = 200 - (i * 60)
        picker.par.label = f'Color {i+1}'
        
        # Set default colors for a nice gradient
        if i == 0:
            picker.par.default1 = 0.2  # R
            picker.par.default2 = 0.3  # G
            picker.par.default3 = 0.8  # B
        elif i == 1:
            picker.par.default1 = 0.5
            picker.par.default2 = 0.2
            picker.par.default3 = 0.9
        elif i == 2:
            picker.par.default1 = 0.9
            picker.par.default2 = 0.3
            picker.par.default3 = 0.5
        elif i == 3:
            picker.par.default1 = 1.0
            picker.par.default2 = 0.7
            picker.par.default3 = 0.2
        else:
            picker.par.default1 = 0.9
            picker.par.default2 = 0.9
            picker.par.default3 = 0.3
        
        color_pickers.append(picker)
    
    # Color count slider
    count_slider = colors_container.create(sliderCOMP, 'color_count')
    count_slider.nodeX = 0
    count_slider.nodeY = -100
    count_slider.par.default1 = 3
    count_slider.par.min1 = 2
    count_slider.par.max1 = 5
    count_slider.par.slidertype = 'int'
    count_slider.par.label = 'Color Count'
    
    # Create parameter collection CHOPs
    # Gradient type
    type_select = container.create(selectCHOP, 'select_type')
    type_select.nodeX = 0
    type_select.nodeY = -200
    type_select.par.chop = '../parameters/gradient_type/out1'
    type_select.par.channames = 'chan1'
    type_select.par.renameto = 'type'
    
    # Convert angle to radians
    math_chop = container.create(mathCHOP, 'angle_radians')
    math_chop.nodeX = 0
    math_chop.nodeY = -250
    math_chop.par.chop = '../parameters/angle/out1'
    math_chop.par.preoff = 0
    math_chop.par.gain = 3.14159265359/180  # Convert degrees to radians
    
    # Link parameters to GLSL uniforms
    glsl_top.par.uniformname0 = 'uGradientType'
    glsl_top.par.uniformvalue0 = "int(op('../select_type')['type'])"
    
    glsl_top.par.uniformname1 = 'uCenter'
    glsl_top.par.uniformvalue1x = "op('../parameters/center/out1')['u']"
    glsl_top.par.uniformvalue1y = "op('../parameters/center/out1')['v']"
    
    glsl_top.par.uniformname2 = 'uAngle'
    glsl_top.par.uniformvalue2 = "op('../angle_radians')[0]"
    
    glsl_top.par.uniformname3 = 'uScale'
    glsl_top.par.uniformvalue3 = "op('../parameters/scale/out1')[0]"
    
    glsl_top.par.uniformname4 = 'uOffset'
    glsl_top.par.uniformvalue4 = "op('../parameters/offset/out1')[0]"
    
    glsl_top.par.uniformname5 = 'uPower'
    glsl_top.par.uniformvalue5 = "op('../parameters/power/out1')[0]"
    
    glsl_top.par.uniformname6 = 'uRepeat'
    glsl_top.par.uniformvalue6 = "int(op('../parameters/repeat/out1')[0])"
    
    glsl_top.par.uniformname7 = 'uMirror'
    glsl_top.par.uniformvalue7 = "int(op('../parameters/mirror/out1')[0])"
    
    glsl_top.par.uniformname8 = 'uSmoothness'
    glsl_top.par.uniformvalue8 = "op('../parameters/smoothness/out1')[0]"
    
    glsl_top.par.uniformname9 = 'uInterpolation'
    glsl_top.par.uniformvalue9 = "int(op('../parameters/interpolation/out1')[0])"
    
    # Link color uniforms
    for i in range(5):
        base_idx = 10 + i
        glsl_top.par[f'uniformname{base_idx}'] = f'uColor{i}'
        glsl_top.par[f'uniformvalue{base_idx}x'] = f"op('../color_palette/color{i}/out1')['r']"
        glsl_top.par[f'uniformvalue{base_idx}y'] = f"op('../color_palette/color{i}/out1')['g']"
        glsl_top.par[f'uniformvalue{base_idx}z'] = f"op('../color_palette/color{i}/out1')['b']"
        glsl_top.par[f'uniformvalue{base_idx}w'] = "1.0"  # Alpha always 1
    
    glsl_top.par.uniformname15 = 'uColorCount'
    glsl_top.par.uniformvalue15 = "int(op('../color_palette/color_count/out1')[0])"
    
    # Create output
    out_top = container.create(outTOP, 'out1')
    out_top.nodeX = 200
    out_top.nodeY = 0
    out_top.inputConnectors[0].connect(glsl_top.outputConnectors[0])
    
    # Create preview window
    preview = container.create(windowCOMP, 'preview')
    preview.nodeX = 200
    preview.nodeY = -100
    preview.par.winoffsety = 100
    preview.par.winoffsetx = 100
    preview.par.winsizew = 640
    preview.par.winsizeh = 360
    preview.par.drawmethod = 'Clear and Draw'
    preview.par.top = '../gradient_glsl'
    
    return container

# Execute the network creation
if __name__ == '__main__':
    network = create_color_gradient_network()
    print(f"Created color gradient network at: {network.path}")