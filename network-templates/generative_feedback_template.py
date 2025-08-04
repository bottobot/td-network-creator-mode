"""
Generative Feedback System Template for TouchDesigner
Creates a feedback loop system for generative visuals
"""

def create_generative_feedback_system():
    """
    Creates a generative feedback system with:
    - Feedback loop setup
    - Transform controls
    - Blend modes
    - Color processing
    """
    
    # Create base container
    base = op('/project1').create(containerCOMP, 'generative_feedback')
    base.par.w = 1200
    base.par.h = 800
    base.nodeX = 0
    base.nodeY = 0
    
    # Initial Source Generation
    print("Creating initial source generators...")
    
    # Noise source
    noise = base.create(noiseTOP, 'noise_source')
    noise.nodeX = -600
    noise.nodeY = 200
    noise.par.resolutionw = 1920
    noise.par.resolutionh = 1080
    noise.par.type = 'sparse'
    noise.par.period = 4
    noise.par.phase = 0
    noise.par.amp = 1
    
    # Ramp source
    ramp = base.create(rampTOP, 'ramp_source')
    ramp.nodeX = -600
    ramp.nodeY = 50
    ramp.par.resolutionw = 1920
    ramp.par.resolutionh = 1080
    ramp.par.type = 'circular'
    ramp.par.phase = 0
    
    # Pattern generator using GLSL
    pattern = base.create(glslTOP, 'pattern_generator')
    pattern.nodeX = -600
    pattern.nodeY = -100
    pattern.par.resolutionw = 1920
    pattern.par.resolutionh = 1080
    
    pattern_shader = '''
uniform float uTime;
uniform float uScale;
uniform float uComplexity;

out vec4 fragColor;

vec2 complexMul(vec2 a, vec2 b) {
    return vec2(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x);
}

void main() {
    vec2 uv = (gl_FragCoord.xy - 0.5 * vec2(textureSize(sTD2DInputs[0], 0))) / 
              float(textureSize(sTD2DInputs[0], 0).y);
    
    vec2 z = uv * uScale;
    vec2 c = vec2(sin(uTime * 0.1), cos(uTime * 0.13));
    
    float iter = 0.0;
    for (int i = 0; i < 32; i++) {
        z = complexMul(z, z) + c;
        if (length(z) > 2.0) break;
        iter += 1.0;
    }
    
    float val = iter / 32.0;
    vec3 color = vec3(
        sin(val * 3.14159 + uTime),
        sin(val * 3.14159 * 2.0 + uTime * 1.3),
        sin(val * 3.14159 * 3.0 + uTime * 0.7)
    ) * 0.5 + 0.5;
    
    fragColor = vec4(color * uComplexity, 1.0);
}
'''
    pattern.par.pixeldat = pattern_shader
    pattern.par.value0name = 'uTime'
    pattern.par.value0.expr = 'absTime.seconds'
    pattern.par.value1name = 'uScale'
    pattern.par.value1 = 2.0
    pattern.par.value2name = 'uComplexity'
    pattern.par.value2 = 1.0
    
    # Source selector
    switch_source = base.create(switchTOP, 'source_selector')
    switch_source.nodeX = -400
    switch_source.nodeY = 50
    switch_source.par.index = 0
    switch_source.inputConnectors[0].connect(noise)
    switch_source.inputConnectors[1].connect(ramp)
    switch_source.inputConnectors[2].connect(pattern)
    
    # Feedback Loop Setup
    print("Setting up feedback loop...")
    
    # Feedback TOP
    feedback = base.create(feedbackTOP, 'feedback_loop')
    feedback.nodeX = 200
    feedback.nodeY = 0
    feedback.par.feedbacktarget = 'transform_feedback'
    
    # Initial blend of source and feedback
    blend_initial = base.create(compositeTOP, 'initial_blend')
    blend_initial.nodeX = -200
    blend_initial.nodeY = 0
    blend_initial.par.operand = 'over'
    blend_initial.inputConnectors[0].connect(feedback)
    blend_initial.inputConnectors[1].connect(switch_source)
    
    # Transform Controls
    print("Adding transform controls...")
    
    # Transform for feedback
    transform_fb = base.create(transformTOP, 'transform_feedback')
    transform_fb.nodeX = 0
    transform_fb.nodeY = 0
    transform_fb.par.scale = 1.01
    transform_fb.par.rotate = 0.5
    transform_fb.par.tx = 0
    transform_fb.par.ty = 0
    transform_fb.inputConnectors[0].connect(blend_initial)
    
    # Connect feedback loop
    feedback.inputConnectors[0].connect(transform_fb)
    
    # Additional transforms
    transform_2 = base.create(transformTOP, 'transform_secondary')
    transform_2.nodeX = 400
    transform_2.nodeY = 0
    transform_2.par.scale = 0.99
    transform_2.par.rotate = -0.3
    transform_2.inputConnectors[0].connect(feedback)
    
    # Blend Modes Section
    print("Creating blend mode options...")
    
    # Multiple blend options
    blend_add = base.create(compositeTOP, 'blend_add')
    blend_add.nodeX = 600
    blend_add.nodeY = 100
    blend_add.par.operand = 'add'
    blend_add.inputConnectors[0].connect(feedback)
    blend_add.inputConnectors[1].connect(transform_2)
    
    blend_mult = base.create(compositeTOP, 'blend_multiply')
    blend_mult.nodeX = 600
    blend_mult.nodeY = 0
    blend_mult.par.operand = 'multiply'
    blend_mult.inputConnectors[0].connect(feedback)
    blend_mult.inputConnectors[1].connect(transform_2)
    
    blend_diff = base.create(compositeTOP, 'blend_difference')
    blend_diff.nodeX = 600
    blend_diff.nodeY = -100
    blend_diff.par.operand = 'difference'
    blend_diff.inputConnectors[0].connect(feedback)
    blend_diff.inputConnectors[1].connect(transform_2)
    
    blend_screen = base.create(compositeTOP, 'blend_screen')
    blend_screen.nodeX = 600
    blend_screen.nodeY = -200
    blend_screen.par.operand = 'screen'
    blend_screen.inputConnectors[0].connect(feedback)
    blend_screen.inputConnectors[1].connect(transform_2)
    
    # Blend mode selector
    switch_blend = base.create(switchTOP, 'blend_selector')
    switch_blend.nodeX = 800
    switch_blend.nodeY = -50
    switch_blend.par.index = 0
    switch_blend.inputConnectors[0].connect(blend_add)
    switch_blend.inputConnectors[1].connect(blend_mult)
    switch_blend.inputConnectors[2].connect(blend_diff)
    switch_blend.inputConnectors[3].connect(blend_screen)
    
    # Color Processing
    print("Adding color processing...")
    
    # HSV adjustment
    hsv = base.create(hsvAdjustTOP, 'color_adjust')
    hsv.nodeX = 1000
    hsv.nodeY = -50
    hsv.par.hueoffset = 0
    hsv.par.saturationmult = 1
    hsv.par.valuemult = 1
    hsv.inputConnectors[0].connect(switch_blend)
    
    # Level adjustment
    levels = base.create(levelTOP, 'level_adjust')
    levels.nodeX = 1000
    levels.nodeY = -150
    levels.par.blacklevel = 0
    levels.par.brightness1 = 1
    levels.par.gamma1 = 1
    levels.par.whitelevel = 1
    levels.par.opacity = 1
    levels.inputConnectors[0].connect(hsv)
    
    # Lookup table for color grading
    lookup = base.create(lookupTOP, 'color_lookup')
    lookup.nodeX = 1000
    lookup.nodeY = -250
    lookup.inputConnectors[0].connect(levels)
    
    # Create gradient for lookup
    gradient = base.create(rampTOP, 'lookup_gradient')
    gradient.nodeX = 800
    gradient.nodeY = -350
    gradient.par.resolutionw = 256
    gradient.par.resolutionh = 1
    gradient.par.type = 'horizontal'
    
    # Apply gradient colors
    gradient_color = base.create(hsvAdjustTOP, 'gradient_colors')
    gradient_color.nodeX = 1000
    gradient_color.nodeY = -350
    gradient_color.par.hueoffset = 0.5
    gradient_color.par.saturationmult = 1.5
    gradient_color.inputConnectors[0].connect(gradient)
    
    lookup.inputConnectors[1].connect(gradient_color)
    
    # Edge and blur effects
    edge = base.create(edgeTOP, 'edge_enhance')
    edge.nodeX = 800
    edge.nodeY = -450
    edge.par.method = 'sobel'
    edge.inputConnectors[0].connect(lookup)
    
    blur = base.create(blurTOP, 'blur_effect')
    blur.nodeX = 1000
    blur.nodeY = -450
    blur.par.size = 1
    blur.inputConnectors[0].connect(lookup)
    
    # Final composite
    final_comp = base.create(compositeTOP, 'final_composite')
    final_comp.nodeX = 1200
    final_comp.nodeY = -250
    final_comp.par.operand = 'over'
    final_comp.inputConnectors[0].connect(lookup)
    final_comp.inputConnectors[1].connect(edge)
    
    # Output
    out = base.create(outTOP, 'output')
    out.nodeX = 1400
    out.nodeY = -250
    out.inputConnectors[0].connect(final_comp)
    
    # Control Panel
    print("Creating control panel...")
    
    controls = base.create(containerCOMP, 'controls')
    controls.nodeX = -600
    controls.nodeY = -400
    controls.par.w = 500
    controls.par.h = 500
    
    # Add custom parameters
    page = controls.appendCustomPage('Feedback Controls')
    
    # Source controls
    page.appendMenu('Source_type', label='Source Type', 
                    menuNames=['Noise', 'Ramp', 'Pattern'],
                    menuLabels=['Noise', 'Ramp', 'Pattern'], 
                    default='Noise')
    
    # Noise parameters
    page.appendFloat('Noise_period', label='Noise Period', size=1, default=4, min=0.1, max=20)
    page.appendFloat('Noise_amp', label='Noise Amplitude', size=1, default=1, min=0, max=2)
    
    # Pattern parameters
    page.appendFloat('Pattern_scale', label='Pattern Scale', size=1, default=2, min=0.5, max=10)
    page.appendFloat('Pattern_complexity', label='Pattern Complexity', size=1, default=1, min=0, max=2)
    
    # Transform controls
    page.appendFloat('Transform_scale', label='Feedback Scale', size=1, default=1.01, min=0.9, max=1.1)
    page.appendFloat('Transform_rotate', label='Feedback Rotate', size=1, default=0.5, min=-5, max=5)
    page.appendXY('Transform_translate', label='Feedback Translate', default=[0, 0], min=-0.1, max=0.1)
    
    page.appendFloat('Transform2_scale', label='Secondary Scale', size=1, default=0.99, min=0.9, max=1.1)
    page.appendFloat('Transform2_rotate', label='Secondary Rotate', size=1, default=-0.3, min=-5, max=5)
    
    # Blend controls
    page.appendMenu('Blend_mode', label='Blend Mode',
                    menuNames=['Add', 'Multiply', 'Difference', 'Screen'],
                    menuLabels=['Add', 'Multiply', 'Difference', 'Screen'],
                    default='Add')
    
    # Color controls
    page.appendFloat('Hue_offset', label='Hue Offset', size=1, default=0, min=-1, max=1)
    page.appendFloat('Saturation', label='Saturation', size=1, default=1, min=0, max=2)
    page.appendFloat('Brightness', label='Brightness', size=1, default=1, min=0, max=2)
    page.appendFloat('Gamma', label='Gamma', size=1, default=1, min=0.1, max=3)
    
    # Effect controls
    page.appendFloat('Edge_mix', label='Edge Mix', size=1, default=0, min=0, max=1)
    page.appendFloat('Blur_size', label='Blur Size', size=1, default=1, min=0, max=10)
    
    # Feedback controls
    page.appendFloat('Feedback_opacity', label='Feedback Opacity', size=1, default=0.95, min=0, max=1)
    page.appendToggle('Clear_feedback', label='Clear Feedback')
    
    # Link parameters to operators
    switch_source.par.index.expr = 'int(op("../controls").par.Source_type)'
    noise.par.period.expr = 'op("../controls").par.Noise_period'
    noise.par.amp.expr = 'op("../controls").par.Noise_amp'
    pattern.par.value1.expr = 'op("../controls").par.Pattern_scale'
    pattern.par.value2.expr = 'op("../controls").par.Pattern_complexity'
    
    transform_fb.par.scale.expr = 'op("../controls").par.Transform_scale'
    transform_fb.par.rotate.expr = 'op("../controls").par.Transform_rotate'
    transform_fb.par.tx.expr = 'op("../controls").par.Transform_translatex'
    transform_fb.par.ty.expr = 'op("../controls").par.Transform_translatey'
    
    transform_2.par.scale.expr = 'op("../controls").par.Transform2_scale'
    transform_2.par.rotate.expr = 'op("../controls").par.Transform2_rotate'
    
    switch_blend.par.index.expr = 'int(op("../controls").par.Blend_mode)'
    
    hsv.par.hueoffset.expr = 'op("../controls").par.Hue_offset'
    hsv.par.saturationmult.expr = 'op("../controls").par.Saturation'
    levels.par.brightness1.expr = 'op("../controls").par.Brightness'
    levels.par.gamma1.expr = 'op("../controls").par.Gamma'
    
    final_comp.par.operand1.expr = 'op("../controls").par.Edge_mix'
    blur.par.size.expr = 'op("../controls").par.Blur_size'
    
    blend_initial.par.operand1.expr = 'op("../controls").par.Feedback_opacity'
    feedback.par.resetpulse.expr = 'op("../controls").par.Clear_feedback'
    
    # Add animation controls
    print("Adding animation system...")
    
    # LFO for automated animation
    lfo = base.create(lfoCHOP, 'animation_lfo')
    lfo.nodeX = -400
    lfo.nodeY = -400
    lfo.par.rate = 0.1
    lfo.par.amplitude = 1
    lfo.par.type = 'sin'
    
    # Noise for random variation
    noise_chop = base.create(noiseCHOP, 'animation_noise')
    noise_chop.nodeX = -400
    noise_chop.nodeY = -500
    noise_chop.par.rate = 0.05
    noise_chop.par.amp = 0.1
    
    print("Generative feedback system created successfully!")
    print(f"System created at: {base.path}")
    print("\nKey features:")
    print("- Multiple source generators")
    print("- Feedback loop with transform controls")
    print("- Various blend modes")
    print("- Comprehensive color processing")
    print("- Edge and blur effects")
    print("- Animation system with LFO and noise")
    print("- Full control panel")
    
    return base

# Execute the template
if __name__ == '__main__':
    create_generative_feedback_system()