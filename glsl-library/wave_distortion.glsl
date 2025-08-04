// Wave-based UV Distortion Shader for TouchDesigner
// Creates various wave distortion effects on textures
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution
uniform float uTDTime;             // Time in seconds

// Custom uniforms for wave control
uniform float amplitude = 0.05;     // Wave amplitude (0-0.5)
uniform float frequency = 10.0;     // Wave frequency (0-50)
uniform float speed = 1.0;          // Animation speed (0-5)
uniform vec2 direction = vec2(1.0, 0.0); // Wave direction
uniform int waveType = 0;           // 0: Sine, 1: Radial, 2: Spiral, 3: Turbulence
uniform float phase = 0.0;          // Phase offset (0-6.28)
uniform vec2 center = vec2(0.5);    // Center point for radial effects
uniform float falloff = 0.0;        // Edge falloff (0-1)

// Output color
out vec4 fragColor;

// 2D rotation matrix
mat2 rotate2D(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return mat2(c, -s, s, c);
}

// Smooth noise function for turbulence
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    
    float a = fract(sin(dot(i, vec2(12.9898, 78.233))) * 43758.5453);
    float b = fract(sin(dot(i + vec2(1.0, 0.0), vec2(12.9898, 78.233))) * 43758.5453);
    float c = fract(sin(dot(i + vec2(0.0, 1.0), vec2(12.9898, 78.233))) * 43758.5453);
    float d = fract(sin(dot(i + vec2(1.0, 1.0), vec2(12.9898, 78.233))) * 43758.5453);
    
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    vec2 distortedUV = uv;
    
    // Calculate time-based animation
    float animTime = uTDTime * speed + phase;
    
    // Calculate distance from center for radial effects
    vec2 toCenter = uv - center;
    float dist = length(toCenter);
    
    // Apply different wave types
    vec2 offset = vec2(0.0);
    
    if (waveType == 0) {
        // Linear sine wave
        float wave = sin(dot(uv, normalize(direction)) * frequency + animTime);
        offset = direction * wave * amplitude;
        
    } else if (waveType == 1) {
        // Radial ripple
        float wave = sin(dist * frequency - animTime);
        offset = normalize(toCenter) * wave * amplitude;
        
    } else if (waveType == 2) {
        // Spiral distortion
        float angle = atan(toCenter.y, toCenter.x);
        float spiralWave = sin(dist * frequency * 0.5 + angle * 3.0 - animTime);
        vec2 spiralDir = vec2(-toCenter.y, toCenter.x) / max(dist, 0.001);
        offset = spiralDir * spiralWave * amplitude * dist;
        
    } else if (waveType == 3) {
        // Turbulent noise distortion
        vec2 noiseCoord = uv * frequency;
        float n1 = noise(noiseCoord + vec2(animTime * 0.1, 0.0)) - 0.5;
        float n2 = noise(noiseCoord + vec2(0.0, animTime * 0.1)) - 0.5;
        offset = vec2(n1, n2) * amplitude * 2.0;
    }
    
    // Apply edge falloff if enabled
    if (falloff > 0.0) {
        float edgeDist = min(min(uv.x, 1.0 - uv.x), min(uv.y, 1.0 - uv.y));
        float falloffFactor = smoothstep(0.0, falloff, edgeDist);
        offset *= falloffFactor;
    }
    
    // Apply distortion
    distortedUV += offset;
    
    // Sample with clamped coordinates to prevent edge artifacts
    distortedUV = clamp(distortedUV, 0.0, 1.0);
    vec4 color = texture(sTD2DInputs[0], distortedUV);
    
    fragColor = color;
}