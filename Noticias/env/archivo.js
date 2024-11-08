// Aquí agregas tu texto, dividido en fragmentos según los tiempos de YouTube
const textSegments = [
    { time: 0, text: "Bienvenidos al tutorial de seguimiento de texto." },
    { time: 5, text: "Este es un ejemplo para sincronizar texto con un video de YouTube." },
    { time: 10, text: "Puedes ajustar los tiempos según tu video." },
    // Agrega más segmentos según sea necesario
];

// Función para actualizar el texto según el tiempo
function updateText(currentTime) {
    const textElement = document.getElementById('text');
    const segment = textSegments.find(seg => seg.time <= currentTime && currentTime < (seg.time + 5));
    if (segment) {
        textElement.innerText = segment.text;
    }
}

// Simulación de tiempo (ajustar según sea necesario)
let simulatedTime = 0;
setInterval(() => {
    updateText(simulatedTime);
    simulatedTime += 1; // Incrementa cada segundo
}, 1000);
