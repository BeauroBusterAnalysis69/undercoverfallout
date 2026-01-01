// UNDERCOVER FALLOUT - Visual Effects System
// Mesmerizing spy-themed animations for listeners to zone out to

class VisualEffectsEngine {
    constructor() {
        this.init();
    }

    init() {
        this.createParticleField();
        this.createDataStreams();
        this.createRadarScanner();
        this.createSignalIndicator();
        this.createScanLine();
        this.createStaticInterference();
        this.createSignalWaves();
        this.createParallaxLayers();
        this.createHexGrid();
        this.applyHolographicBorders();
    }

    // Floating Particle Field - hypnotic dots floating around
    createParticleField() {
        const particleCount = 40;
        const body = document.body;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';

            // Random starting position
            const startX = Math.random() * window.innerWidth;
            const startY = Math.random() * window.innerHeight;

            // Random movement direction
            const moveX = (Math.random() - 0.5) * 400;
            const moveY = (Math.random() - 0.5) * 400;

            // Random delay
            const delay = Math.random() * 10;

            particle.style.left = startX + 'px';
            particle.style.top = startY + 'px';
            particle.style.setProperty('--tx', moveX + 'px');
            particle.style.setProperty('--ty', moveY + 'px');
            particle.style.animationDelay = delay + 's';

            body.appendChild(particle);
        }
    }

    // Matrix-style data streams falling down
    createDataStreams() {
        const streamCount = 3;
        const body = document.body;

        for (let i = 0; i < streamCount; i++) {
            const stream = document.createElement('div');
            stream.className = `data-stream data-stream-${i + 1}`;
            body.appendChild(stream);
        }
    }

    // Radar scanner in corner
    createRadarScanner() {
        const radar = document.createElement('div');
        radar.className = 'radar-scanner';
        document.body.appendChild(radar);
    }

    // Signal strength bars
    createSignalIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'signal-indicator';

        for (let i = 0; i < 5; i++) {
            const bar = document.createElement('div');
            bar.className = 'signal-bar';
            indicator.appendChild(bar);
        }

        document.body.appendChild(indicator);
    }

    // Horizontal scanning line
    createScanLine() {
        const scanLine = document.createElement('div');
        scanLine.className = 'scan-line';
        document.body.appendChild(scanLine);
    }

    // Static TV interference
    createStaticInterference() {
        const static = document.createElement('div');
        static.className = 'static-interference';
        document.body.appendChild(static);
    }

    // Signal waves at bottom
    createSignalWaves() {
        const container = document.createElement('div');
        container.className = 'signal-waves';

        for (let i = 0; i < 2; i++) {
            const wave = document.createElement('div');
            wave.className = 'signal-wave';
            container.appendChild(wave);
        }

        document.body.appendChild(container);
    }

    // 3D parallax depth layers
    createParallaxLayers() {
        for (let i = 1; i <= 2; i++) {
            const layer = document.createElement('div');
            layer.className = `parallax-layer parallax-layer-${i}`;
            document.body.appendChild(layer);
        }
    }

    // Hexagonal grid overlay
    createHexGrid() {
        const grid = document.createElement('div');
        grid.className = 'hex-grid';
        document.body.appendChild(grid);
    }

    // Apply holographic effect to episode cards
    applyHolographicBorders() {
        const episodeCards = document.querySelectorAll('.episode-card, .info-card, .hero');
        episodeCards.forEach(card => {
            card.classList.add('holographic-border');
        });
    }
}

// Audio reactive visualizer - responds to audio playback
class AudioVisualizer {
    constructor() {
        this.audioElement = document.getElementById('mainAudio') || document.getElementById('globalAudio');

        if (this.audioElement) {
            this.setupAudioContext();
            this.createWaveformDisplay();
        }
    }

    setupAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.source = this.audioContext.createMediaElementSource(this.audioElement);

            this.source.connect(this.analyser);
            this.analyser.connect(this.audioContext.destination);

            this.analyser.fftSize = 256;
            this.bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(this.bufferLength);

