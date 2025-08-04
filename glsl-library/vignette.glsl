// Vignette Darkening Effect Shader for TouchDesigner
// Creates customizable vignette effects with various shapes and styles
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for vignette control
uniform float intensity = 0.5;      // Vignette intensity (0-2)
uniform float radius = 0.7;         // Inner radius where vignette starts (0-2)
uniform float softness = 0.5;       // Edge softness (0-1)
uniform vec2 center = vec2(0.5);    // Vignette center position
uniform vec2 aspect = vec2(1.0);    // Aspect ratio adjustment
uniform int shape = 0;              // 0: Circular, 1: Rectangular, 2: Diamond, 3: Star
uniform float rotation = 0.0;       // Shape rotation in radians
uniform vec3 vignetteColor = vec3(0.0); // Vignette color (default black)
uniform int blendMode = 0;          // 0: Multiply, 1: Overlay, 2: Soft Light, 3: Color
uniform float highlights = 0.0;     // Preserve highlights (0-1)
uniform float midtones = 0.0;       // Midtone adjustment (-1 to 1)

// Output color
out vec4 fragColor;

// 2D rotation matrix
mat2 rotate2D(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return mat2(c, -s, s, c);
}

// Overlay blend mode
vec3 overlay(vec3 base, vec3 blend) {
    return mix(
        2.0 * base * blend,
        1.0 - 2.0 * (1.0 - base) * (1.0 - blend),
        step(0.5, base)
    );
}

// Soft light blend mode
vec3 softLight(vec3 base, vec3 blend) {
    return mix(
        2.0 * base * blend + base * base * (1.0 - 2.0 * blend),
        sqrt(base) * (2.0 * blend - 1.0) + 2.0 * base * (1.0 - blend),
        step(0.5, blend)
    );
}

// Get luminance
float getLuminance(vec3 color) {
    return dot(color, vec3(0.299, 0.587, 0.114));
}

// Shape distance functions
float getShapeDistance(vec2 pos, int shape) {
    if (shape == 0) {
        // Circular
        return length(pos);
    } else if (shape == 1) {
        // Rectangular
        vec2 d = abs(pos);
        return max(d.x, d.y);
    } else if (shape == 2) {
        // Diamond
        vec2 d = abs(pos);
        return (d.x + d.y) * 0.7071; // 1/sqrt(2)
    } else {
        // Star (5-pointed)
        float angle = atan(pos.y, pos.x);
        float r = length(pos);
        float star = cos(angle * 5.0) * 0.3 + 0.7;
        return r / star;
    }
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    vec4 color = texture(sTD2DInputs[0], uv);
    
    // Calculate position relative to center
    vec2 pos = (uv - center) * 2.0;
    
    // Apply aspect ratio correction
    pos *= aspect;
    
    // Apply rotation
    if (abs(rotation) > 0.001) {
        pos = rotate2D(rotation) * pos;
    }
    
    // Calculate distance based on shape
    float dist = getShapeDistance(pos, shape);
    
    // Calculate vignette factor
    float vignetteFactor = smoothstep(radius - softness, radius + softness, dist);
    vignetteFactor = pow(vignetteFactor, 1.0 / max(intensity, 0.001));
    
    // Apply midtone adjustment to vignette
    if (abs(midtones) > 0.001) {
        float midtoneCurve = 0.5 + midtones * (vignetteFactor - 0.5) * 2.0;
        vignetteFactor = mix(vignetteFactor, midtoneCurve, abs(midtones));
    }
    
    // Preserve highlights if requested
    if (highlights > 0.0) {
        float lum = getLuminance(color.rgb);
        float highlightMask = smoothstep(0.5, 1.0, lum);
        vignetteFactor = mix(vignetteFactor, 1.0, highlightMask * highlights);
    }
    
    // Apply vignette based on blend mode
    vec3 vignetted;
    
    if (blendMode == 0) {
        // Multiply blend
        vignetted = mix(color.rgb, color.rgb * vignetteColor, vignetteFactor);
    } else if (blendMode == 1) {
        // Overlay blend
        vec3 overlayResult = overlay(color.rgb, vignetteColor);
        vignetted = mix(color.rgb, overlayResult, vignetteFactor);
    } else if (blendMode == 2) {
        // Soft light blend
        vec3 softLightResult = softLight(color.rgb, vignetteColor);
        vignetted = mix(color.rgb, softLightResult, vignetteFactor);
    } else {
        // Color blend (direct mix)
        vignetted = mix(color.rgb, vignetteColor, vignetteFactor);
    }
    
    fragColor = vec4(vignetted, color.a);
}