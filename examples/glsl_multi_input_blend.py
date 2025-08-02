"""
Multi-Input Blending GLSL Shader Network for TouchDesigner
Demonstrates advanced blending of multiple TOP inputs with various blend modes
"""

# The GLSL shader code for multi-input blending
MULTI_INPUT_BLEND_GLSL = '''
// Multi-Input Blending Shader for TouchDesigner
// Blends up to 4 input textures with various blend modes and masks

// Blend mode uniforms for each layer
uniform int uBlendMode1;      // Blend mode for input 1 (0-15)
uniform int uBlendMode2;      // Blend mode for input 2
uniform int uBlendMode3;      // Blend mode for input 3
uniform float uOpacity1;      // Opacity for input 1 (0-1)
uniform float uOpacity2;      // Opacity for input 2
uniform float uOpacity3;      // Opacity for input 3

// Transform uniforms for each input
uniform vec2 uScale1;         // Scale for input 1
uniform vec2 uScale2;         // Scale for input 2
uniform vec2 uScale3;         // Scale for input 3
uniform vec2 uOffset1;        // Offset for input 1
uniform vec2 uOffset2;        // Offset for input 2
uniform vec2 uOffset3;        // Offset for input 3
uniform float uRotation1;     // Rotation for input 1 (radians)
uniform float uRotation2;     // Rotation for input 2
uniform float uRotation3;     // Rotation for input 3

// Color adjustment uniforms
uniform vec3 uTint1;          // Color tint for input 1
uniform vec3 uTint2;          // Color tint for input 2
uniform vec3 uTint3;          // Color tint for input 3
uniform float uContrast;      // Global contrast adjustment
uniform float uBrightness;    // Global brightness adjustment
uniform float uSaturation;    // Global saturation adjustment

// Mask parameters
uniform int uUseMask;         // 0=No mask, 1=Use input 4 as mask
uniform int uMaskChannel;     // Which channel to use as mask (0=R, 1=G, 2=B, 3=A)
uniform int uInvertMask;      // Invert the mask values

// Output
out vec4 fragColor;

// Blend mode functions
vec3 blendNormal(vec3 base, vec3 blend) {
    return blend;
}

vec3 blendMultiply(vec3 base, vec3 blend) {
    return base * blend;
}

vec3 blendScreen(vec3 base, vec3 blend) {
    return 1.0 - (1.0 - base) * (1.0 - blend);
}

vec3 blendOverlay(vec3 base, vec3 blend) {
    return mix(
        2.0 * base * blend,
        1.0 - 2.0 * (1.0 - base) * (1.0 - blend),
        step(0.5, base)
    );
}

vec3 blendSoftLight(vec3 base, vec3 blend) {
    return mix(
        2.0 * base * blend + base * base * (1.0 - 2.0 * blend),
        sqrt(base) * (2.0 * blend - 1.0) + 2.0 * base * (1.0 - blend),
        step(0.5, blend)
    );
}

vec3 blendHardLight(vec3 base, vec3 blend) {
    return blendOverlay(blend, base);
}

vec3 blendColorDodge(vec3 base, vec3 blend) {
    return base / (1.0 - blend + 0.0001);
}

vec3 blendColorBurn(vec3 base, vec3 blend) {
    return 1.0 - (1.0 - base) / (blend + 0.0001);
}

vec3 blendLinearDodge(vec3 base, vec3 blend) {
    return base + blend;
}

vec3 blendLinearBurn(vec3 base, vec3 blend) {
    return base + blend - 1.0;
}

vec3 blendDifference(vec3 base, vec3 blend) {
    return abs(base - blend);
}

vec3 blendExclusion(vec3 base, vec3 blend) {
    return base + blend - 2.0 * base * blend;
}

vec3 blendLighten(vec3 base, vec3 blend) {
    return max(base, blend);
}

vec3 blendDarken(vec3 base, vec3 blend) {
    return min(base, blend);
}

vec3 blendVividLight(vec3 base, vec3 blend) {
    return mix(
        blendColorBurn(base, 2.0 * blend),
        blendColorDodge(base, 2.0 * (blend - 0.5)),
        step(0.5, blend)
    );
}

vec3 blendLinearLight(vec3 base, vec3 blend) {
    return base + 2.0 * blend - 1.0;
}

// Apply blend mode based on index
vec3 applyBlendMode(vec3 base, vec3 blend, int mode) {
    if (mode == 0) return blendNormal(base, blend);
    else if (mode == 1) return blendMultiply(base, blend);
    else if (mode == 2) return blendScreen(base, blend);
    else if (mode == 3) return blendOverlay(base, blend);
    else if (mode == 4) return blendSoftLight(base, blend);
    else if (mode == 5) return blendHardLight(base, blend);
    else if (mode == 6) return blendColorDodge(base, blend);
    else if (mode == 7) return blendColorBurn(base, blend);
    else if (mode == 8) return blendLinearDodge(base, blend);
    else if (mode == 9) return blendLinearBurn(base, blend);
    else if (mode == 10) return blendDifference(base, blend);
    else if (mode == 11) return blendExclusion(base, blend);
    else if (mode == 12) return blendLighten(base, blend);
    else if (mode == 13) return blendDarken(base, blend);
    else if (mode == 14) return blendVividLight(base, blend);
    else if (mode == 15) return blendLinearLight(base, blend);
    return blend; // Default
}

// Transform UV coordinates
vec2 transformUV(vec2 uv, vec2 scale, vec2 offset, float rotation) {
    // Center the UV
    uv -= 0.5;
    
    // Apply scale
    uv /= scale;
    
    // Apply rotation
    float c = cos(rotation);
    float s = sin(rotation);
    mat2 rot = mat2(c, -s, s, c);
    uv = rot * uv;
    
    // Apply offset and recenter
    uv += 0.5 + offset;
    
    return uv;
}

// Adjust color properties
vec3 adjustColor(vec3 color, float contrast, float brightness, float saturation) {
    // Brightness
    color += brightness;
    
    // Contrast
    color = (color - 0.5) * contrast + 0.5;
    
    // Saturation
    float gray = dot(color, vec3(0.299, 0.587, 0.114));
    color = mix(vec3(gray), color, saturation);
    
    return color;
}

void main() {
    vec2 uv = vUV.st;
    
    // Sample base layer (input 0)
    vec4 base = texture(sTD2DInputs[0], uv);
    vec3 result = base.rgb;
    
    // Get mask value if enabled
    float mask = 1.0;
    if (uUseMask == 1 && textureSize(sTD2DInputs[3], 0).x > 0) {
        vec4 maskSample = texture(sTD2DInputs[3], uv);
        if (uMaskChannel == 0) mask = maskSample.r;
        else if (uMaskChannel == 1) mask = maskSample.g;
        else if (uMaskChannel == 2) mask = maskSample.b;
        else mask = maskSample.a;
        
        if (uInvertMask == 1) mask = 1.0 - mask;
    }
    
    // Blend input 1 if available
    if (textureSize(sTD2DInputs[1], 0).x > 0) {
        vec2 uv1 = transformUV(uv, uScale1, uOffset1, uRotation1);
        vec4 tex1 = texture(sTD2DInputs[1], uv1);
        vec3 blend1 = tex1.rgb * uTint1;
        vec3 blended = applyBlendMode(result, blend1, uBlendMode1);
        result = mix(result, blended, uOpacity1 * tex1.a * mask);
    }
    
    // Blend input 2 if available
    if (textureSize(sTD2DInputs[2], 0).x > 0) {
        vec2 uv2 = transformUV(uv, uScale2, uOffset2, uRotation2);
        vec4 tex2 = texture(sTD2DInputs[2], uv2);
        vec3 blend2 = tex2.rgb * uTint2;
        vec3 blended = applyBlendMode(result, blend2, uBlendMode2);
        result = mix(result, blended, uOpacity2 * tex2.a * mask);
    }
    
    // Blend input 3 if available
    if (textureSize(sTD2DInputs[3], 0).x > 0 && uUseMask == 0) {
        vec2 uv3 = transformUV(uv, uScale3, uOffset3, uRotation3);
        vec4 tex3 = texture(sTD2DInputs[3], uv3);
        vec3 blend3 = tex3.rgb * uTint3;
        vec3 blended = applyBlendMode(result, blend3, uBlendMode3);
        result = mix(result, blended, uOpacity3 * tex3.a);
    }
    
    // Apply global color adjustments
    result = adjustColor(result, uContrast, uBrightness, uSaturation);
    
    // Clamp and output
    fragColor = vec4(clamp(result, 0.0, 1.0), base.a);
}
'''

