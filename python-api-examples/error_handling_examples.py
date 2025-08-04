"""
TouchDesigner Python API Examples - Error Handling
This file demonstrates robust error handling techniques for TouchDesigner Python scripts.
"""

# Try/Except Patterns
def try_except_patterns():
    """Examples of try/except patterns in TouchDesigner"""
    
    # Basic error handling
    def safe_operator_creation(parent, op_type, name):
        """Safely create an operator with error handling"""
        try:
            new_op = parent.create(op_type, name)
            print(f"Successfully created {name}")
            return new_op
        except Exception as e:
            print(f"Failed to create {name}: {str(e)}")
            return None
    
    # Test safe creation
    result1 = safe_operator_creation(op('/project1'), noiseTOP, 'error_test_noise')
    result2 = safe_operator_creation(op('/project1'), noiseTOP, 'error_test_noise')  # Duplicate name
    
    # Handling specific exceptions
    def safe_parameter_set(operator, param_name, value):
        """Safely set a parameter with specific error handling"""
        try:
            if not operator:
                raise ValueError("Operator is None")
            
            if not hasattr(operator.par, param_name):
                raise AttributeError(f"Parameter '{param_name}' does not exist")
            
            param = getattr(operator.par, param_name)
            
            # Check if parameter is read-only
            if param.isReadOnly:
                raise RuntimeError(f"Parameter '{param_name}' is read-only")
            
            # Set the value
            param.val = value
            return True
            
        except ValueError as e:
            print(f"Value Error: {e}")
            return False
        except AttributeError as e:
            print(f"Attribute Error: {e}")
            return False
        except RuntimeError as e:
            print(f"Runtime Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error setting {param_name}: {e}")
            return False
    
    # Test parameter setting
    if result1:
        safe_parameter_set(result1, 'period', 10)  # Valid
        safe_parameter_set(result1, 'invalid_param', 10)  # Invalid parameter
        safe_parameter_set(None, 'period', 10)  # None operator
    
    # Error handling with cleanup
    def create_network_with_cleanup():
        """Create a network with proper cleanup on error"""
        created_ops = []
        
        try:
            # Create operators
            noise = op('/project1').create(noiseTOP, 'cleanup_noise')
            created_ops.append(noise)
            
            blur = op('/project1').create(blurTOP, 'cleanup_blur')
            created_ops.append(blur)
            
            # This might fail
            blur.inputConnectors[0].connect(noise)
            
            # Intentional error for demonstration
            if len(created_ops) > 1:
                raise Exception("Simulated error during network creation")
            
            return created_ops
            
        except Exception as e:
            print(f"Error creating network: {e}")
            # Cleanup created operators
            for op_obj in created_ops:
                try:
                    op_obj.destroy()
                    print(f"Cleaned up {op_obj.name}")
                except:
                    pass
            return None
    
    # Test cleanup
    network = create_network_with_cleanup()
    
    # Context manager pattern (custom implementation)
    class OperatorContext:
        """Context manager for operator creation"""
        def __init__(self, parent, op_type, name):
            self.parent = parent
            self.op_type = op_type
            self.name = name
            self.operator = None
        
        def __enter__(self):
            try:
                self.operator = self.parent.create(self.op_type, self.name)
                return self.operator
            except Exception as e:
                print(f"Failed to create operator in context: {e}")
                raise
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                # Error occurred, cleanup
                if self.operator:
                    try:
                        self.operator.destroy()
                        print(f"Cleaned up {self.name} due to error")
                    except:
                        pass
            return False  # Don't suppress exceptions
    
    # Use context manager
    try:
        with OperatorContext(op('/project1'), constantTOP, 'context_test') as const:
            const.par.colorr = 1.0
            # Simulate error
            # raise Exception("Test error")
    except Exception as e:
        print(f"Context manager error: {e}")
    
    return result1


