// Unsharp Mask Sharpening Shader for TouchDesigner
// Enhances image details using unsharp masking technique
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for sharpening control
uniform float amount = 1.0;         // Sharpening strength (0-5)
uniform float radius = 1.0;         // Blur radius for unsharp mask (0.5-5)
uniform float threshold = 0.0;      // Minimum difference to sharpen (0-0.2)
uniform int algorithm = 0;          // 0: Unsharp mask, 1: Simple sharpen, 2: Adaptive
uniform float detail = 0.5;         // Detail enhancement (0-1)
uniform float edgeProtection = 0.5; // Protect edges from over-sharpening (0-1)
uniform vec3 channelWeights = vec3(1.0); // Per-channel sharpening weights

// Output color
out vec4 fragColor;

// Get luminance
float getLuminance(vec3 color) {
    return dot(color, vec3(0.299, 0.587, 0.114));
}

// Simple box blur for unsharp mask
vec3 boxBlur(vec2 uv, float blurRadius) {
    vec2 texelSize = 1.0 / uTDOutputInfo.xy;
    vec3 sum = vec3(0.0);
    float count = 0.0;
    
    int samples = int(ceil(blurRadius));
    for (int x = -samples; x <= samples; x++) {
        for (int y = -samples; y <= samples; y++) {
            vec2 offset = vec2(float(x), float(y));
            float dist = length(offset);
            if (dist <= blurRadius) {
                vec2 sampleUV = uv + offset * texelSize;
                sum += texture(sTD2DInputs[0], sampleUV).rgb;
                count += 1.0;
            }
        }
    }
    
    return sum / count;
}

// Laplacian kernel for simple sharpening
vec3 laplacianSharpen(vec2 uv) {
    vec2 texelSize = 1.0 / uTDOutputInfo.xy;
    
    // Sample neighboring pixels
    vec3 center = texture(sTD2DInputs[0], uv).rgb * 5.0;
    vec3 top = texture(sTD2DInputs[0], uv + vec2(0.0, texelSize.y)).rgb * -1.0;
    vec3 bottom = texture(sTD2DInputs[0], uv - vec2(0.0, texelSize.y)).rgb * -1.0;
    vec3 left = texture(sTD2DInputs[0], uv - vec2(texelSize.x, 0.0)).rgb * -1.0;
    vec3 right = texture(sTD2DInputs[0], uv + vec2(texelSize.x, 0.0)).rgb * -1.0;
    
    return center + top + bottom + left + right;
}

// Edge detection for adaptive sharpening
float detectEdge(vec2 uv) {
    vec2 texelSize = 1.0 / uTDOutputInfo.xy;
    
    // Sobel edge detection
    float tl = getLuminance(texture(sTD2DInputs[0], uv + vec2(-texelSize.x, texelSize.y)).rgb);
    float tm = getLuminance(texture(sTD2DInputs[0], uv + vec2(0.0, texelSize.y)).rgb);
    float tr = getLuminance(texture(sTD2DInputs[0], uv + vec2(texelSize.x, texelSize.y)).rgb);
    float ml = getLuminance(texture(sTD2DInputs[0], uv + vec2(-texelSize.x, 0.0)).rgb);
    float mr = getLuminance(texture(sTD2DInputs[0], uv + vec2(texelSize.x, 0.0)).rgb);
    float bl = getLuminance(texture(sTD2DInputs[0], uv + vec2(-texelSize.x, -texelSize.y)).rgb);
    float bm = getLuminance(texture(sTD2DInputs[0], uv + vec2(0.0, -texelSize.y)).rgb);
    float br = getLuminance(texture(sTD2DInputs[0], uv + vec2(texelSize.x, -texelSize.y)).rgb);
    
    float gx = -1.0 * tl + 1.0 * tr + -2.0 * ml + 2.0 * mr + -1.0 * bl + 1.0 * br;
    float gy = -1.0 * tl + -2.0 * tm + -1.0 * tr + 1.0 * bl + 2.0 * bm + 1.0 * br;
    
    return length(vec2(gx, gy));
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    vec3 original = texture(sTD2DInputs[0], uv).rgb;
    vec3 sharpened = original;
    
    if (algorithm == 0) {
        // Unsharp mask algorithm
        vec3 blurred = boxBlur(uv, radius);
        vec3 highPass = original - blurred;
        
        // Apply threshold
        vec3 mask = step(vec3(threshold), abs(highPass));
        highPass *= mask;
        
        // Apply detail enhancement
        highPass *= mix(1.0, 2.0 - smoothstep(0.0, 0.5, length(highPass)), detail);
        
        // Apply edge protection
        if (edgeProtection > 0.0) {
            float edge = detectEdge(uv);
            float edgeFactor = 1.0 - smoothstep(0.1, 0.3, edge) * edgeProtection;
            highPass *= edgeFactor;
        }
        
        sharpened = original + highPass * amount * channelWeights;
        
    } else if (algorithm == 1) {
        // Simple Laplacian sharpening
        vec3 laplacian = laplacianSharpen(uv);
        sharpened = mix(original, laplacian, amount * 0.2);
        
    } else if (algorithm == 2) {
        // Adaptive sharpening based on local contrast
        vec3 blurred = boxBlur(uv, radius);
        vec3 highPass = original - blurred;
        
        // Calculate local contrast
        float localContrast = length(highPass);
        float contrastFactor = smoothstep(0.0, 0.1, localContrast);
        
        // Stronger sharpening in detailed areas
        float adaptiveAmount = amount * contrastFactor * (1.0 + detail);
        
        // Apply edge protection
        if (edgeProtection > 0.0) {
            float edge = detectEdge(uv);
            adaptiveAmount *= 1.0 - smoothstep(0.2, 0.5, edge) * edgeProtection;
        }
        
        sharpened = original + highPass * adaptiveAmount * channelWeights;
    }
    
    // Prevent color clipping
    sharpened = clamp(sharpened, 0.0, 1.0);
    
    // Preserve original alpha
    fragColor = vec4(sharpened, texture(sTD2DInputs[0], uv).a);
}