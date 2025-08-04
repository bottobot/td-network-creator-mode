"""
TouchDesigner Python API Examples - Parameter Manipulation
This file demonstrates how to work with parameters in TouchDesigner.
"""

# Basic Parameter Setting
def basic_parameter_examples():
    """Examples of basic parameter manipulation"""
    
    # Create a test operator
    noise = op('/project1').create(noiseTOP, 'param_test_noise')
    
    # Set single value parameters
    noise.par.w = 1920
    noise.par.h = 1080
    noise.par.period = 5.0
    noise.par.seed = 1
    
    # Set menu parameters by index or string
    noise.par.type = 'sparse'  # By string
    noise.par.type = 1  # By index
    
    # Set toggle parameters
    noise.par.monochrome = True
    noise.par.normalize = False
    
    # Set color parameters (RGB)
    transform = op('/project1').create(transformTOP, 'param_test_transform')
    transform.par.bgcolor = (0.2, 0.3, 0.8)  # Tuple
    transform.par.bgcolorr = 0.2  # Individual channels
    transform.par.bgcolorg = 0.3
    transform.par.bgcolorb = 0.8
    
    return noise


# Reading Parameter Values
def read_parameter_examples():
    """Examples of reading parameter values"""
    
    # Create test operator
    movie = op('/project1').create(moviefileinTOP, 'read_test_movie')
    movie.par.file = 'C:/media/test.mp4'
    movie.par.speed = 2.0
    
    # Read different parameter types
    file_path = movie.par.file.eval()  # String parameter
    speed_value = movie.par.speed.eval()  # Float parameter
    play_state = movie.par.play.eval()  # Toggle parameter
    
    # Read menu parameter
    extend_mode = movie.par.extend.eval()  # Returns current string value
    extend_index = movie.par.extend.menuIndex  # Returns current index
    extend_names = movie.par.extend.menuNames  # Returns all menu options
    extend_labels = movie.par.extend.menuLabels  # Returns menu labels
    
    # Read parameter properties
    speed_min = movie.par.speed.min
    speed_max = movie.par.speed.max
    speed_default = movie.par.speed.default
    speed_label = movie.par.speed.label
    
    # Print parameter info
    print(f"File: {file_path}")
    print(f"Speed: {speed_value} (min: {speed_min}, max: {speed_max})")
    print(f"Extend Mode: {extend_mode} (index: {extend_index})")
    print(f"Available modes: {extend_names}")
    
    return movie


# Expression Mode
def expression_mode_examples():
    """Examples of using expressions in parameters"""
    
    # Create operators for expression examples
    source = op('/project1').create(constantCHOP, 'expr_source')
    source.par.value0 = 0.5
    
    target = op('/project1').create(circleTOP, 'expr_target')
    
    # Set parameter to expression mode and add expression
    target.par.radius.expr = 'op("expr_source")["chan1"] * 100 + 50'
    target.par.radius.mode = ParMode.EXPRESSION
    
    # Common expression patterns
    level = op('/project1').create(levelTOP, 'expr_level')
    
    # Time-based expression
    level.par.brightness1.expr = 'abs(sin(absTime.seconds * 2))'
    level.par.brightness1.mode = ParMode.EXPRESSION
    
    # Reference another parameter
    level.par.contrast.expr = 'op("expr_level").par.brightness1 * 0.5'
    level.par.contrast.mode = ParMode.EXPRESSION
    
    # Python expression
    level.par.gamma1.expr = 'max(0.5, min(2.0, me.time.seconds % 3))'
    level.par.gamma1.mode = ParMode.EXPRESSION
    
    # Export from CHOP
    math = op('/project1').create(mathCHOP, 'expr_math')
    math.par.gain = 2
    
    # Export to parameter
    target.par.radiusx.mode = ParMode.EXPORT
    target.par.radiusx.export = math
    
    return target


