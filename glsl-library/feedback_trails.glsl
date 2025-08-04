#version 330

/*
 * Feedback Trails Shader for TouchDesigner
 * 
 * Creates motion trails with customizable decay and color effects.
 * Perfect for creating ghosting effects, motion blur, and psychedelic visuals.
 * 
 * Inputs:
 * - sTD2DInputs[0]: Current frame input
 * - sTD2DInputs[1]: Previous frame feedback
 * 
 * Parameters:
 * - feedbackAmount: Controls the intensity of the trail (0.0-1.0)
 * - decay: How quickly trails fade out (0.0-1.0)
 * - colorShift: Amount of hue shift applied to trails
 */

// TouchDesigner inputs
uniform sampler2D sTD2DInputs[2];  // [0] = current frame, [1] = feedback
uniform float feedbackAmount = 0.9;
uniform float decay = 0.02;
uniform float colorShift = 0.01;

// Output
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

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(textureSize(sTD2DInputs[0], 0));
    
    // Sample current frame
    vec4 currentColor = texture(sTD2DInputs[0], uv);
    
    // Sample feedback (previous frame)
    vec4 feedbackColor = texture(sTD2DInputs[1], uv);
    
    // Apply decay to feedback
    feedbackColor.rgb *= (1.0 - decay);
    
    // Apply color shift to feedback
    if (colorShift != 0.0) {
        vec3 hsv = rgb2hsv(feedbackColor.rgb);
        hsv.x = fract(hsv.x + colorShift);  // Shift hue
        feedbackColor.rgb = hsv2rgb(hsv);
    }
    
    // Mix current frame with feedback
    vec3 mixedColor = mix(currentColor.rgb, feedbackColor.rgb, feedbackAmount);
    
    // Ensure we don't exceed 1.0 (additive blending)
    mixedColor = clamp(mixedColor, 0.0, 1.0);
    
    // Handle alpha channel
    float alpha = max(currentColor.a, feedbackColor.a * (1.0 - decay));
    
    fragColor = vec4(mixedColor, alpha);
}