# Operator Existence Checks
def operator_existence_checks():
    """Examples of checking operator existence before operations"""
    
    # Safe operator access
    def safe_op_access(path):
        """Safely access an operator by path"""
        try:
            operator = op(path)
            if operator is None:
                print(f"Operator at '{path}' does not exist")
                return None
            return operator
        except Exception as e:
            print(f"Error accessing operator at '{path}': {e}")
            return None
    
    # Test access
    exists = safe_op_access('/project1')
    not_exists = safe_op_access('/invalid/path')
    
    # Check before connection
    def safe_connect(source_path, target_path, input_index=0):
        """Safely connect two operators"""
        source = safe_op_access(source_path)
        target = safe_op_access(target_path)
        
        if not source:
            return False, "Source operator not found"
        
        if not target:
            return False, "Target operator not found"
        
        try:
            # Check if input index is valid
            if input_index >= len(target.inputConnectors):
                return False, f"Invalid input index {input_index}"
            
            # Make connection
            target.inputConnectors[input_index].connect(source)
            return True, "Connected successfully"
            
        except Exception as e:
            return False, f"Connection failed: {e}"
    
    # Create test operators
    n1 = op('/project1').create(noiseTOP, 'exist_noise1')
    n2 = op('/project1').create(blurTOP, 'exist_blur1')
    
    # Test connections
    success1, msg1 = safe_connect('exist_noise1', 'exist_blur1')
    print(f"Connection 1: {msg1}")
    
    success2, msg2 = safe_connect('invalid_op', 'exist_blur1')
    print(f"Connection 2: {msg2}")
    
    # Batch existence check
    def check_operators_exist(op_names, parent_path='/project1'):
        """Check if multiple operators exist"""
        parent = op(parent_path)
        if not parent:
            return {}
        
        results = {}
        for name in op_names:
            results[name] = parent.op(name) is not None
        
        return results
    
    # Test batch check
    ops_to_check = ['exist_noise1', 'exist_blur1', 'not_exist1', 'not_exist2']
    existence = check_operators_exist(ops_to_check)
    print(f"\nOperator existence: {existence}")
    
    # Safe operator iteration
    def safe_iterate_children(parent_path):
        """Safely iterate through children of an operator"""
        parent = safe_op_access(parent_path)
        if not parent:
            return []
        
        try:
            # Check if operator can have children
            if not isinstance(parent, COMP):
                print(f"{parent_path} is not a COMP and cannot have children")
                return []
            
            return list(parent.children)
        except Exception as e:
            print(f"Error iterating children: {e}")
            return []
    
    # Test iteration
    children = safe_iterate_children('/project1')
    print(f"\nFound {len(children)} children")
    
    return n1, n2


# Parameter Validation
def parameter_validation():
    """Examples of parameter validation before setting"""
    
    # Create test operator
    test_op = op('/project1').create(noiseTOP, 'validation_test')
    test_op.nodeX = 0
    test_op.nodeY = 200
    
    # Validate numeric parameters
    def validate_numeric_parameter(operator, param_name, value):
        """Validate a numeric parameter before setting"""
        if not operator or not hasattr(operator.par, param_name):
            return False, "Invalid operator or parameter"
        
        param = getattr(operator.par, param_name)
        
        # Check if it's a numeric parameter
        if not hasattr(param, 'min') or not hasattr(param, 'max'):
            return False, "Not a numeric parameter"
        
        # Validate value type
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return False, f"Value '{value}' is not numeric"
        
        # Check bounds
        if param.clampMin and numeric_value < param.min:
            return False, f"Value {numeric_value} is below minimum {param.min}"
        
        if param.clampMax and numeric_value > param.max:
            return False, f"Value {numeric_value} is above maximum {param.max}"
        
        return True, numeric_value
    
    # Test validation
    valid, result = validate_numeric_parameter(test_op, 'period', 10)
    print(f"Period validation: {valid}, {result}")
    
    valid, result = validate_numeric_parameter(test_op, 'period', -5)
    print(f"Negative period validation: {valid}, {result}")
    
    # Validate menu parameters
    def validate_menu_parameter(operator, param_name, value):
        """Validate a menu parameter before setting"""
        if not operator or not hasattr(operator.par, param_name):
            return False, "Invalid operator or parameter"
        
        param = getattr(operator.par, param_name)
        
        # Check if it's a menu parameter
        if not hasattr(param, 'menuNames'):
            return False, "Not a menu parameter"
        
        # Check if value is valid
        if isinstance(value, str):
            if value in param.menuNames:
                return True, value
            else:
                return False, f"'{value}' is not a valid option. Valid options: {param.menuNames}"
        elif isinstance(value, int):
            if 0 <= value < len(param.menuNames):
                return True, param.menuNames[value]
            else:
                return False, f"Index {value} is out of range"
        else:
            return False, "Value must be string or integer"
    
    # Test menu validation
    valid, result = validate_menu_parameter(test_op, 'type', 'sparse')
    print(f"\nMenu validation (valid): {valid}, {result}")
    
    valid, result = validate_menu_parameter(test_op, 'type', 'invalid_type')
    print(f"Menu validation (invalid): {valid}, {result}")
    
    # Validate file paths
    def validate_file_parameter(operator, param_name, file_path):
        """Validate a file path parameter"""
        import os
        
        if not operator or not hasattr(operator.par, param_name):
            return False, "Invalid operator or parameter"
        
        # Check if file exists (optional based on use case)
        if file_path and not os.path.exists(file_path):
            return False, f"File does not exist: {file_path}"
        
        # Check file extension if needed
        valid_extensions = ['.jpg', '.png', '.mp4', '.mov', '.tif']
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in valid_extensions:
                return False, f"Invalid file type: {ext}"
        
        return True, file_path
    
    # Create movie file in for testing
    movie = op('/project1').create(moviefileinTOP, 'validation_movie')
    movie.nodeX = 200
    movie.nodeY = 200
    
    # Test file validation
    valid, result = validate_file_parameter(movie, 'file', 'C:/test.mp4')
    print(f"\nFile validation: {valid}, {result}")
    
    return test_op, movie


