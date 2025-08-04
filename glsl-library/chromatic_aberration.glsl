#version 330

/*
 * Chromatic Aberration Shader for TouchDesigner
 * 
 * Simulates lens chromatic aberration by separating RGB channels.
 * Creates a prism-like effect often seen in photography and VHS footage.
 * 
 * Parameters:
 * - aberrationAmount: Strength of the channel separation
 * - radialStrength: How much the effect increases towards edges
 */

// TouchDesigner inputs
uniform sampler2D sTD2DInputs[1];
uniform float aberrationAmount = 0.01;
uniform float radialStrength = 1.0;

// Output
out vec4 fragColor;

void main() {
    vec2 resolution = vec2(textureSize(sTD2DInputs[0], 0));
    vec2 uv = gl_FragCoord.xy / resolution;
    
    // Center the coordinates
    vec2 centered = uv - 0.5;
    
    // Calculate distance from center for radial effect
    float dist = length(centered);
    
    // Calculate aberration offset based on distance
    float aberration = aberrationAmount * mix(1.0, dist * 2.0, radialStrength);
    
    // Direction from center
    vec2 direction = normalize(centered);
    
    // Sample each color channel with different offsets
    float r = texture(sTD2DInputs[0], uv + direction * aberration).r;
    float g = texture(sTD2DInputs[0], uv).g;
    float b = texture(sTD2DInputs[0], uv - direction * aberration).b;
    
    // Get alpha from the center sample
    float a = texture(sTD2DInputs[0], uv).a;
    
    // Combine channels
    fragColor = vec4(r, g, b, a);
}