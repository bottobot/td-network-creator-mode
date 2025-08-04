# TouchDesigner Python API Guide

This guide provides an introduction to the TouchDesigner Python API and explains how to use the example files in this directory.

## Table of Contents

1. [Introduction](#introduction)
2. [Python API Basics](#python-api-basics)
3. [Example Files Overview](#example-files-overview)
4. [Getting Started](#getting-started)
5. [Best Practices](#best-practices)
6. [Common Patterns](#common-patterns)
7. [Performance Tips](#performance-tips)
8. [Troubleshooting](#troubleshooting)

## Introduction

TouchDesigner's Python API provides powerful programmatic control over the software, allowing you to:
- Create and destroy operators
- Set and read parameters
- Make connections between operators
- Navigate the network
- Handle data from various operator types
- Automate complex workflows

## Python API Basics

### Core Concepts

#### 1. The `op()` Function
The most fundamental function in TouchDesigner Python:
```python
# Access operator by name (relative to current location)
my_noise = op('noise1')

# Access operator by absolute path
my_noise = op('/project1/noise1')

# Access operator by relative path
parent_op = op('../')
sibling_op = op('../sibling_operator')
```

#### 2. Operator Types
TouchDesigner has six main operator families:
- **TOP** (Texture Operators): 2D image processing
- **CHOP** (Channel Operators): Motion, audio, control signals
- **SOP** (Surface Operators): 3D geometry
- **DAT** (Data Operators): Text, tables, scripts
- **MAT** (Material Operators): 3D rendering materials
- **COMP** (Component Operators): UI elements, 3D objects, sub-networks

#### 3. Parameters
Every operator has parameters that control its behavior:
```python
# Set parameter value
op('noise1').par.period = 5

# Read parameter value
current_period = op('noise1').par.period.eval()

# Set multiple parameters
noise = op('noise1')
noise.par.period = 5
noise.par.amplitude = 2
noise.par.offset = 0.5
```

#### 4. Connections
Operators connect to form networks:
```python
# Connect output of source to input of target
target.inputConnectors[0].connect(source)

# Or use the output connector
source.outputConnectors[0].connect(target)
```

## Example Files Overview

### 1. **operator_creation_examples.py**
Learn how to create different types of operators programmatically:
- Creating all operator types (TOP, CHOP, SOP, DAT, MAT, COMP)
- Setting operator positions in the network
- Following naming conventions
- Creating parent/child relationships
- Batch creation techniques

**Key Functions:**
- `create_top_examples()`: Create and connect TOP operators
- `create_parent_child_examples()`: Build hierarchical networks
- `batch_create_operators()`: Efficiently create multiple operators

### 2. **parameter_manipulation_examples.py**
Master working with operator parameters:
- Setting and reading parameter values
- Using expression mode for dynamic parameters
- Creating custom parameters and pages
- Animating parameters
- Parameter validation and binding

**Key Functions:**
- `basic_parameter_examples()`: Fundamental parameter operations
- `expression_mode_examples()`: Dynamic parameter expressions
- `custom_parameter_examples()`: Add custom controls to operators

### 3. **connection_examples.py**
Understand how to connect operators:
- Basic input/output connections
- Multiple connections from one source
- Selective connections
- CHOP exports to parameters
- Reference-based connections
- Dynamic connection management

**Key Functions:**
- `basic_connection_examples()`: Simple operator connections
- `chop_export_examples()`: Export CHOP data to parameters
- `dynamic_connection_examples()`: Programmatically manage connections

### 4. **network_navigation_examples.py**
Navigate and search through networks:
- Finding operators by name or pattern
- Parent/child traversal
- Working with operator collections
- Path resolution techniques
- Advanced search patterns

**Key Functions:**
- `find_operators_by_name()`: Search for specific operators
- `parent_child_traversal()`: Navigate hierarchies
- `network_search_patterns()`: Complex search operations

### 5. **data_handling_examples.py**
Work with data in different operator types:
- Table DAT manipulation
- CHOP channel data access
- TOP pixel data (indirect methods)
- JSON/XML parsing
- Data visualization helpers

**Key Functions:**
- `table_dat_examples()`: Work with tabular data
- `chop_channel_examples()`: Access time-series data
- `json_xml_parsing_examples()`: Parse structured data

### 6. **error_handling_examples.py**
Write robust code with proper error handling:
- Try/except patterns
- Operator existence checks
- Parameter validation
- Safe network modifications
- Error recovery patterns

**Key Functions:**
- `try_except_patterns()`: Basic error handling
- `operator_existence_checks()`: Verify operators before use
- `safe_network_modifications()`: Modify networks safely

### 7. **performance_optimization_examples.py**
Optimize your Python scripts for better performance:
- Batch operations
- Cooking control
- Memory management
- Efficient loops
- Network optimization patterns

**Key Functions:**
- `batch_operations_examples()`: Process multiple operators efficiently
- `cooking_control_examples()`: Control when operators cook
- `memory_management_examples()`: Use memory efficiently

## Getting Started

### Running the Examples

1. **In TouchDesigner's Textport:**
   ```python
   # Navigate to the examples directory
   import os
   os.chdir('path/to/td-network-creator-mode/python-api-examples')
   
   # Run an example file
   exec(open('operator_creation_examples.py').read())
   ```

2. **In a Text DAT:**
   - Create a Text DAT
   - Copy the example code
   - Right-click and select "Run Script"

3. **As a Module:**
   ```python
   # Import specific functions
   import sys
   sys.path.append('path/to/td-network-creator-mode/python-api-examples')
   from operator_creation_examples import create_top_examples
   
   # Use the function
   result = create_top_examples()
   ```

### Basic Workflow Example

Here's a simple example that combines concepts from multiple files:

```python
# Create a simple video effect chain
def create_video_effect_chain():
    # Create source (from operator_creation_examples.py)
    movie = op('/project1').create(moviefileinTOP, 'video_source')
    movie.par.file = 'C:/media/sample.mp4'
    
    # Create effects
    blur = op('/project1').create(blurTOP, 'video_blur')
    level = op('/project1').create(levelTOP, 'video_level')
    
    # Set parameters (from parameter_manipulation_examples.py)
    blur.par.sizex = 10
    blur.par.sizey = 10
    level.par.brightness1 = 1.2
    level.par.contrast = 1.1
    
    # Make connections (from connection_examples.py)
    blur.inputConnectors[0].connect(movie)
    level.inputConnectors[0].connect(blur)
    
    # Position operators (from operator_creation_examples.py)
    movie.nodeX, movie.nodeY = 0, 0
    blur.nodeX, blur.nodeY = 200, 0
    level.nodeX, level.nodeY = 400, 0
    
    # Add error handling (from error_handling_examples.py)
    try:
        # Create output
        out = op('/project1').create(nullTOP, 'video_output')
        out.inputConnectors[0].connect(level)
        out.nodeX, out.nodeY = 600, 0
        out.viewer = True  # Enable viewer
        print("Video effect chain created successfully!")
    except Exception as e:
        print(f"Error creating output: {e}")
    
    return movie, blur, level

# Run the example
create_video_effect_chain()
```

## Best Practices

### 1. **Naming Conventions**
```python
# Use descriptive names with type suffixes
noise_generator = op('/project1').create(noiseTOP, 'noiseGenerator_TOP')
audio_analyzer = op('/project1').create(analyzeCHOP, 'audioAnalyzer_CHOP')

# Use prefixes for grouping
ui_button = op('/project1').create(buttonCOMP, 'ui_playButton')
ui_slider = op('/project1').create(sliderCOMP, 'ui_speedSlider')
```

### 2. **Error Handling**
```python
# Always check if operators exist
target_op = op('my_operator')
if target_op:
    target_op.par.value = 1.0
else:
    print("Operator not found!")

# Use try/except for risky operations
try:
    new_op = parent.create(noiseTOP, 'noise1')
except Exception as e:
    print(f"Failed to create operator: {e}")
```

### 3. **Performance Considerations**
```python
# Cache operator references
my_container = op('/project1/container1')
children = my_container.children  # Cache the list

# Use batch operations
for child in children:
    child.par.alpha = 0.5  # More efficient than multiple op() calls
```

## Common Patterns

### 1. **Creating UI Controls**
```python
# Create a control panel
control_panel = op('/project1').create(containerCOMP, 'controls')
control_panel.par.w = 400
control_panel.par.h = 300

# Add custom parameters
page = control_panel.appendCustomPage('Settings')
speed_par = page.appendFloat('Speed', label='Animation Speed')[0]
speed_par.default = 1.0
speed_par.min = 0.0
speed_par.max = 10.0
```

### 2. **Dynamic Networks**
```python
# Create operators based on data
data_table = op('data_source')
for row in range(1, data_table.numRows):
    name = data_table[row, 'name'].val
    op_type = data_table[row, 'type'].val
    
    if op_type == 'noise':
        new_op = op('/project1').create(noiseTOP, name)
    elif op_type == 'constant':
        new_op = op('/project1').create(constantTOP, name)
```

### 3. **Operator Templates**
```python
# Create a reusable operator setup
def create_processor_template(name, process_type='blur'):
    container = op('/project1').create(containerCOMP, f'{name}_processor')
    
    # Input
    in_op = container.create(inTOP, 'input')
    
    # Process
    if process_type == 'blur':
        process = container.create(blurTOP, 'process')
    elif process_type == 'level':
        process = container.create(levelTOP, 'process')
    
    # Output
    out_op = container.create(outTOP, 'output')
    
    # Connect
    process.inputConnectors[0].connect(in_op)
    out_op.inputConnectors[0].connect(process)
    
    return container
```

## Performance Tips

1. **Minimize op() calls**: Cache operator references
2. **Batch operations**: Set multiple parameters at once
3. **Control cooking**: Disable cooking during setup
4. **Use appropriate resolution**: Process at lower resolution when possible
5. **Pool operators**: Reuse operators instead of creating/destroying
6. **Profile your code**: Measure performance bottlenecks

## Troubleshooting

### Common Issues and Solutions

1. **"NoneType has no attribute" errors**
   - Operator doesn't exist at the specified path
   - Solution: Check operator existence before accessing

2. **"Name already exists" errors**
   - Trying to create operator with duplicate name
   - Solution: Use unique names or check existence first

3. **Parameter doesn't update**
   - Parameter might be in expression or export mode
   - Solution: Check parameter mode before setting

4. **Connection fails**
   - Input already connected or incompatible types
   - Solution: Disconnect existing connections first

5. **Performance issues**
   - Too many individual operations
   - Solution: Use batch operations and caching

### Debug Techniques

```python
# Print operator info
print(f"Operator: {op.name}")
print(f"Type: {op.OPType}")
print(f"Path: {op.path}")
print(f"Parent: {op.parent().name}")

# List all parameters
for par in op.pars():
    print(f"{par.name}: {par.eval()}")

# Check connections
for i, conn in enumerate(op.inputConnectors):
    if conn.connections:
        print(f"Input {i}: {conn.connections[0].name}")
```

## Next Steps

1. **Experiment with the examples**: Run each example file and modify the code
2. **Combine techniques**: Create your own scripts using multiple concepts
3. **Build tools**: Create reusable functions for common tasks
4. **Optimize**: Profile and improve your code's performance
5. **Share**: Create your own examples and share with the community

Remember: The TouchDesigner Python API is powerful but requires practice. Start simple, test often, and gradually build more complex systems.

For more information, refer to the official TouchDesigner Python documentation and the Derivative Wiki.