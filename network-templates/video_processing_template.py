"""
Video Processing Template for TouchDesigner
Creates a comprehensive video input and processing pipeline
"""

def create_video_processing_system():
    """
    Creates a video processing system with:
    - Movie file and camera input options
    - Pre-processing chain
    - Effects pipeline
    - Output recording capabilities
    """
    
    # Create base container
    base = op('/project1').create(containerCOMP, 'video_processing')
    base.par.w = 1600
    base.par.h = 900
    base.nodeX = 0
    base.nodeY = 0
    
    # Input Section
    print("Creating video input system...")
    
    # Movie file input
    movie_in = base.create(moviefileinTOP, 'movie_input')
    movie_in.nodeX = -600
    movie_in.nodeY = 200
    movie_in.par.play = True
    movie_in.par.loop = True
    
    # Camera input
    video_in = base.create(videodeviceinTOP, 'camera_input')
    video_in.nodeX = -600
    video_in.nodeY = 50
    video_in.par.active = False  # Start with movie input
    
    # Input selector switch
    switch = base.create(switchTOP, 'input_selector')
    switch.nodeX = -400
    switch.nodeY = 125
    switch.par.index = 0  # 0 = movie, 1 = camera
    switch.inputConnectors[0].connect(movie_in)
    switch.inputConnectors[1].connect(video_in)
    
    # Pre-processing Chain
    print("Setting up pre-processing...")
    
    # Resolution adjustment
    resolution = base.create(resolutionTOP, 'resolution_adjust')
    resolution.nodeX = -200
    resolution.nodeY = 125
    resolution.par.resolution = 'custom'
    resolution.par.resolutionw = 1920
    resolution.par.resolutionh = 1080
    resolution.par.fitmethod = 'fill'
    resolution.inputConnectors[0].connect(switch)
    
    # Color correction
    levels = base.create(levelTOP, 'color_correction')
    levels.nodeX = 0
    levels.nodeY = 125
    levels.par.blacklevel = 0.0
    levels.par.brightness1 = 1.0
    levels.par.gamma1 = 1.0
    levels.par.whitelevel = 1.0
    levels.inputConnectors[0].connect(resolution)
    
    # Crop/Transform
    transform = base.create(transformTOP, 'transform')
    transform.nodeX = 200
    transform.nodeY = 125
    transform.par.scale = 1.0
    transform.par.rotate = 0
    transform.inputConnectors[0].connect(levels)
    
    # Effects Pipeline
    print("Creating effects pipeline...")
    
    # Effect 1: Blur
    blur = base.create(blurTOP, 'blur_effect')
    blur.nodeX = 400
    blur.nodeY = 250
    blur.par.size = 0
    blur.par.fitres = 'fitinput'
    blur.inputConnectors[0].connect(transform)
    
    # Effect 2: Edge Detection
    edge = base.create(edgeTOP, 'edge_detect')
    edge.nodeX = 400
    edge.nodeY = 150
    edge.par.method = 'sobel'
    edge.inputConnectors[0].connect(transform)
    
    # Effect 3: Chromatic Aberration
    chroma_r = base.create(transformTOP, 'chroma_r')
    chroma_r.nodeX = 400
    chroma_r.nodeY = 50
    chroma_r.par.scale = 1.01
    chroma_r.inputConnectors[0].connect(transform)
    
    chroma_g = base.create(transformTOP, 'chroma_g')
    chroma_g.nodeX = 400
    chroma_g.nodeY = -50
    chroma_g.par.scale = 1.0
    chroma_g.inputConnectors[0].connect(transform)
    
    chroma_b = base.create(transformTOP, 'chroma_b')
    chroma_b.nodeX = 400
    chroma_b.nodeY = -150
    chroma_b.par.scale = 0.99
    chroma_b.inputConnectors[0].connect(transform)
    
    # Recompose chromatic aberration
    recompose = base.create(reorderTOP, 'chroma_recompose')
    recompose.nodeX = 600
    recompose.nodeY = -50
    recompose.par.red = 'r'
    recompose.par.green = 'g'
    recompose.par.blue = 'b'
    recompose.par.redinput = 0
    recompose.par.greeninput = 1
    recompose.par.blueinput = 2
    recompose.inputConnectors[0].connect(chroma_r)
    recompose.inputConnectors[1].connect(chroma_g)
    recompose.inputConnectors[2].connect(chroma_b)
    
    # Effect 4: Kaleidoscope
    kaleido = base.create(glslTOP, 'kaleidoscope')
    kaleido.nodeX = 400
    kaleido.nodeY = -250
    kaleido.par.resolutionw = 1920
    kaleido.par.resolutionh = 1080
    kaleido.inputConnectors[0].connect(transform)
    
    kaleido_shader = '''
uniform float uSegments;
uniform float uRotation;

out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(textureSize(sTD2DInputs[0], 0));
    vec2 center = vec2(0.5);
    
    // Convert to polar coordinates
    vec2 delta = uv - center;
    float angle = atan(delta.y, delta.x) + uRotation;
    float radius = length(delta);
    
    // Apply kaleidoscope effect
    float segmentAngle = 2.0 * 3.14159265 / uSegments;
    angle = mod(angle, segmentAngle);
    if (mod(floor(angle / segmentAngle * 2.0), 2.0) == 1.0) {
        angle = segmentAngle - angle;
    }
    
    // Convert back to cartesian
    vec2 newUV = center + radius * vec2(cos(angle), sin(angle));
    
    fragColor = texture(sTD2DInputs[0], newUV);
}
'''
    kaleido.par.pixeldat = kaleido_shader
    kaleido.par.value0name = 'uSegments'
    kaleido.par.value0 = 6
    kaleido.par.value1name = 'uRotation'
    kaleido.par.value1 = 0
    
    # Effects mixer
    print("Creating effects mixer...")
    
    # Create switch for each effect
    effect_switches = []
    effect_outputs = [blur, edge, recompose, kaleido]
    
    for i, effect in enumerate(effect_outputs):
        sw = base.create(switchTOP, f'effect_{i}_switch')
        sw.nodeX = 800
        sw.nodeY = 250 - (i * 100)
        sw.par.index = 0  # 0 = bypass, 1 = effect
        sw.inputConnectors[0].connect(transform)  # Bypass
        sw.inputConnectors[1].connect(effect)     # Effect
        effect_switches.append(sw)
    
    # Chain effects together
    for i in range(1, len(effect_switches)):
        effect_switches[i].inputConnectors[0].connect(effect_switches[i-1])
    
    # Final mix output
    final_mix = effect_switches[-1]
    
    # Output Section
    print("Setting up output recording...")
    
    # Preview monitor
    preview = base.create(nullTOP, 'preview_output')
    preview.nodeX = 1000
    preview.nodeY = 0
    preview.inputConnectors[0].connect(final_mix)
    
    # Record output
    record = base.create(moviefileoutTOP, 'record_output')
    record.nodeX = 1200
    record.nodeY = 0
    record.par.file = 'output.mp4'
    record.par.codec = 'h264'
    record.par.bitrate = 10000
    record.par.record = False
    record.inputConnectors[0].connect(preview)
    
    # Control Panel
    print("Creating control panel...")
    
    controls = base.create(containerCOMP, 'controls')
    controls.nodeX = -600
    controls.nodeY = -400
    controls.par.w = 500
    controls.par.h = 400
    
    # Add custom parameters
    page = controls.appendCustomPage('Video Processing Controls')
    
    # Input controls
    page.appendMenu('Input_source', label='Input Source', menuNames=['Movie File', 'Camera'], 
                    menuLabels=['Movie File', 'Camera'], default='Movie File')
    page.appendFile('Movie_file', label='Movie File')
    page.appendInt('Camera_device', label='Camera Device', size=1, default=0, min=0, max=3)
    
    # Pre-processing controls
    page.appendInt('Resolution_w', label='Resolution Width', size=1, default=1920, min=640, max=3840)
    page.appendInt('Resolution_h', label='Resolution Height', size=1, default=1080, min=480, max=2160)
    page.appendFloat('Brightness', label='Brightness', size=1, default=1.0, min=0, max=2)
    page.appendFloat('Gamma', label='Gamma', size=1, default=1.0, min=0.1, max=3)
    page.appendFloat('Scale', label='Scale', size=1, default=1.0, min=0.1, max=2)
    page.appendFloat('Rotate', label='Rotate', size=1, default=0, min=-180, max=180)
    
    # Effect controls
    page.appendToggle('Effect_blur', label='Enable Blur')
    page.appendFloat('Blur_size', label='Blur Size', size=1, default=0, min=0, max=50)
    
    page.appendToggle('Effect_edge', label='Enable Edge Detection')
    
    page.appendToggle('Effect_chroma', label='Enable Chromatic Aberration')
    page.appendFloat('Chroma_amount', label='Chroma Amount', size=1, default=0.01, min=0, max=0.1)
    
    page.appendToggle('Effect_kaleido', label='Enable Kaleidoscope')
    page.appendInt('Kaleido_segments', label='Kaleidoscope Segments', size=1, default=6, min=2, max=16)
    page.appendFloat('Kaleido_rotation', label='Kaleidoscope Rotation', size=1, default=0, min=0, max=360)
    
    # Recording controls
    page.appendFile('Record_file', label='Record File', mode='save')
    page.appendToggle('Record_enable', label='Record')
    
    # Link parameters to operators
    switch.par.index.expr = 'int(op("../controls").par.Input_source)'
    movie_in.par.file.expr = 'op("../controls").par.Movie_file'
    video_in.par.device.expr = 'op("../controls").par.Camera_device'
    
    resolution.par.resolutionw.expr = 'op("../controls").par.Resolution_w'
    resolution.par.resolutionh.expr = 'op("../controls").par.Resolution_h'
    levels.par.brightness1.expr = 'op("../controls").par.Brightness'
    levels.par.gamma1.expr = 'op("../controls").par.Gamma'
    transform.par.scale.expr = 'op("../controls").par.Scale'
    transform.par.rotate.expr = 'op("../controls").par.Rotate'
    
    blur.par.size.expr = 'op("../controls").par.Blur_size'
    effect_switches[0].par.index.expr = 'int(op("../controls").par.Effect_blur)'
    effect_switches[1].par.index.expr = 'int(op("../controls").par.Effect_edge)'
    effect_switches[2].par.index.expr = 'int(op("../controls").par.Effect_chroma)'
    effect_switches[3].par.index.expr = 'int(op("../controls").par.Effect_kaleido)'
    
    chroma_r.par.scale.expr = '1 + op("../controls").par.Chroma_amount'
    chroma_b.par.scale.expr = '1 - op("../controls").par.Chroma_amount'
    
    kaleido.par.value0.expr = 'op("../controls").par.Kaleido_segments'
    kaleido.par.value1.expr = 'op("../controls").par.Kaleido_rotation * 3.14159265 / 180'
    
    record.par.file.expr = 'op("../controls").par.Record_file'
    record.par.record.expr = 'op("../controls").par.Record_enable'
    
    # Add performance monitor
    print("Adding performance monitor...")
    
    info = base.create(infoCHOP, 'performance_info')
    info.nodeX = -600
    info.nodeY = -200
    info.par.gpu = True
    info.par.cpu = True
    info.par.framerate = True
    
    info_dat = base.create(choptoDAT, 'performance_display')
    info_dat.nodeX = -400
    info_dat.nodeY = -200
    info_dat.inputConnectors[0].connect(info)
    
    print("Video processing system created successfully!")
    print(f"System created at: {base.path}")
    print("\nKey features:")
    print("- Movie file and camera input support")
    print("- Resolution and color correction")
    print("- Multiple effects with bypass options")
    print("- Effects can be chained together")
    print("- Output recording with H.264 codec")
    print("- Comprehensive control panel")
    print("- Performance monitoring")
    
    return base

# Execute the template
if __name__ == '__main__':
    create_video_processing_system()