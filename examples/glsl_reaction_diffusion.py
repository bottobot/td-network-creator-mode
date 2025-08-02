"""
Reaction-Diffusion GLSL Shader Network for TouchDesigner
Creates a Gray-Scott reaction-diffusion system with interactive controls
"""

# The GLSL shader code as a string
REACTION_DIFFUSION_GLSL = '''
// Gray-Scott Reaction-Diffusion System
// Creates organic, evolving patterns through chemical simulation

// TouchDesigner uniforms
uniform float uDiffusionA;    // Diffusion rate for chemical A (0.8-1.0)
uniform float uDiffusionB;    // Diffusion rate for chemical B (0.3-0.6)
uniform float uFeedRate;      // Feed rate (0.01-0.1)
uniform float uKillRate;      // Kill rate (0.045-0.07)
uniform float uTimeStep;      // Simulation time step (0.5-2.0)
uniform vec2 uMousePos;       // Mouse position for interaction
uniform float uMouseRadius;   // Radius of mouse influence
uniform int uIterations;      // Number of iterations per frame (1-10)

// Main output
out vec4 fragColor;

// Laplacian kernel weights for diffusion calculation
const float kernel[9] = float[9](
    0.05, 0.2, 0.05,
    0.2, -1.0, 0.2,
    0.05, 0.2, 0.05
);

// Sample the texture with proper boundary handling
vec2 sampleState(vec2 coord) {
    return texture(sTD2DInputs[0], coord).rg;
}

// Calculate Laplacian for diffusion
vec2 laplacian(vec2 uv, vec2 texelSize) {
    vec2 sum = vec2(0.0);
    
    // Apply 3x3 convolution kernel
    for(int i = -1; i <= 1; i++) {
        for(int j = -1; j <= 1; j++) {
            vec2 offset = vec2(float(i), float(j)) * texelSize;
            vec2 sample = sampleState(uv + offset);
            sum += sample * kernel[(i+1)*3 + (j+1)];
        }
    }
    
    return sum;
}

void main() {
    vec2 uv = vUV.st;
    vec2 texelSize = 1.0 / vec2(textureSize(sTD2DInputs[0], 0));
    
    // Get current state (A in red channel, B in green channel)
    vec2 state = sampleState(uv);
    float a = state.r;
    float b = state.g;
    
    // Run multiple iterations for faster evolution
    for(int iter = 0; iter < uIterations; iter++) {
        // Calculate Laplacian for diffusion
        vec2 lap = laplacian(uv, texelSize);
        
        // Gray-Scott reaction-diffusion equations
        float reaction = a * b * b;
        
        // Update concentrations
        a += (uDiffusionA * lap.r - reaction + uFeedRate * (1.0 - a)) * uTimeStep;
        b += (uDiffusionB * lap.g + reaction - (uKillRate + uFeedRate) * b) * uTimeStep;
        
        // Clamp values to valid range
        a = clamp(a, 0.0, 1.0);
        b = clamp(b, 0.0, 1.0);
    }
    
    // Mouse interaction - add chemical B at mouse position
    float mouseDist = length(uv - uMousePos);
    if(mouseDist < uMouseRadius) {
        float influence = 1.0 - (mouseDist / uMouseRadius);
        influence = smoothstep(0.0, 1.0, influence);
        b = mix(b, 1.0, influence * 0.5);
    }
    
    // Output: A in red, B in green, pattern in blue for visualization
    float pattern = clamp(b - a, 0.0, 1.0);
    fragColor = vec4(a, b, pattern, 1.0);
}
'''

