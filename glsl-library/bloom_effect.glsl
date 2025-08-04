// Bloom/Glow Post-Processing Effect Shader for TouchDesigner
// Creates a bloom effect by extracting bright areas and blurring them
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for bloom control
uniform float threshold = 0.8;      // Brightness threshold for bloom (0-1)
uniform float intensity = 1.0;      // Bloom intensity (0-5)
uniform float radius = 4.0;         // Blur radius (1-20)
uniform vec3 tint = vec3(1.0);     // Bloom color tint
uniform int quality = 2;            // Blur quality: 0=Low, 1=Medium, 2=High
uniform float softKnee = 0.5;       // Soft threshold transition (0-1)

// Output color
out vec4 fragColor;

// Function to extract luminance
float getLuminance(vec3 color) {
    return dot(color, vec3(0.299, 0.587, 0.114));
}

// Soft threshold function for smoother bloom extraction
vec3 softThreshold(vec3 color, float threshold, float knee) {
    float brightness = getLuminance(color);
    float soft = brightness - threshold + knee;
    soft = clamp(soft, 0.0, knee * 2.0);
    soft = soft * soft / (4.0 * knee);
    float multiplier = max(soft, brightness - threshold) / max(brightness, 0.0001);
    return color * multiplier;
}

// Gaussian blur sampling
vec3 gaussianBlur(vec2 uv, vec2 direction, float blurRadius) {
    vec3 result = vec3(0.0);
    float totalWeight = 0.0;
    
    // Determine sample count based on quality
    int samples = quality == 0 ? 5 : (quality == 1 ? 9 : 13);
    float step = blurRadius / float(samples - 1);
    
    // Gaussian weights approximation
    for (int i = 0; i < samples; i++) {
        float offset = -blurRadius * 0.5 + float(i) * step;
        float weight = exp(-0.5 * pow(offset / (blurRadius * 0.3), 2.0));
        
        vec2 sampleUV = uv + direction * offset / uTDOutputInfo.xy;
        result += texture(sTD2DInputs[0], sampleUV).rgb * weight;
        totalWeight += weight;
    }
    
    return result / totalWeight;
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    vec4 originalColor = texture(sTD2DInputs[0], uv);
    
    // Extract bright areas for bloom
    vec3 brightColor = softThreshold(originalColor.rgb, threshold, threshold * softKnee);
    
    // Two-pass separable Gaussian blur
    // First pass: horizontal blur
    vec3 blurredH = gaussianBlur(uv, vec2(1.0, 0.0), radius);
    
    // For a proper two-pass blur, we'd need a second pass
    // Here we simulate it with a diagonal sample for performance
    vec3 blurredV = gaussianBlur(uv, vec2(0.0, 1.0), radius);
    vec3 blurredD1 = gaussianBlur(uv, normalize(vec2(1.0, 1.0)), radius * 0.7);
    vec3 blurredD2 = gaussianBlur(uv, normalize(vec2(-1.0, 1.0)), radius * 0.7);
    
    // Combine blur passes
    vec3 bloomColor = (blurredH + blurredV + blurredD1 + blurredD2) * 0.25;
    
    // Apply only to bright areas
    bloomColor = softThreshold(bloomColor, threshold, threshold * softKnee);
    
    // Apply tint and intensity
    bloomColor *= tint * intensity;
    
    // Additive blending with original
    vec3 finalColor = originalColor.rgb + bloomColor;
    
    // Tone mapping to prevent overexposure
    finalColor = finalColor / (1.0 + getLuminance(finalColor) * 0.1);
    
    fragColor = vec4(finalColor, originalColor.a);
}