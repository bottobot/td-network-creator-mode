"""
TouchDesigner Python API Examples - Connections
This file demonstrates how to make connections between operators.
"""

# Basic Input/Output Connections
def basic_connection_examples():
    """Examples of basic connections between operators"""
    
    # Create source operators
    noise1 = op('/project1').create(noiseTOP, 'conn_noise1')
    noise2 = op('/project1').create(noiseTOP, 'conn_noise2')
    
    # Create target operator
    comp = op('/project1').create(compositeTOP, 'conn_composite')
    
    # Position operators
    noise1.nodeX = -200
    noise1.nodeY = 0
    noise2.nodeX = -200
    noise2.nodeY = -150
    comp.nodeX = 0
    comp.nodeY = -75
    
    # Make connections
    # Method 1: Using inputConnectors
    comp.inputConnectors[0].connect(noise1)
    comp.inputConnectors[1].connect(noise2)
    
    # Create another operator
    blur = op('/project1').create(blurTOP, 'conn_blur')
    blur.nodeX = 200
    blur.nodeY = -75
    
    # Method 2: Using outputConnectors
    comp.outputConnectors[0].connect(blur)
    
    # Method 3: Direct connection (less common)
    # blur.inputConnectors[0].connect(comp.outputConnectors[0])
    
    return blur


# Multiple Output Connections
def multiple_output_connections():
    """Examples of connecting one output to multiple inputs"""
    
    # Create source
    source = op('/project1').create(moviefileinTOP, 'multi_source')
    source.par.file = 'C:/media/video.mp4'
    source.nodeX = -200
    source.nodeY = 200
    
    # Create multiple targets
    targets = []
    effects = ['blur', 'level', 'edge', 'transform']
    
    for i, effect in enumerate(effects):
        if effect == 'blur':
            target = op('/project1').create(blurTOP, f'multi_{effect}')
            target.par.size = 10
        elif effect == 'level':
            target = op('/project1').create(levelTOP, f'multi_{effect}')
            target.par.brightness1 = 1.5
        elif effect == 'edge':
            target = op('/project1').create(edgeTOP, f'multi_{effect}')
        else:  # transform
            target = op('/project1').create(transformTOP, f'multi_{effect}')
            target.par.scale = 0.5
        
        target.nodeX = i * 150
        target.nodeY = 200
        targets.append(target)
        
        # Connect source to each target
        target.inputConnectors[0].connect(source)
    
    return targets


# Selective Connections
def selective_connection_examples():
    """Examples of selective connections for multi-input operators"""
    
    # Create a Switch TOP with multiple inputs
    switch = op('/project1').create(switchTOP, 'selective_switch')
    switch.nodeX = 200
    switch.nodeY = 400
    
    # Create multiple sources
    sources = []
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]
    
    for i, color in enumerate(colors):
        constant = op('/project1').create(constantTOP, f'selective_color_{i}')
        constant.par.colorr = color[0]
        constant.par.colorg = color[1]
        constant.par.colorb = color[2]
        constant.nodeX = i * 100 - 150
        constant.nodeY = 400
        sources.append(constant)
        
        # Connect to switch
        switch.inputConnectors[i].connect(constant)
    
    # Set switch index
    switch.par.index = 0
    
    # Create a Select TOP for selective input
    select = op('/project1').create(selectTOP, 'selective_select')
    select.nodeX = 200
    select.nodeY = 600
    
    # Connect specific operators by name
    select.par.top = 'selective_color_2'
    
    return switch, select


