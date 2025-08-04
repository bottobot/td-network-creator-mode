// HSV Color Manipulation Shader for TouchDesigner
// Provides hue shifting, saturation, and value adjustments
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for HSV control
uniform float hueShift = 0.0;      // Hue rotation in degrees (-180 to 180)
uniform float saturation = 1.0;    // Saturation multiplier (0-2)
uniform float brightness = 1.0;    // Brightness/Value multiplier (0-2)
uniform float contrast = 1.0;      // Contrast adjustment (0-2)
uniform vec3 colorBalance = vec3(1.0); // RGB color balance
uniform float vibrance = 0.0;      // Smart saturation boost (-1 to 1)
uniform vec2 hueRange = vec2(0.0, 360.0); // Hue range to affect (degrees)
uniform float rangeFeather = 30.0; // Feathering for hue range (degrees)
uniform int preserveLuminance = 0; // 0: Off, 1: Preserve luminance after adjustments

// Output color
out vec4 fragColor;

// Convert RGB to HSV
vec3 rgb2hsv(vec3 c) {
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
    
    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

// Convert HSV to RGB
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

// Get luminance
float getLuminance(vec3 color) {
    return dot(color, vec3(0.299, 0.587, 0.114));
}

// Check if hue is within range (handling wraparound)
float hueInRange(float hue, vec2 range, float feather) {
    float h = hue * 360.0; // Convert to degrees
    float start = range.x;
    float end = range.y;
    
    // Normalize range
    if (start > end) {
        // Range wraps around 360
        if (h >= start || h <= end) {
            return 1.0;
        }
        // Check feathering
        float distToStart = min(abs(h - start), abs(h - start + 360.0));
        float distToEnd = min(abs(h - end), abs(h - end - 360.0));
        float minDist = min(distToStart, distToEnd);
        return 1.0 - smoothstep(0.0, feather, minDist);
    } else {
        // Normal range
        if (h >= start && h <= end) {
            return 1.0;
        }
        // Check feathering
        float distToRange = min(abs(h - start), abs(h - end));
        return 1.0 - smoothstep(0.0, feather, distToRange);
    }
}

// Apply vibrance (selective saturation boost)
vec3 applyVibrance(vec3 hsv, float vibrance) {
    // Vibrance boosts saturation more for less saturated colors
    float satBoost = vibrance * (1.0 - hsv.y) * 0.5;
    hsv.y = clamp(hsv.y + satBoost, 0.0, 1.0);
    return hsv;
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    vec4 color = texture(sTD2DInputs[0], uv);
    
    // Store original luminance if needed
    float originalLum = getLuminance(color.rgb);
    
    // Apply color balance first
    color.rgb *= colorBalance;
    
    // Convert to HSV
    vec3 hsv = rgb2hsv(color.rgb);
    
    // Check if current hue is within the specified range
    float rangeMask = hueInRange(hsv.x, hueRange, rangeFeather);
    
    // Apply hue shift (with range mask)
    float hueShiftNorm = hueShift / 360.0;
    hsv.x = fract(hsv.x + hueShiftNorm * rangeMask);
    
    // Apply saturation adjustment
    hsv.y *= mix(1.0, saturation, rangeMask);
    hsv.y = clamp(hsv.y, 0.0, 1.0);
    
    // Apply vibrance
    if (abs(vibrance) > 0.001) {
        hsv = applyVibrance(hsv, vibrance * rangeMask);
    }
    
    // Apply brightness/value adjustment
    hsv.z *= mix(1.0, brightness, rangeMask);
    
    // Convert back to RGB
    color.rgb = hsv2rgb(hsv);
    
    // Apply contrast
    if (abs(contrast - 1.0) > 0.001) {
        vec3 gray = vec3(0.5);
        color.rgb = mix(gray, color.rgb, contrast);
    }
    
    // Preserve luminance if requested
    if (preserveLuminance == 1) {
        float newLum = getLuminance(color.rgb);
        if (newLum > 0.001) {
            color.rgb *= originalLum / newLum;
        }
    }
    
    // Clamp to valid range
    color.rgb = clamp(color.rgb, 0.0, 1.0);
    
    fragColor = color;
}