def create_multi_input_blend_network():
    """
    Creates a multi-input blending network with advanced blend modes
    Returns the main container COMP
    """
    
    # Create main container
    container = op('/project1').create(containerCOMP, 'multi_input_blend')
    container.nodeX = 0
    container.nodeY = -800
    container.nodeWidth = 300
    container.nodeHeight = 250
    
    # Create input TOPs
    inputs = []
    for i in range(4):
        in_top = container.create(inTOP, f'in{i+1}')
        in_top.nodeX = -400 + (i * 100)
        in_top.nodeY = 100
        inputs.append(in_top)
    
    # Create test sources for demonstration
    # Base layer - gradient
    ramp1 = container.create(rampTOP, 'test_base')
    ramp1.nodeX = -400
    ramp1.nodeY = 200
    ramp1.par.ramptype = 'diagonal'
    inputs[0].inputConnectors[0].connect(ramp1.outputConnectors[0])
    
    # Layer 1 - noise
    noise1 = container.create(noiseTOP, 'test_layer1')
    noise1.nodeX = -300
    noise1.nodeY = 200
    noise1.par.type = 'sparse'
    inputs[1].inputConnectors[0].connect(noise1.outputConnectors[0])
    
    # Layer 2 - circle
    circle1 = container.create(circleTOP, 'test_layer2')
    circle1.nodeX = -200
    circle1.nodeY = 200
    circle1.par.radius = 0.3
    inputs[2].inputConnectors[0].connect(circle1.outputConnectors[0])
    
    # Layer 3/Mask - radial gradient
    ramp2 = container.create(rampTOP, 'test_mask')
    ramp2.nodeX = -100
    ramp2.nodeY = 200
    ramp2.par.ramptype = 'radial'
    inputs[3].inputConnectors[0].connect(ramp2.outputConnectors[0])
    
    # Create GLSL TOP for blending
    glsl_top = container.create(glslTOP, 'blend_glsl')
    glsl_top.nodeX = 0
    glsl_top.nodeY = 0
    glsl_top.par.resolution1 = 1920
    glsl_top.par.resolution2 = 1080
    glsl_top.par.pixelformat = 'rgba16float'
    glsl_top.par.numinputs = 4
    
    # Set GLSL code
    glsl_top.par.fragmentshader = MULTI_INPUT_BLEND_GLSL
    
    # Connect inputs
    for i, in_top in enumerate(inputs):
        glsl_top.inputConnectors[i].connect(in_top.outputConnectors[0])
    
    # Create parameter controls
    params_container = container.create(containerCOMP, 'parameters')
    params_container.nodeX = 400
    params_container.nodeY = 0
    params_container.nodeWidth = 250
    params_container.nodeHeight = 600
    
    # Create layer controls for each input (1-3)
    layer_y_positions = [500, 300, 100]
    blend_mode_names = 'Normal Multiply Screen Overlay SoftLight HardLight ColorDodge ColorBurn LinearDodge LinearBurn Difference Exclusion Lighten Darken VividLight LinearLight'
    
    for i in range(3):
        layer_num = i + 1
        y_pos = layer_y_positions[i]
        
        # Layer label
        text_dat = params_container.create(textDAT, f'layer{layer_num}_label')
        text_dat.nodeX = 0
        text_dat.nodeY = y_pos
        text_dat.text = f'LAYER {layer_num}'
        
        # Blend mode menu
        blend_menu = params_container.create(menuCOMP, f'blend_mode{layer_num}')
        blend_menu.nodeX = 0
        blend_menu.nodeY = y_pos - 40
        blend_menu.par.menunames = blend_mode_names
        blend_menu.par.default = 'Normal' if i == 0 else 'Screen'
        blend_menu.par.label = 'Blend Mode'
        
        # Opacity slider
        opacity_slider = params_container.create(sliderCOMP, f'opacity{layer_num}')
        opacity_slider.nodeX = 0
        opacity_slider.nodeY = y_pos - 80
        opacity_slider.par.default1 = 1.0 if i == 0 else 0.7
        opacity_slider.par.min1 = 0
        opacity_slider.par.max1 = 1
        opacity_slider.par.label = 'Opacity'
        
        # Scale XY
        scale_xy = params_container.create(xySliderCOMP, f'scale{layer_num}')
        scale_xy.nodeX = 0
        scale_xy.nodeY = y_pos - 120
        scale_xy.par.default1 = 1
        scale_xy.par.default2 = 1
        scale_xy.par.min1 = 0.1
        scale_xy.par.max1 = 2
        scale_xy.par.min2 = 0.1
        scale_xy.par.max2 = 2
        scale_xy.par.label = 'Scale'
        
        # Rotation slider
        rotation_slider = params_container.create(sliderCOMP, f'rotation{layer_num}')
        rotation_slider.nodeX = 0
        rotation_slider.nodeY = y_pos - 160
        rotation_slider.par.default1 = 0
        rotation_slider.par.min1 = -180
        rotation_slider.par.max1 = 180
        rotation_slider.par.label = 'Rotation'
    
    # Global adjustments
    text_dat2 = params_container.create(textDAT, 'global_label')
    text_dat2.nodeX = 0
    text_dat2.nodeY = -100
    text_dat2.text = 'GLOBAL ADJUSTMENTS'
    
    # Contrast slider
    contrast_slider = params_container.create(sliderCOMP, 'contrast')
    contrast_slider.nodeX = 0
    contrast_slider.nodeY = -140
    contrast_slider.par.default1 = 1
    contrast_slider.par.min1 = 0
    contrast_slider.par.max1 = 2
    contrast_slider.par.label = 'Contrast'
    
    # Brightness slider
    brightness_slider = params_container.create(sliderCOMP, 'brightness')
    brightness_slider.nodeX = 0
    brightness_slider.nodeY = -180
    brightness_slider.par.default1 = 0
    brightness_slider.par.min1 = -1
    brightness_slider.par.max1 = 1
    brightness_slider.par.label = 'Brightness'
    
    # Saturation slider
    saturation_slider = params_container.create(sliderCOMP, 'saturation')
    saturation_slider.nodeX = 0
    saturation_slider.nodeY = -220
    saturation_slider.par.default1 = 1
    saturation_slider.par.min1 = 0
    saturation_slider.par.max1 = 2
    saturation_slider.par.label = 'Saturation'
    
    # Mask controls
    text_dat3 = params_container.create(textDAT, 'mask_label')
    text_dat3.nodeX = 0
    text_dat3.nodeY = -280
    text_dat3.text = 'MASK SETTINGS'
    
    # Use mask toggle
    mask_toggle = params_container.create(toggleCOMP, 'use_mask')
    mask_toggle.nodeX = 0
    mask_toggle.nodeY = -320
    mask_toggle.par.label = 'Use Input 4 as Mask'
    
    # Mask channel menu
    mask_menu = params_container.create(menuCOMP, 'mask_channel')
    mask_menu.nodeX = 0
    mask_menu.nodeY = -360
    mask_menu.par.menunames = 'Red Green Blue Alpha'
    mask_menu.par.default = 'Alpha'
    mask_menu.par.label = 'Mask Channel'
    
    # Invert mask toggle
    invert_toggle = params_container.create(toggleCOMP, 'invert_mask')
    invert_toggle.nodeX = 0
    invert_toggle.nodeY = -400
    invert_toggle.par.label = 'Invert Mask'
    
    # Link parameters to GLSL uniforms
    # Layer parameters
    for i in range(3):
        layer_num = i + 1
        base_idx = i * 7
        
        # Blend mode
        glsl_top.par[f'uniformname{base_idx}'] = f'uBlendMode{layer_num}'
        glsl_top.par[f'uniformvalue{base_idx}'] = f"int(op('../parameters/blend_mode{layer_num}/out1')[0])"
        
        # Opacity
        glsl_top.par[f'uniformname{base_idx+1}'] = f'uOpacity{layer_num}'
        glsl_top.par[f'uniformvalue{base_idx+1}'] = f"op('../parameters/opacity{layer_num}/out1')[0]"
        
        # Scale
        glsl_top.par[f'uniformname{base_idx+2}'] = f'uScale{layer_num}'
        glsl_top.par[f'uniformvalue{base_idx+2}x'] = f"op('../parameters/scale{layer_num}/out1')['u']"
        glsl_top.par[f'uniformvalue{base_idx+2}y'] = f"op('../parameters/scale{layer_num}/out1')['v']"
        
        # Offset (hardcoded to 0 for simplicity)
        glsl_top.par[f'uniformname{base_idx+3}'] = f'uOffset{layer_num}'
        glsl_top.par[f'uniformvalue{base_idx+3}x'] = "0"
        glsl_top.par[f'uniformvalue{base_idx+3}y'] = "0"
        
        # Rotation (convert to radians)
        glsl_top.par[f'uniformname{base_idx+4}'] = f'uRotation{layer_num}'
        glsl_top.par[f'uniformvalue{base_idx+4}'] = f"op('../parameters/rotation{layer_num}/out1')[0] * 3.14159265359 / 180"
        
        # Tint (hardcoded to white for simplicity)
        glsl_top.par[f'uniformname{base_idx+5}'] = f'uTint{layer_num}'
        glsl_top.par[f'uniformvalue{base_idx+5}x'] = "1"
        glsl_top.par[f'uniformvalue{base_idx+5}y'] = "1"
        glsl_top.par[f'uniformvalue{base_idx+5}z'] = "1"
    
    # Global parameters
    glsl_top.par.uniformname21 = 'uContrast'
    glsl_top.par.uniformvalue21 = "op('../parameters/contrast/out1')[0]"
    
    glsl_top.par.uniformname22 = 'uBrightness'
    glsl_top.par.uniformvalue22 = "op('../parameters/brightness/out1')[0]"
    
    glsl_top.par.uniformname23 = 'uSaturation'
    glsl_top.par.uniformvalue23 = "op('../parameters/saturation/out1')[0]"
    
    # Mask parameters
    glsl_top.par.uniformname24 = 'uUseMask'
    glsl_top.par.uniformvalue24 = "int(op('../parameters/use_mask/out1')[0])"
    
    glsl_top.par.uniformname25 = 'uMaskChannel'
    glsl_top.par.uniformvalue25 = "int(op('../parameters/mask_channel/out1')[0])"
    
    glsl_top.par.uniformname26 = 'uInvertMask'
    glsl_top.par.uniformvalue26 = "int(op('../parameters/invert_mask/out1')[0])"
    
    # Create output
    out_top = container.create(outTOP, 'out1')
    out_top.nodeX = 200
    out_top.nodeY = 0
    out_top.inputConnectors[0].connect(glsl_top.outputConnectors[0])
    
    return container

# Execute the network creation
if __name__ == '__main__':
    network = create_multi_input_blend_network()
    print(f"Created multi-input blend network at: {network.path}")