# Safe Network Modifications
def safe_network_modifications():
    """Examples of safe network modification patterns"""
    
    # Safe operator deletion
    def safe_delete_operator(op_path):
        """Safely delete an operator and its connections"""
        try:
            operator = op(op_path)
            if not operator:
                print(f"Operator {op_path} not found")
                return False
            
            # Store connected operators for potential cleanup
            connected_inputs = []
            connected_outputs = []
            
            # Get connections
            for connector in operator.inputConnectors:
                connected_inputs.extend(connector.connections)
            
            for connector in operator.outputConnectors:
                connected_outputs.extend(list(connector.connections))
            
            # Destroy operator
            operator.destroy()
            print(f"Successfully deleted {op_path}")
            
            # Log orphaned connections
            if connected_outputs:
                print(f"  Orphaned outputs: {[c.owner.path for c in connected_outputs]}")
            
            return True
            
        except Exception as e:
            print(f"Error deleting operator: {e}")
            return False
    
    # Create test network
    source = op('/project1').create(noiseTOP, 'safe_source')
    process = op('/project1').create(blurTOP, 'safe_process')
    output = op('/project1').create(nullTOP, 'safe_output')
    
    # Connect them
    process.inputConnectors[0].connect(source)
    output.inputConnectors[0].connect(process)
    
    # Position them
    source.nodeX = 0
    source.nodeY = 400
    process.nodeX = 200
    process.nodeY = 400
    output.nodeX = 400
    output.nodeY = 400
    
    # Safe network rewiring
    def safe_rewire_network(old_op_path, new_op):
        """Safely replace an operator in a network"""
        try:
            old_op = op(old_op_path)
            if not old_op:
                return False, "Old operator not found"
            
            if not new_op:
                return False, "New operator is None"
            
            # Store connections
            input_connections = []
            output_connections = []
            
            # Get input connections
            for i, connector in enumerate(old_op.inputConnectors):
                for conn in connector.connections:
                    input_connections.append((conn, i))
            
            # Get output connections
            for connector in old_op.outputConnectors:
                for conn in connector.connections:
                    output_connections.append(conn)
            
            # Reconnect inputs to new operator
            for source, index in input_connections:
                if index < len(new_op.inputConnectors):
                    new_op.inputConnectors[index].connect(source)
            
            # Reconnect outputs from new operator
            for target in output_connections:
                # Find which input was connected
                for i, connector in enumerate(target.owner.inputConnectors):
                    if old_op in connector.connections:
                        connector.disconnect()
                        connector.connect(new_op)
                        break
            
            # Delete old operator
            old_op.destroy()
            
            return True, "Rewiring successful"
            
        except Exception as e:
            return False, f"Rewiring failed: {e}"
    
    # Create replacement operator
    new_process = op('/project1').create(levelTOP, 'safe_new_process')
    new_process.nodeX = 200
    new_process.nodeY = 500
    
    # Test rewiring
    # success, msg = safe_rewire_network('safe_process', new_process)
    # print(f"\nRewiring result: {msg}")
    
    # Safe batch operations
    def safe_batch_operation(operators, operation_func):
        """Safely perform batch operations with rollback"""
        completed = []
        
        try:
            for op_obj in operators:
                if op_obj:
                    operation_func(op_obj)
                    completed.append(op_obj)
            
            return True, completed
            
        except Exception as e:
            print(f"Batch operation failed: {e}")
            # Rollback could be implemented here
            return False, completed
    
    # Test batch operation
    def set_resolution(op_obj):
        if hasattr(op_obj.par, 'w') and hasattr(op_obj.par, 'h'):
            op_obj.par.w = 512
            op_obj.par.h = 512
    
    test_ops = [source, new_process, output]
    success, processed = safe_batch_operation(test_ops, set_resolution)
    print(f"\nBatch operation: {'Success' if success else 'Failed'}, processed {len(processed)} operators")
    
    return source, new_process, output


