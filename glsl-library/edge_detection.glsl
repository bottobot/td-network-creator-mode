// Sobel Edge Detection Shader for TouchDesigner
// Detects edges using Sobel operator for gradient calculation
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for edge detection control
uniform float threshold = 0.1;      // Edge detection threshold (0-1)
uniform float strength = 1.0;       // Edge strength multiplier (0-5)
uniform int colorMode = 0;          // 0: White edges on black, 1: Black edges on white, 2: Colored edges
uniform float blurRadius = 0.0;     // Pre-blur to reduce noise (0-5)

// Output color
out vec4 fragColor;

// Function to get luminance from RGB
float getLuminance(vec3 color) {
    return dot(color, vec3(0.299, 0.587, 0.114));
}

// Function to sample with optional blur
float sampleLuminance(vec2 uv, vec2 offset) {
    vec2 texelSize = 1.0 / uTDOutputInfo.xy;
    
    if (blurRadius > 0.0) {
        // Simple box blur
        float sum = 0.0;
        float count = 0.0;
        float radius = blurRadius;
        
        for (float x = -radius; x <= radius; x += 1.0) {
            for (float y = -radius; y <= radius; y += 1.0) {
                vec2 sampleUV = uv + (offset + vec2(x, y)) * texelSize;
                sum += getLuminance(texture(sTD2DInputs[0], sampleUV).rgb);
                count += 1.0;
            }
        }
        return sum / count;
    } else {
        return getLuminance(texture(sTD2DInputs[0], uv + offset * texelSize).rgb);
    }
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    
    // Sobel X kernel:
    // -1  0  1
    // -2  0  2
    // -1  0  1
    float sobelX = 0.0;
    sobelX += sampleLuminance(uv, vec2(-1, -1)) * -1.0;
    sobelX += sampleLuminance(uv, vec2(-1,  0)) * -2.0;
    sobelX += sampleLuminance(uv, vec2(-1,  1)) * -1.0;
    sobelX += sampleLuminance(uv, vec2( 1, -1)) *  1.0;
    sobelX += sampleLuminance(uv, vec2( 1,  0)) *  2.0;
    sobelX += sampleLuminance(uv, vec2( 1,  1)) *  1.0;
    
    // Sobel Y kernel:
    // -1 -2 -1
    //  0  0  0
    //  1  2  1
    float sobelY = 0.0;
    sobelY += sampleLuminance(uv, vec2(-1, -1)) * -1.0;
    sobelY += sampleLuminance(uv, vec2( 0, -1)) * -2.0;
    sobelY += sampleLuminance(uv, vec2( 1, -1)) * -1.0;
    sobelY += sampleLuminance(uv, vec2(-1,  1)) *  1.0;
    sobelY += sampleLuminance(uv, vec2( 0,  1)) *  2.0;
    sobelY += sampleLuminance(uv, vec2( 1,  1)) *  1.0;
    
    // Calculate edge magnitude
    float edgeMagnitude = length(vec2(sobelX, sobelY)) * strength;
    
    // Apply threshold
    float edge = smoothstep(threshold - 0.01, threshold + 0.01, edgeMagnitude);
    
    // Apply color mode
    vec4 outputColor;
    if (colorMode == 0) {
        // White edges on black background
        outputColor = vec4(vec3(edge), 1.0);
    } else if (colorMode == 1) {
        // Black edges on white background
        outputColor = vec4(vec3(1.0 - edge), 1.0);
    } else {
        // Colored edges based on gradient direction
        float angle = atan(sobelY, sobelX);
        vec3 edgeColor = vec3(
            sin(angle) * 0.5 + 0.5,
            cos(angle) * 0.5 + 0.5,
            sin(angle * 2.0) * 0.5 + 0.5
        );
        outputColor = vec4(edgeColor * edge, 1.0);
    }
    
    fragColor = outputColor;
}