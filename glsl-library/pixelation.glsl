// Pixelation/Mosaic Effect Shader for TouchDesigner
// Creates a pixelated/mosaic effect by sampling from larger pixel blocks
// Version: GLSL 3.30

#version 330

// TouchDesigner provides these uniforms automatically
uniform sampler2D sTD2DInputs[1];  // Input texture
uniform vec2 uTDOutputInfo;        // Output resolution

// Custom uniforms for pixelation control
uniform float pixelSize = 16.0;    // Size of each pixel block (1-100)
uniform float smoothness = 0.0;    // Smoothing between pixels (0-1)
uniform vec2 aspectCorrection = vec2(1.0, 1.0); // Aspect ratio correction

// Output color
out vec4 fragColor;

void main()
{
    // Get normalized coordinates (0-1)
    vec2 uv = gl_FragCoord.xy / uTDOutputInfo.xy;
    
    // Apply aspect ratio correction to maintain square pixels
    vec2 aspectRatio = uTDOutputInfo.xy / min(uTDOutputInfo.x, uTDOutputInfo.y);
    vec2 correctedUV = uv * aspectRatio * aspectCorrection;
    
    // Calculate the size of each pixel block in UV space
    vec2 pixelBlockSize = vec2(pixelSize) / uTDOutputInfo.xy * aspectRatio;
    
    // Find the center of the current pixel block
    vec2 blockCenter = floor(correctedUV / pixelBlockSize) * pixelBlockSize + pixelBlockSize * 0.5;
    
    // Convert back to regular UV space
    blockCenter = blockCenter / (aspectRatio * aspectCorrection);
    
    // Sample from the block center for hard pixelation
    vec4 pixelatedColor = texture(sTD2DInputs[0], blockCenter);
    
    if (smoothness > 0.0) {
        // Calculate distance from pixel center for smooth transitions
        vec2 pixelPos = fract(correctedUV / pixelBlockSize);
        vec2 distFromCenter = abs(pixelPos - 0.5) * 2.0;
        
        // Create smooth transition at pixel edges
        float edgeFactor = 1.0 - smoothstep(1.0 - smoothness, 1.0, max(distFromCenter.x, distFromCenter.y));
        
        // Blend between pixelated and original
        vec4 originalColor = texture(sTD2DInputs[0], uv);
        pixelatedColor = mix(originalColor, pixelatedColor, edgeFactor);
    }
    
    fragColor = pixelatedColor;
}