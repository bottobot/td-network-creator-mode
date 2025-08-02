// Multi-Input Blending Shader for TouchDesigner
// Blends up to 4 input textures with various blend modes and masks
//
// This shader provides a comprehensive set of blend modes similar to
// those found in image editing software, with additional features for
// transforming and masking inputs.
//
// Usage in TouchDesigner:
// 1. Create a GLSL TOP
// 2. Set Number of Inputs to 4
// 3. Connect your source TOPs to the inputs:
//    - Input 0: Base layer (required)
//    - Input 1-2: Additional layers (optional)
//    - Input 3: Can be used as either a layer or mask
// 4. Copy this code into the fragment shader
// 5. Set up the uniform parameters as listed below
//
// Features:
// - 16 different blend modes
// - Per-layer opacity control
// - Per-layer transform (scale, rotation, offset)
// - Optional masking using input 4
// - Global color adjustments (contrast, brightness, saturation)
// - Tint control for each layer

// Blend mode uniforms for each layer
uniform int uBlendMode1;      // Blend mode for input 1 (0-15, see list below)
uniform int uBlendMode2;      // Blend mode for input 2
uniform int uBlendMode3;      // Blend mode for input 3
uniform float uOpacity1;      // Opacity for input 1 (0-1)
uniform float uOpacity2;      // Opacity for input 2
uniform float uOpacity3;      // Opacity for input 3

// Transform uniforms for each input
uniform vec2 uScale1;         // Scale for input 1 (0.1-2.0 typical)
uniform vec2 uScale2;         // Scale for input 2
uniform vec2 uScale3;         // Scale for input 3
uniform vec2 uOffset1;        // Offset for input 1 (-1 to 1)
uniform vec2 uOffset2;        // Offset for input 2
uniform vec2 uOffset3;        // Offset for input 3
uniform float uRotation1;     // Rotation for input 1 (radians)
uniform float uRotation2;     // Rotation for input 2
uniform float uRotation3;     // Rotation for input 3

// Color adjustment uniforms
uniform vec3 uTint1;          // Color tint for input 1 (RGB multiplier)
uniform vec3 uTint2;          // Color tint for input 2
uniform vec3 uTint3;          // Color tint for input 3
uniform float uContrast;      // Global contrast adjustment (0-2, default 1)
uniform float uBrightness;    // Global brightness adjustment (-1 to 1)
uniform float uSaturation;    // Global saturation adjustment (0-2, default 1)

// Mask parameters
uniform int uUseMask;         // 0=No mask, 1=Use input 4 as mask
uniform int uMaskChannel;     // Which channel to use as mask (0=R, 1=G, 2=B, 3=A)
uniform int uInvertMask;      // Invert the mask values (0=No, 1=Yes)

// Output
out vec4 fragColor;

// Blend Mode Reference:
// 0  = Normal (Replace)
// 1  = Multiply (Darken)
// 2  = Screen (Lighten)
// 3  = Overlay (Contrast)
// 4  = Soft Light (Subtle contrast)
// 5  = Hard Light (Strong contrast)
// 6  = Color Dodge (Extreme lighten)
// 7  = Color Burn (Extreme darken)
// 8  = Linear Dodge/Add (Additive)
// 9  = Linear Burn (Subtractive)
// 10 = Difference (Inversion)
// 11 = Exclusion (Soft inversion)
// 12 = Lighten (Max)
// 13 = Darken (Min)
// 14 = Vivid Light (Extreme contrast)
// 15 = Linear Light (Linear contrast)

// Blend mode implementations
vec3 blendNormal(vec3 base, vec3 blend) {
    return blend;
}

vec3 blendMultiply(vec3 base, vec3 blend) {
    return base * blend;
}

vec3 blendScreen(vec3 base, vec3 blend) {
    return 1.0 - (1.0 - base) * (1.0 - blend);
}

vec3 blendOverlay(vec3 base, vec3 blend) {
    return mix(
        2.0 * base * blend,
        1.0 - 2.0 * (1.0 - base) * (1.0 - blend),
        step(0.5, base)
    );
}

vec3 blendSoftLight(vec3 base, vec3 blend) {
    return mix(
        2.0 * base * blend + base * base * (1.0 - 2.0 * blend),
        sqrt(base) * (2.0 * blend - 1.0) + 2.0 * base * (1.0 - blend),
        step(0.5, blend)
    );
}

vec3 blendHardLight(vec3 base, vec3 blend) {
    return blendOverlay(blend, base);
}

vec3 blendColorDodge(vec3 base, vec3 blend) {
    // Add small epsilon to prevent division by zero
    return base / (1.0 - blend + 0.0001);
}

vec3 blendColorBurn(vec3 base, vec3 blend) {
    // Add small epsilon to prevent division by zero
    return 1.0 - (1.0 - base) / (blend + 0.0001);
}

vec3 blendLinearDodge(vec3 base, vec3 blend) {
    return base + blend;
}

vec3 blendLinearBurn(vec3 base, vec3 blend) {
    return base + blend - 1.0;
}

vec3 blendDifference(vec3 base, vec3 blend) {
    return abs(base - blend);
}

vec3 blendExclusion(vec3 base, vec3 blend) {
    return base + blend - 2.0 * base * blend;
}

vec3 blendLighten(vec3 base, vec3 blend) {
    return max(base, blend);
}

vec3 blendDarken(vec3 base, vec3 blend) {
    return min(base, blend);
}

vec3 blendVividLight(vec3 base, vec3 blend) {
    return mix(
        blendColorBurn(base, 2.0 * blend),
        blendColorDodge(base, 2.0 * (blend - 0.5)),
        step(0.5, blend)
    );
}

vec3 blendLinearLight(vec3 base, vec3 blend) {
    return base + 2.0 * blend - 1.0;
}