# Parameter Pages and Custom Parameters
def custom_parameter_examples():
    """Examples of working with parameter pages and custom parameters"""
    
    # Create a container for custom parameters
    container = op('/project1').create(containerCOMP, 'custom_param_container')
    
    # Add a custom page
    page = container.appendCustomPage('Custom Controls')
    
    # Add different types of custom parameters
    # Float parameter
    float_par = page.appendFloat('Speed', label='Speed Control')[0]
    float_par.default = 1.0
    float_par.min = 0.0
    float_par.max = 10.0
    float_par.clampMin = True
    float_par.clampMax = True
    
    # Integer parameter
    int_par = page.appendInt('Count', label='Object Count')[0]
    int_par.default = 5
    int_par.min = 1
    int_par.max = 100
    
    # String parameter
    str_par = page.appendStr('Label', label='Display Label')[0]
    str_par.default = 'Hello TouchDesigner'
    
    # Menu parameter
    menu_par = page.appendMenu('Mode', label='Operation Mode')[0]
    menu_par.menuNames = ['add', 'multiply', 'subtract', 'divide']
    menu_par.menuLabels = ['Add', 'Multiply', 'Subtract', 'Divide']
    menu_par.default = 'add'
    
    # Toggle parameter
    toggle_par = page.appendToggle('Enable', label='Enable Effect')[0]
    toggle_par.default = True
    
    # Pulse parameter (button)
    pulse_par = page.appendPulse('Reset', label='Reset Values')[0]
    
    # XY parameter
    xy_par = page.appendXY('Position', label='XY Position')[0]
    xy_par[0].default = 0.5  # X
    xy_par[1].default = 0.5  # Y
    
    # XYZ parameter
    xyz_par = page.appendXYZ('Rotation', label='3D Rotation')[0]
    xyz_par[0].default = 0  # X
    xyz_par[1].default = 0  # Y
    xyz_par[2].default = 0  # Z
    
    # RGB parameter
    rgb_par = page.appendRGB('Color', label='Color Selection')[0]
    rgb_par[0].default = 1.0  # R
    rgb_par[1].default = 0.5  # G
    rgb_par[2].default = 0.0  # B
    
    # File parameter
    file_par = page.appendFile('File', label='Select File')[0]
    file_par.default = ''
    
    # Folder parameter
    folder_par = page.appendFolder('Folder', label='Select Folder')[0]
    
    # Add a second custom page
    page2 = container.appendCustomPage('Advanced')
    
    # Python parameter (multi-line text)
    python_par = page2.appendPython('Script', label='Python Script')[0]
    python_par.default = '''# Custom script
def process():
    return True'''
    
    # Set some values
    container.par.Speed = 2.5
    container.par.Count = 10
    container.par.Enable = True
    
    return container


# Parameter Animation
def parameter_animation_examples():
    """Examples of animating parameters"""
    
    # Create operator to animate
    circle = op('/project1').create(circleTOP, 'animated_circle')
    
    # Create animation channels
    animation = op('/project1').create(animationCOMP, 'circle_animation')
    
    # Add channels for parameters
    chan_x = animation.appendChan('tx')
    chan_y = animation.appendChan('ty')
    chan_radius = animation.appendChan('radius')
    
    # Set up keyframes
    # X position animation
    chan_x.addKey(0, -0.5)
    chan_x.addKey(60, 0.5)
    chan_x.addKey(120, -0.5)
    
    # Y position animation (circular motion)
    for i in range(0, 121, 10):
        time = i
        value = math.sin(i * math.pi / 60) * 0.3
        chan_y.addKey(time, value)
    
    # Radius animation
    chan_radius.addKey(0, 50)
    chan_radius.addKey(30, 150)
    chan_radius.addKey(60, 50)
    chan_radius.addKey(90, 100)
    chan_radius.addKey(120, 50)
    
    # Export animation to circle parameters
    circle.par.centerx.expr = 'op("circle_animation")["tx"]'
    circle.par.centery.expr = 'op("circle_animation")["ty"]'
    circle.par.radius.expr = 'op("circle_animation")["radius"]'
    
    # Alternative: Using Pattern CHOP for animation
    pattern = op('/project1').create(patternCHOP, 'param_pattern')
    pattern.par.length = 600
    pattern.par.type = 'sine'
    pattern.par.period = 120
    pattern.par.amplitude = 100
    pattern.par.offset = 100
    
    # Create another circle animated by pattern
    circle2 = op('/project1').create(circleTOP, 'pattern_animated_circle')
    circle2.par.radius.expr = 'op("param_pattern")[0]'
    circle2.nodeY = -200
    
    return animation


# Batch Parameter Operations
def batch_parameter_operations():
    """Examples of setting parameters on multiple operators"""
    
    # Create multiple operators
    noises = []
    for i in range(5):
        n = op('/project1').create(noiseTOP, f'batch_noise_{i}')
        n.nodeX = i * 150
        n.nodeY = -400
        noises.append(n)
    
    # Set parameters on all operators
    for i, noise in enumerate(noises):
        # Common parameters
        noise.par.w = 256
        noise.par.h = 256
        
        # Varying parameters
        noise.par.period = 5 + i * 2
        noise.par.seed = i
        noise.par.amplitude = 0.5 + i * 0.1
    
    # Find and modify operators by pattern
    for op_obj in op('/project1').findChildren(name='batch_noise_*'):
        op_obj.par.monochrome = True
    
    # Copy parameters from one operator to another
    source = noises[0]
    target = op('/project1').create(noiseTOP, 'param_copy_target')
    
    # Copy all parameters from a page
    for par in source.pars('*'):
        if hasattr(target.par, par.name):
            target.par[par.name].val = par.eval()
    
    return noises


