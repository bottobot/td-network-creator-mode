#version 330

/*
 * Kaleidoscope Shader for TouchDesigner
 * 
 * Creates a kaleidoscope effect by mirroring and rotating segments of the input.
 * Great for creating mandala-like patterns and symmetrical visuals.
 * 
 * Parameters:
 * - segments: Number of mirror segments (typically 4-12)
 * - rotation: Overall rotation of the pattern
 * - zoom: Zoom factor for the effect
 */

// TouchDesigner inputs
uniform sampler2D sTD2DInputs[1];
uniform float segments = 6.0;
uniform float rotation = 0.0;
uniform float zoom = 1.0;

// Output
out vec4 fragColor;

// Constants
const float PI = 3.14159265359;
const float TWO_PI = 6.28318530718;

void main() {
    vec2 resolution = vec2(textureSize(sTD2DInputs[0], 0));
    vec2 uv = gl_FragCoord.xy / resolution;
    
    // Center the coordinates
    vec2 centered = (uv - 0.5) * 2.0;
    
    // Apply zoom
    centered /= zoom;
    
    // Convert to polar coordinates
    float radius = length(centered);
    float angle = atan(centered.y, centered.x);
    
    // Apply overall rotation
    angle += rotation;
    
    // Create kaleidoscope effect
    float segmentAngle = TWO_PI / segments;
    
    // Find which segment we're in
    float segmentIndex = floor(angle / segmentAngle);
    
    // Get angle within segment
    float angleInSegment = mod(angle, segmentAngle);
    
    // Mirror every other segment
    if (mod(segmentIndex, 2.0) == 1.0) {
        angleInSegment = segmentAngle - angleInSegment;
    }
    
    // Add segment offset back
    float finalAngle = angleInSegment + segmentIndex * segmentAngle;
    
    // Convert back to cartesian coordinates
    vec2 kaleidoUV;
    kaleidoUV.x = radius * cos(finalAngle);
    kaleidoUV.y = radius * sin(finalAngle);
    
    // Transform back to texture coordinates
    kaleidoUV = kaleidoUV * 0.5 + 0.5;
    
    // Sample the texture
    vec4 color = texture(sTD2DInputs[0], kaleidoUV);
    
    // Optional: Add fade at edges
    float edgeFade = 1.0 - smoothstep(0.8, 1.0, radius);
    color.rgb *= edgeFade;
    
    fragColor = color;
}