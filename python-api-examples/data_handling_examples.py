"""
TouchDesigner Python API Examples - Data Handling
This file demonstrates how to work with data in different operator types.
"""

# Table DAT Manipulation
def table_dat_examples():
    """Examples of working with Table DAT data"""
    
    # Create a Table DAT
    table = op('/project1').create(tableDAT, 'data_table')
    table.nodeX = 0
    table.nodeY = 0
    
    # Clear and initialize table
    table.clear()
    
    # Add headers
    table.appendRow(['ID', 'Name', 'Value', 'Type', 'Active'])
    
    # Add data rows
    data = [
        ['001', 'Speed', '1.5', 'float', '1'],
        ['002', 'Color_R', '0.8', 'float', '1'],
        ['003', 'Color_G', '0.2', 'float', '1'],
        ['004', 'Color_B', '0.5', 'float', '1'],
        ['005', 'Mode', 'blend', 'string', '0'],
        ['006', 'Count', '10', 'int', '1']
    ]
    
    for row in data:
        table.appendRow(row)
    
    # Access table data
    print("Table contents:")
    for row in range(table.numRows):
        row_data = []
        for col in range(table.numCols):
            row_data.append(table[row, col].val)
        print(f"  Row {row}: {row_data}")
    
    # Access specific cells
    speed_value = table['Speed', 'Value'].val
    print(f"\nSpeed value: {speed_value}")
    
    # Modify cells
    table['Mode', 'Value'] = 'add'
    table[5, 4] = '1'  # Activate Mode
    
    # Insert and delete operations
    table.insertRow(['007', 'Scale', '2.0', 'float', '1'], 3)
    table.deleteRow(6)  # Delete the Count row
    
    # Column operations
    table.appendCol(['Units', 'x/sec', '', '', '', 'x', ''])
    
    # Find data in table
    def find_in_table(table_dat, search_value, column=None):
        """Find all cells containing search_value"""
        results = []
        for row in range(table_dat.numRows):
            for col in range(table_dat.numCols):
                if column is None or col == column:
                    if search_value in str(table_dat[row, col].val):
                        results.append((row, col, table_dat[row, col].val))
        return results
    
    # Search examples
    float_cells = find_in_table(table, 'float', 3)  # Search in Type column
    print(f"\nCells with 'float': {float_cells}")
    
    # Convert table to Python data structures
    def table_to_dict(table_dat, key_col=0, value_col=2):
        """Convert table to dictionary using specified columns"""
        result = {}
        for row in range(1, table_dat.numRows):  # Skip header
            key = table_dat[row, key_col].val
            value = table_dat[row, value_col].val
            result[key] = value
        return result
    
    table_dict = table_to_dict(table, 1, 2)  # Name -> Value
    print(f"\nTable as dict: {table_dict}")
    
    # Create a more complex data table
    data_table = op('/project1').create(tableDAT, 'complex_data_table')
    data_table.nodeX = 200
    data_table.nodeY = 0
    
    # JSON-like data in table
    data_table.clear()
    data_table.appendRow(['Parameter', 'Settings'])
    data_table.appendRow(['transform', '{"x": 0, "y": 0, "scale": 1.0, "rotate": 0}'])
    data_table.appendRow(['colors', '{"primary": [1,0,0], "secondary": [0,1,0]}'])
    data_table.appendRow(['options', '{"enabled": true, "mode": "auto", "count": 5}'])
    
    # Parse JSON from table
    import json
    
    def parse_json_table(table_dat):
        """Parse JSON strings from table"""
        parsed_data = {}
        for row in range(1, table_dat.numRows):
            key = table_dat[row, 0].val
            json_str = table_dat[row, 1].val
            try:
                parsed_data[key] = json.loads(json_str)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for {key}")
        return parsed_data
    
    parsed = parse_json_table(data_table)
    print(f"\nParsed JSON data: {parsed}")
    
    return table, data_table


