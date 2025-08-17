// Splash screen
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('splash-active');
});

setTimeout(() => {
    const splash = document.getElementById('splash');
    splash.classList.add('fade-out');
    
    setTimeout(() => {
        splash.classList.add('d-none');
        document.body.classList.remove('splash-active');
    }, 500);
}, 3000);


// Navbar functionality
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if(window.scrollY > 50) {
        navbar.classList.add('navbar-solid');
        navbar.classList.remove('navbar-transparent');
    } else {
        navbar.classList.add('navbar-transparent');
        navbar.classList.remove('navbar-solid');
    }
    
    const sections = document.querySelectorAll('section[id]');
    let currentSection = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= (sectionTop - 100) && 
            window.pageYOffset < (sectionTop + sectionHeight - 100)) {
            currentSection = section.getAttribute('id');
        }
    });
    
    if (currentSection && `#${currentSection}` !== window.location.hash) {
        window.history.replaceState(null, null, `#${currentSection}`);
        updateActiveNavLink();
    }
});

function updateActiveNavLink() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const currentHash = window.location.hash;
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentHash) {
            link.classList.add('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    if(window.scrollY > 50) {
        navbar.classList.add('navbar-solid');
        navbar.classList.remove('navbar-transparent');
    } else {
        navbar.classList.add('navbar-transparent');
        navbar.classList.remove('navbar-solid');
    }
    
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                window.history.pushState(null, null, targetId);
                
                const offsetTop = targetSection.offsetTop - 50;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                this.blur();
            }
        });
    });
    
    updateActiveNavLink();
    window.addEventListener('hashchange', updateActiveNavLink);
});

window.addEventListener('load', function() {
    const hash = window.location.hash;
    if (hash) {
        const targetSection = document.querySelector(hash);
        if (targetSection) {
            setTimeout(() => {
                const offsetTop = targetSection.offsetTop - 50;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }, 100);
        }
    }
});

// handle for button content
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-warning').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId.startsWith('#')) {
                e.preventDefault();
                const targetSection = document.querySelector(targetId);
                if (targetSection) {
                    const offsetTop = targetSection.offsetTop - 50;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});


// Global variables to store current data and results
let currentInputData = null;
let currentResults = null;
let isDataSaved = false;

