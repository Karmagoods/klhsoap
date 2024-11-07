window.addEventListener("load", () => {
    const audio = document.querySelector("audio");
    if (audio) {
        audio.play().catch(error => {
            // Catch autoplay errors (e.g., Chrome blocking it initially)
        });
    }
});