# CHOP to Parameter Connections (Export)
def chop_export_examples():
    """Examples of exporting CHOP channels to parameters"""
    
    # Create CHOP sources
    lfo = op('/project1').create(lfoCHOP, 'export_lfo')
    lfo.par.rate = 0.5
    lfo.par.amplitude = 1
    lfo.nodeX = -200
    lfo.nodeY = 800
    
    noise_chop = op('/project1').create(noiseCHOP, 'export_noise')
    noise_chop.par.roughness = 0.5
    noise_chop.par.amp = 0.5
    noise_chop.nodeX = -200
    noise_chop.nodeY = 950
    
    # Create target operators
    circle = op('/project1').create(circleTOP, 'export_circle')
    circle.nodeX = 100
    circle.nodeY = 800
    
    transform = op('/project1').create(transformTOP, 'export_transform')
    transform.nodeX = 100
    transform.nodeY = 950
    
    # Method 1: Direct export
    circle.par.radiusx.expr = 'op("export_lfo")[0] * 100 + 100'
    circle.par.radiusy.expr = 'op("export_lfo")[0] * 100 + 100'
    
    # Method 2: Export CHOP
    export_chop = op('/project1').create(exportCHOP, 'export_chop')
    export_chop.nodeX = 0
    export_chop.nodeY = 950
    export_chop.inputConnectors[0].connect(noise_chop)
    
    # Set up export
    export_chop.par.exporttable.val = '''op('export_transform').par.tx	tx
op('export_transform').par.ty	ty
op('export_transform').par.rotate	rz'''
    
    # Method 3: Parameter mode export
    math = op('/project1').create(mathCHOP, 'export_math')
    math.inputConnectors[0].connect(lfo)
    math.par.gain = 180
    math.nodeX = 0
    math.nodeY = 800
    
    # Set parameter to export mode
    circle.par.rotate.mode = ParMode.EXPORT
    circle.par.rotate.export = math
    
    return circle, transform


# Reference Connections
def reference_connection_examples():
    """Examples of reference-based connections"""
    
    # Create source operators
    source_movie = op('/project1').create(moviefileinTOP, 'ref_source_movie')
    source_movie.par.file = 'C:/media/video.mp4'
    source_movie.nodeX = -200
    source_movie.nodeY = 1200
    
    # Create Select TOP that references by name
    select1 = op('/project1').create(selectTOP, 'ref_select1')
    select1.par.top = 'ref_source_movie'
    select1.nodeX = 0
    select1.nodeY = 1200
    
    # Create Select TOP that references by path
    select2 = op('/project1').create(selectTOP, 'ref_select2')
    select2.par.top = '/project1/ref_source_movie'
    select2.nodeX = 200
    select2.nodeY = 1200
    
    # Create Select TOP with relative path
    container = op('/project1').create(containerCOMP, 'ref_container')
    container.nodeX = 0
    container.nodeY = 1400
    
    select3 = container.create(selectTOP, 'ref_select3')
    select3.par.top = '../ref_source_movie'  # Parent relative
    
    # Create Null TOP as reference point
    null = op('/project1').create(nullTOP, 'ref_null')
    null.inputConnectors[0].connect(source_movie)
    null.nodeX = -200
    null.nodeY = 1350
    
    # Multiple operators can reference the same null
    for i in range(3):
        ref_user = op('/project1').create(selectTOP, f'ref_user_{i}')
        ref_user.par.top = 'ref_null'
        ref_user.nodeX = i * 100
        ref_user.nodeY = 1500
    
    return select1, select2, select3


# DAT Connections
def dat_connection_examples():
    """Examples of DAT operator connections"""
    
    # Create Table DAT
    table = op('/project1').create(tableDAT, 'dat_table')
    table.clear()
    table.appendRow(['Name', 'Value'])
    table.appendRow(['Speed', '1.0'])
    table.appendRow(['Color', '1,0,0'])
    table.nodeX = -200
    table.nodeY = 1700
    
    # Create Select DAT
    select = op('/project1').create(selectDAT, 'dat_select')
    select.nodeX = 0
    select.nodeY = 1700
    
    # Connect DATs
    select.inputConnectors[0].connect(table)
    select.par.rows = '1'
    
    # Create Merge DAT
    merge = op('/project1').create(mergeDAT, 'dat_merge')
    merge.nodeX = 200
    merge.nodeY = 1700
    
    # Create another table
    table2 = op('/project1').create(tableDAT, 'dat_table2')
    table2.clear()
    table2.appendRow(['Type', 'Description'])
    table2.appendRow(['Float', 'Decimal number'])
    table2.nodeX = -200
    table2.nodeY = 1850
    
    # Connect both tables to merge
    merge.inputConnectors[0].connect(table)
    merge.inputConnectors[1].connect(table2)
    
    # DAT Execute connection
    execute = op('/project1').create(datexecuteDAT, 'dat_execute')
    execute.nodeX = 0
    execute.nodeY = 1850
    
    # Monitor table changes
    execute.par.dat = 'dat_table'
    execute.par.onTableChange = True
    
    # Add execute code
    execute.par.onTableChange = '''def onTableChange(dat):
    print(f"Table {dat.name} changed!")
    return'''
    
    return merge, execute