// Get Recommendation
async function kirim() {
    const form = document.getElementById('fittingForm');
    const inputs = form.querySelectorAll("input");

    inputs.forEach(input => {
        input.oninvalid = function () {
            this.setCustomValidity("Field ini wajib diisi!");
        };
        input.oninput = function () {
            this.setCustomValidity("");
        };
    });

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const data = {
        nama: document.getElementById('nama').value,
        usia: parseFloat(document.getElementById('usia').value),
        noTlp: parseFloat(document.getElementById('noTlp').value),
        tinggi: parseFloat(document.getElementById('tinggi').value),
        inseam: parseFloat(document.getElementById('inseam').value),
        torso: parseFloat(document.getElementById('torso').value),
        lengan: parseFloat(document.getElementById('lengan').value),
        bahu: parseFloat(document.getElementById('bahu').value)
    };
    
    // Store input data globally
    currentInputData = data;

    // Show loading state
    document.getElementById('initialState').style.display = 'none';
    document.getElementById('resultState').style.display = 'none';
    document.getElementById('loadingState').style.display = 'flex';

    try {
        const res = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const hasil = await res.json();
        
        if (!res.ok) {
            throw new Error(hasil.error || 'Terjadi kesalahan pada server');
        }

        // Store results globally
        currentResults = hasil;
        
        // Reset save status
        isDataSaved = false;
        document.getElementById('saveStatus').style.display = 'none';
        document.getElementById('saveBtn').disabled = false;
        
        // Disable print button and show tooltip
        const printBtn = document.getElementById('printBtn');
        const tooltip = document.getElementById('printTooltip');
        printBtn.disabled = true;
        tooltip.classList.remove('hidden');

        // Simulate loading time
        setTimeout(() => {
            // Hide loading, show result
            document.getElementById('loadingState').style.display = 'none';
            document.getElementById('resultState').style.display = 'block';

            // Update results
            document.getElementById('frameSize').textContent = hasil.Frame;
            document.getElementById('saddleHeight').textContent = hasil.Saddle + ' cm';
            document.getElementById('crankSize').textContent = hasil.Crank + ' mm';
            document.getElementById('stemSize').textContent = hasil.Stem + ' mm';
            document.getElementById('handlebarSize').textContent = hasil.Handlebar + ' mm';

            // Update visualisasi
            document.getElementById('frameSizeViz').textContent = 'Frame: ' + hasil.Frame;
            document.getElementById('saddleHeightViz').textContent = 'Saddle: ' + hasil.Saddle + ' cm';
            document.getElementById('crankSizeViz').textContent = 'Crank: ' + hasil.Crank + ' mm';
            document.getElementById('stemSizeViz').textContent = 'Stem: ' + hasil.Stem + ' mm';
            document.getElementById('handlebarSizeViz').textContent = 'Handlebar: ' + hasil.Handlebar + ' mm';

            // Display model scores
            if (hasil.model_scores) {
                displayModelScores(hasil.model_scores);
                document.getElementById('model-performance').style.display = 'block';
            }

            // Update struk template
            document.getElementById('strukNama').textContent = hasil.Nama;
            document.getElementById('strukUsia').textContent = hasil.Usia;
            document.getElementById('struknoTlp').textContent = hasil.noTlp;
            document.getElementById('strukFrameSize').textContent = hasil.Frame;
            document.getElementById('strukSaddleHeight').textContent = hasil.Saddle + ' cm';
            document.getElementById('strukCrankSize').textContent = hasil.Crank + ' mm';
            document.getElementById('strukStemSize').textContent = hasil.Stem + ' mm';
            document.getElementById('strukHandlebarSize').textContent = hasil.Handlebar + ' mm';
            
            // Tanggal
            const now = new Date();
            document.getElementById('strukTanggal').textContent = now.toLocaleDateString() + ' ' + now.toLocaleTimeString();

            // Auto scroll result
            if (window.innerWidth < 992) {
                document.getElementById('resultContainer').scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }, 2000);

    } catch (error) {
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('initialState').style.display = 'block';
        alert('Error: ' + error.message);
        console.error('Error:', error);
        
        // Reset global variables on error
        currentInputData = null;
        currentResults = null;
        isDataSaved = false;
    }
}

// Save function
async function saveResults() {
    if (!currentInputData || !currentResults) {
        alert('Tidak ada data untuk disimpan');
        return;
    }
    
    const saveBtn = document.getElementById('saveBtn');
    const originalText = saveBtn.innerHTML;
    
    // Show loading state
    saveBtn.disabled = true;
    saveBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Menyimpan...';
    
    try {
        const saveData = {
            ...currentInputData,
            ...currentResults
        };
        
        const response = await fetch('/save', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(saveData)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Gagal menyimpan data');
        }
        
        // Success
        isDataSaved = true;
        document.getElementById('saveStatus').style.display = 'block';
        
        // Enable print button and hide tooltip
        const printBtn = document.getElementById('printBtn');
        const tooltip = document.getElementById('printTooltip');
        printBtn.disabled = false;
        tooltip.classList.add('hidden');
        tooltip.textContent = 'Klik untuk mencetak hasil rekomendasi';
        
        saveBtn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Tersimpan';
        saveBtn.classList.remove('btn-success');
        saveBtn.classList.add('btn-outline-success');
        
    } catch (error) {
        alert('Error: ' + error.message);
        saveBtn.disabled = false;
        saveBtn.innerHTML = originalText;
        console.error('Save error:', error);
    }
}

// Print function
function printResults() {
    if (!isDataSaved) {
        alert('Silakan simpan data terlebih dahulu sebelum mencetak!');
        return;
    }
    
    // Temporarily show only the main receipt for printing
    const strukRek = document.getElementById('strukRekomendasi');
    const strukRek2 = document.getElementById('strukRekomendasi2');
    
    // Hide both first
    strukRek2.style.display = 'none';
    strukRek2.style.position = 'absolute';
    strukRek2.style.top = '-9999px';
    
    // Show main receipt temporarily
    strukRek.style.display = 'block';
    strukRek.style.position = 'static';
    strukRek.style.top = 'auto';
    
    // Print and then hide again
    window.print();
    
    // Hide receipt after print dialog closes
    setTimeout(() => {
        strukRek.style.display = 'none';
        strukRek.style.position = 'absolute';
        strukRek.style.top = '-9999px';
    }, 100);
}


// Search and print function using existing struk template
async function searchAndPrint() {
    const phone = document.getElementById('searchPhone').value.trim();
    const resultsList = document.getElementById('searchResultsList');
    const searchResults = document.getElementById('searchResults');
    const noResults = document.getElementById('noResults');
    
    // Reset display
    searchResults.style.display = 'none';
    noResults.style.display = 'none';
    resultsList.innerHTML = '';
    
    if (!phone) {
        alert('Nomor telepon harus diisi.');
        return;
    }
    
    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ noTlp: phone })
        });
        
        const data = await response.json();
        
        if (data.recommendations && data.recommendations.length > 0) {
            // Show results with print buttons
            data.recommendations.forEach((rec, index) => {
                const card = document.createElement('div');
                card.className = 'card mb-2';
                card.innerHTML = `
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-md-8">
                                <h6 class="mb-1">${rec.nama || 'Tidak ada nama'}</h6>
                                <small class="text-muted">No Telepon: ${rec.noTlp} | Usia: ${rec.usia} | Tanggal: ${rec.timestamp}</small>
                            </div>
                            <div class="col-md-4 text-end">
                                <button class="btn btn-outline-primary btn-sm" onclick="printRecommendation(${index})">
                                    <i class="bi bi-printer me-1"></i>Cetak
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                resultsList.appendChild(card);
                
                // Don't populate receipt here - only when printing specific item
            });
            
            // Store data globally for printing
            window.searchedRecommendations = data.recommendations;
            searchResults.style.display = 'block';
            
        } else {
            noResults.style.display = 'block';
        }
        
    } catch (error) {
        alert('Terjadi kesalahan saat mencari data.');
        console.error('Search error:', error);
    }
}

// Print specific recommendation from search results
function printRecommendation(index) {
    if (!window.searchedRecommendations || !window.searchedRecommendations[index]) {
        alert('Data tidak ditemukan');
        return;
    }
    
    const rec = window.searchedRecommendations[index];
    
    // Populate struk2 with selected recommendation data
    document.getElementById('struk2Nama').textContent = rec.nama;
    document.getElementById('struk2Usia').textContent = rec.usia;
    document.getElementById('struk2noTlp').textContent = rec.noTlp;
    document.getElementById('struk2FrameSize').textContent = rec.Frame;
    document.getElementById('struk2SaddleHeight').textContent = rec.Saddle + ' cm';
    document.getElementById('struk2CrankSize').textContent = rec.Crank + ' mm';
    document.getElementById('struk2StemSize').textContent = rec.Stem + ' mm';
    document.getElementById('struk2HandlebarSize').textContent = rec.Handlebar + ' mm';
    document.getElementById('struk2Tanggal').textContent = rec.timestamp;
    
    const strukRek = document.getElementById('strukRekomendasi');
    const strukRek2 = document.getElementById('strukRekomendasi2');
    
    // Hide main receipt first
    strukRek.style.display = 'none';
    strukRek.style.position = 'absolute';
    strukRek.style.top = '-9999px';
    
    // Show search receipt temporarily
    strukRek2.style.display = 'block';
    strukRek2.style.position = 'static';
    strukRek2.style.top = 'auto';
    
    // Print and then hide again
    window.print();
    
    // Hide receipt after print dialog closes
    setTimeout(() => {
        strukRek2.style.display = 'none';
        strukRek2.style.position = 'absolute';
        strukRek2.style.top = '-9999px';
    }, 100);
}

// Function to display model scores in results section
function displayModelScores(scores) {
    const scoresContainer = document.getElementById('performance-scores');
    let html = '';
    
    // Display each component score
    Object.entries(scores).forEach(([component, scoreText]) => {
        const isAccuracy = scoreText.includes('%');
        const badgeClass = isAccuracy ? 
            (parseFloat(scoreText) > 80 ? 'text-success' : parseFloat(scoreText) > 60 ? 'text-warning' : 'text-danger') :
            'text-info';
            
        html += `
            <div class="col-md-3 col-6 mb-2">
                <div class="text-center">
                    <small class="text-muted d-block">${component}</small>
                    <strong class="${badgeClass}">${scoreText}</strong>
                </div>
            </div>
        `;
    });
        
    scoresContainer.innerHTML = html;
}