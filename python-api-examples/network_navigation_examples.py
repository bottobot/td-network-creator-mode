"""
TouchDesigner Python API Examples - Network Navigation
This file demonstrates how to navigate and find operators in the network.
"""

# Finding Operators by Name
def find_operators_by_name():
    """Examples of finding operators by name"""
    
    # Create some test operators
    for i in range(5):
        noise = op('/project1').create(noiseTOP, f'nav_noise_{i}')
        noise.nodeX = i * 150
        noise.nodeY = 0
        
    for i in range(3):
        constant = op('/project1').create(constantTOP, f'nav_constant_{i}')
        constant.nodeX = i * 150
        constant.nodeY = -150
    
    # Find single operator by exact name
    found_op = op('nav_noise_2')
    if found_op:
        print(f"Found operator: {found_op.path}")
        found_op.par.seed = 999  # Modify to confirm we found it
    
    # Find operator with path
    found_op2 = op('/project1/nav_constant_1')
    if found_op2:
        print(f"Found operator with path: {found_op2.path}")
    
    # Find operators by pattern
    noise_ops = op('/project1').findChildren(name='nav_noise_*')
    print(f"Found {len(noise_ops)} noise operators")
    
    # Find operators by type
    all_tops = op('/project1').findChildren(type=TOP)
    print(f"Found {len(all_tops)} TOP operators")
    
    # Find operators by type and name pattern
    constant_ops = op('/project1').findChildren(type=constantTOP, name='nav_constant_*')
    print(f"Found {len(constant_ops)} constant operators")
    
    return noise_ops, constant_ops


# Parent/Child Traversal
def parent_child_traversal():
    """Examples of navigating parent/child relationships"""
    
    # Create nested structure
    parent_comp = op('/project1').create(containerCOMP, 'nav_parent')
    parent_comp.nodeX = 0
    parent_comp.nodeY = 200
    
    # Create children
    child1 = parent_comp.create(noiseTOP, 'child_noise')
    child2 = parent_comp.create(levelTOP, 'child_level')
    child3 = parent_comp.create(containerCOMP, 'child_container')
    
    # Create grandchildren
    grandchild1 = child3.create(constantTOP, 'grandchild_constant')
    grandchild2 = child3.create(circleTOP, 'grandchild_circle')
    
    # Navigate from child to parent
    current_op = grandchild1
    print(f"Current operator: {current_op.path}")
    print(f"Parent: {current_op.parent().path}")
    print(f"Grandparent: {current_op.parent().parent().path}")
    print(f"Root parent: {current_op.parent(3).path}")  # 3 levels up
    
    # Get all children
    all_children = parent_comp.children
    print(f"\nChildren of {parent_comp.name}:")
    for child in all_children:
        print(f"  - {child.name} ({child.OPType})")
    
    # Get children by type
    top_children = parent_comp.findChildren(type=TOP)
    print(f"\nTOP children: {[op.name for op in top_children]}")
    
    # Recursive search for all descendants
    def get_all_descendants(comp):
        """Recursively get all descendants of a COMP"""
        descendants = []
        for child in comp.children:
            descendants.append(child)
            if isinstance(child, COMP):
                descendants.extend(get_all_descendants(child))
        return descendants
    
    all_descendants = get_all_descendants(parent_comp)
    print(f"\nAll descendants: {[op.name for op in all_descendants]}")
    
    return parent_comp


# Operator Collections and Lists
def operator_collections():
    """Examples of working with operator collections"""
    
    # Create a set of operators
    operators = []
    for i in range(5):
        op_type = [noiseTOP, constantTOP, levelTOP, blurTOP, transformTOP][i]
        new_op = op('/project1').create(op_type, f'collection_{op_type.__name__}')
        new_op.nodeX = i * 150
        new_op.nodeY = 400
        operators.append(new_op)
    
    # Filter operators by type
    noise_ops = [op for op in operators if isinstance(op, noiseTOP)]
    print(f"Noise operators: {[op.name for op in noise_ops]}")
    
    # Sort operators by position
    sorted_by_x = sorted(operators, key=lambda op: op.nodeX)
    print(f"Operators sorted by X position: {[op.name for op in sorted_by_x]}")
    
    # Group operators by type
    from collections import defaultdict
    ops_by_type = defaultdict(list)
    for op_obj in operators:
        ops_by_type[op_obj.OPType].append(op_obj)
    
    print("\nOperators grouped by type:")
    for op_type, ops in ops_by_type.items():
        print(f"  {op_type}: {[op.name for op in ops]}")
    
    # Find operators matching criteria
    def find_ops_with_criteria(parent, criteria_func):
        """Find all operators matching a criteria function"""
        return [op for op in parent.children if criteria_func(op)]
    
    # Example: Find all operators with 'collection' in name and nodeX > 200
    matching_ops = find_ops_with_criteria(
        op('/project1'),
        lambda op: 'collection' in op.name and op.nodeX > 200
    )
    print(f"\nOperators with nodeX > 200: {[op.name for op in matching_ops]}")
    
    return operators


