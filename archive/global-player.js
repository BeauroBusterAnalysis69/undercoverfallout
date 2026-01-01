// Global Audio Player with localStorage persistence
// UNDERCOVER FALLOUT

const episodes = [
    {
        number: 1,
        title: "Hacked iPhones, Federal Spies, and a Murder",
        runtime: "13:18",
        audioFile: "Episode-001-Hacked-iPhones-Federal-Spies-and-a-Murder.mp3",
        coverArt: "episode-001-cover.jpg"
    },
    {
        number: 2,
        title: "75 Days till Digital Quicksand: The Coming Apocalypse",
        runtime: "12:52",
        audioFile: "Episode-002-75-Days-till-Digital-Quicksand-The-Coming-Apocalypse.mp3",
        coverArt: "episode-002-cover.jpg"
    },
    {
        number: 3,
        title: "$75,000, The Doctor, and Systematic Theft",
        runtime: "15:28",
        audioFile: "Episode-003-75000-The-Doctor-and-Systematic-Theft.mp3",
        coverArt: "episode-003-cover.jpg"
    },
    {
        number: 4,
        title: "Neighborhood Girl Energy, Tear Gas, and MS-13",
        runtime: "13:26",
        audioFile: "Episode-004-Neighborhood-Girl-Energy-Tear-Gas-and-MS-13.mp3",
        coverArt: "episode-004-cover.jpg"
    },
    {
        number: 5,
        title: "Protection-Free Zone",
        runtime: "14:28",
        audioFile: "Episode-005-Frigidaire-Spies-and-Cocaine-Assets-with-intro.mp3",
        coverArt: "episode-005-cover.jpg"
    },
    {
        number: 6,
        title: "Hacking AI While High: Murder",
        runtime: "12:46",
        audioFile: "Episode-006-Hacking-AI-While-High-Murder-with-intro.mp3",
        coverArt: "episode-006-cover.jpg"
    }
];

class GlobalPlayer {
    constructor() {
        this.audio = document.getElementById('globalAudio');
        this.playBtn = document.getElementById('globalPlayBtn');
        this.prevBtn = document.getElementById('globalPrevBtn');
        this.nextBtn = document.getElementById('globalNextBtn');
        this.progressBar = document.getElementById('globalProgressBar');
        this.progressContainer = document.getElementById('globalProgressContainer');
        this.currentTimeDisplay = document.getElementById('globalCurrentTime');
        this.totalTimeDisplay = document.getElementById('globalTotalTime');
        this.titleDisplay = document.getElementById('globalPlayerTitle');
        this.currentEpisodeIndex = 0;

        this.init();
    }

    init() {
        // Load saved state from localStorage
        const savedState = this.loadState();
        if (savedState) {
            this.currentEpisodeIndex = savedState.episodeIndex;
            this.loadEpisode(this.currentEpisodeIndex, savedState.currentTime, savedState.isPlaying);
        } else {
            this.loadEpisode(0);
        }

        // Set up event listeners
        this.playBtn.addEventListener('click', () => this.togglePlayPause());
        this.prevBtn.addEventListener('click', () => this.previousEpisode());
        this.nextBtn.addEventListener('click', () => this.nextEpisode());

        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('ended', () => this.handleEpisodeEnd());
        this.audio.addEventListener('loadedmetadata', () => this.updateDuration());

        this.progressContainer.addEventListener('click', (e) => this.seek(e));

        // Save state periodically
        setInterval(() => this.saveState(), 1000);
    }

    loadEpisode(index, startTime = 0, autoplay = false) {
        this.currentEpisodeIndex = index;
        const episode = episodes[index];

        this.audio.src = episode.audioFile;
        this.titleDisplay.textContent = `Episode ${episode.number}: ${episode.title}`;
        this.totalTimeDisplay.textContent = episode.runtime;

        this.audio.addEventListener('loadedmetadata', () => {
            if (startTime > 0) {
                this.audio.currentTime = startTime;
            }
            if (autoplay) {
                this.audio.play();
                this.playBtn.textContent = '⏸';
            }
        }, { once: true });

        this.updateButtonStates();
    }

    togglePlayPause() {
        if (this.audio.paused) {
            this.audio.play();
            this.playBtn.textContent = '⏸';
        } else {
            this.audio.pause();
            this.playBtn.textContent = '▶';
        }
    }

    previousEpisode() {
        if (this.currentEpisodeIndex > 0) {
            this.loadEpisode(this.currentEpisodeIndex - 1, 0, true);
        }
    }

    nextEpisode() {
        if (this.currentEpisodeIndex < episodes.length - 1) {
            this.loadEpisode(this.currentEpisodeIndex + 1, 0, true);
        }
    }

    handleEpisodeEnd() {
        this.playBtn.textContent = '▶';
        if (this.currentEpisodeIndex < episodes.length - 1) {
            this.loadEpisode(this.currentEpisodeIndex + 1, 0, true);
        }
    }

    updateProgress() {
        const progress = (this.audio.currentTime / this.audio.duration) * 100;
        this.progressBar.style.width = progress + '%';

        const currentMinutes = Math.floor(this.audio.currentTime / 60);
        const currentSeconds = Math.floor(this.audio.currentTime % 60);
        this.currentTimeDisplay.textContent = `${currentMinutes}:${currentSeconds.toString().padStart(2, '0')}`;
    }

    updateDuration() {
        const durationMinutes = Math.floor(this.audio.duration / 60);
        const durationSeconds = Math.floor(this.audio.duration % 60);
        this.totalTimeDisplay.textContent = `${durationMinutes}:${durationSeconds.toString().padStart(2, '0')}`;
    }

    seek(e) {
        const rect = this.progressContainer.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const percentage = x / rect.width;
        this.audio.currentTime = percentage * this.audio.duration;
    }

    updateButtonStates() {
        this.prevBtn.disabled = this.currentEpisodeIndex === 0;
        this.nextBtn.disabled = this.currentEpisodeIndex === episodes.length - 1;
    }

    saveState() {
        const state = {
            episodeIndex: this.currentEpisodeIndex,
            currentTime: this.audio.currentTime,
            isPlaying: !this.audio.paused
        };
        localStorage.setItem('ufPlayerState', JSON.stringify(state));
    }

    loadState() {
        const saved = localStorage.getItem('ufPlayerState');
        return saved ? JSON.parse(saved) : null;
    }

    // Public method to load specific episode (called from episode list)
    playEpisode(index) {
        this.loadEpisode(index, 0, true);
    }
}

// Initialize player when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.globalPlayer = new GlobalPlayer();
});
