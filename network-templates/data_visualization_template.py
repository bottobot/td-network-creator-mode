"""
Data Visualization System Template for TouchDesigner
Creates a complete data-driven visualization network with CSV/JSON input and dynamic visual mapping
"""

def create_data_visualization_system():
    """
    Creates a data visualization system with:
    - Data input setup (CSV/JSON via DAT)
    - Data parsing and processing
    - Visual mapping (bars, lines, points)
    - Animation controls
    - Color mapping based on data values
    """
    
    # Create base container for organization
    base = op('/project1').create(containerCOMP, 'data_visualization_system')
    base.par.w = 1400
    base.par.h = 900
    base.nodeX = 0
    base.nodeY = 0
    
    # Data Input Section
    print("Creating data input system...")
    
    # File input for CSV data
    csv_file = base.create(fileinDAT, 'csv_input')
    csv_file.nodeX = -600
    csv_file.nodeY = 300
    csv_file.par.file = 'data.csv'  # Default filename
    
    # Alternative JSON input
    json_file = base.create(fileinDAT, 'json_input')
    json_file.nodeX = -600
    json_file.nodeY = 200
    json_file.par.file = 'data.json'
    
    # Switch between CSV and JSON
    switch_dat = base.create(switchDAT, 'data_switch')
    switch_dat.nodeX = -400
    switch_dat.nodeY = 250
    switch_dat.par.index = 0  # Default to CSV
    switch_dat.inputConnectors[0].connect(csv_file)
    switch_dat.inputConnectors[1].connect(json_file)
    
    # Data Processing Section
    print("Setting up data processing...")
    
    # Convert CSV to table
    csv_to_table = base.create(convertDAT, 'csv_to_table')
    csv_to_table.nodeX = -200
    csv_to_table.nodeY = 300
    csv_to_table.par.how = 'csv to table'
    csv_to_table.inputConnectors[0].connect(csv_file)
    
    # Extract data columns
    select_cols = base.create(selectDAT, 'select_columns')
    select_cols.nodeX = 0
    select_cols.nodeY = 300
    select_cols.par.extractcols = '1-3'  # Select first 3 columns
    select_cols.par.outputdatamode = 'cols'
    select_cols.inputConnectors[0].connect(csv_to_table)
    
    # Convert to CHOP for numeric processing
    dat_to_chop = base.create(dattoCHOP, 'data_to_chop')
    dat_to_chop.nodeX = 200
    dat_to_chop.nodeY = 300
    dat_to_chop.par.firstcolumn = 1
    dat_to_chop.par.firstrow = 1
    dat_to_chop.inputConnectors[0].connect(select_cols)
    
    # Normalize data values
    normalize = base.create(mathCHOP, 'normalize_data')
    normalize.nodeX = 400
    normalize.nodeY = 300
    normalize.par.rangelow = 0
    normalize.par.rangehigh = 1
    normalize.inputConnectors[0].connect(dat_to_chop)
    
    # Data statistics
    analyze = base.create(analyzeCHOP, 'data_stats')
    analyze.nodeX = 400
    analyze.nodeY = 200
    analyze.par.function = 'average'
    analyze.inputConnectors[0].connect(dat_to_chop)
    
    # Visualization Generators
    print("Creating visualization generators...")
    
    # Bar Chart Generator
    bar_container = base.create(containerCOMP, 'bar_chart')
    bar_container.nodeX = -400
    bar_container.nodeY = 0
    bar_container.par.w = 300
    bar_container.par.h = 200
    
    # Create bars using instancing
    bar_geo = bar_container.create(boxSOP, 'bar_geometry')
    bar_geo.nodeX = -100
    bar_geo.nodeY = 0
    bar_geo.par.sizey = 1
    
    # Instance bars based on data
    bar_instance = bar_container.create(geometryCOMP, 'bar_instances')
    bar_instance.nodeX = 100
    bar_instance.nodeY = 0
    bar_instance.par.instanceop = '../data_to_chop'
    bar_instance.par.instancetx = 'tx'
    bar_instance.par.instancesy = 'chan1'
    bar_instance.inputConnectors[0].connect(bar_geo)
    
    # Line Chart Generator
    line_container = base.create(containerCOMP, 'line_chart')
    line_container.nodeX = -100
    line_container.nodeY = 0
    line_container.par.w = 300
    line_container.par.h = 200
    
    # Convert data to line
    chop_to_sop = line_container.create(choptoSOP, 'data_to_line')
    chop_to_sop.nodeX = -100
    chop_to_sop.nodeY = 0
    chop_to_sop.inputConnectors[0].connect(normalize)
    
    # Add line material
    line_mat = line_container.create(lineMAT, 'line_material')
    line_mat.nodeX = 0
    line_mat.nodeY = -100
    line_mat.par.width = 2
    
    # Render line
    line_geo = line_container.create(geometryCOMP, 'line_render')
    line_geo.nodeX = 100
    line_geo.nodeY = 0
    line_geo.par.material = './line_material'
    line_geo.inputConnectors[0].connect(chop_to_sop)
    
    # Scatter Plot Generator
    scatter_container = base.create(containerCOMP, 'scatter_plot')
    scatter_container.nodeX = 200
    scatter_container.nodeY = 0
    scatter_container.par.w = 300
    scatter_container.par.h = 200
    
    # Create point geometry
    points = scatter_container.create(sphereSOP, 'point_geometry')
    points.nodeX = -100
    points.nodeY = 0
    points.par.rad = 0.02
    
    # Instance points based on data pairs
    scatter_instance = scatter_container.create(geometryCOMP, 'scatter_instances')
    scatter_instance.nodeX = 100
    scatter_instance.nodeY = 0
    scatter_instance.par.instanceop = '../data_to_chop'
    scatter_instance.par.instancetx = 'chan1'
    scatter_instance.par.instancety = 'chan2'
    scatter_instance.inputConnectors[0].connect(points)
    
    # Color Mapping Section
    print("Creating color mapping system...")
    
    # Create color ramp for data values
    color_ramp = base.create(rampTOP, 'color_map')
    color_ramp.nodeX = -400
    color_ramp.nodeY = -200
    color_ramp.par.resolutionw = 256
    color_ramp.par.resolutionh = 1
    color_ramp.par.type = 'horizontal'
    
    # Sample colors based on data values
    color_lookup = base.create(lookupTOP, 'color_lookup')
    color_lookup.nodeX = -200
    color_lookup.nodeY = -200
    color_lookup.par.lookup = 'luminance'
    color_lookup.inputConnectors[0].connect(color_ramp)
    
    # Animation Controls
    print("Adding animation controls...")
    
    # Time-based animation
    timer = base.create(timerCHOP, 'animation_timer')
    timer.nodeX = 600
    timer.nodeY = 300
    timer.par.length = 5
    timer.par.loop = True
    timer.par.play = True
    
    # Interpolate data over time
    interpolate = base.create(interpCHOP, 'data_interpolate')
    interpolate.nodeX = 600
    interpolate.nodeY = 200
    interpolate.par.timeslice = True
    interpolate.inputConnectors[0].connect(normalize)
    interpolate.inputConnectors[1].connect(timer)
    
    # Smooth transitions
    smooth = base.create(lagCHOP, 'smooth_animation')
    smooth.nodeX = 600
    smooth.nodeY = 100
    smooth.par.lag1 = 0.2
    smooth.inputConnectors[0].connect(interpolate)
    
    # Composite Visualization
    print("Creating composite visualization...")
    
    # Create render setup
    camera = base.create(cameraCOMP, 'viz_camera')
    camera.nodeX = -200
    camera.nodeY = -400
    camera.par.tz = 5
    
    light = base.create(lightCOMP, 'viz_light')
    light.nodeX = 0
    light.nodeY = -400
    light.par.ty = 2
    light.par.tz = 2
    
    # Main render
    render = base.create(renderTOP, 'main_render')
    render.nodeX = 200
    render.nodeY = -400
    render.par.resolutionw = 1920
    render.par.resolutionh = 1080
    render.par.camera = './viz_camera'
    render.par.lights = './viz_light'
    render.par.geometry = '../bar_chart/bar_instances ../line_chart/line_render ../scatter_plot/scatter_instances'
    
    # Add background
    background = base.create(constantTOP, 'background')
    background.nodeX = 400
    background.nodeY = -300
    background.par.resolutionw = 1920
    background.par.resolutionh = 1080
    background.par.colorr = 0.1
    background.par.colorg = 0.1
    background.par.colorb = 0.15
    
    # Composite
    comp = base.create(compositeTOP, 'final_comp')
    comp.nodeX = 400
    comp.nodeY = -400
    comp.inputConnectors[0].connect(background)
    comp.inputConnectors[1].connect(render)
    
    # Output
    out = base.create(outTOP, 'output')
    out.nodeX = 600
    out.nodeY = -400
    out.inputConnectors[0].connect(comp)
    
    # Control Panel
    print("Creating control panel...")
    
    # Create parameter container
    controls = base.create(containerCOMP, 'controls')
    controls.nodeX = -600
    controls.nodeY = -400
    controls.par.w = 400
    controls.par.h = 300
    
    # Add custom parameters
    page = controls.appendCustomPage('Data Visualization Controls')
    
    # Data source selection
    page.appendMenu('Data_source', label='Data Source', 
                    menuNames=['CSV', 'JSON'], menuLabels=['CSV File', 'JSON File'])
    
    # Visualization type
    page.appendMenu('Viz_type', label='Visualization Type',
                    menuNames=['bars', 'line', 'scatter', 'all'],
                    menuLabels=['Bar Chart', 'Line Chart', 'Scatter Plot', 'All'])
    
    # Animation controls
    page.appendToggle('Animate', label='Animate Data')
    page.appendFloat('Anim_speed', label='Animation Speed', size=1, default=1.0, min=0.1, max=5.0)
    
    # Color controls
    page.appendRGB('Color_start', label='Start Color', default=[0.2, 0.4, 0.8])
    page.appendRGB('Color_end', label='End Color', default=[0.8, 0.2, 0.4])
    
    # Scale controls
    page.appendFloat('Data_scale', label='Data Scale', size=1, default=1.0, min=0.1, max=2.0)
    page.appendInt('Bar_count', label='Bar Count', size=1, default=10, min=1, max=50)
    
    # Link parameters
    switch_dat.par.index.expr = 'op("../controls").par.Data_source'
    timer.par.play.expr = 'op("../controls").par.Animate'
    timer.par.rate.expr = 'op("../controls").par.Anim_speed'
    normalize.par.mult.expr = 'op("../controls").par.Data_scale'
    
    # Add data preview
    table_viewer = controls.create(tableDAT, 'data_preview')
    table_viewer.nodeX = 0
    table_viewer.nodeY = 0
    table_viewer.par.w = 300
    table_viewer.par.h = 150
    table_viewer.inputConnectors[0].connect(csv_to_table)
    
    # Add info text
    info = base.create(textDAT, 'info')
    info.nodeX = -600
    info.nodeY = -600
    info.text = """Data Visualization System
    
1. Load your data:
   - Place CSV or JSON file in project folder
   - Update file path in csv_input or json_input
   - Select data source in control panel

2. Configure visualization:
   - Choose visualization type (bar/line/scatter)
   - Adjust animation settings
   - Customize colors and scaling

3. Data format:
   - CSV: First row as headers, numeric data in columns
   - JSON: Array of objects with numeric properties
   
4. Extend the system:
   - Add more visualization types
   - Implement real-time data updates
   - Create custom color mappings
"""
    
    print("Data visualization system created successfully!")
    print(f"System created at: {base.path}")
    print("\nKey components:")
    print("- CSV/JSON data input")
    print("- Data parsing and normalization")
    print("- Bar chart, line chart, and scatter plot generators")
    print("- Color mapping system")
    print("- Animation controls")
    print("- Comprehensive control panel")
    
    return base

# Execute the template
if __name__ == '__main__':
    create_data_visualization_system()