"""
Audio Reactive Visual System Template for TouchDesigner
Creates a complete audio-reactive network with FFT analysis and visual mapping
"""

def create_audio_reactive_system():
    """
    Creates an audio-reactive visual system with:
    - Audio input and analysis
    - FFT frequency band extraction
    - Visual parameter mapping
    - Output composition
    """
    
    # Create base container for organization
    base = op('/project1').create(containerCOMP, 'audio_reactive_system')
    base.par.w = 1200
    base.par.h = 800
    base.nodeX = 0
    base.nodeY = 0
    
    # Audio Input Section
    print("Creating audio input...")
    audio_in = base.create(audiodeviceinCHOP, 'audio_input')
    audio_in.nodeX = -400
    audio_in.nodeY = 200
    audio_in.par.device = 0  # Default audio device
    audio_in.par.rate = 44100
    
    # Add audio level meter
    level_meter = base.create(levelCHOP, 'audio_level')
    level_meter.nodeX = -200
    level_meter.nodeY = 200
    level_meter.inputConnectors[0].connect(audio_in)
    
    # FFT Analysis
    print("Setting up FFT analysis...")
    fft = base.create(analyzeCHOP, 'fft_analysis')
    fft.nodeX = -200
    fft.nodeY = 100
    fft.par.function = 'fft'
    fft.par.size = 2048
    fft.inputConnectors[0].connect(audio_in)
    
    # Frequency Band Extraction
    print("Creating frequency band extractors...")
    
    # Low frequencies (bass)
    bass_select = base.create(selectCHOP, 'bass_band')
    bass_select.nodeX = 0
    bass_select.nodeY = 150
    bass_select.par.channames = 'chan[1-10]'  # Low frequency bins
    bass_select.inputConnectors[0].connect(fft)
    
    bass_math = base.create(mathCHOP, 'bass_average')
    bass_math.nodeX = 200
    bass_math.nodeY = 150
    bass_math.par.chopop = 'average'
    bass_math.par.ignorefirstrow = True
    bass_math.inputConnectors[0].connect(bass_select)
    
    # Mid frequencies
    mid_select = base.create(selectCHOP, 'mid_band')
    mid_select.nodeX = 0
    mid_select.nodeY = 50
    mid_select.par.channames = 'chan[11-50]'  # Mid frequency bins
    mid_select.inputConnectors[0].connect(fft)
    
    mid_math = base.create(mathCHOP, 'mid_average')
    mid_math.nodeX = 200
    mid_math.nodeY = 50
    mid_math.par.chopop = 'average'
    mid_math.par.ignorefirstrow = True
    mid_math.inputConnectors[0].connect(mid_select)
    
    # High frequencies
    high_select = base.create(selectCHOP, 'high_band')
    high_select.nodeX = 0
    high_select.nodeY = -50
    high_select.par.channames = 'chan[51-200]'  # High frequency bins
    high_select.inputConnectors[0].connect(fft)
    
    high_math = base.create(mathCHOP, 'high_average')
    high_math.nodeX = 200
    high_math.nodeY = -50
    high_math.par.chopop = 'average'
    high_math.par.ignorefirstrow = True
    high_math.inputConnectors[0].connect(high_select)
    
    # Smoothing filters for each band
    print("Adding smoothing filters...")
    
    bass_smooth = base.create(lagCHOP, 'bass_smooth')
    bass_smooth.nodeX = 400
    bass_smooth.nodeY = 150
    bass_smooth.par.lag1 = 0.1
    bass_smooth.par.lag2 = 0.05
    bass_smooth.inputConnectors[0].connect(bass_math)
    
    mid_smooth = base.create(lagCHOP, 'mid_smooth')
    mid_smooth.nodeX = 400
    mid_smooth.nodeY = 50
    mid_smooth.par.lag1 = 0.08
    mid_smooth.par.lag2 = 0.04
    mid_smooth.inputConnectors[0].connect(mid_math)
    
    high_smooth = base.create(lagCHOP, 'high_smooth')
    high_smooth.nodeX = 400
    high_smooth.nodeY = -50
    high_smooth.par.lag1 = 0.05
    high_smooth.par.lag2 = 0.02
    high_smooth.inputConnectors[0].connect(high_math)
    
    # Visual Generation Section
    print("Creating visual generators...")
    
    # Background gradient reactive to bass
    gradient = base.create(rampTOP, 'bass_gradient')
    gradient.nodeX = -400
    gradient.nodeY = -200
    gradient.par.resolutionw = 1920
    gradient.par.resolutionh = 1080
    gradient.par.type = 'radial'
    gradient.par.phase = 0
    
    # Add CHOP reference for gradient phase
    gradient.par.phase.expr = 'op("../bass_smooth")[0] * 2'
    
    # Noise pattern reactive to mids
    noise = base.create(noiseTOP, 'mid_noise')
    noise.nodeX = -200
    noise.nodeY = -200
    noise.par.resolutionw = 1920
    noise.par.resolutionh = 1080
    noise.par.type = 'sparse'
    noise.par.period = 8
    
    # Add CHOP reference for noise amplitude
    noise.par.amp.expr = 'op("../mid_smooth")[0] * 2 + 0.5'
    
    # Circle pattern reactive to highs
    circle = base.create(circleTOP, 'high_circles')
    circle.nodeX = 0
    circle.nodeY = -200
    circle.par.resolutionw = 1920
    circle.par.resolutionh = 1080
    circle.par.radius = 0.1
    
    # Add CHOP reference for circle radius
    circle.par.radiusx.expr = 'op("../high_smooth")[0] * 0.3 + 0.05'
    circle.par.radiusy.expr = 'op("../high_smooth")[0] * 0.3 + 0.05'
    
    # Composition Section
    print("Creating composition network...")
    
    # Blend noise over gradient
    comp1 = base.create(compositeTOP, 'blend_1')
    comp1.nodeX = 200
    comp1.nodeY = -200
    comp1.par.operand = 'screen'
    comp1.inputConnectors[0].connect(gradient)
    comp1.inputConnectors[1].connect(noise)
    
    # Add circles
    comp2 = base.create(compositeTOP, 'blend_2')
    comp2.nodeX = 400
    comp2.nodeY = -200
    comp2.par.operand = 'add'
    comp2.inputConnectors[0].connect(comp1)
    comp2.inputConnectors[1].connect(circle)
    
    # Color correction
    hsv_adjust = base.create(hsvAdjustTOP, 'color_adjust')
    hsv_adjust.nodeX = 600
    hsv_adjust.nodeY = -200
    hsv_adjust.inputConnectors[0].connect(comp2)
    
    # Add overall brightness control from audio level
    hsv_adjust.par.valueoffset.expr = 'op("../audio_level")[0] * 0.3'
    
    # Final output
    out = base.create(outTOP, 'output')
    out.nodeX = 800
    out.nodeY = -200
    out.inputConnectors[0].connect(hsv_adjust)
    
    # Control Panel
    print("Creating control panel...")
    
    # Create parameter container
    params = base.create(containerCOMP, 'controls')
    params.nodeX = -400
    params.nodeY = -400
    params.par.w = 300
    params.par.h = 200
    
    # Add custom parameters
    page = params.appendCustomPage('Audio Reactive Controls')
    
    # Bass controls
    page.appendFloat('Bass_gain', label='Bass Gain', size=1, default=1.0, min=0, max=2)
    page.appendFloat('Bass_smooth', label='Bass Smooth', size=1, default=0.1, min=0, max=1)
    
    # Mid controls
    page.appendFloat('Mid_gain', label='Mid Gain', size=1, default=1.0, min=0, max=2)
    page.appendFloat('Mid_smooth', label='Mid Smooth', size=1, default=0.08, min=0, max=1)
    
    # High controls
    page.appendFloat('High_gain', label='High Gain', size=1, default=1.0, min=0, max=2)
    page.appendFloat('High_smooth', label='High Smooth', size=1, default=0.05, min=0, max=1)
    
    # Link parameters to operators
    bass_smooth.par.lag1.expr = 'op("../controls").par.Bass_smooth'
    mid_smooth.par.lag1.expr = 'op("../controls").par.Mid_smooth'
    high_smooth.par.lag1.expr = 'op("../controls").par.High_smooth'
    
    # Add gain controls
    bass_gain = base.create(mathCHOP, 'bass_gain')
    bass_gain.nodeX = 300
    bass_gain.nodeY = 150
    bass_gain.par.gain = 1.0
    bass_gain.par.gain.expr = 'op("../controls").par.Bass_gain'
    bass_gain.inputConnectors[0].connect(bass_math)
    bass_smooth.inputConnectors[0].connect(bass_gain)
    
    mid_gain = base.create(mathCHOP, 'mid_gain')
    mid_gain.nodeX = 300
    mid_gain.nodeY = 50
    mid_gain.par.gain = 1.0
    mid_gain.par.gain.expr = 'op("../controls").par.Mid_gain'
    mid_gain.inputConnectors[0].connect(mid_math)
    mid_smooth.inputConnectors[0].connect(mid_gain)
    
    high_gain = base.create(mathCHOP, 'high_gain')
    high_gain.nodeX = 300
    high_gain.nodeY = -50
    high_gain.par.gain = 1.0
    high_gain.par.gain.expr = 'op("../controls").par.High_gain'
    high_gain.inputConnectors[0].connect(high_math)
    high_smooth.inputConnectors[0].connect(high_gain)
    
    # Add visualization of frequency bands
    print("Adding frequency visualization...")
    
    trail = base.create(trailCHOP, 'freq_history')
    trail.nodeX = 600
    trail.nodeY = 100
    trail.par.histlength = 2
    trail.par.capture = 1
    
    # Merge all bands
    merge = base.create(mergeCHOP, 'freq_merge')
    merge.nodeX = 600
    merge.nodeY = 0
    merge.inputConnectors[0].connect(bass_smooth)
    merge.inputConnectors[1].connect(mid_smooth)
    merge.inputConnectors[2].connect(high_smooth)
    trail.inputConnectors[0].connect(merge)
    
    # Convert to TOP for visualization
    chop_to_top = base.create(choptoTOP, 'freq_viz')
    chop_to_top.nodeX = 800
    chop_to_top.nodeY = 100
    chop_to_top.inputConnectors[0].connect(trail)
    
    print("Audio reactive system created successfully!")
    print(f"System created at: {base.path}")
    print("\nKey components:")
    print("- Audio input and FFT analysis")
    print("- Frequency band extraction (bass/mid/high)")
    print("- Visual generators mapped to frequency bands")
    print("- Composition and color adjustment")
    print("- Control panel for fine-tuning")
    
    return base

# Execute the template
if __name__ == '__main__':
    create_audio_reactive_system()