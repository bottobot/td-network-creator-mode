// Multi-type Color Gradient Generator for TouchDesigner
// Supports linear, radial, angular, diamond, and spiral gradients
// with customizable color palettes and blending options
//
// This shader generates smooth gradients between multiple colors
// with various geometric patterns and interpolation methods.
//
// Usage in TouchDesigner:
// 1. Create a GLSL TOP
// 2. Copy this code into the fragment shader
// 3. Set up the uniform parameters as listed below
// 4. Connect color inputs or use constant values
//
// Features:
// - 5 gradient types: Linear, Radial, Angular, Diamond, Spiral
// - Up to 5 colors in the palette
// - Smooth, linear, or cubic interpolation
// - Repeat and mirror options
// - Power curve for non-linear falloff

// Gradient type selection
uniform int uGradientType;     // 0=Linear, 1=Radial, 2=Angular, 3=Diamond, 4=Spiral
uniform vec2 uCenter;          // Center point for radial/angular gradients (0-1 range)
uniform float uAngle;          // Angle for linear gradient (in radians)
uniform float uScale;          // Scale factor for the gradient (0.1-5.0)
uniform float uOffset;         // Offset/phase for the gradient (-1 to 1)
uniform float uPower;          // Power curve for gradient falloff (0.1-4.0)
uniform int uRepeat;           // Number of repetitions (1-10)
uniform int uMirror;           // 0=No mirror, 1=Mirror gradient

// Color palette uniforms (up to 5 colors)
uniform vec4 uColor0;          // First color (RGBA)
uniform vec4 uColor1;          // Second color (RGBA)
uniform vec4 uColor2;          // Third color (RGBA)
uniform vec4 uColor3;          // Fourth color (RGBA)
uniform vec4 uColor4;          // Fifth color (RGBA)
uniform int uColorCount;       // Number of active colors (2-5)

// Blending parameters
uniform float uSmoothness;     // Smoothness of color transitions (0-1)
uniform int uInterpolation;    // 0=Linear, 1=Smooth, 2=Cubic

// Output
out vec4 fragColor;

// Constants
const float PI = 3.14159265359;
const float TWO_PI = 6.28318530718;

// Smooth interpolation function (ease in/out)
// Creates an S-curve for smoother transitions
float smoothInterpolate(float t) {
    return t * t * (3.0 - 2.0 * t);
}

// Cubic interpolation function (smoother than smooth)
// Creates an even smoother S-curve with zero acceleration at endpoints
float cubicInterpolate(float t) {
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}

// Apply interpolation based on selected mode
float applyInterpolation(float t, int mode) {
    if (mode == 1) return smoothInterpolate(t);
    else if (mode == 2) return cubicInterpolate(t);
    return t; // Linear (mode == 0)
}

// Calculate gradient value based on type
float calculateGradient(vec2 uv) {
    float value = 0.0;
    
    if (uGradientType == 0) {
        // Linear gradient
        // Project UV onto gradient direction vector
        vec2 dir = vec2(cos(uAngle), sin(uAngle));
        value = dot(uv - vec2(0.5), dir) + 0.5;
    }
    else if (uGradientType == 1) {
        // Radial gradient
        // Distance from center point
        value = length(uv - uCenter) * 2.0;
    }
    else if (uGradientType == 2) {
        // Angular gradient
        // Angle around center point
        vec2 delta = uv - uCenter;
        value = atan(delta.y, delta.x) / TWO_PI + 0.5;
    }
    else if (uGradientType == 3) {
        // Diamond gradient
        // Manhattan distance from center
        vec2 delta = abs(uv - uCenter);
        value = max(delta.x, delta.y) * 2.0;
    }
    else if (uGradientType == 4) {
        // Spiral gradient
        // Combination of angle and radius
        vec2 delta = uv - uCenter;
        float angle = atan(delta.y, delta.x);
        float radius = length(delta);
        // Create spiral by adding radius to angle
        value = fract(angle / TWO_PI + radius * 2.0);
    }
    
    // Apply scale and offset
    value = value * uScale + uOffset;
    
    // Apply repetition
    if (uRepeat > 1) {
        value = fract(value * float(uRepeat));
    }
    
    // Apply mirroring (creates a ping-pong effect)
    if (uMirror == 1) {
        value = 1.0 - abs(1.0 - 2.0 * value);
    }
    
    // Clamp to valid range before power curve
    value = clamp(value, 0.0, 1.0);
    
    // Apply power curve for non-linear falloff
    value = pow(value, uPower);
    
    return value;
}

// Multi-color gradient mixing with smooth transitions
vec4 mixColors(float t) {
    // Ensure t is in valid range
    t = clamp(t, 0.0, 1.0);
    
    // Create array of colors for easier indexing
    vec4 colors[5];
    colors[0] = uColor0;
    colors[1] = uColor1;
    colors[2] = uColor2;
    colors[3] = uColor3;
    colors[4] = uColor4;
    
    // Handle edge cases
    if (uColorCount <= 1) return colors[0];
    if (t <= 0.0) return colors[0];
    if (t >= 1.0) return colors[uColorCount - 1];
    
    // Calculate position in gradient
    // Scale t to span across all color stops
    float scaledT = t * float(uColorCount - 1);
    int index = int(floor(scaledT));
    float localT = fract(scaledT);
    
    // Apply smoothness control
    // Mix between linear and selected interpolation
    localT = mix(localT, applyInterpolation(localT, uInterpolation), uSmoothness);
    
    // Ensure index is within bounds
    index = clamp(index, 0, uColorCount - 2);
    
    // Mix between adjacent colors
    return mix(colors[index], colors[index + 1], localT);
}

void main() {
    // Get normalized coordinates
    vec2 uv = vUV.st;
    
    // Calculate gradient value at this pixel
    float gradientValue = calculateGradient(uv);
    
    // Get interpolated color from palette
    vec4 color = mixColors(gradientValue);
    
    // Output final color
    fragColor = color;
}

// Preset Examples:
//
// Rainbow Linear:
// - Type: Linear
// - Colors: Red -> Orange -> Yellow -> Green -> Blue
// - Smoothness: 0.8
// - Interpolation: Smooth
//
// Sunset Radial:
// - Type: Radial
// - Colors: Dark Blue -> Purple -> Orange -> Yellow
// - Center: (0.5, 0.3)
// - Power: 1.5
//
// Color Wheel Angular:
// - Type: Angular
// - Colors: Full HSV spectrum (5 colors)
// - Center: (0.5, 0.5)
// - Mirror: Off
//
// Neon Diamond:
// - Type: Diamond
// - Colors: Black -> Cyan -> Magenta
// - Repeat: 3
// - Mirror: On
//
// Psychedelic Spiral:
// - Type: Spiral
// - Colors: All 5 vibrant colors
// - Scale: 2.0
// - Smoothness: 1.0