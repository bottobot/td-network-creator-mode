# TouchDesigner GLSL Shader Library

A comprehensive collection of GLSL shaders optimized for TouchDesigner. Each shader uses TouchDesigner-specific syntax and includes customizable uniform parameters.

## Shader Index

### 1. **noise_simplex.glsl**
Simplex noise implementation for procedural texture generation.
- **Parameters:**
  - `scale`: Noise frequency/scale (default: 5.0)
  - `time`: Animation time offset
  - `octaves`: Number of noise layers (default: 4)
  - `persistence`: Amplitude falloff per octave (default: 0.5)

### 2. **feedback_trails.glsl**
Creates motion trails with customizable decay and color mixing.
- **Parameters:**
  - `feedbackAmount`: Trail intensity (0.0-1.0, default: 0.9)
  - `decay`: Trail fade speed (0.0-1.0, default: 0.02)
  - `colorShift`: Hue shift amount for trails (default: 0.01)

### 3. **kaleidoscope.glsl**
Kaleidoscope effect with rotation and segment control.
- **Parameters:**
  - `segments`: Number of mirror segments (default: 6)
  - `rotation`: Overall rotation angle
  - `zoom`: Zoom factor (default: 1.0)

### 4. **chromatic_aberration.glsl**
RGB channel separation for lens distortion effects.
- **Parameters:**
  - `aberrationAmount`: Separation strength (default: 0.01)
  - `radialStrength`: Radial distortion factor (default: 1.0)

### 5. **pixelation.glsl**
Pixelation/mosaic effect with adjustable block size.
- **Parameters:**
  - `pixelSize`: Size of pixel blocks (1-100, default: 16.0)
  - `smoothness`: Edge smoothing amount (0.0-1.0, default: 0.0)
  - `aspectCorrection`: Aspect ratio correction (default: vec2(1.0, 1.0))

### 6. **edge_detection.glsl**
Sobel edge detection for outline effects.
- **Parameters:**
  - `threshold`: Edge detection sensitivity (0-1, default: 0.1)
  - `strength`: Edge strength multiplier (0-5, default: 1.0)
  - `colorMode`: 0=White edges, 1=Black edges, 2=Colored edges (default: 0)
  - `blurRadius`: Pre-blur to reduce noise (0-5, default: 0.0)

### 7. **bloom_effect.glsl**
Bloom/glow post-processing effect.
- **Parameters:**
  - `threshold`: Brightness threshold (0-1, default: 0.8)
  - `intensity`: Bloom intensity (0-5, default: 1.0)
  - `radius`: Blur radius (1-20, default: 4.0)
  - `tint`: Bloom color tint (default: vec3(1.0))
  - `quality`: Blur quality 0=Low, 1=Medium, 2=High (default: 2)
  - `softKnee`: Soft threshold transition (0-1, default: 0.5)

### 8. **wave_distortion.glsl**
Wave-based UV distortion for liquid effects.
- **Parameters:**
  - `amplitude`: Wave strength (0-0.5, default: 0.05)
  - `frequency`: Wave frequency (0-50, default: 10.0)
  - `speed`: Animation speed (0-5, default: 1.0)
  - `direction`: Wave direction (default: vec2(1.0, 0.0))
  - `waveType`: 0=Sine, 1=Radial, 2=Spiral, 3=Turbulence (default: 0)
  - `phase`: Phase offset (0-6.28, default: 0.0)
  - `center`: Center point for radial effects (default: vec2(0.5))
  - `falloff`: Edge falloff (0-1, default: 0.0)

### 9. **voronoi_cells.glsl**
Voronoi/cellular pattern generation.
- **Parameters:**
  - `cellSize`: Size of cells (0.01-1.0, default: 0.1)
  - `randomness`: Cell position randomness (0-1, default: 1.0)
  - `speed`: Animation speed (0-5, default: 0.0)
  - `cellCount`: Grid resolution (2-20, default: 5)
  - `displayMode`: 0=Distance field, 1=Cell colors, 2=Borders, 3=Combined (default: 0)
  - `borderWidth`: Cell border thickness (0-0.1, default: 0.02)
  - `borderColor`: Border color (default: vec3(0.0))
  - `distancePower`: Distance field power (0.5-3.0, default: 1.0)
  - `distanceType`: 0=Euclidean, 1=Manhattan, 2=Chebyshev (default: 0)
  - `colorVariation`: Random color variation (0-1, default: 0.5)

### 10. **film_grain.glsl**
Film grain post-processing for vintage looks.
- **Parameters:**
  - `grainAmount`: Grain intensity (0-0.5, default: 0.05)
  - `grainSize`: Grain particle size (0.5-3.0, default: 1.0)
  - `coloredNoise`: Colored vs monochrome noise (0-1, default: 0.1)
  - `speed`: Grain animation speed/fps (default: 24.0)
  - `luminanceAmount`: Grain affected by brightness (0-2, default: 1.0)
  - `scratchAmount`: Film scratch intensity (0-1, default: 0.0)
  - `vignetteAmount`: Vignette darkness (0-1, default: 0.3)
  - `flickerAmount`: Brightness flicker (0-0.2, default: 0.0)
  - `tint`: Film color tint (default: vec3(1.0, 0.95, 0.85))

