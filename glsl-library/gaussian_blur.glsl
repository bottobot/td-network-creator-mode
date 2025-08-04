// Two-Pass Gaussian Blur Shader for TouchDesigner
// Implements separable Gaussian blur for efficient high-quality blurring
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for blur control
uniform float blurRadius = 10.0;    // Blur radius in pixels (0-50)
uniform vec2 direction = vec2(1.0, 0.0); // Blur direction: (1,0) for horizontal, (0,1) for vertical
uniform int samples = 15;           // Number of samples (5-30, must be odd)
uniform float sigma = 0.0;          // Gaussian sigma (0 = auto-calculate)
uniform int edgeMode = 0;           // 0: Clamp, 1: Wrap, 2: Mirror
uniform float centerWeight = 1.0;   // Extra weight for center sample (1-2)
uniform vec2 aspectCorrection = vec2(1.0); // Aspect ratio correction

// Output color
out vec4 fragColor;

// Calculate Gaussian weight
float gaussian(float x, float sigma) {
    return exp(-(x * x) / (2.0 * sigma * sigma));
}

// Sample texture with edge handling
vec4 sampleWithEdgeMode(vec2 uv, int mode) {
    if (mode == 0) {
        // Clamp mode
        uv = clamp(uv, 0.0, 1.0);
    } else if (mode == 1) {
        // Wrap mode
        uv = fract(uv);
    } else if (mode == 2) {
        // Mirror mode
        vec2 phase = floor(uv);
        uv = fract(uv);
        // Mirror on odd phases
        if (mod(phase.x, 2.0) == 1.0) uv.x = 1.0 - uv.x;
        if (mod(phase.y, 2.0) == 1.0) uv.y = 1.0 - uv.y;
    }
    
    return texture(sTD2DInputs[0], uv);
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    
    // Ensure odd number of samples
    int sampleCount = samples;
    if (mod(sampleCount, 2) == 0) {
        sampleCount += 1;
    }
    
    // Calculate or use provided sigma
    float currentSigma = sigma;
    if (currentSigma <= 0.0) {
        // Auto-calculate sigma based on radius
        currentSigma = blurRadius * 0.3;
    }
    
    // Apply aspect correction to direction
    vec2 correctedDirection = normalize(direction * aspectCorrection);
    
    // Calculate texel size
    vec2 texelSize = 1.0 / uTDOutputInfo.xy;
    
    // Initialize accumulation
    vec4 colorSum = vec4(0.0);
    float weightSum = 0.0;
    
    // Center sample index
    int centerIndex = sampleCount / 2;
    
    // Perform Gaussian blur
    for (int i = 0; i < sampleCount; i++) {
        // Calculate offset from center
        float offset = float(i - centerIndex);
        
        // Calculate sample position
        vec2 sampleOffset = correctedDirection * offset * blurRadius / float(centerIndex);
        vec2 sampleUV = uv + sampleOffset * texelSize;
        
        // Calculate Gaussian weight
        float weight = gaussian(offset / float(centerIndex), currentSigma);
        
        // Apply extra center weight if at center
        if (i == centerIndex) {
            weight *= centerWeight;
        }
        
        // Sample and accumulate
        vec4 sampleColor = sampleWithEdgeMode(sampleUV, edgeMode);
        colorSum += sampleColor * weight;
        weightSum += weight;
    }
    
    // Normalize result
    vec4 blurredColor = colorSum / weightSum;
    
    // Preserve alpha channel from original
    vec4 originalColor = texture(sTD2DInputs[0], uv);
    blurredColor.a = originalColor.a;
    
    fragColor = blurredColor;
}

// Usage Notes:
// For a complete Gaussian blur, use this shader twice:
// 1. First pass: Set direction to (1.0, 0.0) for horizontal blur
// 2. Second pass: Set direction to (0.0, 1.0) for vertical blur
// 
// The two-pass approach is much more efficient than a single-pass 2D blur
// because it reduces the number of texture samples from O(n²) to O(2n).
//
// Tips for optimization:
// - Use lower sample counts for real-time applications
// - Adjust sigma based on visual quality needs
// - Consider using lower resolution for the blur passes
// - The edge mode affects performance: Clamp is fastest