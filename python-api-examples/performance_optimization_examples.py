"""
TouchDesigner Python API Examples - Performance Optimization
This file demonstrates techniques for optimizing performance in TouchDesigner Python scripts.
"""

import time

# Batch Operations
def batch_operations_examples():
    """Examples of efficient batch operations"""
    
    # Inefficient: Individual operations
    def inefficient_creation():
        """Create operators one by one (slow)"""
        start_time = time.time()
        operators = []
        
        for i in range(20):
            op_obj = op('/project1').create(constantTOP, f'inefficient_{i}')
            op_obj.par.colorr = i / 20
            op_obj.par.colorg = 0.5
            op_obj.par.colorb = 1 - (i / 20)
            op_obj.nodeX = i * 50
            op_obj.nodeY = 0
            operators.append(op_obj)
        
        elapsed = time.time() - start_time
        print(f"Inefficient creation took: {elapsed:.4f} seconds")
        
        # Cleanup
        for op_obj in operators:
            op_obj.destroy()
        
        return elapsed
    
    # Efficient: Batch operations
    def efficient_creation():
        """Create operators with optimized batch operations"""
        start_time = time.time()
        
        # Pre-calculate values
        positions = [(i * 50, 100) for i in range(20)]
        colors = [(i / 20, 0.5, 1 - (i / 20)) for i in range(20)]
        
        # Create all operators first
        operators = []
        for i in range(20):
            op_obj = op('/project1').create(constantTOP, f'efficient_{i}')
            operators.append(op_obj)
        
        # Then set parameters in batch
        for i, op_obj in enumerate(operators):
            op_obj.nodeX, op_obj.nodeY = positions[i]
            op_obj.par.colorr, op_obj.par.colorg, op_obj.par.colorb = colors[i]
        
        elapsed = time.time() - start_time
        print(f"Efficient creation took: {elapsed:.4f} seconds")
        
        # Cleanup
        for op_obj in operators:
            op_obj.destroy()
        
        return elapsed
    
    # Compare methods
    inefficient_time = inefficient_creation()
    efficient_time = efficient_creation()
    print(f"Speed improvement: {inefficient_time / efficient_time:.2f}x faster")
    
    # Batch parameter updates
    def batch_parameter_update():
        """Efficiently update parameters on multiple operators"""
        # Create test operators
        test_ops = []
        for i in range(10):
            noise = op('/project1').create(noiseTOP, f'batch_noise_{i}')
            noise.nodeX = i * 100
            noise.nodeY = 300
            test_ops.append(noise)
        
        # Inefficient: Multiple lookups and individual sets
        start_time = time.time()
        for i in range(10):
            op_obj = op(f'/project1/batch_noise_{i}')
            if op_obj:
                op_obj.par.period = 5
                op_obj.par.amplitude = 1
                op_obj.par.offset = 0
        inefficient_time = time.time() - start_time
        
        # Efficient: Direct access and batch updates
        start_time = time.time()
        for op_obj in test_ops:
            op_obj.par.period = 10
            op_obj.par.amplitude = 2
            op_obj.par.offset = 0.5
        efficient_time = time.time() - start_time
        
        print(f"\nParameter update - Inefficient: {inefficient_time:.4f}s, Efficient: {efficient_time:.4f}s")
        
        # Cleanup
        for op_obj in test_ops:
            op_obj.destroy()
    
    batch_parameter_update()
    
    return True