# Parameter Binding and References
def parameter_binding_examples():
    """Examples of binding parameters together"""
    
    # Create master control
    master = op('/project1').create(containerCOMP, 'master_control')
    page = master.appendCustomPage('Master')
    
    # Add master parameters
    master_speed = page.appendFloat('MasterSpeed', label='Master Speed')[0]
    master_speed.default = 1.0
    master_color = page.appendRGB('MasterColor', label='Master Color')[0]
    
    # Create slave operators
    slaves = []
    for i in range(3):
        slave = op('/project1').create(constantTOP, f'slave_{i}')
        slave.nodeX = i * 150
        slave.nodeY = -600
        slaves.append(slave)
        
        # Bind to master parameters
        slave.par.colorr.expr = f'op("master_control").par.MasterColorr'
        slave.par.colorg.expr = f'op("master_control").par.MasterColorg'
        slave.par.colorb.expr = f'op("master_control").par.MasterColorb'
    
    # Create speed-controlled animation
    speed_lfo = op('/project1').create(lfoCHOP, 'speed_lfo')
    speed_lfo.par.rate.expr = 'op("master_control").par.MasterSpeed'
    
    # Set master values
    master.par.MasterSpeed = 2.0
    master.par.MasterColorr = 1.0
    master.par.MasterColorg = 0.5
    master.par.MasterColorb = 0.0
    
    return master


# Parameter Sequences and Patterns
def parameter_sequence_examples():
    """Examples of creating parameter sequences"""
    
    # Create a sequence of transforms
    prev_op = None
    for i in range(5):
        transform = op('/project1').create(transformTOP, f'sequence_transform_{i}')
        transform.nodeX = i * 150
        transform.nodeY = -800
        
        # Sequential rotation
        transform.par.rotate = i * 15
        
        # Sequential scale
        transform.par.scale = 1.0 - (i * 0.15)
        
        # Connect to previous
        if prev_op:
            transform.inputConnectors[0].connect(prev_op)
        else:
            # Create source for first transform
            source = op('/project1').create(noiseTOP, 'sequence_source')
            source.nodeX = -150
            source.nodeY = -800
            transform.inputConnectors[0].connect(source)
        
        prev_op = transform
    
    return prev_op


# Advanced Parameter Techniques
def advanced_parameter_techniques():
    """Advanced parameter manipulation techniques"""
    
    # Create test operator
    comp = op('/project1').create(compositeTOP, 'advanced_params')
    
    # Parameter state management
    # Save current state
    saved_params = {}
    for par in comp.pars():
        saved_params[par.name] = par.eval()
    
    # Modify parameters
    comp.par.operand = 'multiply'
    comp.par.prefitr = 0.5
    
    # Restore saved state
    for name, value in saved_params.items():
        if hasattr(comp.par, name):
            comp.par[name].val = value
    
    # Parameter validation
    def validate_and_set_parameter(op_obj, param_name, value):
        """Safely set parameter with validation"""
        if hasattr(op_obj.par, param_name):
            par = op_obj.par[param_name]
            
            # Check if parameter is read-only
            if par.isReadOnly:
                print(f"Parameter {param_name} is read-only")
                return False
            
            # Validate numeric parameters
            if hasattr(par, 'min') and hasattr(par, 'max'):
                if par.clampMin and value < par.min:
                    value = par.min
                if par.clampMax and value > par.max:
                    value = par.max
            
            # Set the value
            par.val = value
            return True
        else:
            print(f"Parameter {param_name} does not exist")
            return False
    
    # Test validation
    validate_and_set_parameter(comp, 'prefitr', 2.0)  # Will be clamped
    validate_and_set_parameter(comp, 'invalid_param', 1.0)  # Will fail
    
    return comp


# Main execution example
if __name__ == '__main__':
    import math
    
    # Run all examples
    basic = basic_parameter_examples()
    reading = read_parameter_examples()
    expressions = expression_mode_examples()
    custom = custom_parameter_examples()
    animation = parameter_animation_examples()
    batch = batch_parameter_operations()
    binding = parameter_binding_examples()
    sequence = parameter_sequence_examples()
    advanced = advanced_parameter_techniques()
    
    print("All parameter manipulation examples completed!")