# Path Resolution
def path_resolution_examples():
    """Examples of resolving operator paths"""
    
    # Create test structure
    root = op('/project1').create(containerCOMP, 'path_root')
    level1 = root.create(containerCOMP, 'level1')
    level2 = level1.create(containerCOMP, 'level2')
    target = level2.create(noiseTOP, 'target_noise')
    
    # Absolute path
    abs_path = '/project1/path_root/level1/level2/target_noise'
    found_abs = op(abs_path)
    print(f"Found by absolute path: {found_abs.path if found_abs else 'Not found'}")
    
    # Relative paths from different contexts
    # From level2 perspective
    me.parent = level2  # Simulate being inside level2
    found_rel1 = op('target_noise')  # Direct child
    found_rel2 = op('../')  # Parent (level1)
    found_rel3 = op('../../')  # Grandparent (path_root)
    
    # Using op with different starting points
    # From level1
    found_from_level1 = level1.op('level2/target_noise')
    print(f"Found from level1: {found_from_level1.path if found_from_level1 else 'Not found'}")
    
    # Using shortnames
    target.shortcutName = 'mytarget'
    found_by_shortcut = op.mytarget
    print(f"Found by shortcut: {found_by_shortcut.path if found_by_shortcut else 'Not found'}")
    
    # Path utilities
    def get_relative_path(from_op, to_op):
        """Get relative path from one operator to another"""
        from_parts = from_op.path.split('/')
        to_parts = to_op.path.split('/')
        
        # Find common ancestor
        common_len = 0
        for i in range(min(len(from_parts), len(to_parts))):
            if from_parts[i] == to_parts[i]:
                common_len = i + 1
            else:
                break
        
        # Build relative path
        up_levels = len(from_parts) - common_len
        rel_path = '../' * up_levels
        rel_path += '/'.join(to_parts[common_len:])
        
        return rel_path
    
    # Test relative path
    rel_path = get_relative_path(level1, target)
    print(f"Relative path from {level1.name} to {target.name}: {rel_path}")
    
    return root