            this.animate();
        } catch (e) {
            console.log('Audio visualizer not supported');
        }
    }

    createWaveformDisplay() {
        // Create canvas for waveform
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'audioVisualizer';
        this.canvas.style.position = 'fixed';
        this.canvas.style.bottom = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '200px';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '2';
        this.canvas.style.opacity = '0.15';

        document.body.appendChild(this.canvas);

        this.canvasCtx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth;
        this.canvas.height = 200;
    }

    animate() {
        if (!this.analyser || !this.canvasCtx) return;

        requestAnimationFrame(() => this.animate());

        this.analyser.getByteFrequencyData(this.dataArray);

        this.canvasCtx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.canvasCtx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        const barWidth = (this.canvas.width / this.bufferLength) * 2.5;
        let x = 0;

        for (let i = 0; i < this.bufferLength; i++) {
            const barHeight = (this.dataArray[i] / 255) * this.canvas.height;

            // Green to amber gradient based on frequency
            const r = Math.floor(i / this.bufferLength * 255);
            const g = 255 - Math.floor(i / this.bufferLength * 100);
            const b = 65 - Math.floor(i / this.bufferLength * 65);

            this.canvasCtx.fillStyle = `rgba(${r}, ${g}, ${b}, 0.8)`;
            this.canvasCtx.fillRect(x, this.canvas.height - barHeight, barWidth, barHeight);

            x += barWidth + 1;
        }
    }
}

// Glitch effect on random elements
class GlitchEffect {
    constructor() {
        this.elements = document.querySelectorAll('h1, h2, h3, .btn');
        this.applyGlitchHover();
    }

    applyGlitchHover() {
        this.elements.forEach(el => {
            el.classList.add('encrypted-hover');
        });
    }

    randomGlitch() {
        setInterval(() => {
            if (Math.random() > 0.95) {
                const randomEl = this.elements[Math.floor(Math.random() * this.elements.length)];
                randomEl.style.animation = 'textGlitch 0.3s ease-in-out';
                setTimeout(() => {
                    randomEl.style.animation = '';
                }, 300);
            }
        }, 2000);
    }
}

// Matrix rain effect
class MatrixRain {
    constructor() {
        this.createCanvas();
        this.setupMatrix();
        this.animate();
    }

    createCanvas() {
        this.canvas = document.createElement('canvas');
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '1';
        this.canvas.style.opacity = '0.08';

        document.body.appendChild(this.canvas);

        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    setupMatrix() {
        this.fontSize = 14;
        this.columns = Math.floor(this.canvas.width / this.fontSize);
        this.drops = Array(this.columns).fill(1);

        // Spy-themed characters
        this.chars = 'CLASSIFIED•ENCRYPTED•SIGNAL•INTERCEPT•01'.split('');
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        this.ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = '#00ff41';
        this.ctx.font = this.fontSize + 'px monospace';

        for (let i = 0; i < this.drops.length; i++) {
            const text = this.chars[Math.floor(Math.random() * this.chars.length)];
            this.ctx.fillText(text, i * this.fontSize, this.drops[i] * this.fontSize);

            if (this.drops[i] * this.fontSize > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }

            this.drops[i]++;
        }
    }
}

// Pulsing glow effect on active elements
class PulsingGlow {
    constructor() {
        this.addGlowToActiveElements();
    }

    addGlowToActiveElements() {
        setInterval(() => {
            // Make random particles glow brighter
            const particles = document.querySelectorAll('.particle');
            if (particles.length > 0) {
                const randomParticle = particles[Math.floor(Math.random() * particles.length)];
                randomParticle.style.boxShadow = '0 0 20px var(--glow-green)';
                randomParticle.style.transform = 'scale(2)';

                setTimeout(() => {
                    randomParticle.style.boxShadow = '0 0 4px var(--glow-green)';
                    randomParticle.style.transform = 'scale(1)';
                }, 500);
            }
        }, 3000);
    }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait a moment for page to settle
    setTimeout(() => {
        new VisualEffectsEngine();
        new AudioVisualizer();
        new GlitchEffect();
        new MatrixRain();
        new PulsingGlow();

        console.log('🎬 UNDERCOVER FALLOUT Visual Effects: ACTIVE');
    }, 500);
});

// Handle window resize
window.addEventListener('resize', () => {
    const canvas = document.getElementById('audioVisualizer');
    if (canvas) {
        canvas.width = window.innerWidth;
    }
});
