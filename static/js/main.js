// Splash screen
// document.addEventListener('DOMContentLoaded', function() {
//     document.body.classList.add('splash-active');
// });

// setTimeout(() => {
//     const splash = document.getElementById('splash');
//     splash.classList.add('fade-out');
    
//     setTimeout(() => {
//         splash.classList.add('d-none');
//         document.body.classList.remove('splash-active');
//     }, 500);
// }, 3000);


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
        tinggi: parseFloat(document.getElementById('tinggi').value),
        inseam: parseFloat(document.getElementById('inseam').value),
        torso: parseFloat(document.getElementById('torso').value),
        lengan: parseFloat(document.getElementById('lengan').value),
        bahu: parseFloat(document.getElementById('bahu').value)
    };

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

            // Update struk template
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
    }
}

// Print function
function printResults() {
    window.print();
}