# Network Search Patterns
def network_search_patterns():
    """Advanced search patterns in the network"""
    
    # Create complex test network
    base = op('/project1').create(containerCOMP, 'search_base')
    
    # Create various operators with tags
    for i in range(10):
        if i < 3:
            op_obj = base.create(noiseTOP, f'generator_{i}')
            op_obj.tags.add('generator')
            op_obj.tags.add('source')
        elif i < 6:
            op_obj = base.create(levelTOP, f'filter_{i-3}')
            op_obj.tags.add('filter')
            op_obj.tags.add('effect')
        else:
            op_obj = base.create(compositeTOP, f'mixer_{i-6}')
            op_obj.tags.add('mixer')
            op_obj.tags.add('combine')
        
        op_obj.nodeX = (i % 5) * 150
        op_obj.nodeY = (i // 5) * -150
    
    # Search by tags
    generators = base.findChildren(tags=['generator'])
    print(f"Generators: {[op.name for op in generators]}")
    
    # Search by multiple tags (operators with both tags)
    source_filters = base.findChildren(tags=['source', 'filter'])  # This would need custom implementation
    
    # Custom search function
    def search_by_multiple_criteria(parent, **criteria):
        """Search operators by multiple criteria"""
        results = []
        for child in parent.children:
            match = True
            
            # Check name pattern
            if 'name_pattern' in criteria:
                import re
                if not re.match(criteria['name_pattern'], child.name):
                    match = False
            
            # Check type
            if 'op_type' in criteria:
                if not isinstance(child, criteria['op_type']):
                    match = False
            
            # Check tags
            if 'has_tags' in criteria:
                for tag in criteria['has_tags']:
                    if tag not in child.tags:
                        match = False
                        break
            
            # Check position
            if 'x_range' in criteria:
                min_x, max_x = criteria['x_range']
                if not (min_x <= child.nodeX <= max_x):
                    match = False
            
            if match:
                results.append(child)
                
        return results
    
    # Example searches
    results1 = search_by_multiple_criteria(
        base,
        name_pattern=r'generator_\d+',
        has_tags=['source']
    )
    print(f"\nGenerators with 'source' tag: {[op.name for op in results1]}")
    
    results2 = search_by_multiple_criteria(
        base,
        op_type=TOP,
        x_range=(100, 400)
    )
    print(f"TOPs in X range 100-400: {[op.name for op in results2]}")
    
    return base


# Navigation Utilities
def navigation_utilities():
    """Utility functions for network navigation"""
    
    # Create test network
    root = op('/project1').create(containerCOMP, 'nav_utils_root')
    
    # Create branching structure
    branch1 = root.create(containerCOMP, 'branch1')
    branch2 = root.create(containerCOMP, 'branch2')
    
    # Add operators to branches
    for i in range(3):
        b1_op = branch1.create(noiseTOP, f'b1_noise_{i}')
        b2_op = branch2.create(constantTOP, f'b2_const_{i}')
        
        # Connect them
        if i > 0:
            b1_op.inputConnectors[0].connect(branch1.children[i-1])
            b2_op.inputConnectors[0].connect(branch2.children[i-1])
    
    # Utility: Find common parent
    def find_common_parent(op1, op2):
        """Find the common parent of two operators"""
        parents1 = []
        current = op1
        while current:
            parents1.append(current)
            current = current.parent() if hasattr(current.parent(), 'name') else None
        
        current = op2
        while current:
            if current in parents1:
                return current
            current = current.parent() if hasattr(current.parent(), 'name') else None
        
        return None
    
    # Test common parent
    op1 = branch1.children[0]
    op2 = branch2.children[0]
    common = find_common_parent(op1, op2)
    print(f"Common parent of {op1.name} and {op2.name}: {common.name if common else 'None'}")
    
    # Utility: Get network depth
    def get_network_depth(comp):
        """Get the maximum depth of a network"""
        if not isinstance(comp, COMP) or not comp.children:
            return 0
        
        max_depth = 0
        for child in comp.children:
            if isinstance(child, COMP):
                child_depth = get_network_depth(child)
                max_depth = max(max_depth, child_depth + 1)
        
        return max_depth
    
    depth = get_network_depth(root)
    print(f"Network depth: {depth}")
    
    # Utility: Find all paths between operators
    def find_paths(start_op, end_op, visited=None):
        """Find all paths between two operators"""
        if visited is None:
            visited = set()
        
        if start_op == end_op:
            return [[start_op]]
        
        visited.add(start_op)
        paths = []
        
        # Check all outputs
        for connector in start_op.outputConnectors:
            for connection in connector.connections:
                next_op = connection.owner
                if next_op not in visited:
                    sub_paths = find_paths(next_op, end_op, visited.copy())
                    for path in sub_paths:
                        paths.append([start_op] + path)
        
        return paths
    
    # Create connection for path finding
    cross_connect = root.create(nullTOP, 'cross_connect')
    cross_connect.inputConnectors[0].connect(branch1.children[-1])
    branch2.children[-1].inputConnectors[0].connect(cross_connect)
    
    # Find paths
    paths = find_paths(branch1.children[0], branch2.children[-1])
    print(f"\nPaths found: {len(paths)}")
    for i, path in enumerate(paths):
        print(f"  Path {i+1}: {' -> '.join([op.name for op in path])}")
    
    return root


# Performance Considerations
def performance_navigation():
    """Examples showing performance considerations when navigating"""
    
    # Create large network for testing
    container = op('/project1').create(containerCOMP, 'perf_container')
    
    # Bad practice: Multiple lookups
    import time
    
    # Create many operators
    for i in range(100):
        container.create(noiseTOP, f'perf_noise_{i}')
    
    # Inefficient: Multiple op() calls
    start_time = time.time()
    for i in range(100):
        op_found = op(f'/project1/perf_container/perf_noise_{i}')
        if op_found:
            op_found.par.seed = i
    inefficient_time = time.time() - start_time
    
    # Efficient: Cache parent and use relative lookup
    start_time = time.time()
    parent = op('/project1/perf_container')
    for i in range(100):
        op_found = parent.op(f'perf_noise_{i}')
        if op_found:
            op_found.par.seed = i * 2
    efficient_time = time.time() - start_time
    
    # Most efficient: Direct children access
    start_time = time.time()
    for child in container.children:
        if child.name.startswith('perf_noise_'):
            child.par.seed = int(child.name.split('_')[-1]) * 3
    direct_time = time.time() - start_time
    
    print(f"Performance comparison:")
    print(f"  Inefficient (multiple op() calls): {inefficient_time:.4f}s")
    print(f"  Efficient (cached parent): {efficient_time:.4f}s")
    print(f"  Most efficient (direct children): {direct_time:.4f}s")
    
    # Caching frequently accessed operators
    class NetworkCache:
        """Cache for frequently accessed operators"""
        def __init__(self):
            self._cache = {}
        
        def get(self, path):
            if path not in self._cache:
                self._cache[path] = op(path)
            return self._cache[path]
        
        def clear(self):
            self._cache.clear()
    
    # Use cache
    cache = NetworkCache()
    cached_op = cache.get('/project1/perf_container')
    
    return container


# Global Network Operations
def global_network_operations():
    """Examples of operations across the entire network"""
    
    # Get all operators of specific type in project
    all_noise_tops = root.findChildren(type=noiseTOP, depth=9999)
    print(f"Total Noise TOPs in project: {len(all_noise_tops)}")
    
    # Find all operators with errors
    def find_operators_with_errors(search_root):
        """Find all operators that have errors"""
        error_ops = []
        for op_obj in search_root.findChildren(depth=9999):
            if op_obj.errors():
                error_ops.append(op_obj)
        return error_ops
    
    # Find all operators with specific parameter values
    def find_ops_by_parameter(search_root, param_name, param_value):
        """Find operators with specific parameter value"""
        matching_ops = []
        for op_obj in search_root.findChildren(depth=9999):
            if hasattr(op_obj.par, param_name):
                if op_obj.par[param_name].eval() == param_value:
                    matching_ops.append(op_obj)
        return matching_ops
    
    # Example: Find all TOPs with resolution 1920x1080
    def find_hd_tops(search_root):
        """Find all TOPs with HD resolution"""
        hd_tops = []
        for op_obj in search_root.findChildren(type=TOP, depth=9999):
            if hasattr(op_obj.par, 'w') and hasattr(op_obj.par, 'h'):
                if op_obj.par.w.eval() == 1920 and op_obj.par.h.eval() == 1080:
                    hd_tops.append(op_obj)
        return hd_tops
    
    # Network statistics
    def get_network_stats(search_root):
        """Get statistics about the network"""
        stats = {
            'total_operators': 0,
            'operators_by_type': defaultdict(int),
            'max_depth': 0,
            'containers': 0
        }
        
        def analyze_comp(comp, depth=0):
            stats['max_depth'] = max(stats['max_depth'], depth)
            
            for child in comp.children:
                stats['total_operators'] += 1
                stats['operators_by_type'][child.OPType] += 1
                
                if isinstance(child, COMP):
                    stats['containers'] += 1
                    analyze_comp(child, depth + 1)
        
        analyze_comp(search_root)
        return stats
    
    # Get stats for current project
    stats = get_network_stats(root)
    print("\nNetwork Statistics:")
    for key, value in stats.items():
        if key == 'operators_by_type':
            print(f"  Operators by type:")
            for op_type, count in value.items():
                print(f"    {op_type}: {count}")
        else:
            print(f"  {key}: {value}")
    
    return stats


# Main execution example
if __name__ == '__main__':
    from collections import defaultdict
    
    # Get root for examples
    root = op('/project1')
    
    # Run all examples
    name_search = find_operators_by_name()
    traversal = parent_child_traversal()
    collections = operator_collections()
    paths = path_resolution_examples()
    search = network_search_patterns()
    utils = navigation_utilities()
    perf = performance_navigation()
    global_ops = global_network_operations()
    
    print("\nAll network navigation examples completed!")