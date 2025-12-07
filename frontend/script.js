const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const previewCard = document.getElementById('preview-card');
const previewImage = document.getElementById('preview-image');
const removeBtn = document.getElementById('remove-image');
const resultCard = document.getElementById('result-card');
const analyzeBtn = document.getElementById('analyze-btn');
const loadingOverlay = document.getElementById('loading-overlay');

const scoreText = document.getElementById('score-text');
const progressBar = document.getElementById('progress-bar');
const categoryText = document.getElementById('category-text');
const heatmapContainer = document.getElementById('heatmap-container');
const heatmapImage = document.getElementById('heatmap-image');

let selectedFile = null;

// Handle Drag & Drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('drag-over'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('drag-over'), false);
});

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// Handle File Input
fileInput.addEventListener('change', function () {
    handleFiles(this.files);
});

function handleFiles(files) {
    if (files.length > 0) {
        selectedFile = files[0];
        showPreview(selectedFile);
    }
}

function showPreview(file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
        previewImage.src = reader.result;
        dropArea.classList.add('hidden');
        previewCard.classList.remove('hidden');
        resultCard.classList.add('hidden'); // Hide previous results
    }
}

// Remove Image
removeBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    previewCard.classList.add('hidden');
    dropArea.classList.remove('hidden');
    resultCard.classList.add('hidden');
});

// Analyze Image
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Show Loading
    loadingOverlay.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', selectedFile);

    // Determine API URL (Handles both Local file:// and Hosted modes)
    const API_URL = window.location.protocol === 'file:'
        ? 'http://localhost:8000/predict'
        : '/predict';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.statusText}`);
        }

        const data = await response.json();
        displayResult(data);

    } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error.message + '. \nMake sure the backend is running!');
    } finally {
        loadingOverlay.classList.add('hidden');
    }
});

function displayResult(data) {
    // Reveal Result Card
    resultCard.classList.remove('hidden');

    // Update Text
    scoreText.textContent = `${data.score.toFixed(2)}/100`;
    categoryText.textContent = data.class;

    // Update Progress Bar
    // Timeout to allow DOM transition to work
    setTimeout(() => {
        progressBar.style.width = `${data.score}%`;

        // Dynamic Color based on score
        if (data.score < 40) {
            progressBar.style.backgroundColor = '#ff4d4d'; // Red
            categoryText.style.color = '#ff4d4d';
        } else if (data.score <= 60) {
            progressBar.style.backgroundColor = '#ffa500'; // Orange
            categoryText.style.color = '#ffa500';
        } else {
            progressBar.style.backgroundColor = '#00f260'; // Green
            categoryText.style.color = '#00f260';
        }

        // Show Heatmap
        if (data.heatmap) {
            heatmapImage.src = data.heatmap;
            heatmapContainer.classList.remove('hidden');
        }
    }, 100);
}
