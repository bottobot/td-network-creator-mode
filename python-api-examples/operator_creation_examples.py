"""
TouchDesigner Python API Examples - Operator Creation
This file demonstrates how to create different types of operators programmatically.
"""

# Creating TOPs (Texture Operators)
def create_top_examples():
    """Examples of creating various TOP operators"""
    
    # Create a Noise TOP
    noise = op('/project1').create(noiseT, 'noise1')
    noise.par.w = 1920
    noise.par.h = 1080
    noise.par.type = 'sparse'
    noise.par.period = 5
    
    # Create a Movie File In TOP
    movie = op('/project1').create(moviefileinTOP, 'movie1')
    movie.par.file = 'C:/media/video.mp4'
    movie.par.play = True
    
    # Create a Composite TOP
    comp = op('/project1').create(compositeTOP, 'comp1')
    comp.par.operand = 'over'
    comp.par.alignorder = 1
    
    # Position operators
    noise.nodeX = -200
    noise.nodeY = 0
    movie.nodeX = -200
    movie.nodeY = -150
    comp.nodeX = 0
    comp.nodeY = -75
    
    # Connect operators
    comp.inputConnectors[0].connect(noise)
    comp.inputConnectors[1].connect(movie)
    
    return comp


# Creating CHOPs (Channel Operators)
def create_chop_examples():
    """Examples of creating various CHOP operators"""
    
    # Create an Audio Device In CHOP
    audio_in = op('/project1').create(audiodeviceinCHOP, 'audio_in1')
    audio_in.par.device = 0  # Default device
    audio_in.par.channels = 2
    
    # Create an Analyze CHOP
    analyze = op('/project1').create(analyzeCHOP, 'analyze1')
    analyze.par.function = 'rms'
    
    # Create a Math CHOP
    math = op('/project1').create(mathCHOP, 'math1')
    math.par.gain = 2.0
    math.par.offset = 0.5
    
    # Position and connect
    audio_in.nodeX = -200
    audio_in.nodeY = 200
    analyze.nodeX = 0
    analyze.nodeY = 200
    math.nodeX = 200
    math.nodeY = 200
    
    analyze.inputConnectors[0].connect(audio_in)
    math.inputConnectors[0].connect(analyze)
    
    return math


# Creating SOPs (Surface Operators)
def create_sop_examples():
    """Examples of creating various SOP operators"""
    
    # Create a Sphere SOP
    sphere = op('/project1').create(sphereSOP, 'sphere1')
    sphere.par.rad = (1, 1, 1)
    sphere.par.rows = 32
    sphere.par.cols = 32
    
    # Create a Noise SOP
    noise = op('/project1').create(noiseSOP, 'noise1')
    noise.par.amp = 0.5
    noise.par.period = 2
    noise.par.roughness = 0.5
    
    # Create a Transform SOP
    transform = op('/project1').create(transformSOP, 'transform1')
    transform.par.r = (0, 45, 0)
    transform.par.s = (1.5, 1.5, 1.5)
    
    # Position and connect
    sphere.nodeX = -200
    sphere.nodeY = 400
    noise.nodeX = 0
    noise.nodeY = 400
    transform.nodeX = 200
    transform.nodeY = 400
    
    noise.inputConnectors[0].connect(sphere)
    transform.inputConnectors[0].connect(noise)
    
    return transform


# Creating DATs (Data Operators)
def create_dat_examples():
    """Examples of creating various DAT operators"""
    
    # Create a Table DAT
    table = op('/project1').create(tableDAT, 'table1')
    table.clear()
    table.appendRow(['Name', 'Value', 'Type'])
    table.appendRow(['Speed', '1.0', 'float'])
    table.appendRow(['Color', '1,0,0', 'rgb'])
    
    # Create a Text DAT
    text = op('/project1').create(textDAT, 'text1')
    text.text = '''# TouchDesigner Script
import math

def process_data(val):
    return math.sin(val) * 0.5 + 0.5
'''
    
    # Create a Select DAT
    select = op('/project1').create(selectDAT, 'select1')
    select.par.dat = table
    select.par.rows = '1-2'
    select.par.cols = '*'
    
    # Position operators
    table.nodeX = -200
    table.nodeY = 600
    text.nodeX = 0
    text.nodeY = 600
    select.nodeX = 200
    select.nodeY = 600
    
    return select


# Creating MATs (Material Operators)
def create_mat_examples():
    """Examples of creating various MAT operators"""
    
    # Create a Phong MAT
    phong = op('/project1').create(phongMAT, 'phong1')
    phong.par.diffr = 0.8
    phong.par.diffg = 0.2
    phong.par.diffb = 0.2
    phong.par.specr = 1
    phong.par.specg = 1
    phong.par.specb = 1
    phong.par.shininess = 0.5
    
    # Create a PBR MAT
    pbr = op('/project1').create(pbrMAT, 'pbr1')
    pbr.par.basecolorr = 0.5
    pbr.par.basecolorg = 0.5
    pbr.par.basecolorb = 0.8
    pbr.par.roughness = 0.3
    pbr.par.metallic = 0.8
    
    # Create a GLSL MAT
    glsl = op('/project1').create(glslMAT, 'glsl1')
    # GLSL shader would be set via the vertex and pixel shader parameters
    
    # Position operators
    phong.nodeX = -200
    phong.nodeY = 800
    pbr.nodeX = 0
    pbr.nodeY = 800
    glsl.nodeX = 200
    glsl.nodeY = 800
    
    return pbr


