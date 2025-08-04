// Halftone Dot Pattern Effect Shader for TouchDesigner
// Creates various halftone patterns for print-style effects
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for halftone control
uniform float dotSize = 8.0;        // Size of halftone dots (2-50)
uniform float angle = 45.0;         // Pattern rotation in degrees
uniform int pattern = 0;            // 0: Dots, 1: Lines, 2: Cross, 3: Square
uniform vec3 inkColor = vec3(0.0); // Ink color (usually black)
uniform vec3 paperColor = vec3(1.0); // Paper color (usually white)
uniform float contrast = 1.0;       // Contrast adjustment (0.5-2)
uniform int colorMode = 0;          // 0: B&W, 1: CMY, 2: CMYK, 3: RGB
uniform float smoothing = 0.1;      // Edge smoothing (0-0.5)
uniform vec2 anglesCMYK = vec2(15.0, 75.0); // Additional angles for C and M
uniform float dotGain = 0.0;        // Simulates dot gain in printing (0-0.5)

// Output color
out vec4 fragColor;

// 2D rotation matrix
mat2 rotate2D(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return mat2(c, -s, s, c);
}

// Get luminance
float getLuminance(vec3 color) {
    return dot(color, vec3(0.299, 0.587, 0.114));
}

// Convert RGB to CMY
vec3 rgb2cmy(vec3 rgb) {
    return vec3(1.0) - rgb;
}

// Convert RGB to CMYK (returns vec4)
vec4 rgb2cmyk(vec3 rgb) {
    vec3 cmy = rgb2cmy(rgb);
    float k = min(min(cmy.r, cmy.g), cmy.b);
    if (k >= 0.99) {
        return vec4(0.0, 0.0, 0.0, 1.0);
    }
    vec3 c = (cmy - k) / (1.0 - k);
    return vec4(c, k);
}

// Halftone pattern functions
float halftonePattern(vec2 pos, float value, int pattern) {
    if (pattern == 0) {
        // Circular dots
        float dist = length(fract(pos) - 0.5) * 2.0;
        return smoothstep(value - smoothing, value + smoothing, dist);
        
    } else if (pattern == 1) {
        // Lines
        float line = abs(fract(pos.y) - 0.5) * 2.0;
        return smoothstep(value - smoothing, value + smoothing, line);
        
    } else if (pattern == 2) {
        // Cross pattern
        vec2 grid = abs(fract(pos) - 0.5) * 2.0;
        float cross = min(grid.x, grid.y);
        return smoothstep(value - smoothing, value + smoothing, cross);
        
    } else {
        // Square dots
        vec2 grid = abs(fract(pos) - 0.5) * 2.0;
        float square = max(grid.x, grid.y);
        return smoothstep(value - smoothing, value + smoothing, square);
    }
}

// Apply halftone to a single channel
float applyHalftone(vec2 uv, float value, float angle) {
    // Apply rotation
    vec2 rotatedUV = rotate2D(radians(angle)) * uv;
    
    // Scale by dot size
    vec2 pos = rotatedUV * uTDOutputInfo.xy / dotSize;
    
    // Apply contrast
    value = pow(value, 1.0 / contrast);
    
    // Apply dot gain
    value = clamp(value - dotGain, 0.0, 1.0);
    
    // Generate pattern
    return halftonePattern(pos, value, pattern);
}

void main()
{
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    vec3 color = texture(sTD2DInputs[0], uv).rgb;
    vec3 result;
    
    if (colorMode == 0) {
        // Black and white halftone
        float gray = getLuminance(color);
        float halftone = applyHalftone(uv, gray, angle);
        result = mix(inkColor, paperColor, halftone);
        
    } else if (colorMode == 1) {
        // CMY color halftone
        vec3 cmy = rgb2cmy(color);
        
        float c = applyHalftone(uv, cmy.r, anglesCMYK.x);
        float m = applyHalftone(uv, cmy.g, anglesCMYK.y);
        float y = applyHalftone(uv, cmy.b, angle);
        
        // Subtractive color mixing
        result = paperColor;
        result *= mix(vec3(1.0), vec3(0.0, 1.0, 1.0), 1.0 - c); // Cyan
        result *= mix(vec3(1.0), vec3(1.0, 0.0, 1.0), 1.0 - m); // Magenta
        result *= mix(vec3(1.0), vec3(1.0, 1.0, 0.0), 1.0 - y); // Yellow
        
    } else if (colorMode == 2) {
        // CMYK color halftone
        vec4 cmyk = rgb2cmyk(color);
        
        float c = applyHalftone(uv, cmyk.r, anglesCMYK.x);
        float m = applyHalftone(uv, cmyk.g, anglesCMYK.y);
        float y = applyHalftone(uv, cmyk.b, angle);
        float k = applyHalftone(uv, cmyk.a, angle + 45.0);
        
        // Subtractive color mixing with black
        result = paperColor;
        result *= mix(vec3(1.0), vec3(0.0, 1.0, 1.0), 1.0 - c); // Cyan
        result *= mix(vec3(1.0), vec3(1.0, 0.0, 1.0), 1.0 - m); // Magenta
        result *= mix(vec3(1.0), vec3(1.0, 1.0, 0.0), 1.0 - y); // Yellow
        result *= mix(vec3(1.0), inkColor, 1.0 - k);            // Black
        
    } else {
        // RGB color halftone (additive)
        float r = applyHalftone(uv, color.r, anglesCMYK.x);
        float g = applyHalftone(uv, color.g, anglesCMYK.y);
        float b = applyHalftone(uv, color.b, angle);
        
        // Additive color mixing
        result = inkColor;
        result = mix(result, result + vec3(1.0, 0.0, 0.0), 1.0 - r);
        result = mix(result, result + vec3(0.0, 1.0, 0.0), 1.0 - g);
        result = mix(result, result + vec3(0.0, 0.0, 1.0), 1.0 - b);
        result = clamp(result, 0.0, 1.0);
    }
    
    fragColor = vec4(result, 1.0);
}