# SOP Connections
def sop_connection_examples():
    """Examples of SOP operator connections"""
    
    # Create SOP chain
    sphere = op('/project1').create(sphereSOP, 'sop_sphere')
    sphere.par.rad = (1, 1, 1)
    sphere.nodeX = -200
    sphere.nodeY = 2000
    
    # Transform SOP
    transform = op('/project1').create(transformSOP, 'sop_transform')
    transform.par.s = (2, 1, 1)
    transform.nodeX = 0
    transform.nodeY = 2000
    transform.inputConnectors[0].connect(sphere)
    
    # Noise SOP
    noise = op('/project1').create(noiseSOP, 'sop_noise')
    noise.par.amp = 0.3
    noise.nodeX = 200
    noise.nodeY = 2000
    noise.inputConnectors[0].connect(transform)
    
    # Merge SOP with multiple inputs
    merge = op('/project1').create(mergeSOP, 'sop_merge')
    merge.nodeX = 400
    merge.nodeY = 2000
    
    # Create additional geometry
    box = op('/project1').create(boxSOP, 'sop_box')
    box.par.size = (0.5, 0.5, 0.5)
    box.nodeX = 200
    box.nodeY = 2150
    
    # Connect to merge
    merge.inputConnectors[0].connect(noise)
    merge.inputConnectors[1].connect(box)
    
    return merge


# Dynamic Connection Management
def dynamic_connection_examples():
    """Examples of dynamically managing connections"""
    
    # Create a network
    sources = []
    for i in range(4):
        src = op('/project1').create(noiseTOP, f'dynamic_source_{i}')
        src.nodeX = i * 150 - 300
        src.nodeY = 2300
        src.par.period = 5 + i * 2
        sources.append(src)
    
    # Create composite
    comp = op('/project1').create(compositeTOP, 'dynamic_comp')
    comp.nodeX = 150
    comp.nodeY = 2300
    
    # Function to connect sources dynamically
    def connect_sources(composite, source_list, max_inputs=2):
        """Connect sources to composite, limited by max_inputs"""
        for i, src in enumerate(source_list[:max_inputs]):
            if i < len(composite.inputConnectors):
                composite.inputConnectors[i].connect(src)
    
    # Connect first two sources
    connect_sources(comp, sources, 2)
    
    # Function to disconnect all inputs
    def disconnect_all_inputs(operator):
        """Disconnect all inputs from an operator"""
        for connector in operator.inputConnectors:
            if connector.connections:
                connector.disconnect()
    
    # Function to rewire connections
    def rewire_connection(old_source, new_source, target):
        """Replace old_source with new_source in target's connections"""
        for i, connector in enumerate(target.inputConnectors):
            if connector.connections and connector.connections[0] == old_source:
                connector.disconnect()
                connector.connect(new_source)
                break
    
    # Example: Create a switch mechanism
    switch_control = op('/project1').create(constantCHOP, 'dynamic_switch_control')
    switch_control.par.value0 = 0
    switch_control.nodeX = -300
    switch_control.nodeY = 2450
    
    # Create output
    output = op('/project1').create(nullTOP, 'dynamic_output')
    output.nodeX = 350
    output.nodeY = 2300
    output.inputConnectors[0].connect(comp)
    
    return sources, comp, output


