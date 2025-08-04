// Voronoi/Cellular Pattern Generation Shader for TouchDesigner
// Creates Voronoi diagrams and cellular patterns with various styles
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture (optional)
uniform vec2 uTDOutputInfo;        // Output resolution
uniform float uTDTime;             // Time in seconds

// Custom uniforms for Voronoi control
uniform float cellSize = 0.1;       // Size of cells (0.01-1.0)
uniform float randomness = 1.0;     // Cell position randomness (0-1)
uniform float speed = 0.0;          // Animation speed (0-5)
uniform int cellCount = 5;          // Grid resolution (2-20)
uniform int displayMode = 0;        // 0: Distance field, 1: Cell colors, 2: Borders, 3: Combined
uniform float borderWidth = 0.02;   // Width of cell borders (0-0.1)
uniform vec3 borderColor = vec3(0.0); // Border color
uniform float distancePower = 1.0;  // Distance field power (0.5-3.0)
uniform int distanceType = 0;       // 0: Euclidean, 1: Manhattan, 2: Chebyshev
uniform float colorVariation = 0.5; // Random color variation (0-1)

// Output color
out vec4 fragColor;

// Hash function for randomization
vec2 hash2(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)),
             dot(p, vec2(269.5, 183.3)));
    return fract(sin(p) * 43758.5453);
}

// 3D hash for color generation
vec3 hash3(vec2 p) {
    vec3 q = vec3(dot(p, vec2(127.1, 311.7)),
                  dot(p, vec2(269.5, 183.3)),
                  dot(p, vec2(419.2, 371.9)));
    return fract(sin(q) * 43758.5453);
}

// Distance functions
float getDistance(vec2 a, vec2 b, int type) {
    vec2 d = abs(a - b);
    if (type == 0) {
        // Euclidean distance
        return length(d);
    } else if (type == 1) {
        // Manhattan distance
        return d.x + d.y;
    } else {
        // Chebyshev distance
        return max(d.x, d.y);
    }
}

// Voronoi function returning distance to closest and second closest points
vec4 voronoi(vec2 p, float time) {
    vec2 n = floor(p);
    vec2 f = fract(p);
    
    float minDist = 10.0;
    float secondMinDist = 10.0;
    vec2 closestCell = vec2(0.0);
    vec2 secondClosestCell = vec2(0.0);
    
    // Check neighboring cells
    for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
            vec2 neighbor = vec2(float(i), float(j));
            vec2 cellPos = neighbor + n;
            
            // Random offset for cell center
            vec2 randomOffset = hash2(cellPos + floor(time)) * randomness;
            
            // Animate cell positions
            if (speed > 0.0) {
                randomOffset = mix(randomOffset, hash2(cellPos + floor(time + 1.0)) * randomness, fract(time));
            }
            
            vec2 cellCenter = neighbor + randomOffset;
            float dist = getDistance(cellCenter, f, distanceType);
            
            if (dist < minDist) {
                secondMinDist = minDist;
                secondClosestCell = closestCell;
                minDist = dist;
                closestCell = cellPos;
            } else if (dist < secondMinDist) {
                secondMinDist = dist;
                secondClosestCell = cellPos;
            }
        }
    }
    
    return vec4(minDist, secondMinDist, closestCell);
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    
    // Scale UV by cell count
    vec2 scaledUV = uv * float(cellCount);
    
    // Get Voronoi data
    vec4 voronoiData = voronoi(scaledUV, uTDTime * speed);
    float dist1 = voronoiData.x * cellSize;
    float dist2 = voronoiData.y * cellSize;
    vec2 cellID = voronoiData.zw;
    
    vec3 color = vec3(0.0);
    
    if (displayMode == 0) {
        // Distance field visualization
        float distField = pow(dist1, distancePower);
        color = vec3(1.0 - distField);
        
    } else if (displayMode == 1) {
        // Random cell colors
        vec3 cellColor = hash3(cellID);
        if (colorVariation < 1.0) {
            cellColor = mix(vec3(0.5), cellColor, colorVariation);
        }
        color = cellColor;
        
    } else if (displayMode == 2) {
        // Cell borders only
        float border = smoothstep(borderWidth * 0.5, borderWidth, dist2 - dist1);
        color = mix(borderColor, vec3(1.0), border);
        
    } else if (displayMode == 3) {
        // Combined: colored cells with borders
        vec3 cellColor = hash3(cellID);
        if (colorVariation < 1.0) {
            cellColor = mix(vec3(0.5), cellColor, colorVariation);
        }
        float border = smoothstep(borderWidth * 0.5, borderWidth, dist2 - dist1);
        color = mix(borderColor, cellColor, border);
    }
    
    // Optional: blend with input texture if provided
    vec4 inputColor = texture(sTD2DInputs[0], uv);
    if (inputColor.a > 0.0) {
        color = mix(color, inputColor.rgb, 0.5);
    }
    
    fragColor = vec4(color, 1.0);
}