# TD Network Creator Validation System Guidelines

This document provides comprehensive guidelines for implementing robust validation systems in the TD Network Creator mode. These guidelines ensure network integrity, performance optimization, and error prevention throughout the generation process.

## Table of Contents

1. [Pre-Generation Validation](#pre-generation-validation)
2. [During Generation Validation](#during-generation-validation)
3. [Post-Generation Validation](#post-generation-validation)
4. [GLSL-Specific Validation](#glsl-specific-validation)
5. [Error Recovery Strategies](#error-recovery-strategies)
6. [Validation Code Examples](#validation-code-examples)
7. [Common Error Patterns](#common-error-patterns)
8. [Best Practices for Validation](#best-practices-for-validation)

## Pre-Generation Validation

Pre-generation validation ensures that all inputs and parameters are valid before attempting to create any TouchDesigner operators.

### User Input Validation

```python
def validate_user_input(input_data):
    """
    Validate user-provided input data before network generation.
    
    Args:
        input_data (dict): User input parameters
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields
    required_fields = ['network_name', 'output_type']
    for field in required_fields:
        if field not in input_data or not input_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate network name
    if 'network_name' in input_data:
        name = input_data['network_name']
        if not name.replace('_', '').isalnum():
            errors.append("Network name must contain only alphanumeric characters and underscores")
        if name[0].isdigit():
            errors.append("Network name cannot start with a number")
    
    # Validate output type
    valid_output_types = ['TOP', 'CHOP', 'SOP', 'DAT', 'MAT', 'COMP']
    if 'output_type' in input_data:
        if input_data['output_type'] not in valid_output_types:
            errors.append(f"Invalid output type. Must be one of: {', '.join(valid_output_types)}")
    
    return len(errors) == 0, errors
```

### Resolution Validation

```python
def validate_resolution(width, height):
    """
    Validate resolution values for TouchDesigner compatibility.
    
    Args:
        width (int): Width in pixels
        height (int): Height in pixels
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Common TouchDesigner resolutions
    standard_resolutions = [
        (256, 256), (512, 512), (1024, 1024), (2048, 2048),
        (640, 480), (1280, 720), (1920, 1080), (3840, 2160),
        (1024, 768), (1280, 1024), (1920, 1200)
    ]
    
    # Check if resolution is standard
    if (width, height) in standard_resolutions:
        return True, None
    
    # Validate custom resolutions
    if width < 1 or height < 1:
        return False, "Resolution must be positive integers"
    
    if width > 16384 or height > 16384:
        return False, "Resolution exceeds TouchDesigner maximum (16384x16384)"
    
    # Warn about non-power-of-2 resolutions
    if not (width & (width - 1) == 0) or not (height & (height - 1) == 0):
        print(f"Warning: Non-power-of-2 resolution ({width}x{height}) may impact performance")
    
    return True, None
```

### Parameter Range Checking

```python
def validate_parameter_range(param_name, value, param_spec):
    """
    Validate parameter values against their specifications.
    
    Args:
        param_name (str): Parameter name
        value: Parameter value
        param_spec (dict): Parameter specification
        
    Returns:
        tuple: (is_valid, error_message)
    """
    param_type = param_spec.get('type', 'float')
    
    # Type validation
    if param_type == 'float':
        try:
            value = float(value)
        except (TypeError, ValueError):
            return False, f"{param_name} must be a float"
            
        # Range validation
        if 'min' in param_spec and value < param_spec['min']:
            return False, f"{param_name} must be >= {param_spec['min']}"
        if 'max' in param_spec and value > param_spec['max']:
            return False, f"{param_name} must be <= {param_spec['max']}"
            
    elif param_type == 'int':
        try:
            value = int(value)
        except (TypeError, ValueError):
            return False, f"{param_name} must be an integer"
            
        # Range validation
        if 'min' in param_spec and value < param_spec['min']:
            return False, f"{param_name} must be >= {param_spec['min']}"
        if 'max' in param_spec and value > param_spec['max']:
            return False, f"{param_name} must be <= {param_spec['max']}"
            
    elif param_type == 'menu':
        valid_options = param_spec.get('options', [])
        if value not in valid_options:
            return False, f"{param_name} must be one of: {', '.join(valid_options)}"
    
    return True, None
```

### GLSL Syntax Pre-Validation

```python
import re

def pre_validate_glsl(glsl_code):
    """
    Perform basic GLSL syntax validation before compilation.
    
    Args:
        glsl_code (str): GLSL shader code
        
    Returns:
        tuple: (is_valid, warnings, errors)
    """
    warnings = []
    errors = []
    
    # Check for TouchDesigner-specific uniforms
    td_uniforms = ['sTD2DInputs', 'uTDOutputInfo', 'uTD2DInfos']
    for uniform in td_uniforms:
        if uniform in glsl_code and f'uniform' not in glsl_code:
            warnings.append(f"Using {uniform} without proper uniform declaration")
    
    # Check for main function
    if 'void main()' not in glsl_code:
        errors.append("Missing main() function")
    
    # Check for output variable
    if 'fragColor' not in glsl_code and 'gl_FragColor' not in glsl_code:
        errors.append("No output color variable found")
    
    # Check for balanced braces
    open_braces = glsl_code.count('{')
    close_braces = glsl_code.count('}')
    if open_braces != close_braces:
        errors.append(f"Unbalanced braces: {open_braces} open, {close_braces} close")
    
    # Check for common syntax errors
    if re.search(r';\s*;', glsl_code):
        warnings.append("Double semicolon detected")
    
    # Check for undefined variables (basic)
    declared_vars = re.findall(r'(?:uniform|varying|attribute|const)?\s*(?:float|vec2|vec3|vec4|mat2|mat3|mat4|sampler2D)\s+(\w+)', glsl_code)
    used_vars = re.findall(r'(?<!\.)\b(\w+)\s*[=\+\-\*\/\(\[]', glsl_code)
    
    undefined = set(used_vars) - set(declared_vars) - {'gl_FragCoord', 'fragColor', 'texture', 'vec2', 'vec3', 'vec4'}
    if undefined:
        warnings.append(f"Potentially undefined variables: {', '.join(undefined)}")
    
    return len(errors) == 0, warnings, errors
```

### Network Complexity Assessment

```python
def assess_network_complexity(network_spec):
    """
    Assess the complexity of the proposed network to warn about potential issues.
    
    Args:
        network_spec (dict): Network specification
        
    Returns:
        dict: Complexity assessment with warnings
    """
    assessment = {
        'operator_count': 0,
        'connection_count': 0,
        'feedback_loops': 0,
        'glsl_operators': 0,
        'warnings': [],
        'estimated_cook_time': 0.0
    }
    
    # Count operators
    assessment['operator_count'] = len(network_spec.get('operators', []))
    
    # Count connections
    for op in network_spec.get('operators', []):
        assessment['connection_count'] += len(op.get('connections', []))
    
    # Count GLSL operators (more expensive)
    glsl_ops = [op for op in network_spec.get('operators', []) if op.get('type') == 'glslTOP']
    assessment['glsl_operators'] = len(glsl_ops)
    
    # Detect feedback loops
    connections = []
    for op in network_spec.get('operators', []):
        for conn in op.get('connections', []):
            connections.append((conn['from'], op['name']))
    
    assessment['feedback_loops'] = detect_cycles(connections)
    
    # Generate warnings
    if assessment['operator_count'] > 100:
        assessment['warnings'].append(f"High operator count ({assessment['operator_count']}) may impact performance")
    
    if assessment['glsl_operators'] > 10:
        assessment['warnings'].append(f"Multiple GLSL operators ({assessment['glsl_operators']}) may cause GPU bottlenecks")
    
    if assessment['feedback_loops'] > 0:
        assessment['warnings'].append(f"Network contains {assessment['feedback_loops']} feedback loops")
    
    # Estimate cook time (rough approximation)
    assessment['estimated_cook_time'] = (
        assessment['operator_count'] * 0.001 +
        assessment['glsl_operators'] * 0.01 +
        assessment['feedback_loops'] * 0.005
    )
    
    return assessment

def detect_cycles(edges):
    """Detect cycles in a directed graph."""
    from collections import defaultdict, deque
    
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Find all nodes
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    
    # Topological sort to detect cycles
    queue = deque([node for node in all_nodes if in_degree[node] == 0])
    visited = 0
    
    while queue:
        node = queue.popleft()
        visited += 1
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we haven't visited all nodes, there's a cycle
    return len(all_nodes) - visited
```

## During Generation Validation

Validation during the generation process ensures each step succeeds before proceeding.

### Operator Creation Verification

```python
def verify_operator_creation(op_name, op_type, parent=None):
    """
    Verify that an operator was successfully created.
    
    Args:
        op_name (str): Operator name
        op_type (str): Operator type
        parent: Parent operator (optional)
        
    Returns:
        tuple: (success, operator_or_error)
    """
    try:
        if parent:
            op = parent.op(op_name)
        else:
            op = op(op_name)
        
        if op is None:
            return False, f"Failed to create operator {op_name}"
        
        # Verify type matches
        if not op.type.endswith(op_type.upper()):
            return False, f"Operator type mismatch: expected {op_type}, got {op.type}"
        
        # Check for initialization errors
        if hasattr(op, 'errors') and op.errors:
            return False, f"Operator has errors: {op.errors}"
        
        return True, op
        
    except Exception as e:
        return False, f"Exception creating operator: {str(e)}"
```

### Connection Compatibility Checking

```python
def check_connection_compatibility(source_op, source_output, target_op, target_input):
    """
    Check if a connection between operators is valid.
    
    Args:
        source_op: Source operator
        source_output (int): Source output index
        target_op: Target operator
        target_input (int): Target input index
        
    Returns:
        tuple: (is_compatible, error_message)
    """
    # Get operator families
    source_family = source_op.family
    target_family = target_op.family
    
    # Define compatibility rules
    compatibility_matrix = {
        'TOP': ['TOP', 'COMP'],
        'CHOP': ['CHOP', 'COMP', 'SOP'],
        'SOP': ['SOP', 'COMP'],
        'DAT': ['DAT', 'COMP'],
        'MAT': ['MAT', 'COMP'],
        'COMP': ['TOP', 'CHOP', 'SOP', 'DAT', 'MAT', 'COMP']
    }
    
    # Check basic compatibility
    if target_family not in compatibility_matrix.get(source_family, []):
        return False, f"Cannot connect {source_family} to {target_family}"
    
    # Check output index validity
    if source_output >= len(source_op.outputs):
        return False, f"Invalid output index {source_output} for {source_op.name}"
    
    # Check input index validity
    if target_input >= len(target_op.inputs):
        return False, f"Invalid input index {target_input} for {target_op.name}"
    
    # Special case: Check resolution compatibility for TOPs
    if source_family == 'TOP' and target_family == 'TOP':
        source_res = (source_op.width, source_op.height)
        target_res = (target_op.width, target_op.height)
        
        # Some operators require matching resolutions
        resolution_sensitive_ops = ['compositeTOP', 'differenceTOP', 'addTOP']
        if target_op.type in resolution_sensitive_ops and source_res != target_res:
            return False, f"Resolution mismatch: {source_res} != {target_res}"
    
    return True, None
```

### Parameter Type Matching

```python
def validate_parameter_type(op, param_name, value):
    """
    Validate that a parameter value matches the expected type.
    
    Args:
        op: TouchDesigner operator
        param_name (str): Parameter name
        value: Value to set
        
    Returns:
        tuple: (is_valid, converted_value, error_message)
    """
    try:
        param = op.par[param_name]
        if param is None:
            return False, None, f"Parameter {param_name} not found"
        
        # Get parameter style
        param_style = param.style
        
        # Handle different parameter styles
        if param_style == 'Float':
            try:
                converted = float(value)
                return True, converted, None
            except (TypeError, ValueError):
                return False, None, f"Parameter {param_name} requires float value"
                
        elif param_style == 'Int':
            try:
                converted = int(value)
                return True, converted, None
            except (TypeError, ValueError):
                return False, None, f"Parameter {param_name} requires integer value"
                
        elif param_style == 'Toggle':
            if isinstance(value, bool):
                converted = value
            elif isinstance(value, (int, float)):
                converted = bool(value)
            elif isinstance(value, str):
                converted = value.lower() in ['true', '1', 'yes', 'on']
            else:
                return False, None, f"Parameter {param_name} requires boolean value"
            return True, converted, None
            
        elif param_style == 'Menu':
            # Check if value is in menu items
            menu_items = param.menuNames
            if value not in menu_items:
                return False, None, f"Parameter {param_name} must be one of: {', '.join(menu_items)}"
            return True, value, None
            
        elif param_style == 'Str':
            return True, str(value), None
            
        else:
            # Default: try to set as-is
            return True, value, None
            
    except Exception as e:
        return False, None, f"Error validating parameter: {str(e)}"
```

### Memory Usage Estimation

```python
def estimate_memory_usage(network_spec):
    """
    Estimate memory usage for the network.
    
    Args:
        network_spec (dict): Network specification
        
    Returns:
        dict: Memory usage estimation
    """
    memory_estimate = {
        'texture_memory_mb': 0,
        'cpu_memory_mb': 0,
        'total_mb': 0,
        'warnings': []
    }
    
    # Memory usage per operator type (rough estimates in MB)
    memory_per_op = {
        'noiseTOP': 0.5,
        'glslTOP': 1.0,
        'renderTOP': 2.0,
        'moviefileinTOP': 10.0,
        'cacheTOP': 50.0,
        'feedbackTOP': 1.0,
        'constantTOP': 0.1,
        'default': 0.2
    }
    
    for op in network_spec.get('operators', []):
        op_type = op.get('type', 'default')
        base_memory = memory_per_op.get(op_type, memory_per_op['default'])
        
        # Adjust for resolution if TOP
        if op_type.endswith('TOP'):
            width = op.get('parameters', {}).get('width', 1280)
            height = op.get('parameters', {}).get('height', 720)
            pixel_count = width * height
            
            # 4 bytes per pixel (RGBA), convert to MB
            texture_memory = (pixel_count * 4) / (1024 * 1024)
            memory_estimate['texture_memory_mb'] += texture_memory
            
            # Add base operator memory
            memory_estimate['cpu_memory_mb'] += base_memory
        else:
            memory_estimate['cpu_memory_mb'] += base_memory
    
    memory_estimate['total_mb'] = (
        memory_estimate['texture_memory_mb'] + 
        memory_estimate['cpu_memory_mb']
    )
    
    # Generate warnings
    if memory_estimate['total_mb'] > 1000:
        memory_estimate['warnings'].append(
            f"High memory usage estimated: {memory_estimate['total_mb']:.1f} MB"
        )
    
    if memory_estimate['texture_memory_mb'] > 500:
        memory_estimate['warnings'].append(
            f"High texture memory usage: {memory_estimate['texture_memory_mb']:.1f} MB"
        )
    
    return memory_estimate
```

### Circular Dependency Detection

```python
def detect_circular_dependencies(operators, connections):
    """
    Detect circular dependencies in the network.
    
    Args:
        operators (list): List of operators
        connections (list): List of connections
        
    Returns:
        list: List of circular dependency chains
    """
    from collections import defaultdict
    
    # Build adjacency list
    graph = defaultdict(list)
    for conn in connections:
        graph[conn['from']].append(conn['to'])
    
    # DFS to detect cycles
    def has_cycle_util(node, visited, rec_stack, path):
        visited[node] = True
        rec_stack[node] = True
        path.append(node)
        
        cycles = []
        
        for neighbor in graph[node]:
            if not visited.get(neighbor, False):
                cycles.extend(has_cycle_util(neighbor, visited, rec_stack, path.copy()))
            elif rec_stack.get(neighbor, False):
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
        
        path.pop()
        rec_stack[node] = False
        return cycles
    
    visited = {}
    rec_stack = {}
    all_cycles = []
    
    for op in operators:
        if not visited.get(op['name'], False):
            cycles = has_cycle_util(op['name'], visited, rec_stack, [])
            all_cycles.extend(cycles)
    
    return all_cycles
```

## Post-Generation Validation

Validation after network generation ensures everything works correctly.

### Network Integrity Checks

```python
def validate_network_integrity(root_op):
    """
    Perform comprehensive network integrity checks.
    
    Args:
        root_op: Root operator of the network
        
    Returns:
        dict: Validation results
    """
    results = {
        'valid': True,
        'operator_count': 0,
        'connection_count': 0,
        'errors': [],
        'warnings': [],
        'orphaned_operators': [],
        'missing_connections': []
    }
    
    # Collect all operators
    all_ops = root_op.findChildren('*')
    results['operator_count'] = len(all_ops)
    
    # Check each operator
    for op in all_ops:
        # Check for errors
        if hasattr(op, 'errors') and op.errors:
            results['errors'].append(f"{op.path}: {op.errors}")
            results['valid'] = False
        
        # Check for warnings
        if hasattr(op, 'warnings') and op.warnings:
            results['warnings'].append(f"{op.path}: {op.warnings}")
        
        # Check connections
        for i, input_op in enumerate(op.inputs):
            if input_op is None and op.inputConnectors[i]:
                results['missing_connections'].append(f"{op.path} input {i}")
        
        # Count connections
        results['connection_count'] += len([i for i in op.inputs if i is not None])
    
    # Find orphaned operators (no inputs or outputs)
    for op in all_ops:
        has_inputs = any(i is not None for i in op.inputs)
        has_outputs = any(other_op.inputs[i] == op 
                         for other_op in all_ops 
                         for i in range(len(other_op.inputs)))
        
        if not has_inputs and not has_outputs and op != root_op:
            results['orphaned_operators'].append(op.path)
    
    return results
```

### GLSL Compilation Verification

```python
def verify_glsl_compilation(glsl_op):
    """
    Verify GLSL shader compilation and get detailed error information.
    
    Args:
        glsl_op: GLSL TOP operator
        
    Returns:
        dict: Compilation results
    """
    results = {
        'compiled': False,
        'errors': [],
        'warnings': [],
        'performance_info': {}
    }
    
    # Force cook to ensure compilation
    glsl_op.cook(force=True)
    
    # Check for compilation errors
    if hasattr(glsl_op, 'errors') and glsl_op.errors:
        results['errors'] = glsl_op.errors.split('\n')
        return results
    
    # Check if output is valid
    if glsl_op.width == 0 or glsl_op.height == 0:
        results['errors'].append("GLSL output has zero dimensions")
        return results
    
    # Get shader info if available
    if hasattr(glsl_op, 'shaderInfo'):
        info = glsl_op.shaderInfo
        results['performance_info'] = {
            'instruction_count': info.get('instructionCount', 'N/A'),
            'register_count': info.get('registerCount', 'N/A'),
            'texture_count': info.get('textureCount', 'N/A')
        }
    
    results['compiled'] = True
    
    # Performance warnings
    if results['performance_info'].get('instruction_count', 0) > 1000:
        results['warnings'].append("High instruction count may impact performance")
    
    return results
```

### Performance Profiling Setup

```python
def setup_performance_profiling(network_root):
    """
    Set up performance monitoring for the network.
    
    Args:
        network_root: Root operator of the network
        
    Returns:
        dict: Performance monitoring setup
    """
    profiling = {
        'monitors': [],
        'baseline_metrics': {},
        'thresholds': {
            'cook_time_ms': 16.67,  # 60 FPS threshold
            'gpu_memory_mb': 1000,
            'cpu_percent': 80
        }
    }
    
    # Create performance CHOP
    perf_chop = network_root.create(performanceCHOP, 'performance_monitor')
    perf_chop.par.active = True
    perf_chop.par.filterlevel = 'operators'
    perf_chop.par.filterpath = network_root.path + '/*'
    
    profiling['monitors'].append(perf_chop)
    
    # Create info DAT for system metrics
    info_dat = network_root.create(infoDat, 'system_info')
    info_dat.par.info = 'system'
    
    profiling['monitors'].append(info_dat)
    
    # Get baseline metrics
    network_root.cook(force=True)
    
    if perf_chop.numChans > 0:
        profiling['baseline_metrics']['avg_cook_time'] = perf_chop['cook_time'].eval()
        profiling['baseline_metrics']['avg_gpu_mem'] = perf_chop['gpu_mem_used'].eval()
    
    # Create performance warning logic
    logic_dat = network_root.create(datexecDAT, 'performance_warnings')
    logic_dat.par.language = 'python'
    logic_dat.text = '''
def onCook(dat):
    perf = op('../performance_monitor')
    warnings = []
    
    if perf['cook_time'].eval() > 16.67:
        warnings.append(f"Slow cook time: {perf['cook_time'].eval():.2f}ms")
    
    if perf['gpu_mem_used'].eval() > 1000:
        warnings.append(f"High GPU memory: {perf['gpu_mem_used'].eval():.0f}MB")
    
    if warnings:
        print("Performance warnings:", warnings)
    '''
    
    profiling['monitors'].append(logic_dat)
    
    return profiling
```

### Error Node Detection

```python
def detect_error_nodes(network_root):
    """
    Detect and categorize error nodes in the network.
    
    Args:
        network_root: Root operator of the network
        
    Returns:
        dict: Error node information
    """
    error_info = {
        'error_nodes': [],
        'warning_nodes': [],
        'cook_errors': [],
        'parameter_errors': [],
        'connection_errors': []
    }
    
    all_ops = network_root.findChildren('*')
    
    for op in all_ops:
        # Check for general errors
        if hasattr(op, 'errors') and op.errors:
            error_info['error_nodes'].append({
                'path': op.path,
                'type': op.type,
                'errors': op.errors
            })
        
        # Check for warnings
        if hasattr(op, 'warnings') and op.warnings:
            error_info['warning_nodes'].append({
                'path': op.path,
                'type': op.type,
                'warnings': op.warnings
            })
        
        # Check cook state
        if hasattr(op, 'cookState') and not op.cookState:
            error_info['cook_errors'].append({
                'path': op.path,
                'reason': 'Failed to cook'
            })
        
        # Check for parameter errors
        for par in op.pars():
            if par.error:
                error_info['parameter_errors'].append({
                    'path': op.path,
                    'parameter': par.name,
                    'error': par.error
                })
        
        # Check for missing connections
        for i, input_op in enumerate(op.inputs):
            if input_op is None and i < len(op.inputConnectors):
                if op.inputConnectors[i]:
                    error_info['connection_errors'].append({
                        'path': op.path,
                        'input': i,
                        'error': 'Missing required connection'
                    })
    
    return error_info
```

### Output Validation

```python
def validate_output(output_op, expected_type, expected_properties=None):
    """
    Validate the final output of the network.
    
    Args:
        output_op: Output operator
        expected_type (str): Expected operator type
        expected_properties (dict): Expected properties to validate
        
    Returns:
        dict: Validation results
    """
    results = {
        'valid': True,
        'type_match': False,
        'property_checks': {},
        'errors': []
    }
    
    # Check type
    if output_op.type == expected_type:
        results['type_match'] = True
    else:
        results['errors'].append(f"Type mismatch: expected {expected_type}, got {output_op.type}")
        results['valid'] = False
    
    # Check properties if provided
    if expected_properties:
        for prop, expected_value in expected_properties.items():
            actual_value = None
            
            # Handle different property types
            if prop == 'resolution' and output_op.family == 'TOP':
                actual_value = (output_op.width, output_op.height)
            elif prop == 'channels' and output_op.family == 'CHOP':
                actual_value = output_op.numChans
            elif prop == 'samples' and output_op.family == 'CHOP':
                actual_value = output_op.numSamples
            elif hasattr(output_op, prop):
                actual_value = getattr(output_op, prop)
            
            if actual_value is not None:
                if actual_value == expected_value:
                    results['property_checks'][prop] = 'passed'
                else:
                    results['property_checks'][prop] = f'failed: expected {expected_value}, got {actual_value}'
                    results['errors'].append(f"Property {prop} mismatch")
                    results['valid'] = False
    
    # Check if output is producing data
    if output_op.family == 'TOP':
        if output_op.width == 0 or output_op.height == 0:
            results['errors'].append("Output has zero dimensions")
            results['valid'] = False
    elif output_op.family == 'CHOP':
        if output_op.numChans == 0 or output_op.numSamples == 0:
            results['errors'].append("Output has no data")
            results['valid'] = False
    
    return results
```

## GLSL-Specific Validation

Specialized validation for GLSL shaders in TouchDesigner.

### TouchDesigner Syntax Compliance

```python
def validate_