def create_reaction_diffusion_network():
    """
    Creates a complete reaction-diffusion network in TouchDesigner
    Returns the main container COMP
    """
    
    # Create main container
    container = op('/project1').create(containerCOMP, 'reaction_diffusion')
    container.nodeX = 0
    container.nodeY = 0
    container.nodeWidth = 200
    container.nodeHeight = 150
    
    # Create feedback loop for state persistence
    feedback_top = container.create(feedbackTOP, 'feedback')
    feedback_top.nodeX = -200
    feedback_top.nodeY = 0
    feedback_top.par.resetpulse.pulse()  # Initialize
    
    # Create noise for initial state
    noise_top = container.create(noiseTOP, 'initial_noise')
    noise_top.nodeX = -400
    noise_top.nodeY = 0
    noise_top.par.resolution1 = 1024
    noise_top.par.resolution2 = 1024
    noise_top.par.type = 'sparse'
    noise_top.par.period = 8
    noise_top.par.amplitude = 0.5
    noise_top.par.offset = 0.5
    
    # Create GLSL TOP for reaction-diffusion
    glsl_top = container.create(glslTOP, 'reaction_diffusion_glsl')
    glsl_top.nodeX = 0
    glsl_top.nodeY = 0
    glsl_top.par.resolution1 = 1024
    glsl_top.par.resolution2 = 1024
    glsl_top.par.pixelformat = 'rgba32float'  # High precision for simulation
    
    # Set GLSL code
    glsl_top.par.fragmentshader = REACTION_DIFFUSION_GLSL
    
    # Connect feedback loop
    glsl_top.inputConnectors[0].connect(feedback_top.outputConnectors[0])
    feedback_top.inputConnectors[0].connect(glsl_top.outputConnectors[0])
    
    # Create parameter controls
    params_container = container.create(containerCOMP, 'parameters')
    params_container.nodeX = 300
    params_container.nodeY = 0
    params_container.nodeWidth = 150
    params_container.nodeHeight = 200
    
    # Diffusion A slider
    diff_a_slider = params_container.create(sliderCOMP, 'diffusion_a')
    diff_a_slider.nodeX = 0
    diff_a_slider.nodeY = 150
    diff_a_slider.par.default1 = 0.9
    diff_a_slider.par.min1 = 0.8
    diff_a_slider.par.max1 = 1.0
    diff_a_slider.par.label = 'Diffusion A'
    
    # Diffusion B slider
    diff_b_slider = params_container.create(sliderCOMP, 'diffusion_b')
    diff_b_slider.nodeX = 0
    diff_b_slider.nodeY = 100
    diff_b_slider.par.default1 = 0.4
    diff_b_slider.par.min1 = 0.3
    diff_b_slider.par.max1 = 0.6
    diff_b_slider.par.label = 'Diffusion B'
    
    # Feed rate slider
    feed_slider = params_container.create(sliderCOMP, 'feed_rate')
    feed_slider.nodeX = 0
    feed_slider.nodeY = 50
    feed_slider.par.default1 = 0.055
    feed_slider.par.min1 = 0.01
    feed_slider.par.max1 = 0.1
    feed_slider.par.label = 'Feed Rate'
    
    # Kill rate slider
    kill_slider = params_container.create(sliderCOMP, 'kill_rate')
    kill_slider.nodeX = 0
    kill_slider.nodeY = 0
    kill_slider.par.default1 = 0.062
    kill_slider.par.min1 = 0.045
    kill_slider.par.max1 = 0.07
    kill_slider.par.label = 'Kill Rate'
    
    # Time step slider
    time_slider = params_container.create(sliderCOMP, 'time_step')
    time_slider.nodeX = 0
    time_slider.nodeY = -50
    time_slider.par.default1 = 1.0
    time_slider.par.min1 = 0.5
    time_slider.par.max1 = 2.0
    time_slider.par.label = 'Time Step'
    
    # Iterations slider
    iter_slider = params_container.create(sliderCOMP, 'iterations')
    iter_slider.nodeX = 0
    iter_slider.nodeY = -100
    iter_slider.par.default1 = 3
    iter_slider.par.min1 = 1
    iter_slider.par.max1 = 10
    iter_slider.par.slidertype = 'int'
    iter_slider.par.label = 'Iterations'
    
    # Create CHOPs for parameter values
    # Merge all parameters into one CHOP
    merge_chop = container.create(mergeCHOP, 'param_merge')
    merge_chop.nodeX = 200
    merge_chop.nodeY = -200
    
    # Connect sliders to merge CHOP
    for i, slider in enumerate([diff_a_slider, diff_b_slider, feed_slider, 
                                kill_slider, time_slider, iter_slider]):
        slider_name = slider.name
        select_chop = container.create(selectCHOP, f'select_{slider_name}')
        select_chop.nodeX = 0
        select_chop.nodeY = -200 - (i * 50)
        select_chop.par.chop = f'../parameters/{slider_name}/out1'
        select_chop.par.channames = 'chan1'
        select_chop.par.renameto = slider_name
        merge_chop.inputConnectors[i].connect(select_chop.outputConnectors[0])
    
    # Create mouse input
    mouse_in = container.create(mouseinCHOP, 'mouse')
    mouse_in.nodeX = -200
    mouse_in.nodeY = -200
    
    # Create constant for mouse radius
    const_chop = container.create(constantCHOP, 'mouse_radius')
    const_chop.nodeX = -200
    const_chop.nodeY = -300
    const_chop.par.name0 = 'radius'
    const_chop.par.value0 = 0.05
    
    # Link parameters to GLSL uniforms
    glsl_top.par.uniformname0 = 'uDiffusionA'
    glsl_top.par.uniformvalue0 = "op('../param_merge')['diffusion_a']"
    
    glsl_top.par.uniformname1 = 'uDiffusionB'
    glsl_top.par.uniformvalue1 = "op('../param_merge')['diffusion_b']"
    
    glsl_top.par.uniformname2 = 'uFeedRate'
    glsl_top.par.uniformvalue2 = "op('../param_merge')['feed_rate']"
    
    glsl_top.par.uniformname3 = 'uKillRate'
    glsl_top.par.uniformvalue3 = "op('../param_merge')['kill_rate']"
    
    glsl_top.par.uniformname4 = 'uTimeStep'
    glsl_top.par.uniformvalue4 = "op('../param_merge')['time_step']"
    
    glsl_top.par.uniformname5 = 'uMousePos'
    glsl_top.par.uniformvalue5x = "op('../mouse')['tx']"
    glsl_top.par.uniformvalue5y = "op('../mouse')['ty']"
    
    glsl_top.par.uniformname6 = 'uMouseRadius'
    glsl_top.par.uniformvalue6 = "op('../mouse_radius')['radius']"
    
    glsl_top.par.uniformname7 = 'uIterations'
    glsl_top.par.uniformvalue7 = "int(op('../param_merge')['iterations'])"
    
    # Create color mapping
    ramp_top = container.create(rampTOP, 'color_ramp')
    ramp_top.nodeX = 200
    ramp_top.nodeY = 0
    ramp_top.par.ramptype = 'radial'
    ramp_top.par.phase = 0
    
    # Lookup TOP for color mapping
    lookup_top = container.create(lookupTOP, 'color_lookup')
    lookup_top.nodeX = 400
    lookup_top.nodeY = 0
    lookup_top.inputConnectors[0].connect(glsl_top.outputConnectors[0])
    lookup_top.inputConnectors[1].connect(ramp_top.outputConnectors[0])
    lookup_top.par.lookupmode = 'luminance'
    
    # Output
    out_top = container.create(outTOP, 'out1')
    out_top.nodeX = 600
    out_top.nodeY = 0
    out_top.inputConnectors[0].connect(lookup_top.outputConnectors[0])
    
    # Create reset button
    button_comp = container.create(buttonCOMP, 'reset')
    button_comp.nodeX = 300
    button_comp.nodeY = -300
    button_comp.par.buttonlabel = 'Reset'
    
    # Create execute DAT for reset logic
    exec_dat = container.create(executeDat, 'reset_exec')
    exec_dat.nodeX = 500
    exec_dat.nodeY = -300
    exec_dat.par.executepars = 'offtooncook'
    exec_dat.par.dat = '../reset'
    exec_dat.text = '''
def onOffToOn(channel, sampleIndex, val, prev):
    op('../feedback').par.resetpulse.pulse()
    return
'''
    
    return container

# Execute the network creation
if __name__ == '__main__':
    network = create_reaction_diffusion_network()
    print(f"Created reaction-diffusion network at: {network.path}")