# CHOP Channel Access
def chop_channel_examples():
    """Examples of accessing and manipulating CHOP channel data"""
    
    # Create CHOPs with data
    constant = op('/project1').create(constantCHOP, 'data_constant')
    constant.par.name0 = 'speed'
    constant.par.value0 = 2.5
    constant.nodeX = 0
    constant.nodeY = 200
    
    # Create multi-channel CHOP
    noise = op('/project1').create(noiseCHOP, 'data_noise')
    noise.par.numchans = 4
    noise.par.channelname = 'chan[1-4]'
    noise.par.amp = 1.0
    noise.par.roughness = 0.5
    noise.nodeX = 200
    noise.nodeY = 200
    
    # Access channel data
    # Single sample access
    speed_value = constant['speed'][0]
    print(f"Speed value: {speed_value}")
    
    # Access all samples in a channel
    noise_samples = noise['chan1'].vals
    print(f"Noise channel 1 samples: {len(noise_samples)} samples")
    print(f"First 10 values: {noise_samples[:10]}")
    
    # Access channel by index
    chan2_value = noise[1][0]  # Second channel, first sample
    print(f"Channel 2, sample 0: {chan2_value}")
    
    # Get channel information
    print(f"\nNoise CHOP info:")
    print(f"  Number of channels: {noise.numChans}")
    print(f"  Number of samples: {noise.numSamples}")
    print(f"  Sample rate: {noise.rate}")
    print(f"  Channel names: {[noise[i].name for i in range(noise.numChans)]}")
    
    # Create Pattern CHOP for more complex data
    pattern = op('/project1').create(patternCHOP, 'data_pattern')
    pattern.par.length = 100
    pattern.par.type = 'sine'
    pattern.par.period = 50
    pattern.par.numchans = 3
    pattern.par.channelname = 'x y z'
    pattern.nodeX = 0
    pattern.nodeY = 350
    
    # Process channel data
    def process_chop_data(chop, operation='average'):
        """Process all channels in a CHOP"""
        results = {}
        for i in range(chop.numChans):
            chan = chop[i]
            values = chan.vals
            
            if operation == 'average':
                result = sum(values) / len(values)
            elif operation == 'max':
                result = max(values)
            elif operation == 'min':
                result = min(values)
            elif operation == 'range':
                result = max(values) - min(values)
            else:
                result = None
            
            results[chan.name] = result
        
        return results
    
    # Process pattern data
    pattern_stats = process_chop_data(pattern, 'range')
    print(f"\nPattern channel ranges: {pattern_stats}")
    
    # Create Math CHOP to combine channels
    math = op('/project1').create(mathCHOP, 'data_math')
    math.par.chopop = 'add'
    math.nodeX = 200
    math.nodeY = 350
    
    # Connect multiple inputs
    math.inputConnectors[0].connect(pattern)
    math.inputConnectors[1].connect(noise)
    
    # Channel manipulation with Script CHOP
    script = op('/project1').create(scriptCHOP, 'data_script')
    script.nodeX = 0
    script.nodeY = 500
    script.inputConnectors[0].connect(pattern)
    
    # Set up script to process channels
    script_code = '''def onCook(scriptOp):
    # Copy input
    scriptOp.copy(scriptOp.inputs[0])
    
    # Process each channel
    for i in range(scriptOp.numChans):
        chan = scriptOp[i]
        # Apply custom processing
        for j in range(len(chan)):
            # Example: Apply envelope
            envelope = j / float(len(chan) - 1)
            chan[j] = chan[j] * envelope
    
    return'''
    
    script.par.text = script_code
    
    # Create Analyze CHOP for statistics
    analyze = op('/project1').create(analyzeCHOP, 'data_analyze')
    analyze.par.function = 'average'
    analyze.par.perchanel = True
    analyze.nodeX = 200
    analyze.nodeY = 500
    analyze.inputConnectors[0].connect(pattern)
    
    return pattern, analyze


