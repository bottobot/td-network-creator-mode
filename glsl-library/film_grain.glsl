// Film Grain Post-Processing Effect Shader for TouchDesigner
// Adds realistic film grain and noise to simulate analog film characteristics
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution
uniform float uTDTime;             // Time in seconds

// Custom uniforms for film grain control
uniform float grainAmount = 0.05;   // Grain intensity (0-0.5)
uniform float grainSize = 1.0;      // Grain particle size (0.5-3.0)
uniform float coloredNoise = 0.1;   // Amount of colored vs monochrome noise (0-1)
uniform float speed = 24.0;         // Grain animation speed (fps simulation)
uniform float luminanceAmount = 1.0; // How much grain is affected by image brightness (0-2)
uniform float scratchAmount = 0.0;  // Film scratch intensity (0-1)
uniform float vignetteAmount = 0.3; // Vignette darkness (0-1)
uniform float flickerAmount = 0.0;  // Brightness flicker (0-0.2)
uniform vec3 tint = vec3(1.0, 0.95, 0.85); // Film color tint

// Output color
out vec4 fragColor;

// Hash functions for pseudo-random generation
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

float hash3D(vec3 p) {
    return fract(sin(dot(p, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
}

// Noise function for grain
float noise(vec2 p, float time) {
    vec2 seed = p + vec2(time);
    return hash(seed) * 2.0 - 1.0;
}

// Film scratch generation
float filmScratch(vec2 uv, float time) {
    float scratchSeed = floor(time * 6.0);
    float scratchX = hash(vec2(scratchSeed, 0.0));
    
    // Vertical scratches
    float scratch = 0.0;
    if (scratchAmount > hash(vec2(scratchSeed, 1.0))) {
        float width = 0.001 + hash(vec2(scratchSeed, 2.0)) * 0.002;
        float intensity = 0.3 + hash(vec2(scratchSeed, 3.0)) * 0.7;
        float dist = abs(uv.x - scratchX);
        scratch = (1.0 - smoothstep(0.0, width, dist)) * intensity;
        
        // Add some noise to the scratch
        scratch *= 0.5 + 0.5 * noise(vec2(uv.y * 100.0, time), 0.0);
    }
    
    return scratch * scratchAmount;
}

// Vignette function
float vignette(vec2 uv) {
    vec2 center = uv - 0.5;
    float dist = length(center);
    return 1.0 - smoothstep(0.3, 0.8, dist) * vignetteAmount;
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    vec4 color = texture(sTD2DInputs[0], uv);
    
    // Calculate time-based seed for grain animation
    float frameTime = floor(uTDTime * speed) / speed;
    
    // Generate film grain
    vec2 grainUV = uv * uTDOutputInfo.xy / grainSize;
    
    // Monochrome grain
    float monoGrain = noise(grainUV, frameTime);
    
    // Colored grain (different noise per channel)
    vec3 colorGrain = vec3(
        noise(grainUV, frameTime),
        noise(grainUV + vec2(1000.0, 0.0), frameTime),
        noise(grainUV + vec2(2000.0, 0.0), frameTime)
    );
    
    // Mix monochrome and colored grain
    vec3 grain = mix(vec3(monoGrain), colorGrain, coloredNoise);
    
    // Modulate grain by luminance
    float luminance = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    float lumFactor = mix(1.0, 1.0 - pow(luminance, 0.5), luminanceAmount);
    grain *= lumFactor;
    
    // Apply grain to image
    color.rgb += grain * grainAmount;
    
    // Add film scratches
    float scratch = filmScratch(uv, uTDTime);
    color.rgb = mix(color.rgb, vec3(0.9), scratch);
    
    // Add flicker
    if (flickerAmount > 0.0) {
        float flicker = 1.0 + sin(uTDTime * 50.0) * flickerAmount * hash(vec2(frameTime, 0.0));
        color.rgb *= flicker;
    }
    
    // Apply vignette
    color.rgb *= vignette(uv);
    
    // Apply color tint
    color.rgb *= tint;
    
    // Ensure we stay in valid color range
    color.rgb = clamp(color.rgb, 0.0, 1.0);
    
    fragColor = color;
}