# Cooking Control
def cooking_control_examples():
    """Examples of controlling operator cooking for performance"""
    
    # Create test network
    source = op('/project1').create(noiseTOP, 'cook_source')
    source.nodeX = 0
    source.nodeY = 500
    
    # Create processing chain
    processors = []
    prev = source
    for i in range(5):
        proc = op('/project1').create(blurTOP, f'cook_processor_{i}')
        proc.nodeX = (i + 1) * 150
        proc.nodeY = 500
        proc.par.sizex = 10 + i * 5
        proc.inputConnectors[0].connect(prev)
        processors.append(proc)
        prev = proc
    
    # Disable cooking during setup
    def setup_with_cooking_disabled():
        """Setup network with cooking disabled"""
        start_time = time.time()
        
        # Disable cooking
        for op_obj in processors:
            op_obj.allowCooking = False
        
        # Make changes
        for i, op_obj in enumerate(processors):
            op_obj.par.sizex = 20 + i * 10
            op_obj.par.sizey = 20 + i * 10
            op_obj.par.filter = 'gaussian'
        
        # Re-enable cooking
        for op_obj in processors:
            op_obj.allowCooking = True
        
        # Force cook once
        processors[-1].cook(force=True)
        
        elapsed = time.time() - start_time
        print(f"Setup with cooking disabled: {elapsed:.4f} seconds")
        return elapsed
    
    # Setup without cooking control
    def setup_with_cooking_enabled():
        """Setup network with cooking enabled (default)"""
        start_time = time.time()
        
        # Make changes (cooking happens after each change)
        for i, op_obj in enumerate(processors):
            op_obj.par.sizex = 30 + i * 10
            op_obj.par.sizey = 30 + i * 10
            op_obj.par.filter = 'box'
        
        elapsed = time.time() - start_time
        print(f"Setup with cooking enabled: {elapsed:.4f} seconds")
        return elapsed
    
    # Compare methods
    disabled_time = setup_with_cooking_disabled()
    enabled_time = setup_with_cooking_enabled()
    
    # Selective cooking
    def selective_cooking_example():
        """Example of selective cooking for optimization"""
        # Create viewer-dependent network
        viewer = op('/project1').create(nullTOP, 'cook_viewer')
        viewer.nodeX = 1000
        viewer.nodeY = 500
        viewer.viewer = True  # Enable viewer
        
        # Create multiple branches
        branches = []
        for i in range(3):
            branch = op('/project1').create(levelTOP, f'cook_branch_{i}')
            branch.nodeX = 800
            branch.nodeY = 400 + i * 100
            branch.inputConnectors[0].connect(processors[-1])
            branch.par.brightness1 = 0.5 + i * 0.25
            branches.append(branch)
        
        # Only connect one branch to viewer
        viewer.inputConnectors[0].connect(branches[0])
        
        # Check cooking status
        print("\nCooking status:")
        for i, branch in enumerate(branches):
            print(f"  Branch {i}: {'Cooking' if branch.isCooking else 'Not cooking'}")
        
        # Cleanup
        viewer.destroy()
        for branch in branches:
            branch.destroy()
    
    selective_cooking_example()
    
    # Cleanup
    source.destroy()
    for op_obj in processors:
        op_obj.destroy()
    
    return True


