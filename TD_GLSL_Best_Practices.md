# TouchDesigner GLSL Best Practices and Guidelines

## Table of Contents
1. [Introduction to GLSL in TouchDesigner](#introduction-to-glsl-in-touchdesigner)
2. [TouchDesigner-Specific GLSL Syntax](#touchdesigner-specific-glsl-syntax)
3. [Common GLSL Patterns](#common-glsl-patterns)
4. [GLSL Code Structure Best Practices](#glsl-code-structure-best-practices)
5. [Performance Optimization](#performance-optimization)
6. [Debugging Techniques](#debugging-techniques)
7. [VS Codium Setup for GLSL](#vs-codium-setup-for-glsl)
8. [Code Examples and Templates](#code-examples-and-templates)

---

## 1. Introduction to GLSL in TouchDesigner

### Overview of GLSL Usage in TD

GLSL (OpenGL Shading Language) in TouchDesigner provides powerful GPU-accelerated processing capabilities for real-time graphics and computation. TouchDesigner supports GLSL through several operators:

- **GLSL TOP**: For 2D image processing and effects
- **GLSL MAT**: For 3D material shaders (vertex and fragment)
- **Compute Shader TOP**: For general-purpose GPU computing

### Key Differences from Standard OpenGL GLSL

TouchDesigner's GLSL implementation includes several unique features and conventions:

1. **Automatic Uniform Binding**: TD automatically binds many uniforms without explicit declaration
2. **Input Texture Arrays**: Uses `sTD2DInputs[]` array for multiple input textures
3. **Built-in Functions**: Provides TD-specific helper functions for common operations
4. **Coordinate System**: Uses normalized coordinates (0-1) by default
5. **Output Convention**: Uses `fragColor` instead of `gl_FragColor` (deprecated)

---

## 2. TouchDesigner-Specific GLSL Syntax

### Input Texture Access (sTD2DInputs)

TouchDesigner provides a uniform array for accessing input textures:

```glsl
// Accessing the first input texture
vec4 color = texture(sTD2DInputs[0], vUV.st);

// Accessing multiple inputs
vec4 tex1 = texture(sTD2DInputs[0], vUV.st);
vec4 tex2 = texture(sTD2DInputs[1], vUV.st);
```

### Texture Coordinate Calculation

TouchDesigner provides several methods for texture coordinates:

```glsl
// Using vertex shader provided coordinates
vec2 uv = vUV.st;

// Manual calculation from fragment position
vec2 uv = gl_FragCoord.xy / uTD2DInfos[0].res.zw;

// Using TD's built-in function
vec2 uv = TDGetTexCoord();
```

### Output Variable (fragColor)

Modern TouchDesigner uses `out vec4 fragColor` instead of the deprecated `gl_FragColor`:

```glsl
// Correct output declaration
out vec4 fragColor;

void main() {
    fragColor = vec4(1.0, 0.0, 0.0, 1.0); // Red color
}
```

### Built-in Uniforms and Functions

TouchDesigner provides numerous built-in uniforms:

```glsl
// Time uniforms
uniform float uTime;          // Time in seconds
uniform float uFrame;         // Frame number

// Resolution and texture info
uniform vec4 uTD2DInfos[TD_NUM_2D_INPUTS];
// .xy = texture resolution
// .zw = 1.0 / texture resolution

// Camera matrices (for GLSL MAT)
uniform mat4 uTDMat.worldCam;
uniform mat4 uTDMat.camProj;
uniform mat4 uTDMat.worldCamProj;

// Common TD functions
vec2 TDGetTexCoord();         // Get current texture coordinate
vec4 TDDither(vec4 color);    // Apply dithering
```

---

## 3. Common GLSL Patterns

### Reaction-Diffusion Systems

A classic pattern for creating organic, animated textures:

```glsl
uniform float uFeedRate;
uniform float uKillRate;
uniform float uDiffusionA;
uniform float uDiffusionB;
uniform float uTimestep;

out vec4 fragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / uTD2DInfos[0].res.zw;
    vec2 texel = uTD2DInfos[0].res.zw;
    
    // Sample current state
    vec4 current = texture(sTD2DInputs[0], uv);
    float a = current.r;
    float b = current.g;
    
    // Laplacian calculation
    vec2 laplacian = vec2(0.0);
    laplacian += texture(sTD2DInputs[0], uv + vec2(-texel.x, 0)).rg * 0.2;
    laplacian += texture(sTD2DInputs[0], uv + vec2(texel.x, 0)).rg * 0.2;
    laplacian += texture(sTD2DInputs[0], uv + vec2(0, -texel.y)).rg * 0.2;
    laplacian += texture(sTD2DInputs[0], uv + vec2(0, texel.y)).rg * 0.2;
    laplacian += texture(sTD2DInputs[0], uv + vec2(-texel.x, -texel.y)).rg * 0.05;
    laplacian += texture(sTD2DInputs[0], uv + vec2(texel.x, -texel.y)).rg * 0.05;
    laplacian += texture(sTD2DInputs[0], uv + vec2(-texel.x, texel.y)).rg * 0.05;
    laplacian += texture(sTD2DInputs[0], uv + vec2(texel.x, texel.y)).rg * 0.05;
    laplacian -= current.rg;
    
    // Reaction-diffusion equation
    float reaction = a * b * b;
    float da = uDiffusionA * laplacian.r - reaction + uFeedRate * (1.0 - a);
    float db = uDiffusionB * laplacian.g + reaction - (uKillRate + uFeedRate) * b;
    
    // Update concentrations
    a = clamp(a + da * uTimestep, 0.0, 1.0);
    b = clamp(b + db * uTimestep, 0.0, 1.0);
    
    fragColor = vec4(a, b, 0.0, 1.0);
}
```

### Color Mapping Techniques

Converting grayscale or data values to colors:

```glsl
// Simple gradient mapping
vec3 gradientMap(float value) {
    vec3 color1 = vec3(0.0, 0.2, 0.4);  // Dark blue
    vec3 color2 = vec3(0.0, 0.6, 0.8);  // Light blue
    vec3 color3 = vec3(1.0, 0.8, 0.2);  // Yellow
    vec3 color4 = vec3(1.0, 0.2, 0.0);  // Red
    
    float t = value * 3.0;
    vec3 color;
    
    if (t < 1.0) {
        color = mix(color1, color2, t);
    } else if (t < 2.0) {
        color = mix(color2, color3, t - 1.0);
    } else {
        color = mix(color3, color4, t - 2.0);
    }
    
    return color;
}

// HSV to RGB conversion
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}
```

### Projection Mapping

Handling UV coordinates for projection mapping:

```glsl
uniform mat4 uProjectionMatrix;
uniform vec2 uAspectCorrection;

vec2 projectUV(vec2 uv) {
    // Apply aspect ratio correction
    vec2 correctedUV = (uv - 0.5) * uAspectCorrection + 0.5;
    
    // Apply projection matrix
    vec4 projected = uProjectionMatrix * vec4(correctedUV, 0.0, 1.0);
    
    // Perspective divide
    vec2 finalUV = projected.xy / projected.w;
    
    return finalUV * 0.5 + 0.5;
}
```

### Feedback Loops

Creating feedback effects with proper handling:

```glsl
uniform float uFeedbackAmount;
uniform vec2 uFeedbackOffset;
uniform float uFeedbackRotation;

out vec4 fragColor;

void main() {
    vec2 uv = vUV.st;
    
    // Current frame
    vec4 current = texture(sTD2DInputs[0], uv);
    
    // Feedback transformation
    vec2 feedbackUV = uv - 0.5;
    float s = sin(uFeedbackRotation);
    float c = cos(uFeedbackRotation);
    feedbackUV = mat2(c, -s, s, c) * feedbackUV;
    feedbackUV = feedbackUV + 0.5 + uFeedbackOffset;
    
    // Sample feedback
    vec4 feedback = texture(sTD2DInputs[1], feedbackUV);
    
    // Blend
    fragColor = mix(current, feedback, uFeedbackAmount);
}
```

### Multi-pass Rendering

Structure for multi-pass effects:

```glsl
// Pass 1: Blur horizontal
uniform float uBlurSize;

out vec4 fragColor;

void main() {
    vec2 uv = vUV.st;
    vec2 texel = uTD2DInfos[0].res.zw;
    vec4 sum = vec4(0.0);
    
    // Gaussian weights
    float weights[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);
    
    sum += texture(sTD2DInputs[0], uv) * weights[0];
    
    for(int i = 1; i < 5; i++) {
        vec2 offset = vec2(texel.x * float(i) * uBlurSize, 0.0);
        sum += texture(sTD2DInputs[0], uv + offset) * weights[i];
        sum += texture(sTD2DInputs[0], uv - offset) * weights[i];
    }
    
    fragColor = sum;
}
```

---

## 4. GLSL Code Structure Best Practices

### Proper Shader Header Format

Always start your shaders with proper version and precision declarations:

```glsl
// Fragment shader header
#version 330 core

// Precision qualifiers (optional but recommended)
precision highp float;
precision highp int;
precision highp sampler2D;

// Input/output declarations
in vec2 vUV;
out vec4 fragColor;
```

### Uniform Declarations

Organize uniforms logically:

```glsl
// Group related uniforms together
// Animation parameters
uniform float uTime;
uniform float uSpeed;
uniform float uPhase;

// Color parameters
uniform vec3 uColorPrimary;
uniform vec3 uColorSecondary;
uniform float uColorMix;

// Effect parameters
uniform float uIntensity;
uniform vec2 uScale;
uniform float uRotation;
```

### Function Organization

Structure functions clearly:

```glsl
// Constants at the top
const float PI = 3.14159265359;
const float TAU = 6.28318530718;

// Utility functions
float remap(float value, float low1, float high1, float low2, float high2) {
    return low2 + (value - low1) * (high2 - low2) / (high1 - low1);
}

// Effect-specific functions
vec3 applyEffect(vec3 color, vec2 uv) {
    // Implementation
    return color;
}

// Main function
void main() {
    vec2 uv = vUV.st;
    vec3 color = texture(sTD2DInputs[0], uv).rgb;
    color = applyEffect(color, uv);
    fragColor = vec4(color, 1.0);
}
```

### Comments and Documentation

Use clear, meaningful comments:

```glsl
/*
 * Reaction-Diffusion Shader
 * Implements Gray-Scott model for pattern generation
 * 
 * Inputs:
 *   0: Previous state (RG = concentrations)
 *   1: Optional seed texture
 * 
 * Parameters:
 *   uFeedRate: Feed rate of chemical A (0.01-0.1)
 *   uKillRate: Kill rate of chemical B (0.045-0.07)
 */

// Calculate laplacian using 9-point stencil
// This provides better stability than 5-point
vec2 laplacian = vec2(0.0);
```

---

## 5. Performance Optimization

### Resolution Management

```glsl
// Use lower resolution for expensive calculations
vec2 lowResUV = floor(uv * uLowResScale) / uLowResScale;

// Use texture LOD for performance
vec4 color = textureLod(sTD2DInputs[0], uv, uLODLevel);

// Skip pixels for preview mode
if (uPreviewMode > 0.5 && mod(gl_FragCoord.x + gl_FragCoord.y, 2.0) > 0.5) {
    discard;
}
```

### Texture Sampling Optimization

```glsl
// Cache texture lookups
vec4 center = texture(sTD2DInputs[0], uv);

// Use textureGather for 2x2 samples
vec4 reds = textureGather(sTD2DInputs[0], uv, 0);

// Minimize dependent texture reads
vec2 offset = vec2(sin(uTime), cos(uTime)) * 0.1;
vec4 displaced = texture(sTD2DInputs[0], uv + offset);
```

### Conditional Branching Best Practices

```glsl
// Avoid branching in inner loops
// Bad:
for (int i = 0; i < 100; i++) {
    if (condition) {
        // expensive operation
    }
}

// Better:
float mask = float(condition);
for (int i = 0; i < 100; i++) {
    // expensive operation * mask
}

// Use mix() instead of if/else for simple cases
// Bad:
if (value > 0.5) {
    color = colorA;
} else {
    color = colorB;
}

// Better:
color = mix(colorB, colorA, step(0.5, value));
```

### Memory Access Patterns

```glsl
// Access textures in cache-friendly patterns
// Process in tiles when possible
vec2 tileSize = vec2(8.0);
vec2 tileCoord = floor(gl_FragCoord.xy / tileSize);

// Minimize register usage
// Reuse variables when possible
vec3 temp = texture(sTD2DInputs[0], uv).rgb;
temp = processStep1(temp);
temp = processStep2(temp);
fragColor = vec4(temp, 1.0);
```

---

## 6. Debugging Techniques

### Using Info DAT for Compile Errors

1. Connect an Info DAT to your GLSL operator
2. Set the Info DAT's parameter to "Compile Errors"
3. Check for shader compilation errors and warnings

### TOP to CHOP Debugging

Debug shader values by outputting them as colors:

```glsl
// Debug mode uniform
uniform int uDebugMode;

void main() {
    vec2 uv = vUV.st;
    
    if (uDebugMode == 1) {
        // Output UV coordinates as RG
        fragColor = vec4(uv, 0.0, 1.0);
    } else if (uDebugMode == 2) {
        // Output a specific value as grayscale
        float debugValue = calculateSomething();
        fragColor = vec4(vec3(debugValue), 1.0);
    } else {
        // Normal rendering
        fragColor = calculateFinalColor();
    }
}
```

### Environment Variables for Debugging

TouchDesigner environment variables for GLSL debugging:
- `TOUCH_GL_DEBUG=1`: Enable OpenGL debug output
- `TOUCH_GLSL_PREPROCESS=1`: Output preprocessed GLSL

### Common Error Patterns and Solutions

```glsl
// Error: Undefined variable
// Solution: Check uniform declarations and spelling

// Error: No matching overloaded function
// Solution: Check parameter types
// Wrong: texture(sTD2DInputs[0], vec3(uv, 0.0))
// Right: texture(sTD2DInputs[0], uv)

// Error: Array index out of bounds
// Solution: Check TD_NUM_2D_INPUTS
#if TD_NUM_2D_INPUTS > 1
    vec4 tex2 = texture(sTD2DInputs[1], uv);
#endif

// Error: Precision mismatch
// Solution: Use consistent precision qualifiers
precision highp float;
```

---

## 7. VS Codium Setup for GLSL

### Recommended Extensions

1. **Shader languages support for VS Code**
   - Extension ID: `slevesque.shader`
   - Provides syntax highlighting for GLSL

2. **GLSL Lint**
   - Extension ID: `dtoplak.vscode-glsllint`
   - Real-time error checking

3. **GLSL Canvas**
   - Extension ID: `circledev.glsl-canvas`
   - Preview shaders directly in VS Codium

### Configuration Tips

Add to your `settings.json`:

```json
{
    "files.associations": {
        "*.glsl": "glsl",
        "*.frag": "glsl",
        "*.vert": "glsl",
        "*.comp": "glsl"
    },
    "glsl-canvas.textures": {
        "0": "./textures/noise.png",
        "1": "./textures/feedback.png"
    },
    "glsllint.glslangValidatorPath": "/path/to/glslangValidator"
}
```

### Syntax Highlighting Setup

Create custom snippets for TouchDesigner in `.vscode/glsl.code-snippets`:

```json
{
    "TD Fragment Shader": {
        "prefix": "tdfrag",
        "body": [
            "out vec4 fragColor;",
            "",
            "void main() {",
            "    vec2 uv = vUV.st;",
            "    vec4 color = texture(sTD2DInputs[0], uv);",
            "    ",
            "    $0",
            "    ",
            "    fragColor = color;",
            "}"
        ]
    },
    "TD Uniform Time": {
        "prefix": "tdtime",
        "body": ["uniform float uTime;"]
    }
}
```

---

## 8. Code Examples and Templates

### Basic Fragment Shader Template

```glsl
// Basic TouchDesigner Fragment Shader Template
out vec4 fragColor;

// Custom uniforms
uniform float uIntensity;
uniform vec3 uTint;

void main() {
    // Get UV coordinates
    vec2 uv = vUV.st;
    
    // Sample input texture
    vec4 inputColor = texture(sTD2DInputs[0], uv);
    
    // Apply effect
    vec3 color = inputColor.rgb;
    color *= uTint;
    color *= uIntensity;
    
    // Output
    fragColor = vec4(color, inputColor.a);
}
```

### Compute Shader Template

```glsl
// TouchDesigner Compute Shader Template
#version 430

layout(local_size_x = 8, local_size_y = 8) in;

// Input/output images
layout(binding = 0, rgba32f) uniform image2D inputImage;
layout(binding = 1, rgba32f) uniform image2D outputImage;

// Uniforms
uniform float uTime;
uniform vec2 uResolution;

void main() {
    ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
    
    // Bounds check
    if (coord.x >= int(uResolution.x) || coord.y >= int(uResolution.y)) {
        return;
    }
    
    // Read input
    vec4 inputValue = imageLoad(inputImage, coord);
    
    // Process
    vec4 outputValue = inputValue;
    // Add your processing here
    
    // Write output
    imageStore(outputImage, coord, outputValue);
}
```

### Multi-input Shader Template

```glsl
// Multi-input TouchDesigner Fragment Shader
out vec4 fragColor;

// Blend modes
uniform int uBlendMode;
uniform float uMix;

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

void main() {
    vec2 uv = vUV.st;
    
    // Sample inputs
    vec3 tex1 = texture(sTD2DInputs[0], uv).rgb;
    #if TD_NUM_2D_INPUTS > 1
        vec3 tex2 = texture(sTD2DInputs[1], uv).rgb;
    #else
        vec3 tex2 = vec3(0.0);
    #endif
    
    // Blend based on mode
    vec3 result;
    if (uBlendMode == 0) {
        result = mix(tex1, tex2, uMix);
    } else if (uBlendMode == 1) {
        result = blendMultiply(tex1, tex2);
    } else if (uBlendMode == 2) {
        result = blendScreen(tex1, tex2);
    } else if (uBlendMode == 3) {
        result = blendOverlay(tex1, tex2);
    } else {
        result = tex1;
    }
    
    fragColor = vec4(result, 1.0);
}
```

---

## Additional Resources

- [TouchDesigner GLSL Documentation](https://docs.derivative.ca/GLSL)
- [TouchDesigner Forum - GLSL Category](https://forum.derivative.ca/c/glsl)
- [The Book of Shaders](https://thebookofshaders.com/)
- [Shadertoy](https://www.shadertoy.com/) - For shader inspiration (requires adaptation for TD)

## Contributing

This document is a living guide. If you have additional tips, patterns, or corrections, please contribute to keep it current with TouchDesigner's evolving GLSL capabilities.