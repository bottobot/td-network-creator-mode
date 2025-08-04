# TouchDesigner Network Templates Guide

This directory contains Python templates for creating common TouchDesigner network patterns. Each template is a complete, working script that can be executed in TouchDesigner's textport to generate a fully functional network.

## How to Use These Templates

1. Open TouchDesigner
2. Open the Textport (Alt+T)
3. Copy and paste the entire template code
4. Press Enter to execute
5. The network will be created in `/project1`

## Available Templates

### 1. Audio Reactive Template (`audio_reactive_template.py`)

Creates a complete audio-reactive visual system.

**Features:**
- Audio device input with level monitoring
- FFT analysis for frequency spectrum
- Frequency band extraction (bass, mid, high)
- Smoothing filters for each band
- Visual generators mapped to frequency bands
- Composition and color adjustment
- Control panel for fine-tuning

**Key Components:**
- `audio_input` - Audio device input
- `fft_analysis` - FFT frequency analysis
- `bass_band`, `mid_band`, `high_band` - Frequency extractors
- `controls` - Parameter control panel

**Usage Example:**
```python
exec(open('audio_reactive_template.py').read())
```

### 2. Particle System Template (`particle_system_template.py`)

Creates a GPU-accelerated particle system with physics simulation.

**Features:**
- GPU-based particle physics using GLSL
- Configurable forces (gravity, wind, turbulence)
- Efficient instancing for thousands of particles
- Particle life cycle management
- Post-processing with bloom effect
- Comprehensive control panel

**Key Components:**
- `particle_physics` - GLSL physics simulation
- `particle_instances` - Geometry instancing
- `controls` - Physics and visual parameters

**Performance Notes:**
- Default: 10,000 particles
- Can handle up to 50,000 particles on modern GPUs
- Uses texture-based position storage for efficiency

### 3. Video Processing Template (`video_processing_template.py`)

Creates a comprehensive video input and processing pipeline.

**Features:**
- Movie file and camera input support
- Resolution adjustment and color correction
- Multiple chainable effects:
  - Blur
  - Edge detection
  - Chromatic aberration
  - Kaleidoscope
- Output recording with H.264 codec
- Performance monitoring

**Key Components:**
- `input_selector` - Switch between movie/camera
- `effect_*_switch` - Individual effect toggles
- `record_output` - Video recording
- `controls` - All processing parameters

### 4. Generative Feedback Template (`generative_feedback_template.py`)

Creates a feedback loop system for generative visuals.

**Features:**
- Multiple source generators (noise, ramp, patterns)
- Feedback loop with transform controls
- Various blend modes (add, multiply, difference, screen)
- HSV color adjustment
- Edge detection and blur effects
- Animation system with LFO and noise

**Key Components:**
- `feedback_loop` - Main feedback TOP
- `transform_feedback` - Feedback transformation
- `blend_selector` - Blend mode switching
- `controls` - Comprehensive parameter control

**Creative Tips:**
- Start with small transform values (scale: 1.01, rotate: 0.5)
- Use different blend modes for varied effects
- Combine with audio reactive template for music visuals

### 5. Projection Mapping Template (`projection_mapping_template.py`)

Creates a multi-projector mapping setup with edge blending.

**Features:**
- Support for 2 projectors (easily extendable)
- Cornerpin correction for each projector
- Edge blending with gamma correction
- Test patterns:
  - Grid
  - Alignment cross
  - Color bars
- Per-projector brightness and gamma
- Preview composite view

**Key Components:**
- `projector_*_cornerpin` - Geometric correction
- `projector_*_edge_mask` - Edge blend masks
- `pattern_selector` - Test pattern switching
- `controls` - Mapping and blend parameters

**Setup Tips:**
- Start with test patterns for alignment
- Adjust cornerpin first, then edge blending
- Use preview composite to check overlap
- Connect Window COMPs for actual output

### 6. Data Visualization Template (`data_visualization_template.py`)

Creates a complete data-driven visualization system.

**Features:**
- CSV and JSON data input support
- Data parsing and normalization
- Multiple visualization types:
  - Bar charts with instancing
  - Line charts with smooth curves
  - Scatter plots with point clouds
- Dynamic color mapping based on data values
- Animation controls with interpolation
- Real-time data preview

**Key Components:**
- `csv_input`, `json_input` - Data file inputs
- `data_to_chop` - Convert table data to numeric
- `bar_chart`, `line_chart`, `scatter_plot` - Visualization generators
- `color_map` - Data-driven color mapping
- `controls` - Visualization parameters

**Data Format:**
- CSV: First row as headers, numeric data in columns
- JSON: Array of objects with numeric properties

**Usage Tips:**
- Place data files in project folder
- Select data source in control panel
- Adjust visualization type and scaling
- Enable animation for dynamic presentations

### 7. UI Control Template (`ui_control_template.py`)

Creates a comprehensive control system with external mapping.

**Features:**
- Multi-page custom parameter interface
- MIDI input with flexible CC mapping
- OSC bidirectional communication
- Preset save/load system with interpolation
- Performance mode UI:
  - XY pad for 2D control
  - 8-channel fader bank
  - 4x4 button grid
- Parameter feedback display
- Output routing for easy integration

**Key Components:**
- `main_controls` - Central parameter container
- `midi_system` - MIDI input and mapping
- `osc_system` - OSC input/output
- `preset_system` - Preset management
- `performance_ui` - Live control interface

**Control Types:**
- Sliders (float parameters)
- Toggles (boolean switches)
- RGB color pickers
- XY/XYZ position controls
- Pulse buttons
- Menu selectors

**Integration:**
- Reference output nulls: `op('ui_control_system/output_routing/out_Master_intensity')`
- Map MIDI in `midi_mapping` table
- Configure OSC addresses and ports
- Save up to 8 presets

## Common Patterns Across Templates

### Control Panels
All templates include a `controls` container with custom parameters. These are linked to operators using expressions like:
```python
operator.par.parameter.expr = 'op("../controls").par.Custom_param'
```

### Performance Optimization
- Use instancing for multiple objects
- GPU-based processing with GLSL
- Feedback loops for iterative effects
- Efficient data flow with minimal CPU operations

### Modular Design
Each template creates a self-contained container that can be:
- Copied and reused
- Modified without affecting other parts
- Combined with other templates

## Extending Templates

To modify or extend these templates:

1. **Add Parameters**: Append to the control panel's custom page
2. **Add Operators**: Create new operators and connect them
3. **Link Parameters**: Use expressions to connect controls
4. **Save as .tox**: Right-click the container and save as component

## Best Practices

1. **Organization**: Keep related operators close together
2. **Naming**: Use descriptive names for operators
3. **Comments**: Add comments in Python code
4. **Parameters**: Group related parameters together
5. **Performance**: Monitor GPU/CPU usage with Info CHOP

## Troubleshooting

- **No audio input**: Check audio device settings
- **Low performance**: Reduce particle count or resolution
- **Black output**: Check input connections and blend modes
- **Projection alignment**: Use test patterns first

## Combining Templates

Templates can be combined for complex setups:
- Audio reactive + Particle system = Music-driven particles
- Video processing + Projection mapping = Live video mapping
- Generative feedback + Audio reactive = Audio-visual feedback
- Data visualization + UI control = Interactive data dashboard
- Audio reactive + Data visualization = Music-driven data viz
- UI control + Any template = External control integration

Simply create multiple templates and connect their outputs as needed. The UI control template is especially useful for adding external control to any other template.