# Connection Utilities
def connection_utility_examples():
    """Utility functions for working with connections"""
    
    # Create test network
    n1 = op('/project1').create(noiseTOP, 'util_noise1')
    n2 = op('/project1').create(noiseTOP, 'util_noise2')
    blur = op('/project1').create(blurTOP, 'util_blur')
    comp = op('/project1').create(compositeTOP, 'util_comp')
    
    # Position
    n1.nodeX, n1.nodeY = -200, 2600
    n2.nodeX, n2.nodeY = -200, 2750
    blur.nodeX, blur.nodeY = 0, 2600
    comp.nodeX, comp.nodeY = 200, 2675
    
    # Connect
    blur.inputConnectors[0].connect(n1)
    comp.inputConnectors[0].connect(blur)
    comp.inputConnectors[1].connect(n2)
    
    # Utility: Check if operators are connected
    def are_connected(source, target):
        """Check if source is connected to target"""
        for connector in target.inputConnectors:
            if connector.connections and source in connector.connections:
                return True
        return False
    
    # Utility: Get all downstream operators
    def get_downstream_ops(operator):
        """Get all operators downstream from the given operator"""
        downstream = []
        for connector in operator.outputConnectors:
            for connection in connector.connections:
                downstream.append(connection.owner)
                # Recursive call to get further downstream
                downstream.extend(get_downstream_ops(connection.owner))
        return list(set(downstream))  # Remove duplicates
    
    # Utility: Get all upstream operators
    def get_upstream_ops(operator):
        """Get all operators upstream from the given operator"""
        upstream = []
        for connector in operator.inputConnectors:
            for connection in connector.connections:
                upstream.append(connection)
                # Recursive call to get further upstream
                upstream.extend(get_upstream_ops(connection))
        return list(set(upstream))  # Remove duplicates
    
    # Utility: Insert operator between two connected operators
    def insert_operator_between(new_op, source, target):
        """Insert new_op between source and target"""
        # Find the connection
        for i, connector in enumerate(target.inputConnectors):
            if connector.connections and source in connector.connections:
                # Disconnect original
                connector.disconnect()
                # Connect source to new_op
                new_op.inputConnectors[0].connect(source)
                # Connect new_op to target
                connector.connect(new_op)
                return True
        return False
    
    # Test utilities
    print(f"n1 connected to blur: {are_connected(n1, blur)}")
    print(f"Downstream from n1: {[op.name for op in get_downstream_ops(n1)]}")
    print(f"Upstream from comp: {[op.name for op in get_upstream_ops(comp)]}")
    
    # Insert a level between blur and comp
    level = op('/project1').create(levelTOP, 'util_level')
    level.nodeX, level.nodeY = 100, 2600
    insert_operator_between(level, blur, comp)
    
    return comp


# Wire Appearance and Layout
def wire_appearance_examples():
    """Examples of managing wire appearance and layout"""
    
    # Create operators with specific layout
    source = op('/project1').create(moviefileinTOP, 'wire_source')
    source.nodeX = -300
    source.nodeY = 2900
    
    # Create a chain with different wire styles
    ops = []
    prev = source
    
    for i in range(4):
        # Create different operators
        if i == 0:
            op_new = op('/project1').create(levelTOP, f'wire_op_{i}')
        elif i == 1:
            op_new = op('/project1').create(blurTOP, f'wire_op_{i}')
        elif i == 2:
            op_new = op('/project1').create(transformTOP, f'wire_op_{i}')
        else:
            op_new = op('/project1').create(compositeTOP, f'wire_op_{i}')
        
        # Position in a curve
        op_new.nodeX = -150 + i * 150
        op_new.nodeY = 2900 + (i % 2) * 100
        
        # Connect
        op_new.inputConnectors[0].connect(prev)
        
        ops.append(op_new)
        prev = op_new
    
    # Create a feedback loop example
    feedback = op('/project1').create(feedbackTOP, 'wire_feedback')
    feedback.nodeX = 300
    feedback.nodeY = 3100
    
    level = op('/project1').create(levelTOP, 'wire_feedback_level')
    level.nodeX = 500
    level.nodeY = 3100
    level.par.brightness1 = 0.95
    
    # Connect feedback loop
    feedback.inputConnectors[0].connect(ops[-1])
    level.inputConnectors[0].connect(feedback)
    feedback.par.top = 'wire_feedback_level'
    
    return feedback


# Main execution example
if __name__ == '__main__':
    # Run all examples
    basic = basic_connection_examples()
    multiple = multiple_output_connections()
    selective = selective_connection_examples()
    export = chop_export_examples()
    reference = reference_connection_examples()
    dat = dat_connection_examples()
    sop = sop_connection_examples()
    dynamic = dynamic_connection_examples()
    utilities = connection_utility_examples()
    wires = wire_appearance_examples()
    
    print("All connection examples completed!")