// Apply blend mode based on index
vec3 applyBlendMode(vec3 base, vec3 blend, int mode) {
    if (mode == 0) return blendNormal(base, blend);
    else if (mode == 1) return blendMultiply(base, blend);
    else if (mode == 2) return blendScreen(base, blend);
    else if (mode == 3) return blendOverlay(base, blend);
    else if (mode == 4) return blendSoftLight(base, blend);
    else if (mode == 5) return blendHardLight(base, blend);
    else if (mode == 6) return blendColorDodge(base, blend);
    else if (mode == 7) return blendColorBurn(base, blend);
    else if (mode == 8) return blendLinearDodge(base, blend);
    else if (mode == 9) return blendLinearBurn(base, blend);
    else if (mode == 10) return blendDifference(base, blend);
    else if (mode == 11) return blendExclusion(base, blend);
    else if (mode == 12) return blendLighten(base, blend);
    else if (mode == 13) return blendDarken(base, blend);
    else if (mode == 14) return blendVividLight(base, blend);
    else if (mode == 15) return blendLinearLight(base, blend);
    return blend; // Default fallback
}

// Transform UV coordinates with scale, rotation, and offset
vec2 transformUV(vec2 uv, vec2 scale, vec2 offset, float rotation) {
    // Center the UV coordinates
    uv -= 0.5;
    
    // Apply scale (inverse to make larger scale values zoom in)
    uv /= scale;
    
    // Apply rotation
    float c = cos(rotation);
    float s = sin(rotation);
    mat2 rot = mat2(c, -s, s, c);
    uv = rot * uv;
    
    // Apply offset and recenter
    uv += 0.5 + offset;
    
    return uv;
}

// Adjust color properties (brightness, contrast, saturation)
vec3 adjustColor(vec3 color, float contrast, float brightness, float saturation) {
    // Apply brightness (additive)
    color += brightness;
    
    // Apply contrast (multiply around 0.5)
    color = (color - 0.5) * contrast + 0.5;
    
    // Apply saturation
    // Calculate luminance using standard weights
    float gray = dot(color, vec3(0.299, 0.587, 0.114));
    color = mix(vec3(gray), color, saturation);
    
    return color;
}

void main() {
    vec2 uv = vUV.st;
    
    // Sample base layer (input 0) - this is always required
    vec4 base = texture(sTD2DInputs[0], uv);
    vec3 result = base.rgb;
    
    // Get mask value if enabled
    float mask = 1.0;
    if (uUseMask == 1 && textureSize(sTD2DInputs[3], 0).x > 0) {
        vec4 maskSample = texture(sTD2DInputs[3], uv);
        
        // Select mask channel
        if (uMaskChannel == 0) mask = maskSample.r;
        else if (uMaskChannel == 1) mask = maskSample.g;
        else if (uMaskChannel == 2) mask = maskSample.b;
        else mask = maskSample.a;
        
        // Invert if requested
        if (uInvertMask == 1) mask = 1.0 - mask;
    }
    
    // Blend input 1 if available
    if (textureSize(sTD2DInputs[1], 0).x > 0) {
        // Transform UV coordinates
        vec2 uv1 = transformUV(uv, uScale1, uOffset1, uRotation1);
        
        // Sample texture
        vec4 tex1 = texture(sTD2DInputs[1], uv1);
        
        // Apply tint
        vec3 blend1 = tex1.rgb * uTint1;
        
        // Apply blend mode
        vec3 blended = applyBlendMode(result, blend1, uBlendMode1);
        
        // Mix with opacity and mask
        result = mix(result, blended, uOpacity1 * tex1.a * mask);
    }
    
    // Blend input 2 if available
    if (textureSize(sTD2DInputs[2], 0).x > 0) {
        vec2 uv2 = transformUV(uv, uScale2, uOffset2, uRotation2);
        vec4 tex2 = texture(sTD2DInputs[2], uv2);
        vec3 blend2 = tex2.rgb * uTint2;
        vec3 blended = applyBlendMode(result, blend2, uBlendMode2);
        result = mix(result, blended, uOpacity2 * tex2.a * mask);
    }
    
    // Blend input 3 if available and not being used as mask
    if (textureSize(sTD2DInputs[3], 0).x > 0 && uUseMask == 0) {
        vec2 uv3 = transformUV(uv, uScale3, uOffset3, uRotation3);
        vec4 tex3 = texture(sTD2DInputs[3], uv3);
        vec3 blend3 = tex3.rgb * uTint3;
        vec3 blended = applyBlendMode(result, blend3, uBlendMode3);
        // Note: No mask applied to layer 3 since it could BE the mask
        result = mix(result, blended, uOpacity3 * tex3.a);
    }
    
    // Apply global color adjustments
    result = adjustColor(result, uContrast, uBrightness, uSaturation);
    
    // Clamp to valid range and output with original alpha
    fragColor = vec4(clamp(result, 0.0, 1.0), base.a);
}

// Usage Examples:
//
// 1. Simple Two-Layer Composite:
//    - Input 0: Background image
//    - Input 1: Foreground with alpha
//    - Blend Mode 1: Normal
//    - Opacity 1: 1.0
//
// 2. Texture Overlay:
//    - Input 0: Base image
//    - Input 1: Texture/pattern
//    - Blend Mode 1: Overlay or Soft Light
//    - Opacity 1: 0.5
//
// 3. Masked Composite:
//    - Input 0: Background
//    - Input 1-2: Layers to composite
//    - Input 3: Grayscale mask
//    - Use Mask: On
//    - Mask Channel: Red (for grayscale)
//
// 4. Color Grading:
//    - Input 0: Original image
//    - Input 1: Color gradient
//    - Blend Mode 1: Overlay
//    - Adjust global Contrast/Brightness/Saturation