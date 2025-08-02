// Gray-Scott Reaction-Diffusion System for TouchDesigner
// Creates organic, evolving patterns through chemical simulation
//
// This shader simulates the interaction between two chemicals (A and B)
// following the Gray-Scott model. The result creates organic patterns
// that resemble coral growth, fingerprints, or cellular structures.
//
// Usage in TouchDesigner:
// 1. Create a GLSL TOP
// 2. Set up a feedback loop: GLSL TOP -> Feedback TOP -> back to GLSL TOP input
// 3. Set pixel format to 32-bit float for precision
// 4. Connect this shader as the fragment shader
// 5. Add the uniform parameters listed below
//
// Chemical A: The substrate chemical that gets consumed
// Chemical B: The activator chemical that catalyzes the reaction
// The reaction: A + 2B -> 3B (autocatalytic)

// TouchDesigner uniforms - these need to be set up in the GLSL TOP
uniform float uDiffusionA;    // Diffusion rate for chemical A (typical: 0.8-1.0)
uniform float uDiffusionB;    // Diffusion rate for chemical B (typical: 0.3-0.6)
uniform float uFeedRate;      // Feed rate - how fast A is replenished (typical: 0.01-0.1)
uniform float uKillRate;      // Kill rate - how fast B is removed (typical: 0.045-0.07)
uniform float uTimeStep;      // Simulation time step (typical: 0.5-2.0)
uniform vec2 uMousePos;       // Mouse position for interaction (normalized 0-1)
uniform float uMouseRadius;   // Radius of mouse influence (typical: 0.02-0.1)
uniform int uIterations;      // Number of iterations per frame (typical: 1-10)

// Main output - TouchDesigner specific
out vec4 fragColor;

// Laplacian kernel weights for diffusion calculation
// This approximates the second derivative (rate of change of the rate of change)
const float kernel[9] = float[9](
    0.05, 0.2, 0.05,    // Top row
    0.2, -1.0, 0.2,     // Middle row (center is negative sum of others)
    0.05, 0.2, 0.05     // Bottom row
);

// Sample the texture with proper boundary handling
// Returns vec2(A, B) - the concentrations of both chemicals
vec2 sampleState(vec2 coord) {
    // TouchDesigner's sTD2DInputs array contains input textures
    // We're using the red and green channels to store A and B respectively
    return texture(sTD2DInputs[0], coord).rg;
}

// Calculate Laplacian for diffusion using discrete convolution
// This measures how different a pixel is from its neighbors
vec2 laplacian(vec2 uv, vec2 texelSize) {
    vec2 sum = vec2(0.0);
    
    // Apply 3x3 convolution kernel
    for(int i = -1; i <= 1; i++) {
        for(int j = -1; j <= 1; j++) {
            // Calculate neighbor position
            vec2 offset = vec2(float(i), float(j)) * texelSize;
            vec2 sample = sampleState(uv + offset);
            
            // Apply kernel weight
            int kernelIndex = (i+1)*3 + (j+1);
            sum += sample * kernel[kernelIndex];
        }
    }
    
    return sum;
}

void main() {
    // Get current pixel coordinates
    vec2 uv = vUV.st;  // TouchDesigner provides vUV
    vec2 texelSize = 1.0 / vec2(textureSize(sTD2DInputs[0], 0));
    
    // Get current state (A in red channel, B in green channel)
    vec2 state = sampleState(uv);
    float a = state.r;
    float b = state.g;
    
    // Run multiple iterations for faster evolution
    // This allows the simulation to progress faster without increasing framerate
    for(int iter = 0; iter < uIterations; iter++) {
        // Calculate Laplacian for diffusion
        // This represents how the chemicals spread out over time
        vec2 lap = laplacian(uv, texelSize);
        
        // Gray-Scott reaction-diffusion equations
        // Reaction term: A + 2B -> 3B (autocatalytic reaction)
        float reaction = a * b * b;
        
        // Update chemical A concentration
        // Diffusion term: chemicals spread out based on concentration gradient
        // Reaction term: A is consumed in the reaction
        // Feed term: A is replenished at a constant rate
        float da = uDiffusionA * lap.r - reaction + uFeedRate * (1.0 - a);
        
        // Update chemical B concentration
        // Diffusion term: B spreads out
        // Reaction term: B is produced in the reaction
        // Kill + Feed term: B decays and is diluted by the feed
        float db = uDiffusionB * lap.g + reaction - (uKillRate + uFeedRate) * b;
        
        // Apply changes scaled by time step
        a += da * uTimeStep;
        b += db * uTimeStep;
        
        // Clamp values to valid range [0,1]
        a = clamp(a, 0.0, 1.0);
        b = clamp(b, 0.0, 1.0);
    }
    
    // Mouse interaction - add chemical B at mouse position
    // This allows users to "seed" patterns by clicking/dragging
    float mouseDist = length(uv - uMousePos);
    if(mouseDist < uMouseRadius) {
        // Smooth falloff from center to edge of mouse influence
        float influence = 1.0 - (mouseDist / uMouseRadius);
        influence = smoothstep(0.0, 1.0, influence);
        
        // Add chemical B (but don't completely overwrite)
        b = mix(b, 1.0, influence * 0.5);
    }
    
    // Output: 
    // Red channel: Chemical A concentration
    // Green channel: Chemical B concentration  
    // Blue channel: Difference pattern for visualization
    // Alpha: Always 1.0 (fully opaque)
    float pattern = clamp(b - a, 0.0, 1.0);
    fragColor = vec4(a, b, pattern, 1.0);
}

// Parameter Guidelines for Different Patterns:
//
// Mitosis (cells that divide):
// - Feed Rate: 0.0367
// - Kill Rate: 0.0649
// - Diffusion A: 1.0
// - Diffusion B: 0.5
//
// Coral Growth:
// - Feed Rate: 0.0545
// - Kill Rate: 0.062
// - Diffusion A: 1.0
// - Diffusion B: 0.5
//
// Fingerprint/Maze:
// - Feed Rate: 0.029
// - Kill Rate: 0.057
// - Diffusion A: 1.0
// - Diffusion B: 0.5
//
// Spots and Worms:
// - Feed Rate: 0.034
// - Kill Rate: 0.0618
// - Diffusion A: 1.0
// - Diffusion B: 0.5
//
// Spirals:
// - Feed Rate: 0.014
// - Kill Rate: 0.054
// - Diffusion A: 1.0
// - Diffusion B: 0.5