# TOP Pixel Data
def top_pixel_data_examples():
    """Examples of accessing TOP pixel data"""
    
    # Create TOPs with data
    ramp = op('/project1').create(rampTOP, 'data_ramp')
    ramp.par.resolutionw = 256
    ramp.par.resolutionh = 256
    ramp.par.type = 'radial'
    ramp.nodeX = 0
    ramp.nodeY = 700
    
    # Note: Direct pixel access in TouchDesigner Python is limited
    # Most pixel operations should be done with TOPs or GLSL
    
    # Sample pixel values using CHOP
    sample_chop = op('/project1').create(choptoTOP, 'data_sample')
    sample_chop.nodeX = 200
    sample_chop.nodeY = 700
    
    # Create sampling positions
    positions = op('/project1').create(constantCHOP, 'sample_positions')
    positions.par.numchans = 2
    positions.par.name0 = 'u'
    positions.par.name1 = 'v'
    positions.par.value0 = 0.5  # Center X
    positions.par.value1 = 0.5  # Center Y
    positions.nodeX = 0
    positions.nodeY = 850
    
    # TOP to CHOP for analysis
    top_to_chop = op('/project1').create(topToCHOP, 'data_top_to_chop')
    top_to_chop.par.crop = True
    top_to_chop.par.cropl = 128
    top_to_chop.par.cropr = 129
    top_to_chop.par.cropt = 128
    top_to_chop.par.cropb = 129
    top_to_chop.nodeX = 200
    top_to_chop.nodeY = 850
    top_to_chop.inputConnectors[0].connect(ramp)
    
    # Create Texture 3D TOP for volume data
    tex3d = op('/project1').create(texture3dTOP, 'data_volume')
    tex3d.par.resolutionw = 32
    tex3d.par.resolutionh = 32
    tex3d.par.resolutiond = 32
    tex3d.nodeX = 0
    tex3d.nodeY = 1000
    
    # Create noise for each slice
    for i in range(32):
        slice_noise = op('/project1').create(noiseTOP, f'slice_{i}')
        slice_noise.par.resolutionw = 32
        slice_noise.par.resolutionh = 32
        slice_noise.par.seed = i
        slice_noise.nodeX = -200 + (i % 8) * 50
        slice_noise.nodeY = 1000 + (i // 8) * 100
        
        # Connect to texture 3D
        if i < len(tex3d.inputConnectors):
            tex3d.inputConnectors[i].connect(slice_noise)
    
    # Analyze TOP data
    analyze_top = op('/project1').create(analyzeTOP, 'data_analyze_top')
    analyze_top.nodeX = 200
    analyze_top.nodeY = 1000
    analyze_top.inputConnectors[0].connect(ramp)
    
    # Info CHOP for TOP metadata
    info = op('/project1').create(infoCHOP, 'data_top_info')
    info.par.op = '../data_ramp'
    info.nodeX = 400
    info.nodeY = 700
    
    return ramp, top_to_chop, tex3d


# JSON/XML Parsing
def json_xml_parsing_examples():
    """Examples of parsing JSON and XML data"""
    
    # Create Text DAT with JSON
    json_dat = op('/project1').create(textDAT, 'data_json')
    json_dat.nodeX = 0
    json_dat.nodeY = 1300
    
    json_data = {
        "project": {
            "name": "TouchDesigner Example",
            "version": "1.0",
            "settings": {
                "resolution": [1920, 1080],
                "fps": 60,
                "format": "HAP"
            },
            "operators": [
                {"type": "noise", "name": "noise1", "params": {"period": 5}},
                {"type": "level", "name": "level1", "params": {"brightness": 1.5}},
                {"type": "blur", "name": "blur1", "params": {"size": 10}}
            ]
        }
    }
    
    json_dat.text = json.dumps(json_data, indent=2)
    
    # Parse JSON
    import json
    parsed_json = json.loads(json_dat.text)
    
    # Create operators from JSON
    def create_from_json(json_data, parent):
        """Create operators from JSON description"""
        created_ops = []
        
        for i, op_desc in enumerate(json_data['project']['operators']):
            op_type = op_desc['type']
            op_name = op_desc['name']
            params = op_desc.get('params', {})
            
            # Map type strings to operator types
            type_map = {
                'noise': noiseTOP,
                'level': levelTOP,
                'blur': blurTOP
            }
            
            if op_type in type_map:
                new_op = parent.create(type_map[op_type], op_name)
                new_op.nodeX = i * 150
                new_op.nodeY = 1300
                
                # Set parameters
                for param, value in params.items():
                    if hasattr(new_op.par, param):
                        setattr(new_op.par, param, value)
                
                created_ops.append(new_op)
                
                # Connect to previous
                if i > 0:
                    new_op.inputConnectors[0].connect(created_ops[i-1])
        
        return created_ops
    
    created = create_from_json(parsed_json, op('/project1'))
    print(f"Created {len(created)} operators from JSON")
    
    # Create XML DAT
    xml_dat = op('/project1').create(textDAT, 'data_xml')
    xml_dat.nodeX = 0
    xml_dat.nodeY = 1500
    
    xml_data = '''<?xml version="1.0" encoding="UTF-8"?>
<network>
    <metadata>
        <author>TD User</author>
        <created>2024-01-01</created>
    </metadata>
    <operators>
        <operator type="constant" name="const1">
            <param name="colorr">1.0</param>
            <param name="colorg">0.5</param>
            <param name="colorb">0.0</param>
        </operator>
        <operator type="transform" name="trans1">
            <param name="scale">0.5</param>
            <param name="rotate">45</param>
        </operator>
    </operators>
    <connections>
        <connection from="const1" to="trans1" />
    </connections>
</network>'''
    
    xml_dat.text = xml_data
    
    # Parse XML
    import xml.etree.ElementTree as ET
    
    def parse_network_xml(xml_text, parent):
        """Parse network description from XML"""
        root = ET.fromstring(xml_text)
        
        # Get metadata
        metadata = {}
        for meta in root.find('metadata'):
            metadata[meta.tag] = meta.text
        
        print(f"Network metadata: {metadata}")
        
        # Create operators
        created_ops = {}
        operators = root.find('operators')
        
        for i, op_elem in enumerate(operators.findall('operator')):
            op_type = op_elem.get('type')
            op_name = op_elem.get('name')
            
            # Map types
            type_map = {
                'constant': constantTOP,
                'transform': transformTOP
            }
            
            if op_type in type_map:
                new_op = parent.create(type_map[op_type], f'xml_{op_name}')
                new_op.nodeX = i * 150
                new_op.nodeY = 1500
                
                # Set parameters
                for param in op_elem.findall('param'):
                    param_name = param.get('name')
                    param_value = float(param.text)
                    
                    if hasattr(new_op.par, param_name):
                        setattr(new_op.par, param_name, param_value)
                
                created_ops[op_name] = new_op
        
        # Create connections
        connections = root.find('connections')
        if connections is not None:
            for conn in connections.findall('connection'):
                from_op = created_ops.get(conn.get('from'))
                to_op = created_ops.get(conn.get('to'))
                
                if from_op and to_op:
                    to_op.inputConnectors[0].connect(from_op)
        
        return created_ops
    
    xml_ops = parse_network_xml(xml_data, op('/project1'))
    
    # Create Web Client DAT for external data
    web_client = op('/project1').create(webclientDAT, 'data_web_client')
    web_client.nodeX = 0
    web_client.nodeY = 1700
    
    # Example: Fetch JSON from API (commented out to avoid actual request)
    # web_client.par.url = 'https://api.example.com/data.json'
    # web_client.par.request = True
    
    return json_dat, xml_dat, web_client


# Advanced Data Processing
def advanced_data_processing():
    """Advanced data processing examples"""
    
    # Create data pipeline
    # Source data table
    source_table = op('/project1').create(tableDAT, 'pipeline_source')
    source_table.clear()
    source_table.appendRow(['Time', 'Value', 'Category'])
    
    # Generate sample data
    import random
    categories = ['A', 'B', 'C']
    for i in range(50):
        time = i * 0.1
        value = random.uniform(0, 100)
        category = random.choice(categories)
        source_table.appendRow([f'{time:.1f}', f'{value:.2f}', category])
    
    source_table.nodeX = 0
    source_table.nodeY = 1900
    
    # Convert table to CHOP
    dat_to_chop = op('/project1').create(datToCHOP, 'pipeline_dat_to_chop')
    dat_to_chop.par.dat = 'pipeline_source'
    dat_to_chop.par.firstrow = 1
    dat_to_chop.par.firstcol = 1
    dat_to_chop.par.extractcols = 2
    dat_to_chop.nodeX = 200
    dat_to_chop.nodeY = 1900
    
    # Process with Filter CHOP
    filter_chop = op('/project1').create(filterCHOP, 'pipeline_filter')
    filter_chop.par.filter = 'gaussian'
    filter_chop.par.width = 5
    filter_chop.nodeX = 400
    filter_chop.nodeY = 1900
    filter_chop.inputConnectors[0].connect(dat_to_chop)
    
    # Resample data
    resample = op('/project1').create(resampleCHOP, 'pipeline_resample')
    resample.par.rate = 10
    resample.par.method = 'cubic'
    resample.nodeX = 600
    resample.nodeY = 1900
    resample.inputConnectors[0].connect(filter_chop)
    
    # Convert back to table
    chop_to_dat = op('/project1').create(choptoDAT, 'pipeline_chop_to_dat')
    chop_to_dat.par.includename = True
    chop_to_dat.nodeX = 800
    chop_to_dat.nodeY = 1900
    chop_to_dat.inputConnectors[0].connect(resample)
    
    # Create data aggregation
    def aggregate_table_data(table_dat, group_col, value_col, operation='sum'):
        """Aggregate table data by group"""
        from collections import defaultdict
        
        groups = defaultdict(list)
        
        # Group data
        for row in range(1, table_dat.numRows):
            group = table_dat[row, group_col].val
            value = float(table_dat[row, value_col].val)
            groups[group].append(value)
        
        # Aggregate
        result_table = op('/project1').create(tableDAT, 'aggregated_data')
        result_table.clear()
        result_table.appendRow(['Group', operation.capitalize()])
        
        for group, values in groups.items():
            if operation == 'sum':
                result = sum(values)
            elif operation == 'average':
                result = sum(values) / len(values)
            elif operation == 'max':
                result = max(values)
            elif operation == 'min':
                result = min(values)
            elif operation == 'count':
                result = len(values)
            
            result_table.appendRow([group, f'{result:.2f}'])
        
        result_table.nodeX = 0
        result_table.nodeY = 2100
        
        return result_table
    
    # Aggregate by category
    aggregated = aggregate_table_data(source_table, 2, 1, 'average')
    
    # Create Execute DAT for real-time processing
    execute = op('/project1').create(executeDAT, 'pipeline_execute')
    execute.nodeX = 200
    execute.nodeY = 2100
    
    execute_code = '''# Real-time data processing
def onFrameStart(frame):
    # Process incoming data each frame
    source = op('pipeline_source')
    
    # Example: Add new row with current frame data
    if frame % 10 == 0:  # Every 10 frames
        import random
        time = frame / 60.0
        value = random.uniform(0, 100)
        category = ['A', 'B', 'C'][frame % 3]
        source.appendRow([f'{time:.1f}', f'{value:.2f}', category])
        
        # Keep table size manageable
        if source.numRows > 100:
            source.deleteRow(1)  # Remove oldest data
    
    return'''
    
    execute.par.text = execute_code
    
    return source_table, chop_to_dat, aggregated


# Data Visualization Helpers
def data_visualization_helpers():
    """Helper functions for data visualization"""
    
    # Create visualization container
    viz_container = op('/project1').create(containerCOMP, 'data_viz')
    viz_container.par.w = 800
    viz_container.par.h = 600
    viz_container.nodeX = 0
    viz_container.nodeY = 2300
    
    # Function to create bar chart from table
    def create_bar_chart(data_table, label_col, value_col, container):
        """Create a simple bar chart from table data"""
        num_bars = data_table.numRows - 1  # Exclude header
        bar_width = container.par.w.eval() / num_bars
        max_value = 0
        
        # Find max value for scaling
        for row in range(1, data_table.numRows):
            value = float(data_table[row, value_col].val)
            max_value = max(max_value, value)
        
        # Create bars
        for i in range(1, data_table.numRows):
            label = data_table[i, label_col].val
            value = float(data_table[i, value_col].val)
            
            # Create rectangle for bar
            bar = container.create(rectangleTOP, f'bar_{label}')
            bar.par.resolutionw = int(bar_width * 0.8)
            bar.par.resolutionh = int((value / max_value) * container.par.h.eval() * 0.8)
            bar.par.fillr = 0.2
            bar.par.fillg = 0.6
            bar.par.fillb = 1.0
            
            # Position bar
            bar.nodeX = (i - 1) * 100
            bar.nodeY = 0
        
        return container
    
    # Create sample data for visualization
    viz_data = op('/project1').create(tableDAT, 'viz_data')
    viz_data.clear()
    viz_data.appendRow(['Month', 'Sales'])
    viz_data.appendRow(['Jan', '45.5'])
    viz_data.appendRow(['Feb', '52.3'])
    viz_data.appendRow(['Mar', '48.7'])
    viz_data.appendRow(['Apr', '61.2'])
    viz_data.nodeX = -200
    viz_data.nodeY = 2300
    
    # Create bar chart
    chart = create_bar_chart(viz_data, 0, 1, viz_container)
    
    return viz_container, viz_data


# Main execution example
if __name__ == '__main__':
    import json
    
    # Run all examples
    tables = table_dat_examples()
    chops = chop_channel_examples()
    tops = top_pixel_data_examples()
    parsing = json_xml_parsing_examples()
    advanced = advanced_data_processing()
    viz = data_visualization_helpers()
    
    print("\nAll data handling examples completed!")