# Memory Management
def memory_management_examples():
    """Examples of memory-efficient operations"""
    
    # Efficient data structures
    def efficient_data_storage():
        """Use efficient data structures for large datasets"""
        
        # Create large table
        table = op('/project1').create(tableDAT, 'memory_table')
        table.nodeX = 0
        table.nodeY = 800
        
        # Inefficient: Store as individual strings
        start_time = time.time()
        inefficient_data = []
        for i in range(1000):
            row = [str(i), str(i * 2), str(i * 3), str(i * 4)]
            inefficient_data.append(row)
        inefficient_time = time.time() - start_time
        
        # Efficient: Store as numpy arrays (if using numpy)
        start_time = time.time()
        # Simulate efficient storage
        efficient_data = []
        for i in range(1000):
            row = (i, i * 2, i * 3, i * 4)  # Tuples are more memory efficient
            efficient_data.append(row)
        efficient_time = time.time() - start_time
        
        print(f"Data storage - Inefficient: {inefficient_time:.4f}s, Efficient: {efficient_time:.4f}s")
        
        # Clear table data periodically
        table.clear()
        table.destroy()
        
        return efficient_data
    
    # Operator pooling
    class OperatorPool:
        """Pool of reusable operators to avoid creation/destruction overhead"""
        
        def __init__(self, op_type, pool_size=10, name_prefix='pool'):
            self.op_type = op_type
            self.pool_size = pool_size
            self.name_prefix = name_prefix
            self.available = []
            self.in_use = []
            
            # Pre-create operators
            for i in range(pool_size):
                op_obj = op('/project1').create(op_type, f'{name_prefix}_{i}')
                op_obj.nodeX = -1000  # Hide off-screen
                op_obj.nodeY = -1000
                op_obj.bypass = True
                self.available.append(op_obj)
        
        def acquire(self):
            """Get an operator from the pool"""
            if self.available:
                op_obj = self.available.pop()
                self.in_use.append(op_obj)
                op_obj.bypass = False
                return op_obj
            return None
        
        def release(self, op_obj):
            """Return an operator to the pool"""
            if op_obj in self.in_use:
                self.in_use.remove(op_obj)
                self.available.append(op_obj)
                op_obj.bypass = True
                op_obj.nodeX = -1000
                op_obj.nodeY = -1000
                # Reset parameters to defaults
                self.reset_operator(op_obj)
        
        def reset_operator(self, op_obj):
            """Reset operator to default state"""
            # Reset common parameters
            if hasattr(op_obj.par, 'seed'):
                op_obj.par.seed = 0
            if hasattr(op_obj.par, 'period'):
                op_obj.par.period = 1
        
        def cleanup(self):
            """Destroy all pooled operators"""
            for op_obj in self.available + self.in_use:
                op_obj.destroy()
    
    # Test operator pool
    pool = OperatorPool(noiseTOP, pool_size=5)
    
    # Use operators from pool
    active_ops = []
    for i in range(3):
        op_obj = pool.acquire()
        if op_obj:
            op_obj.nodeX = i * 150
            op_obj.nodeY = 1000
            op_obj.par.period = 5 + i
            active_ops.append(op_obj)
    
    print(f"\nOperator pool - Available: {len(pool.available)}, In use: {len(pool.in_use)}")
    
    # Return operators to pool
    for op_obj in active_ops:
        pool.release(op_obj)
    
    print(f"After release - Available: {len(pool.available)}, In use: {len(pool.in_use)}")
    
    # Cleanup
    pool.cleanup()
    
    # Memory-efficient parameter storage
    def compress_parameter_data():
        """Store parameter data efficiently"""
        
        # Create test operators
        test_ops = []
        for i in range(10):
            const = op('/project1').create(constantTOP, f'memory_const_{i}')
            const.nodeX = i * 50
            const.nodeY = 1200
            test_ops.append(const)
        
        # Inefficient: Store all parameter objects
        inefficient_storage = {}
        for op_obj in test_ops:
            inefficient_storage[op_obj.name] = {
                'pars': dict([(p.name, p) for p in op_obj.pars()])
            }
        
        # Efficient: Store only values
        efficient_storage = {}
        for op_obj in test_ops:
            efficient_storage[op_obj.name] = {
                'color': (op_obj.par.colorr.eval(), 
                         op_obj.par.colorg.eval(), 
                         op_obj.par.colorb.eval()),
                'alpha': op_obj.par.alpha.eval()
            }
        
        print(f"\nParameter storage comparison:")
        print(f"  Inefficient: Storing parameter objects")
        print(f"  Efficient: Storing only values")
        
        # Cleanup
        for op_obj in test_ops:
            op_obj.destroy()
        
        return efficient_storage
    
    efficient_data = efficient_data_storage()
    compressed_params = compress_parameter_data()
    
    return True


