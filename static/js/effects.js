// Three.js Background Effect
const canvas = document.getElementById('bg-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

// Particle System
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 1500;
const posArray = new Float32Array(particlesCount * 3);

for (let i = 0; i < particlesCount * 3; i += 3) {
    posArray[i] = (Math.random() - 0.5) * 200;
    posArray[i+1] = (Math.random() - 0.5) * 100;
    posArray[i+2] = (Math.random() - 0.5) * 100 - 50;
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

const particlesMaterial = new THREE.PointsMaterial({
    size: 0.2,
    color: 0x8b5cf6,
    transparent: true,
    opacity: 0.5,
    blending: THREE.AdditiveBlending
});

const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

// Multiple color particles
const particlesGeometry2 = new THREE.BufferGeometry();
const posArray2 = new Float32Array(800 * 3);
for (let i = 0; i < 800 * 3; i += 3) {
    posArray2[i] = (Math.random() - 0.5) * 150;
    posArray2[i+1] = (Math.random() - 0.5) * 80;
    posArray2[i+2] = (Math.random() - 0.5) * 80;
}
particlesGeometry2.setAttribute('position', new THREE.BufferAttribute(posArray2, 3));
const particlesMaterial2 = new THREE.PointsMaterial({
    size: 0.15,
    color: 0x06b6d4,
    transparent: true,
    opacity: 0.4,
    blending: THREE.AdditiveBlending
});
const particlesMesh2 = new THREE.Points(particlesGeometry2, particlesMaterial2);
scene.add(particlesMesh2);

camera.position.z = 30;

// Animation
let time = 0;
function animate() {
    requestAnimationFrame(animate);
    time += 0.005;

    particlesMesh.rotation.y = time * 0.1;
    particlesMesh.rotation.x = time * 0.05;
    particlesMesh2.rotation.y = time * 0.15;
    particlesMesh2.rotation.x = time * 0.08;

    renderer.render(scene, camera);
}
animate();

// GSAP Animations on load
window.addEventListener('load', () => {
    gsap.from('.hero-title', { duration: 1, y: 50, opacity: 0, ease: 'power3.out' });
    gsap.from('.hero-desc', { duration: 1, y: 30, opacity: 0, delay: 0.3 });
    gsap.from('.hero-buttons', { duration: 1, y: 20, opacity: 0, delay: 0.6 });
    gsap.from('.float-card', { duration: 0.8, scale: 0, opacity: 0, stagger: 0.2, delay: 0.8 });

    // Animate stats numbers
    document.querySelectorAll('.stat-number').forEach(counter => {
        const target = parseInt(counter.dataset.target);
        let current = 0;
        const increment = target / 50;
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.innerText = Math.ceil(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target;
            }
        };
        updateCounter();
    });
});

// Glow effect on cards
document.querySelectorAll('[data-glow]').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--x', `${x}px`);
        card.style.setProperty('--y', `${y}px`);
    });
});

// Auto-hide messages
setTimeout(() => {
    document.querySelectorAll('.message-toast').forEach(msg => {
        gsap.to(msg, { duration: 0.5, opacity: 0, x: -20, onComplete: () => msg.remove() });
    });
}, 3000);

// Responsive resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});