"""
GPU Particle System Template for TouchDesigner
Creates a high-performance particle system with physics and instancing
"""

def create_particle_system():
    """
    Creates a GPU-based particle system with:
    - Particle emitter configuration
    - Forces and physics simulation
    - Efficient rendering pipeline
    - Instancing setup for performance
    """
    
    # Create base container
    base = op('/project1').create(containerCOMP, 'particle_system')
    base.par.w = 1400
    base.par.h = 900
    base.nodeX = 0
    base.nodeY = 0
    
    # Particle Emitter Setup
    print("Creating particle emitter...")
    
    # Create particle count and initial positions
    particle_count = base.create(tableSOP, 'particle_count')
    particle_count.nodeX = -600
    particle_count.nodeY = 200
    particle_count.par.rows = 10000  # Number of particles
    particle_count.par.cols = 1
    
    # Convert to points
    points = base.create(soptoSOP, 'particle_points')
    points.nodeX = -400
    points.nodeY = 200
    points.par.soptype = 'points'
    points.inputConnectors[0].connect(particle_count)
    
    # Add initial position attributes
    attrib_create = base.create(attribcreateSOP, 'initial_positions')
    attrib_create.nodeX = -200
    attrib_create.nodeY = 200
    attrib_create.par.name0 = 'P'
    attrib_create.par.type0 = 'vector'
    attrib_create.par.value0x = 0
    attrib_create.par.value0y = 0
    attrib_create.par.value0z = 0
    attrib_create.inputConnectors[0].connect(points)
    
    # Add velocity attributes
    velocity_attrib = base.create(attribcreateSOP, 'initial_velocity')
    velocity_attrib.nodeX = 0
    velocity_attrib.nodeY = 200
    velocity_attrib.par.name0 = 'v'
    velocity_attrib.par.type0 = 'vector'
    velocity_attrib.par.value0x = 0
    velocity_attrib.par.value0y = 1
    velocity_attrib.par.value0z = 0
    velocity_attrib.inputConnectors[0].connect(attrib_create)
    
    # Add life attribute
    life_attrib = base.create(attribcreateSOP, 'particle_life')
    life_attrib.nodeX = 200
    life_attrib.nodeY = 200
    life_attrib.par.name0 = 'life'
    life_attrib.par.type0 = 'float'
    life_attrib.par.value00 = 1.0
    life_attrib.inputConnectors[0].connect(velocity_attrib)
    
    # Physics Simulation using GLSL
    print("Setting up physics simulation...")
    
    # Create GLSL shader for particle physics
    physics_glsl = base.create(glslTOP, 'particle_physics')
    physics_glsl.nodeX = -400
    physics_glsl.nodeY = 0
    physics_glsl.par.resolutionw = 512
    physics_glsl.par.resolutionh = 512
    
    # Particle physics shader
    physics_shader = '''
// Particle Physics Simulation
uniform float uTime;
uniform float uDeltaTime;
uniform vec3 uGravity;
uniform vec3 uWind;
uniform float uDrag;
uniform float uNoiseScale;
uniform float uNoiseSpeed;
uniform sampler2D sPositions;
uniform sampler2D sVelocities;

// Simplex noise function
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

float snoise(vec2 v) {
    const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                       -0.577350269189626, 0.024390243902439);
    vec2 i  = floor(v + dot(v, C.yy));
    vec2 x0 = v -   i + dot(i, C.xx);
    vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;
    i = mod289(i);
    vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0))
                           + i.x + vec3(0.0, i1.x, 1.0));
    vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy),
                           dot(x12.zw,x12.zw)), 0.0);
    m = m*m;
    m = m*m;
    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;
    m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
    vec3 g;
    g.x  = a0.x  * x0.x  + h.x  * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);
}

out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(textureSize(sPositions, 0));
    
    // Read current state
    vec4 posData = texture(sPositions, uv);
    vec4 velData = texture(sVelocities, uv);
    
    vec3 pos = posData.xyz;
    float life = posData.w;
    vec3 vel = velData.xyz;
    
    // Apply forces
    vec3 force = vec3(0.0);
    
    // Gravity
    force += uGravity;
    
    // Wind with turbulence
    vec2 noiseCoord = pos.xz * uNoiseScale + uTime * uNoiseSpeed;
    float turbulence = snoise(noiseCoord);
    force += uWind * (1.0 + turbulence * 0.5);
    
    // Drag
    force -= vel * uDrag;
    
    // Update velocity
    vel += force * uDeltaTime;
    
    // Update position
    pos += vel * uDeltaTime;
    
    // Update life
    life -= uDeltaTime * 0.2; // Particles live for ~5 seconds
    
    // Reset particle if dead
    if (life <= 0.0) {
        pos = vec3(
            (fract(sin(uTime + uv.x * 12.9898) * 43758.5453) - 0.5) * 2.0,
            0.0,
            (fract(sin(uTime + uv.y * 78.233) * 43758.5453) - 0.5) * 2.0
        );
        vel = vec3(0.0, 2.0 + fract(sin(uv.x * 34.123) * 23421.631), 0.0);
        life = 1.0;
    }
    
    // Output updated state
    if (gl_FragCoord.x < 256.0) {
        fragColor = vec4(pos, life);
    } else {
        fragColor = vec4(vel, 1.0);
    }
}
'''
    
    physics_glsl.par.pixeldat = physics_shader
    
    # Create feedback loop for physics
    feedback = base.create(feedbackTOP, 'physics_feedback')
    feedback.nodeX = -200
    feedback.nodeY = 0
    feedback.inputConnectors[0].connect(physics_glsl)
    
    # Rendering Pipeline
    print("Creating rendering pipeline...")
    
    # Convert physics data to CHOP
    physics_to_chop = base.create(topToCHOP, 'physics_data')
    physics_to_chop.nodeX = 0
    physics_to_chop.nodeY = 0
    physics_to_chop.par.crop = 0
    physics_to_chop.par.rgbatofields = 1
    physics_to_chop.inputConnectors[0].connect(feedback)
    
    # Split position and velocity data
    pos_select = base.create(selectCHOP, 'position_data')
    pos_select.nodeX = 200
    pos_select.nodeY = 50
    pos_select.par.channames = 'r g b'
    pos_select.inputConnectors[0].connect(physics_to_chop)
    
    life_select = base.create(selectCHOP, 'life_data')
    life_select.nodeX = 200
    life_select.nodeY = -50
    life_select.par.channames = 'a'
    life_select.inputConnectors[0].connect(physics_to_chop)
    
    # Create instance geometry
    print("Setting up instancing...")
    
    # Particle geometry (sphere)
    particle_geo = base.create(sphereSOP, 'particle_geometry')
    particle_geo.nodeX = -400
    particle_geo.nodeY = -200
    particle_geo.par.rad = 0.02
    particle_geo.par.rows = 8
    particle_geo.par.cols = 16
    
    # Instance setup
    instance = base.create(geometryCOMP, 'particle_instances')
    instance.nodeX = 0
    instance.nodeY = -200
    instance.par.instanceop = '../particle_geometry'
    instance.par.instancetx = '../position_data'
    instance.par.instancety = '../position_data'
    instance.par.instancetz = '../position_data'
    instance.par.instancetxchan = 'r'
    instance.par.instancetychan = 'g'
    instance.par.instancetzchan = 'b'
    
    # Add scale based on life
    instance.par.instancesx = '../life_data'
    instance.par.instancesy = '../life_data'
    instance.par.instancesz = '../life_data'
    instance.par.instancesxchan = 'a'
    instance.par.instancesychan = 'a'
    instance.par.instanceszchan = 'a'
    
    # Material setup
    material = base.create(constantMAT, 'particle_material')
    material.nodeX = -200
    material.nodeY = -300
    material.par.colorr = 1.0
    material.par.colorg = 0.5
    material.par.colorb = 0.2
    material.par.alpha = 0.8
    
    instance.par.material = '../particle_material'
    
    # Camera setup
    camera = base.create(cameraCOMP, 'render_camera')
    camera.nodeX = 200
    camera.nodeY = -300
    camera.par.tz = 5
    camera.par.ty = 2
    camera.par.rx = -15
    
    # Render TOP
    render = base.create(renderTOP, 'particle_render')
    render.nodeX = 400
    render.nodeY = -200
    render.par.resolutionw = 1920
    render.par.resolutionh = 1080
    render.par.geometry = '../particle_instances'
    render.par.camera = '../render_camera'
    render.par.lights = ''  # No lights needed for constant material
    
    # Post-processing
    print("Adding post-processing...")
    
    # Bloom effect
    blur1 = base.create(blurTOP, 'bloom_blur1')
    blur1.nodeX = 600
    blur1.nodeY = -200
    blur1.par.size = 10
    blur1.inputConnectors[0].connect(render)
    
    level = base.create(levelTOP, 'bloom_threshold')
    level.nodeX = 600
    level.nodeY = -300
    level.par.blacklevel = 0.5
    level.inputConnectors[0].connect(blur1)
    
    blur2 = base.create(blurTOP, 'bloom_blur2')
    blur2.nodeX = 800
    blur2.nodeY = -300
    blur2.par.size = 20
    blur2.inputConnectors[0].connect(level)
    
    comp = base.create(compositeTOP, 'bloom_composite')
    comp.nodeX = 1000
    comp.nodeY = -200
    comp.par.operand = 'add'
    comp.inputConnectors[0].connect(render)
    comp.inputConnectors[1].connect(blur2)
    
    # Final output
    out = base.create(outTOP, 'output')
    out.nodeX = 1200
    out.nodeY = -200
    out.inputConnectors[0].connect(comp)
    
    # Control Panel
    print("Creating control panel...")
    
    controls = base.create(containerCOMP, 'controls')
    controls.nodeX = -600
    controls.nodeY = -400
    controls.par.w = 400
    controls.par.h = 300
    
    # Add custom parameters
    page = controls.appendCustomPage('Particle Controls')
    
    # Physics parameters
    page.appendXYZ('Gravity', label='Gravity', default=[0, -9.8, 0])
    page.appendXYZ('Wind', label='Wind Force', default=[1, 0, 0])
    page.appendFloat('Drag', label='Air Drag', size=1, default=0.1, min=0, max=1)
    
    # Turbulence parameters
    page.appendFloat('Noise_scale', label='Turbulence Scale', size=1, default=0.5, min=0.1, max=2)
    page.appendFloat('Noise_speed', label='Turbulence Speed', size=1, default=0.2, min=0, max=1)
    
    # Particle parameters
    page.appendInt('Particle_count', label='Particle Count', size=1, default=10000, min=100, max=50000)
    page.appendFloat('Particle_size', label='Particle Size', size=1, default=0.02, min=0.001, max=0.1)
    
    # Visual parameters
    page.appendRGB('Particle_color', label='Particle Color', default=[1, 0.5, 0.2])
    page.appendFloat('Particle_alpha', label='Particle Alpha', size=1, default=0.8, min=0, max=1)
    
    # Link parameters to operators
    physics_glsl.par.value0name = 'uGravity'
    physics_glsl.par.value0x.expr = 'op("../controls").par.Gravityx'
    physics_glsl.par.value0y.expr = 'op("../controls").par.Gravityy'
    physics_glsl.par.value0z.expr = 'op("../controls").par.Gravityz'
    
    physics_glsl.par.value1name = 'uWind'
    physics_glsl.par.value1x.expr = 'op("../controls").par.Windx'
    physics_glsl.par.value1y.expr = 'op("../controls").par.Windy'
    physics_glsl.par.value1z.expr = 'op("../controls").par.Windz'
    
    physics_glsl.par.value2name = 'uDrag'
    physics_glsl.par.value2.expr = 'op("../controls").par.Drag'
    
    physics_glsl.par.value3name = 'uNoiseScale'
    physics_glsl.par.value3.expr = 'op("../controls").par.Noise_scale'
    
    physics_glsl.par.value4name = 'uNoiseSpeed'
    physics_glsl.par.value4.expr = 'op("../controls").par.Noise_speed'
    
    # Link visual parameters
    particle_count.par.rows.expr = 'op("../controls").par.Particle_count'
    particle_geo.par.rad.expr = 'op("../controls").par.Particle_size'
    material.par.colorr.expr = 'op("../controls").par.Particle_colorr'
    material.par.colorg.expr = 'op("../controls").par.Particle_colorg'
    material.par.colorb.expr = 'op("../controls").par.Particle_colorb'
    material.par.alpha.expr = 'op("../controls").par.Particle_alpha'
    
    print("GPU particle system created successfully!")
    print(f"System created at: {base.path}")
    print("\nKey features:")
    print("- GPU-based physics simulation")
    print("- Efficient instancing for thousands of particles")
    print("- Turbulent wind forces")
    print("- Particle life cycle management")
    print("- Post-processing with bloom")
    print("- Comprehensive control panel")
    
    return base

# Execute the template
if __name__ == '__main__':
    create_particle_system()