# Efficient Loops
def efficient_loop_examples():
    """Examples of efficient loop patterns"""
    
    # List comprehensions vs loops
    def compare_loop_methods():
        """Compare different loop methods"""
        
        # Create test data
        test_ops = []
        for i in range(50):
            noise = op('/project1').create(noiseTOP, f'loop_test_{i}')
            noise.nodeX = (i % 10) * 100
            noise.nodeY = 1400 + (i // 10) * 100
            test_ops.append(noise)
        
        # Method 1: Traditional loop
        start_time = time.time()
        results1 = []
        for op_obj in test_ops:
            if op_obj.par.period.eval() > 0:
                results1.append(op_obj.name)
        loop_time = time.time() - start_time
        
        # Method 2: List comprehension
        start_time = time.time()
        results2 = [op_obj.name for op_obj in test_ops if op_obj.par.period.eval() > 0]
        comprehension_time = time.time() - start_time
        
        # Method 3: Generator expression (memory efficient)
        start_time = time.time()
        results3 = list(op_obj.name for op_obj in test_ops if op_obj.par.period.eval() > 0)
        generator_time = time.time() - start_time
        
        print(f"Loop performance comparison:")
        print(f"  Traditional loop: {loop_time:.6f}s")
        print(f"  List comprehension: {comprehension_time:.6f}s")
        print(f"  Generator expression: {generator_time:.6f}s")
        
        # Cleanup
        for op_obj in test_ops:
            op_obj.destroy()
    
    compare_loop_methods()
    
    # Early exit optimization
    def early_exit_example():
        """Use early exit to optimize loops"""
        
        # Create test network
        containers = []
        for i in range(10):
            cont = op('/project1').create(containerCOMP, f'exit_container_{i}')
            cont.nodeX = i * 150
            cont.nodeY = 2000
            
            # Add children
            for j in range(5):
                child = cont.create(constantTOP, f'child_{j}')
                child.par.name = f'data_{i}_{j}'
            
            containers.append(cont)
        
        # Find specific operator with early exit
        def find_operator_optimized(target_name):
            """Find operator with early exit"""
            start_time = time.time()
            
            for container in containers:
                for child in container.children:
                    if child.par.name.eval() == target_name:
                        elapsed = time.time() - start_time
                        print(f"Found {target_name} in {elapsed:.6f}s")
                        return child
            
            return None
        
        # Test search
        result = find_operator_optimized('data_5_3')
        
        # Cleanup
        for cont in containers:
            cont.destroy()
    
    early_exit_example()
    
    # Cached iterations
    class CachedIterator:
        """Iterator with caching for repeated access"""
        
        def __init__(self, parent_op):
            self.parent_op = parent_op
            self._cache = None
            self._cache_time = 0
            self.cache_duration = 1.0  # Cache for 1 second
        
        def get_children(self):
            """Get children with caching"""
            current_time = time.time()
            
            if (self._cache is None or 
                current_time - self._cache_time > self.cache_duration):
                # Refresh cache
                self._cache = list(self.parent_op.children)
                self._cache_time = current_time
            
            return self._cache
        
        def invalidate(self):
            """Invalidate cache"""
            self._cache = None
    
    # Test cached iterator
    test_parent = op('/project1').create(containerCOMP, 'cache_test_parent')
    for i in range(20):
        test_parent.create(textDAT, f'cache_child_{i}')
    
    iterator = CachedIterator(test_parent)
    
    # First access (builds cache)
    start_time = time.time()
    children1 = iterator.get_children()
    first_time = time.time() - start_time
    
    # Second access (uses cache)
    start_time = time.time()
    children2 = iterator.get_children()
    cached_time = time.time() - start_time
    
    print(f"\nCached iteration:")
    print(f"  First access: {first_time:.6f}s")
    print(f"  Cached access: {cached_time:.6f}s")
    print(f"  Speed improvement: {first_time / cached_time:.2f}x")
    
    # Cleanup
    test_parent.destroy()
    
    return True


# Network Optimization Patterns
def network_optimization_patterns():
    """Examples of network-level optimizations"""
    
    # Minimize operator count
    def optimize_operator_count():
        """Reduce operator count for better performance"""
        
        # Inefficient: Many single-purpose operators
        print("\nCreating inefficient network...")
        inefficient_ops = []
        
        # Create separate operators for each operation
        source1 = op('/project1').create(noiseTOP, 'inefficient_source')
        source1.nodeX = 0
        source1.nodeY = 2200
        inefficient_ops.append(source1)
        
        # Separate brightness adjustment
        bright = op('/project1').create(levelTOP, 'inefficient_bright')
        bright.nodeX = 150
        bright.nodeY = 2200
        bright.par.brightness1 = 1.5
        bright.inputConnectors[0].connect(source1)
        inefficient_ops.append(bright)
        
        # Separate contrast adjustment
        contrast = op('/project1').create(levelTOP, 'inefficient_contrast')
        contrast.nodeX = 300
        contrast.nodeY = 2200
        contrast.par.contrast = 1.2
        contrast.inputConnectors[0].connect(bright)
        inefficient_ops.append(contrast)
        
        # Separate gamma adjustment
        gamma = op('/project1').create(levelTOP, 'inefficient_gamma')
        gamma.nodeX = 450
        gamma.nodeY = 2200
        gamma.par.gamma1 = 0.8
        gamma.inputConnectors[0].connect(contrast)
        inefficient_ops.append(gamma)
        
        print(f"Inefficient network: {len(inefficient_ops)} operators")
        
        # Efficient: Combined operations
        print("\nCreating efficient network...")
        efficient_ops = []
        
        # Same source
        source2 = op('/project1').create(noiseTOP, 'efficient_source')
        source2.nodeX = 0
        source2.nodeY = 2400
        efficient_ops.append(source2)
        
        # Combined adjustments in one operator
        combined = op('/project1').create(levelTOP, 'efficient_combined')
        combined.nodeX = 150
        combined.nodeY = 2400
        combined.par.brightness1 = 1.5
        combined.par.contrast = 1.2
        combined.par.gamma1 = 0.8
        combined.inputConnectors[0].connect(source2)
        efficient_ops.append(combined)
        
        print(f"Efficient network: {len(efficient_ops)} operators")
        
        # Cleanup
        for op_obj in inefficient_ops + efficient_ops:
            op_obj.destroy()
    
    optimize_operator_count()
    
    # Resolution optimization
    def resolution_optimization():
        """Optimize resolution for performance"""
        
        # Create high-res source
        source = op('/project1').create(noiseTOP, 'res_source')
        source.par.resolutionw = 4096
        source.par.resolutionh = 4096
        source.nodeX = 0
        source.nodeY = 2600
        
        # Process at lower resolution
        downres = op('/project1').create(resolutionTOP, 'res_downscale')
        downres.par.resolutionw = 512
        downres.par.resolutionh = 512
        downres.par.outputresolution = 'custom'
        downres.nodeX = 150
        downres.nodeY = 2600
        downres.inputConnectors[0].connect(source)
        
        # Heavy processing at low res
        blur = op('/project1').create(blurTOP, 'res_blur')
        blur.par.sizex = 50
        blur.par.sizey = 50
        blur.nodeX = 300
        blur.nodeY = 2600
        blur.inputConnectors[0].connect(downres)
        
        # Scale back up if needed
        upres = op('/project1').create(resolutionTOP, 'res_upscale')
        upres.par.outputresolution = 'inputresolution'
        upres.par.inputresolution = 0  # Use first input
        upres.nodeX = 450
        upres.nodeY = 2600
        upres.inputConnectors[0].connect(blur)
        upres.inputConnectors[1].connect(source)  # Reference for resolution
        
        print("\nResolution optimization chain created")
        print(f"  Source: {source.par.resolutionw}x{source.par.resolutionh}")
        print(f"  Processing: {downres.par.resolutionw}x{downres.par.resolutionh}")
        print("  Output: Matched to source")
        
        # Cleanup
        source.destroy()
        downres.destroy()
        blur.destroy()
        upres.destroy()
    
    resolution_optimization()
    
    # Selective updates
    def selective_update_pattern():
        """Update only what's necessary"""
        
        # Create container with custom parameters
        container = op('/project1').create(containerCOMP, 'selective_container')
        container.nodeX = 0
        container.nodeY = 2800
        
        # Add custom page
        page = container.appendCustomPage('Settings')
        update_trigger = page.appendPulse('UpdateNetwork', label='Update Network')[0]
        auto_update = page.appendToggle('AutoUpdate', label='Auto Update')[0]
        auto_update.default = False
        
        # Create internal network
        internal_noise = container.create(noiseTOP, 'internal_noise')
        internal_transform = container.create(transformTOP, 'internal_transform')
        internal_transform.inputConnectors[0].connect(internal_noise)
        
        # Create Execute DAT for selective updates
        execute = container.create(executeDAT, 'update_controller')
        execute.par.executeonstart = True
        
        execute_code = '''
def onPulse(par):
    if par.name == 'UpdateNetwork':
        # Perform expensive update only when triggered
        noise = op('internal_noise')
        transform = op('internal_transform')
        
        import random
        noise.par.seed = random.randint(0, 1000)
        transform.par.rotate = random.uniform(0, 360)
        
        print("Network updated manually")
    return

def onValueChange(par):
    if par.name == 'AutoUpdate' and par.eval():
        print("Auto-update enabled - performance may decrease")
    return
'''
        execute.par.text = execute_code
        
        print("\nSelective update pattern created")
        print("  Use UpdateNetwork pulse to trigger updates")
        print("  Toggle AutoUpdate for continuous updates")
        
        return container
    
    selective_container = selective_update_pattern()
    
    return selective_container


# Profiling and Measurement
def profiling_and_measurement():
    """Examples of profiling and performance measurement"""
    
    # Performance profiler class
    class PerformanceProfiler:
        """Profile TouchDesigner operations"""
        
        def __init__(self):
            self.measurements = {}
            self.log_dat = op('/project1').create(tableDAT, 'performance_log')
            self.log_dat.clear()
            self.log_dat.appendRow(['Operation', 'Time (ms)', 'Count', 'Avg (ms)'])
            self.log_dat.nodeX = 0
            self.log_dat.nodeY = 3000
        
        def measure(self, operation_name):
            """Decorator to measure operation time"""
            def decorator(func):
                def wrapper(*args, **kwargs):
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    elapsed = (time.time() - start_time) * 1000  # Convert to ms
                    
                    # Update measurements
                    if operation_name not in self.measurements:
                        self.measurements[operation_name] = {
                            'total_time': 0,
                            'count': 0,
                            'times': []
                        }
                    
                    self.measurements[operation_name]['total_time'] += elapsed
                    self.measurements[operation_name]['count'] += 1
                    self.measurements[operation_name]['times'].append(elapsed)
                    
                    # Update log
                    self.update_log()
                    
                    return result
                return wrapper
            return decorator
        
        def update_log(self):
            """Update the log table"""
            self.log_dat.clear()
            self.log_dat.appendRow(['Operation', 'Time (ms)', 'Count', 'Avg (ms)'])
            
            for op_name, data in self.measurements.items():
                avg_time = data['total_time'] / data['count']
                self.log_dat.appendRow([
                    op_name,
                    f"{data['total_time']:.2f}",
                    str(data['count']),
                    f"{avg_time:.2f}"
                ])
    
    # Create profiler
    profiler = PerformanceProfiler()
    
    # Test operations with profiling
    @profiler.measure('Create Noise TOP')
    def create_noise_test():
        op_obj = op('/project1').create(noiseTOP, 'profile_noise_test')
        op_obj.destroy()
        return True
    
    @profiler.measure('Parameter Update')
    def update_parameters_test():
        op_obj = op('/project1').create(constantTOP, 'profile_param_test')
        for i in range(10):
            op_obj.par.colorr = i / 10
            op_obj.par.colorg = 0.5
            op_obj.par.colorb = 1 - (i / 10)
        op_obj.destroy()
        return True
    
    @profiler.measure('Network Creation')
    def create_network_test():
        ops = []
        for i in range(5):
            op_obj = op('/project1').create(levelTOP, f'profile_level_{i}')
            ops.append(op_obj)
        
        for i in range(1, 5):
            ops[i].inputConnectors[0].connect(ops[i-1])
        
        for op_obj in ops:
            op_obj.destroy()
        return True
    
    # Run tests multiple times
    print("\nRunning performance tests...")
    for i in range(5):
        create_noise_test()
        update_parameters_test()
        create_network_test()
    
    print("Performance measurements logged to table")
    
    # Cook time analysis
    def analyze_cook_times():
        """Analyze operator cook times"""
        
        # Create test network
        source = op('/project1').create(noiseTOP, 'cook_analysis_source')
        source.nodeX = 300
        source.nodeY = 3000
        
        # Create chain with different complexities
        blur1 = op('/project1').create(blurTOP, 'cook_analysis_blur1')
        blur1.par.sizex = 5
        blur1.nodeX = 450
        blur1.nodeY = 3000
        blur1.inputConnectors[0].connect(source)
        
        blur2 = op('/project1').create(blurTOP, 'cook_analysis_blur2')
        blur2.par.sizex = 20
        blur2.nodeX = 600
        blur2.nodeY = 3000
        blur2.inputConnectors[0].connect(blur1)
        
        # Create Info CHOP to monitor cook times
        info = op('/project1').create(infoCHOP, 'cook_time_info')
        info.par.op = '../cook_analysis_*'
        info.par.cooktime = True
        info.nodeX = 750
        info.nodeY = 3000
        
        print("\nCook time analysis network created")
        print("  Monitor cook times with Info CHOP")
        
        return source, blur1, blur2, info
    
    cook_analysis = analyze_cook_times()
    
    return profiler, cook_analysis


# Main execution example
if __name__ == '__main__':
    print("Running performance optimization examples...\n")
    
    # Run all examples
    batch = batch_operations_examples()
    cooking = cooking_control_examples()
    memory = memory_management_examples()
    loops = efficient_loop_examples()
    network = network_optimization_patterns()
    profiling = profiling_and_measurement()
    
    print("\nAll performance optimization examples completed!")
    print("\nKey takeaways:")
    print("- Batch operations are significantly faster than individual operations")
    print("- Control cooking to avoid unnecessary calculations")
    print("- Use efficient data structures and operator pooling")
    print("- Optimize loops with comprehensions and early exits")
    print("- Minimize operator count and optimize resolution")
    