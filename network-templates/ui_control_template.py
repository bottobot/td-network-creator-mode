"""
UI Control System Template for TouchDesigner
Creates a comprehensive control system with custom parameters, MIDI/OSC mapping, and preset management
"""

def create_ui_control_system():
    """
    Creates a UI control system with:
    - Custom parameter page setup
    - Slider, button, and menu controls
    - MIDI input mapping
    - OSC input/output setup
    - Preset save/load system
    - Performance mode controls
    """
    
    # Create base container for organization
    base = op('/project1').create(containerCOMP, 'ui_control_system')
    base.par.w = 1600
    base.par.h = 900
    base.nodeX = 0
    base.nodeY = 0
    
    # Main Control Panel
    print("Creating main control panel...")
    
    control_panel = base.create(containerCOMP, 'main_controls')
    control_panel.nodeX = -600
    control_panel.nodeY = 300
    control_panel.par.w = 400
    control_panel.par.h = 500
    
    # Add custom parameter pages
    page1 = control_panel.appendCustomPage('Performance')
    page2 = control_panel.appendCustomPage('Effects')
    page3 = control_panel.appendCustomPage('Mapping')
    
    # Performance page parameters
    page1.appendFloat('Master_intensity', label='Master Intensity', 
                      size=1, default=1.0, min=0, max=1, clampMin=True, clampMax=True)
    page1.appendFloat('Speed', label='Animation Speed', 
                      size=1, default=1.0, min=0.1, max=10, clampMin=True, clampMax=True)
    page1.appendToggle('Play_pause', label='Play/Pause')
    page1.appendPulse('Reset', label='Reset All')
    page1.appendMenu('Mode', label='Performance Mode',
                     menuNames=['auto', 'manual', 'midi', 'osc'],
                     menuLabels=['Automatic', 'Manual', 'MIDI Control', 'OSC Control'])
    
    # Effects page parameters
    page2.appendRGB('Color_primary', label='Primary Color', default=[0.2, 0.5, 0.8])
    page2.appendRGB('Color_secondary', label='Secondary Color', default=[0.8, 0.3, 0.2])
    page2.appendFloat('Blur_amount', label='Blur Amount', 
                      size=1, default=0, min=0, max=10, clampMin=True, clampMax=True)
    page2.appendFloat('Feedback', label='Feedback', 
                      size=1, default=0, min=0, max=0.99, clampMin=True, clampMax=True)
    page2.appendXY('Position', label='Position', default=[0, 0], min=-1, max=1)
    page2.appendXYZ('Rotation', label='Rotation', default=[0, 0, 0], min=-180, max=180)
    
    # Mapping page parameters
    page3.appendInt('Midi_channel', label='MIDI Channel', size=1, default=1, min=1, max=16)
    page3.appendStr('Osc_address', label='OSC Address', default='/td/control')
    page3.appendInt('Osc_port', label='OSC Port', size=1, default=9000, min=1000, max=65535)
    page3.appendToggle('Enable_midi', label='Enable MIDI')
    page3.appendToggle('Enable_osc', label='Enable OSC')
    
    # MIDI Input Section
    print("Setting up MIDI input...")
    
    midi_container = base.create(containerCOMP, 'midi_system')
    midi_container.nodeX = -200
    midi_container.nodeY = 300
    midi_container.par.w = 300
    midi_container.par.h = 400
    
    # MIDI device input
    midi_in = midi_container.create(midiinCHOP, 'midi_input')
    midi_in.nodeX = -100
    midi_in.nodeY = 100
    midi_in.par.device = 'All Devices'
    
    # MIDI mapping table
    midi_map = midi_container.create(tableDAT, 'midi_mapping')
    midi_map.nodeX = -100
    midi_map.nodeY = 0
    midi_map.par.rows = 9
    midi_map.par.cols = 4
    
    # Set up mapping table headers
    midi_map[0, 0] = 'CC'
    midi_map[0, 1] = 'Parameter'
    midi_map[0, 2] = 'Min'
    midi_map[0, 3] = 'Max'
    
    # Default MIDI mappings
    midi_map[1, 0] = '1'
    midi_map[1, 1] = 'Master_intensity'
    midi_map[1, 2] = '0'
    midi_map[1, 3] = '1'
    
    midi_map[2, 0] = '2'
    midi_map[2, 1] = 'Speed'
    midi_map[2, 2] = '0.1'
    midi_map[2, 3] = '10'
    
    midi_map[3, 0] = '3'
    midi_map[3, 1] = 'Blur_amount'
    midi_map[3, 2] = '0'
    midi_map[3, 3] = '10'
    
    # MIDI processor
    midi_process = midi_container.create(selectCHOP, 'midi_select')
    midi_process.nodeX = 100
    midi_process.nodeY = 100
    midi_process.par.channames = 'c[1-8]'
    midi_process.inputConnectors[0].connect(midi_in)
    
    # Scale MIDI values
    midi_scale = midi_container.create(mathCHOP, 'midi_scale')
    midi_scale.nodeX = 100
    midi_scale.nodeY = 0
    midi_scale.par.fromrange1 = 0
    midi_scale.par.fromrange2 = 127
    midi_scale.par.torange1 = 0
    midi_scale.par.torange2 = 1
    midi_scale.inputConnectors[0].connect(midi_process)
    
    # OSC Input/Output Section
    print("Setting up OSC communication...")
    
    osc_container = base.create(containerCOMP, 'osc_system')
    osc_container.nodeX = 200
    osc_container.nodeY = 300
    osc_container.par.w = 300
    osc_container.par.h = 400
    
    # OSC input
    osc_in = osc_container.create(oscinCHOP, 'osc_input')
    osc_in.nodeX = -100
    osc_in.nodeY = 100
    osc_in.par.port = 9000
    
    # OSC output
    osc_out = osc_container.create(oscoutCHOP, 'osc_output')
    osc_out.nodeX = -100
    osc_out.nodeY = 0
    osc_out.par.host = 'localhost'
    osc_out.par.port = 9001
    osc_out.par.sendlocal = False
    
    # OSC address routing
    osc_route = osc_container.create(selectCHOP, 'osc_route')
    osc_route.nodeX = 100
    osc_route.nodeY = 100
    osc_route.par.channames = '/td/control/*'
    osc_route.inputConnectors[0].connect(osc_in)
    
    # Preset System
    print("Creating preset management system...")
    
    preset_container = base.create(containerCOMP, 'preset_system')
    preset_container.nodeX = -600
    preset_container.nodeY = -200
    preset_container.par.w = 400
    preset_container.par.h = 300
    
    # Preset storage table
    preset_storage = preset_container.create(tableDAT, 'preset_storage')
    preset_storage.nodeX = -100
    preset_storage.nodeY = 0
    preset_storage.par.rows = 10
    preset_storage.par.cols = 20
    
    # Preset manager script
    preset_script = preset_container.create(textDAT, 'preset_manager')
    preset_script.nodeX = 100
    preset_script.nodeY = 0
    preset_script.text = '''# Preset Manager Script

def savePreset(presetIndex):
    """Save current parameter values to preset slot"""
    controls = op('../main_controls')
    storage = op('preset_storage')
    
    # Get all custom parameters
    params = []
    for page in controls.customPages:
        for par in page.pars:
            params.append({
                'name': par.name,
                'value': par.eval()
            })
    
    # Store in table
    import json
    storage[presetIndex, 0] = json.dumps(params)
    
def loadPreset(presetIndex):
    """Load parameter values from preset slot"""
    controls = op('../main_controls')
    storage = op('preset_storage')
    
    # Get preset data
    import json
    try:
        params = json.loads(storage[presetIndex, 0].val)
        
        # Apply values
        for param in params:
            try:
                setattr(controls.par, param['name'], param['value'])
            except:
                pass
    except:
        print(f"No preset found at index {presetIndex}")

def interpolatePresets(preset1, preset2, blend):
    """Interpolate between two presets"""
    # Implementation for smooth preset transitions
    pass
'''
    
    # Preset UI
    preset_ui = preset_container.create(containerCOMP, 'preset_ui')
    preset_ui.nodeX = -100
    preset_ui.nodeY = -100
    preset_ui.par.w = 300
    preset_ui.par.h = 100
    
    # Add preset controls
    preset_page = preset_ui.appendCustomPage('Presets')
    preset_page.appendInt('Preset_slot', label='Preset Slot', size=1, default=1, min=1, max=8)
    preset_page.appendPulse('Save_preset', label='Save Preset')
    preset_page.appendPulse('Load_preset', label='Load Preset')
    preset_page.appendFloat('Preset_blend', label='Preset Blend', 
                           size=1, default=0, min=0, max=1, clampMin=True, clampMax=True)
    
    # Performance Mode UI
    print("Creating performance mode interface...")
    
    perf_container = base.create(containerCOMP, 'performance_ui')
    perf_container.nodeX = -200
    perf_container.nodeY = -200
    perf_container.par.w = 600
    perf_container.par.h = 300
    
    # XY pad for 2D control
    xy_pad = perf_container.create(containerCOMP, 'xy_pad')
    xy_pad.nodeX = -200
    xy_pad.nodeY = 0
    xy_pad.par.w = 200
    xy_pad.par.h = 200
    
    # Create visual feedback for XY pad
    xy_bg = xy_pad.create(rectangleTOP, 'background')
    xy_bg.nodeX = 0
    xy_bg.nodeY = 0
    xy_bg.par.resolutionw = 200
    xy_bg.par.resolutionh = 200
    xy_bg.par.fillr = 0.1
    xy_bg.par.fillg = 0.1
    xy_bg.par.fillb = 0.1
    
    # Crosshair for position
    crosshair = xy_pad.create(crossTOP, 'crosshair')
    crosshair.nodeX = 0
    crosshair.nodeY = -100
    crosshair.par.resolutionw = 200
    crosshair.par.resolutionh = 200
    crosshair.par.crosswidth = 2
    
    # Fader bank
    fader_bank = perf_container.create(containerCOMP, 'fader_bank')
    fader_bank.nodeX = 100
    fader_bank.nodeY = 0
    fader_bank.par.w = 300
    fader_bank.par.h = 200
    
    # Create 8 faders
    for i in range(8):
        fader = fader_bank.create(sliderCOMP, f'fader_{i+1}')
        fader.nodeX = i * 35 - 120
        fader.nodeY = 0
        fader.par.w = 30
        fader.par.h = 150
        fader.par.value0 = 0.5
    
    # Button grid
    button_grid = perf_container.create(containerCOMP, 'button_grid')
    button_grid.nodeX = -200
    button_grid.nodeY = -150
    button_grid.par.w = 200
    button_grid.par.h = 100
    
    # Create 4x4 button grid
    for row in range(4):
        for col in range(4):
            btn = button_grid.create(buttonCOMP, f'btn_{row}_{col}')
            btn.nodeX = col * 45 - 70
            btn.nodeY = row * -25 + 30
            btn.par.w = 40
            btn.par.h = 20
    
    # Parameter Feedback Display
    print("Creating parameter feedback display...")
    
    feedback_container = base.create(containerCOMP, 'parameter_feedback')
    feedback_container.nodeX = 200
    feedback_container.nodeY = -200
    feedback_container.par.w = 400
    feedback_container.par.h = 300
    
    # Parameter monitor
    param_monitor = feedback_container.create(parameterexecuteDAT, 'param_monitor')
    param_monitor.nodeX = -100
    param_monitor.nodeY = 0
    param_monitor.par.op = '../main_controls'
    param_monitor.par.allpars = True
    
    # Visual feedback
    param_text = feedback_container.create(textTOP, 'param_display')
    param_text.nodeX = 100
    param_text.nodeY = 0
    param_text.par.resolutionw = 400
    param_text.par.resolutionh = 300
    param_text.par.fontsize = 14
    param_text.par.text = 'Parameter Values'
    
    # Output routing
    print("Setting up output routing...")
    
    output_container = base.create(containerCOMP, 'output_routing')
    output_container.nodeX = 600
    output_container.nodeY = 0
    output_container.par.w = 300
    output_container.par.h = 400
    
    # Collect all control values
    control_merge = output_container.create(mergeCHOP, 'control_values')
    control_merge.nodeX = -100
    control_merge.nodeY = 100
    
    # Create null outputs for easy access
    for param_name in ['Master_intensity', 'Speed', 'Blur_amount', 'Feedback']:
        null_out = output_container.create(nullCHOP, f'out_{param_name}')
        null_out.nodeX = 100
        null_out.nodeY = 100 - output_container.children.index(null_out) * 50
        null_out.cook(force=True)
    
    # Add info text
    info = base.create(textDAT, 'info')
    info.nodeX = -600
    info.nodeY = -500
    info.text = """UI Control System

Components:
1. Main Control Panel - Custom parameters organized by function
2. MIDI System - Maps MIDI CC to parameters
3. OSC System - Bidirectional OSC communication
4. Preset System - Save/load parameter states
5. Performance UI - XY pad, faders, and button grid
6. Parameter Feedback - Visual monitoring

Usage:
- Set parameters in main_controls
- Enable MIDI/OSC in Mapping page
- Configure MIDI mappings in midi_mapping table
- Save presets with preset UI
- Use performance UI for live control

Extending:
- Add more parameter types
- Create custom UI widgets
- Implement parameter recording
- Add network sync capabilities
"""
    
    print("UI control system created successfully!")
    print(f"System created at: {base.path}")
    print("\nKey components:")
    print("- Comprehensive parameter control panel")
    print("- MIDI input with flexible mapping")
    print("- OSC input/output for network control")
    print("- Preset save/load system")
    print("- Performance mode interface")
    print("- Parameter feedback display")
    
    return base

# Execute the template
if __name__ == '__main__':
    create_ui_control_system()