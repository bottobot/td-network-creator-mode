"""
Projection Mapping Template for TouchDesigner
Creates a complete projection mapping setup with multi-projector support
"""

def create_projection_mapping_system():
    """
    Creates a projection mapping system with:
    - Cornerpin/keystone correction
    - Edge blending
    - Multi-projector setup
    - Test patterns
    """
    
    # Create base container
    base = op('/project1').create(containerCOMP, 'projection_mapping')
    base.par.w = 1600
    base.par.h = 1000
    base.nodeX = 0
    base.nodeY = 0
    
    # Content Input Section
    print("Creating content input system...")
    
    # Content source (can be replaced with any content)
    content = base.create(noiseTOP, 'content_source')
    content.nodeX = -600
    content.nodeY = 400
    content.par.resolutionw = 1920
    content.par.resolutionh = 1080
    content.par.type = 'sparse'
    content.par.period = 8
    
    # Test Patterns
    print("Creating test patterns...")
    
    # Grid pattern
    grid = base.create(glslTOP, 'grid_pattern')
    grid.nodeX = -600
    grid.nodeY = 250
    grid.par.resolutionw = 1920
    grid.par.resolutionh = 1080
    
    grid_shader = '''
uniform float uGridSize;
uniform vec3 uLineColor;
uniform vec3 uBackgroundColor;
uniform float uLineWidth;

out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy;
    vec2 grid = mod(uv, uGridSize);
    
    float line = 0.0;
    if (grid.x < uLineWidth || grid.y < uLineWidth) {
        line = 1.0;
    }
    
    vec3 color = mix(uBackgroundColor, uLineColor, line);
    fragColor = vec4(color, 1.0);
}
'''
    grid.par.pixeldat = grid_shader
    grid.par.value0name = 'uGridSize'
    grid.par.value0 = 50
    grid.par.value1name = 'uLineWidth'
    grid.par.value1 = 2
    grid.par.vector0name = 'uLineColor'
    grid.par.vector0 = [1, 1, 1]
    grid.par.vector1name = 'uBackgroundColor'
    grid.par.vector1 = [0, 0, 0]
    
    # Alignment cross
    cross = base.create(glslTOP, 'alignment_cross')
    cross.nodeX = -600
    cross.nodeY = 100
    cross.par.resolutionw = 1920
    cross.par.resolutionh = 1080
    
    cross_shader = '''
uniform float uCrossSize;
uniform float uLineWidth;
uniform vec3 uColor;

out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy;
    vec2 center = vec2(textureSize(sTD2DInputs[0], 0)) * 0.5;
    vec2 dist = abs(uv - center);
    
    float cross = 0.0;
    if ((dist.x < uLineWidth && dist.y < uCrossSize) ||
        (dist.y < uLineWidth && dist.x < uCrossSize)) {
        cross = 1.0;
    }
    
    fragColor = vec4(uColor * cross, cross);
}
'''
    cross.par.pixeldat = cross_shader
    cross.par.value0name = 'uCrossSize'
    cross.par.value0 = 200
    cross.par.value1name = 'uLineWidth'
    cross.par.value1 = 4
    cross.par.vector0name = 'uColor'
    cross.par.vector0 = [1, 0, 0]
    
    # Color bars
    bars = base.create(glslTOP, 'color_bars')
    bars.nodeX = -600
    bars.nodeY = -50
    bars.par.resolutionw = 1920
    bars.par.resolutionh = 1080
    
    bars_shader = '''
out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(textureSize(sTD2DInputs[0], 0));
    
    vec3 color;
    float x = uv.x * 7.0;
    int bar = int(x);
    
    if (bar == 0) color = vec3(1.0, 1.0, 1.0);      // White
    else if (bar == 1) color = vec3(1.0, 1.0, 0.0); // Yellow
    else if (bar == 2) color = vec3(0.0, 1.0, 1.0); // Cyan
    else if (bar == 3) color = vec3(0.0, 1.0, 0.0); // Green
    else if (bar == 4) color = vec3(1.0, 0.0, 1.0); // Magenta
    else if (bar == 5) color = vec3(1.0, 0.0, 0.0); // Red
    else color = vec3(0.0, 0.0, 1.0);                // Blue
    
    fragColor = vec4(color, 1.0);
}
'''
    bars.par.pixeldat = bars_shader
    
    # Pattern selector
    pattern_switch = base.create(switchTOP, 'pattern_selector')
    pattern_switch.nodeX = -400
    pattern_switch.nodeY = 200
    pattern_switch.par.index = 0
    pattern_switch.inputConnectors[0].connect(content)
    pattern_switch.inputConnectors[1].connect(grid)
    pattern_switch.inputConnectors[2].connect(cross)
    pattern_switch.inputConnectors[3].connect(bars)
    
    # Multi-Projector Setup
    print("Creating multi-projector outputs...")
    
    # Create 2 projector outputs (can be extended)
    projectors = []
    for i in range(2):
        proj_y = 0 - (i * 300)
        
        # Cornerpin for each projector
        cornerpin = base.create(cornerpinTOP, f'projector_{i+1}_cornerpin')
        cornerpin.nodeX = -200
        cornerpin.nodeY = proj_y
        cornerpin.par.fitmethod = 'fill'
        cornerpin.par.cornerpin = True
        cornerpin.par.topleftx = -0.1 * i
        cornerpin.par.toplefty = 0.1 * i
        cornerpin.par.toprightx = 0.1 * i
        cornerpin.par.toprighty = 0.1 * i
        cornerpin.inputConnectors[0].connect(pattern_switch)
        
        # Edge blend mask
        edge_mask = base.create(glslTOP, f'projector_{i+1}_edge_mask')
        edge_mask.nodeX = 0
        edge_mask.nodeY = proj_y
        edge_mask.par.resolutionw = 1920
        edge_mask.par.resolutionh = 1080
        
        edge_shader = '''
uniform float uBlendLeft;
uniform float uBlendRight;
uniform float uBlendTop;
uniform float uBlendBottom;
uniform float uGamma;

out vec4 fragColor;

float smoothBlend(float edge, float blend) {
    if (blend <= 0.0) return 1.0;
    float t = clamp(edge / blend, 0.0, 1.0);
    return pow(t, uGamma);
}

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(textureSize(sTD2DInputs[0], 0));
    
    float left = smoothBlend(uv.x, uBlendLeft);
    float right = smoothBlend(1.0 - uv.x, uBlendRight);
    float top = smoothBlend(1.0 - uv.y, uBlendTop);
    float bottom = smoothBlend(uv.y, uBlendBottom);
    
    float mask = left * right * top * bottom;
    
    vec4 color = texture(sTD2DInputs[0], uv);
    fragColor = vec4(color.rgb * mask, 1.0);
}
'''
        edge_mask.par.pixeldat = edge_shader
        edge_mask.par.value0name = 'uBlendLeft'
        edge_mask.par.value0 = 0.1 if i == 1 else 0
        edge_mask.par.value1name = 'uBlendRight'
        edge_mask.par.value1 = 0.1 if i == 0 else 0
        edge_mask.par.value2name = 'uBlendTop'
        edge_mask.par.value2 = 0
        edge_mask.par.value3name = 'uBlendBottom'
        edge_mask.par.value3 = 0
        edge_mask.par.value4name = 'uGamma'
        edge_mask.par.value4 = 2.2
        edge_mask.inputConnectors[0].connect(cornerpin)
        
        # Brightness/contrast adjustment per projector
        level = base.create(levelTOP, f'projector_{i+1}_levels')
        level.nodeX = 200
        level.nodeY = proj_y
        level.par.brightness1 = 1.0
        level.par.gamma1 = 1.0
        level.inputConnectors[0].connect(edge_mask)
        
        # Output
        out = base.create(outTOP, f'projector_{i+1}_output')
        out.nodeX = 400
        out.nodeY = proj_y
        out.inputConnectors[0].connect(level)
        
        projectors.append({
            'cornerpin': cornerpin,
            'edge_mask': edge_mask,
            'level': level,
            'output': out
        })
    
    # Preview composite
    print("Creating preview composite...")
    
    # Scale down projector outputs for preview
    preview_scales = []
    for i, proj in enumerate(projectors):
        scale = base.create(resolutionTOP, f'preview_scale_{i+1}')
        scale.nodeX = 600
        scale.nodeY = 0 - (i * 150)
        scale.par.resolution = 'quarter'
        scale.inputConnectors[0].connect(proj['output'])
        preview_scales.append(scale)
    
    # Composite preview
    over = base.create(overTOP, 'preview_composite')
    over.nodeX = 800
    over.nodeY = -75
    over.par.operand = 'add'
    over.inputConnectors[0].connect(preview_scales[0])
    over.inputConnectors[1].connect(preview_scales[1])
    
    # Control Panel
    print("Creating control panel...")
    
    controls = base.create(containerCOMP, 'controls')
    controls.nodeX = -600
    controls.nodeY = -400
    controls.par.w = 600
    controls.par.h = 600
    
    # Add custom parameters
    page = controls.appendCustomPage('Projection Mapping Controls')
    
    # Pattern selection
    page.appendMenu('Test_pattern', label='Test Pattern',
                    menuNames=['Content', 'Grid', 'Cross', 'Bars'],
                    menuLabels=['Content', 'Grid', 'Cross', 'Color Bars'],
                    default='Content')
    
    # Grid controls
    page.appendInt('Grid_size', label='Grid Size', size=1, default=50, min=10, max=200)
    page.appendFloat('Grid_line_width', label='Grid Line Width', size=1, default=2, min=1, max=10)
    
    # Add projector-specific controls
    for i in range(2):
        # Cornerpin controls
        page.appendXY(f'P{i+1}_topleft', label=f'Proj {i+1} Top Left', default=[-0.1*i, 0.1*i])
        page.appendXY(f'P{i+1}_topright', label=f'Proj {i+1} Top Right', default=[0.1*i, 0.1*i])
        page.appendXY(f'P{i+1}_bottomleft', label=f'Proj {i+1} Bottom Left', default=[-0.1*i, -0.1*i])
        page.appendXY(f'P{i+1}_bottomright', label=f'Proj {i+1} Bottom Right', default=[0.1*i, -0.1*i])
        
        # Edge blend controls
        page.appendFloat(f'P{i+1}_blend_left', label=f'Proj {i+1} Blend Left', 
                        size=1, default=0.1 if i==1 else 0, min=0, max=0.5)
        page.appendFloat(f'P{i+1}_blend_right', label=f'Proj {i+1} Blend Right', 
                        size=1, default=0.1 if i==0 else 0, min=0, max=0.5)
        page.appendFloat(f'P{i+1}_blend_top', label=f'Proj {i+1} Blend Top', 
                        size=1, default=0, min=0, max=0.5)
        page.appendFloat(f'P{i+1}_blend_bottom', label=f'Proj {i+1} Blend Bottom', 
                        size=1, default=0, min=0, max=0.5)
        
        # Level controls
        page.appendFloat(f'P{i+1}_brightness', label=f'Proj {i+1} Brightness', 
                        size=1, default=1.0, min=0, max=2)
        page.appendFloat(f'P{i+1}_gamma', label=f'Proj {i+1} Gamma', 
                        size=1, default=1.0, min=0.1, max=3)
    
    # Global controls
    page.appendFloat('Edge_gamma', label='Edge Blend Gamma', size=1, default=2.2, min=1, max=3)
    page.appendToggle('Show_preview', label='Show Preview Composite', default=True)
    
    # Link parameters to operators
    pattern_switch.par.index.expr = 'int(op("../controls").par.Test_pattern)'
    grid.par.value0.expr = 'op("../controls").par.Grid_size'
    grid.par.value1.expr = 'op("../controls").par.Grid_line_width'
    
    # Link projector parameters
    for i, proj in enumerate(projectors):
        # Cornerpin
        proj['cornerpin'].par.topleftx.expr = f'op("../controls").par.P{i+1}_topleftx'
        proj['cornerpin'].par.toplefty.expr = f'op("../controls").par.P{i+1}_toplefty'
        proj['cornerpin'].par.toprightx.expr = f'op("../controls").par.P{i+1}_toprightx'
        proj['cornerpin'].par.toprighty.expr = f'op("../controls").par.P{i+1}_toprighty'
        proj['cornerpin'].par.bottomleftx.expr = f'op("../controls").par.P{i+1}_bottomleftx'
        proj['cornerpin'].par.bottomlefty.expr = f'op("../controls").par.P{i+1}_bottomlefty'
        proj['cornerpin'].par.bottomrightx.expr = f'op("../controls").par.P{i+1}_bottomrightx'
        proj['cornerpin'].par.bottomrighty.expr = f'op("../controls").par.P{i+1}_bottomrighty'
        
        # Edge blend
        proj['edge_mask'].par.value0.expr = f'op("../controls").par.P{i+1}_blend_left'
        proj['edge_mask'].par.value1.expr = f'op("../controls").par.P{i+1}_blend_right'
        proj['edge_mask'].par.value2.expr = f'op("../controls").par.P{i+1}_blend_top'
        proj['edge_mask'].par.value3.expr = f'op("../controls").par.P{i+1}_blend_bottom'
        proj['edge_mask'].par.value4.expr = 'op("../controls").par.Edge_gamma'
        
        # Levels
        proj['level'].par.brightness1.expr = f'op("../controls").par.P{i+1}_brightness'
        proj['level'].par.gamma1.expr = f'op("../controls").par.P{i+1}_gamma'
    
    # Calibration helpers
    print("Adding calibration helpers...")
    
    # Warp point visualizer
    warp_viz = base.create(glslTOP, 'warp_visualizer')
    warp_viz.nodeX = -200
    warp_viz.nodeY = -400
    warp_viz.par.resolutionw = 1920
    warp_viz.par.resolutionh = 1080
    
    warp_shader = '''
uniform vec2 uPoint1;
uniform vec2 uPoint2;
uniform vec2 uPoint3;
uniform vec2 uPoint4;
uniform float uPointSize;

out vec4 fragColor;

float drawPoint(vec2 uv, vec2 point) {
    float dist = length(uv - point);
    return smoothstep(uPointSize, uPointSize * 0.8, dist);
}

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(textureSize(sTD2DInputs[0], 0));
    
    vec4 color = texture(sTD2DInputs[0], uv);
    
    // Draw corner points
    float points = 0.0;
    points += drawPoint(uv, uPoint1);
    points += drawPoint(uv, uPoint2);
    points += drawPoint(uv, uPoint3);
    points += drawPoint(uv, uPoint4);
    
    vec3 pointColor = vec3(1.0, 0.0, 0.0);
    color.rgb = mix(color.rgb, pointColor, points);
    
    fragColor = color;
}
'''
    warp_viz.par.pixeldat = warp_shader
    warp_viz.inputConnectors[0].connect(pattern_switch)
    
    print("Projection mapping system created successfully!")
    print(f"System created at: {base.path}")
    print("\nKey features:")
    print("- Multi-projector support (2 projectors)")
    print("- Cornerpin correction for each projector")
    print("- Edge blending with gamma correction")
    print("- Test patterns (grid, cross, color bars)")
    print("- Per-projector brightness and gamma")
    print("- Preview composite view")
    print("- Comprehensive control panel")
    print("\nTo extend:")
    print("- Add more projectors by duplicating the projector setup")
    print("- Connect actual content to 'content_source'")
    print("- Use Window COMP to output to actual projectors")
    
    return base

# Execute the template
if __name__ == '__main__':
    create_projection_mapping_system()