# Error Recovery Patterns
def error_recovery_patterns():
    """Examples of error recovery and fallback patterns"""
    
    # Retry pattern
    def retry_operation(func, max_attempts=3, delay=0.1):
        """Retry an operation multiple times"""
        import time
        
        for attempt in range(max_attempts):
            try:
                result = func()
                return True, result
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(delay)
                else:
                    return False, str(e)
    
    # Test retry
    attempt_count = 0
    def flaky_operation():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 2:
            raise Exception("Temporary failure")
        return "Success!"
    
    success, result = retry_operation(flaky_operation)
    print(f"Retry result: {success}, {result}")
    
    # Fallback pattern
    def create_with_fallback(parent, preferred_name, op_type):
        """Create operator with fallback naming"""
        base_name = preferred_name
        attempt = 0
        
        while attempt < 10:
            try:
                name = base_name if attempt == 0 else f"{base_name}_{attempt}"
                new_op = parent.create(op_type, name)
                print(f"Created operator with name: {name}")
                return new_op
            except Exception as e:
                attempt += 1
        
        print(f"Failed to create operator after {attempt} attempts")
        return None
    
    # Test fallback
    op1 = create_with_fallback(op('/project1'), 'fallback_test', noiseTOP)
    op2 = create_with_fallback(op('/project1'), 'fallback_test', noiseTOP)
    
    # State preservation
    class NetworkState:
        """Preserve and restore network state"""
        def __init__(self):
            self.state = {}
        
        def save_operator_state(self, operator):
            """Save operator parameters"""
            if not operator:
                return
            
            op_state = {
                'type': type(operator).__name__,
                'name': operator.name,
                'position': (operator.nodeX, operator.nodeY),
                'parameters': {}
            }
            
            # Save parameter values
            for par in operator.pars():
                try:
                    op_state['parameters'][par.name] = par.eval()
                except:
                    pass
            
            self.state[operator.path] = op_state
        
        def restore_operator_state(self, operator):
            """Restore operator parameters"""
            if not operator or operator.path not in self.state:
                return False
            
            op_state = self.state[operator.path]
            
            try:
                # Restore position
                operator.nodeX = op_state['position'][0]
                operator.nodeY = op_state['position'][1]
                
                # Restore parameters
                for par_name, value in op_state['parameters'].items():
                    if hasattr(operator.par, par_name):
                        try:
                            setattr(operator.par, par_name, value)
                        except:
                            pass
                
                return True
            except Exception as e:
                print(f"Failed to restore state: {e}")
                return False
    
    # Test state preservation
    state_manager = NetworkState()
    
    if op1:
        # Modify operator
        op1.par.period = 20
        op1.nodeX = 100
        
        # Save state
        state_manager.save_operator_state(op1)
        
        # Change values
        op1.par.period = 5
        op1.nodeX = 200
        
        # Restore state
        state_manager.restore_operator_state(op1)
        print(f"\nRestored state - Period: {op1.par.period}, X: {op1.nodeX}")
    
    return op1, op2


# Logging and Debugging
def logging_and_debugging():
    """Examples of logging and debugging patterns"""
    
    import datetime
    
    # Create debug logger
    class DebugLogger:
        """Simple debug logger for TouchDesigner"""
        def __init__(self, log_dat_name='debug_log'):
            self.log_dat = op('/project1').create(textDAT, log_dat_name)
            self.log_dat.nodeX = 0
            self.log_dat.nodeY = 800
            self.log_dat.clear()
            self.log_dat.text = "=== Debug Log Started ===\n"
        
        def log(self, message, level='INFO'):
            """Add log entry"""
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] [{level}] {message}\n"
            self.log_dat.text += log_entry
        
        def error(self, message):
            """Log error"""
            self.log(message, 'ERROR')
        
        def warning(self, message):
            """Log warning"""
            self.log(message, 'WARNING')
        
        def info(self, message):
            """Log info"""
            self.log(message, 'INFO')
    
    # Create logger
    logger = DebugLogger()
    
    # Debugging decorator
    def debug_operation(func):
        """Decorator to debug function calls"""
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            logger.info(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
            
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func_name} failed: {str(e)}")
                raise
        
        return wrapper
    
    # Test debugging
    @debug_operation
    def test_function(x, y):
        """Test function with debugging"""
        if y == 0:
            raise ValueError("Division by zero")
        return x / y
    
    # Run tests
    try:
        result1 = test_function(10, 2)
        result2 = test_function(10, 0)  # Will raise error
    except Exception as e:
        print(f"Caught error: {e}")
    
    # Performance monitoring
    def monitor_performance(func):
        """Monitor function performance"""
        import time
        
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info(f"{func.__name__} took {elapsed:.4f} seconds")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"{func.__name__} failed after {elapsed:.4f} seconds")
                raise
        
        return wrapper
    
    @monitor_performance
    def slow_operation():
        """Simulate slow operation"""
        import time
        time.sleep(0.1)
        return "Complete"
    
    # Test performance monitoring
    result = slow_operation()
    
    return logger.log_dat


# Main execution example
if __name__ == '__main__':
    print("Running error handling examples...\n")
    
    # Run all examples
    patterns = try_except_patterns()
    existence = operator_existence_checks()
    validation = parameter_validation()
    modifications = safe_network_modifications()
    recovery = error_recovery_patterns()
    logging = logging_and_debugging()
    
    print("\nAll error handling examples completed!")