### 11. **hue_shift.glsl**
HSV color manipulation for color grading.
- **Parameters:**
  - `hueShift`: Hue rotation in degrees (-180 to 180, default: 0.0)
  - `saturation`: Saturation multiplier (0-2, default: 1.0)
  - `brightness`: Brightness/Value multiplier (0-2, default: 1.0)
  - `contrast`: Contrast adjustment (0-2, default: 1.0)
  - `colorBalance`: RGB color balance (default: vec3(1.0))
  - `vibrance`: Smart saturation boost (-1 to 1, default: 0.0)
  - `hueRange`: Hue range to affect in degrees (default: vec2(0.0, 360.0))
  - `rangeFeather`: Feathering for hue range (default: 30.0)
  - `preserveLuminance`: 0=Off, 1=Preserve luminance (default: 0)

### 12. **vignette.glsl**
Vignette darkening effect for focus enhancement.
- **Parameters:**
  - `intensity`: Vignette intensity (0-2, default: 0.5)
  - `radius`: Inner radius where vignette starts (0-2, default: 0.7)
  - `softness`: Edge softness (0-1, default: 0.5)
  - `center`: Vignette center position (default: vec2(0.5))
  - `aspect`: Aspect ratio adjustment (default: vec2(1.0))
  - `shape`: 0=Circular, 1=Rectangular, 2=Diamond, 3=Star (default: 0)
  - `rotation`: Shape rotation in radians (default: 0.0)
  - `vignetteColor`: Vignette color (default: vec3(0.0))
  - `blendMode`: 0=Multiply, 1=Overlay, 2=Soft Light, 3=Color (default: 0)
  - `highlights`: Preserve highlights (0-1, default: 0.0)
  - `midtones`: Midtone adjustment (-1 to 1, default: 0.0)

### 13. **gaussian_blur.glsl**
Two-pass Gaussian blur for smooth blurring.
- **Parameters:**
  - `blurRadius`: Blur radius in pixels (0-50, default: 10.0)
  - `direction`: Blur direction: (1,0) for horizontal, (0,1) for vertical
  - `samples`: Number of samples (5-30, must be odd, default: 15)
  - `sigma`: Gaussian sigma (0=auto-calculate, default: 0.0)
  - `edgeMode`: 0=Clamp, 1=Wrap, 2=Mirror (default: 0)
  - `centerWeight`: Extra weight for center sample (1-2, default: 1.0)
  - `aspectCorrection`: Aspect ratio correction (default: vec2(1.0))

### 14. **sharpen.glsl**
Unsharp mask sharpening for detail enhancement.
- **Parameters:**
  - `amount`: Sharpening strength (0-5, default: 1.0)
  - `radius`: Blur radius for unsharp mask (0.5-5, default: 1.0)
  - `threshold`: Minimum difference to sharpen (0-0.2, default: 0.0)
  - `algorithm`: 0=Unsharp mask, 1=Simple sharpen, 2=Adaptive (default: 0)
  - `detail`: Detail enhancement (0-1, default: 0.5)
  - `edgeProtection`: Protect edges from over-sharpening (0-1, default: 0.5)
  - `channelWeights`: Per-channel sharpening weights (default: vec3(1.0))

### 15. **halftone.glsl**
Halftone dot pattern for print-style effects.
- **Parameters:**
  - `dotSize`: Size of halftone dots (2-50, default: 8.0)
  - `angle`: Pattern rotation in degrees (default: 45.0)
  - `pattern`: 0=Dots, 1=Lines, 2=Cross, 3=Square (default: 0)
  - `inkColor`: Ink color (default: vec3(0.0))
  - `paperColor`: Paper color (default: vec3(1.0))
  - `contrast`: Contrast adjustment (0.5-2, default: 1.0)
  - `colorMode`: 0=B&W, 1=CMY, 2=CMYK, 3=RGB (default: 0)
  - `smoothing`: Edge smoothing (0-0.5, default: 0.1)
  - `anglesCMYK`: Additional angles for C and M (default: vec2(15.0, 75.0))
  - `dotGain`: Simulates dot gain in printing (0-0.5, default: 0.0)

## Usage

All shaders follow TouchDesigner's GLSL conventions:
- Input textures are accessed via `sTD2DInputs[]` array
- Output is written to `fragColor`
- Use `#version 330` for compatibility
- Uniforms can be connected to TouchDesigner parameters

Example setup in TouchDesigner:
1. Create a GLSL TOP
2. Copy shader code into the pixel shader
3. Connect input TOPs
4. Add custom parameters matching the uniform names

## Notes

- All shaders are optimized for real-time performance
- Parameters include sensible defaults and ranges
- Many shaders include multiple modes or algorithms for flexibility
- Some shaders (like gaussian_blur) are designed for multi-pass use
- Color values are in 0-1 range unless otherwise specified