# Creating COMPs (Component Operators)
def create_comp_examples():
    """Examples of creating various COMP operators"""
    
    # Create a Container COMP
    container = op('/project1').create(containerCOMP, 'container1')
    container.par.w = 400
    container.par.h = 300
    container.par.display = True
    
    # Create a Geometry COMP
    geo = op('/project1').create(geometryCOMP, 'geo1')
    geo.par.scale = (2, 2, 2)
    
    # Create a Camera COMP
    camera = op('/project1').create(cameraCOMP, 'camera1')
    camera.par.t = (0, 0, 5)
    camera.par.lookat = (0, 0, 0)
    
    # Create a Light COMP
    light = op('/project1').create(lightCOMP, 'light1')
    light.par.t = (2, 2, 2)
    light.par.lighttype = 'point'
    light.par.dimmer = 1
    
    # Position operators
    container.nodeX = -200
    container.nodeY = 1000
    geo.nodeX = 0
    geo.nodeY = 1000
    camera.nodeX = 200
    camera.nodeY = 1000
    light.nodeX = 400
    light.nodeY = 1000
    
    return container


# Parent/Child Relationships
def create_parent_child_examples():
    """Examples of creating parent/child relationships"""
    
    # Create parent container
    parent_container = op('/project1').create(containerCOMP, 'parent_container')
    parent_container.par.w = 600
    parent_container.par.h = 400
    
    # Create child operators inside parent
    child_noise = parent_container.create(noiseTOP, 'child_noise')
    child_noise.par.w = 256
    child_noise.par.h = 256
    
    child_level = parent_container.create(levelTOP, 'child_level')
    child_level.par.brightness1 = 1.5
    
    # Position children relative to parent
    child_noise.nodeX = -100
    child_noise.nodeY = 0
    child_level.nodeX = 100
    child_level.nodeY = 0
    
    # Connect children
    child_level.inputConnectors[0].connect(child_noise)
    
    # Create nested container
    nested_container = parent_container.create(containerCOMP, 'nested_container')
    nested_container.nodeX = 0
    nested_container.nodeY = -200
    
    # Create operator in nested container
    deep_child = nested_container.create(constantTOP, 'deep_child')
    deep_child.par.colorr = 1
    deep_child.par.colorg = 0
    deep_child.par.colorb = 0
    
    return parent_container


# Naming Conventions and Best Practices
def create_with_naming_conventions():
    """Examples of good naming conventions"""
    
    # Use descriptive names with type suffixes
    video_input = op('/project1').create(moviefileinTOP, 'videoInput_TOP')
    audio_analyzer = op('/project1').create(analyzeCHOP, 'audioAnalyzer_CHOP')
    
    # Use numbering for multiple similar operators
    for i in range(3):
        noise = op('/project1').create(noiseTOP, f'noise{i+1}_TOP')
        noise.nodeX = i * 150
        noise.nodeY = 1200
        noise.par.period = 5 + i * 2
    
    # Use prefixes for grouping
    ui_container = op('/project1').create(containerCOMP, 'ui_mainPanel')
    ui_button = ui_container.create(buttonCOMP, 'ui_playButton')
    ui_slider = ui_container.create(sliderCOMP, 'ui_speedSlider')
    
    # Use underscores for multi-word names
    particle_system = op('/project1').create(containerCOMP, 'particle_system_COMP')
    particle_emitter = particle_system.create(sopTOP, 'particle_emitter_SOP')
    
    return ui_container


# Batch Creation Example
def batch_create_operators():
    """Example of creating multiple operators efficiently"""
    
    # Create a grid of operators
    grid_container = op('/project1').create(containerCOMP, 'grid_container')
    
    rows = 4
    cols = 4
    spacing = 150
    
    for row in range(rows):
        for col in range(cols):
            # Create operator with grid position in name
            cell = grid_container.create(rectangleTOP, f'cell_{row}_{col}')
            
            # Position in grid
            cell.nodeX = col * spacing - (cols - 1) * spacing / 2
            cell.nodeY = row * spacing - (rows - 1) * spacing / 2
            
            # Set parameters based on position
            cell.par.fillr = row / (rows - 1)
            cell.par.fillg = col / (cols - 1)
            cell.par.fillb = 0.5
            
    return grid_container


# Main execution example
if __name__ == '__main__':
    # Clear the network (optional)
    # for op in op('/project1').children:
    #     op.destroy()
    
    # Create examples
    top_result = create_top_examples()
    chop_result = create_chop_examples()
    sop_result = create_sop_examples()
    dat_result = create_dat_examples()
    mat_result = create_mat_examples()
    comp_result = create_comp_examples()
    parent_child = create_parent_child_examples()
    naming_example = create_with_naming_conventions()
    batch_example = batch_create_operators()
    
    print("All operator creation examples completed!")