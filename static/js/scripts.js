document.addEventListener("DOMContentLoaded", function() {
    const texts = ["I am Bilal", "MERN Stack Developer", "Full Stack Developer", "Graphic Designer"];
    let count = 0;
    let index = 0;
    let currentText = '';
    let letter = '';

    (function type() {
        if (count === texts.length) {
            count = 0;
        }
        currentText = texts[count];
        letter = currentText.slice(0, ++index);

        document.getElementById('changing-text').textContent = letter;
        if (letter.length === currentText.length) {
            count++;
            index = 0;
            setTimeout(type, 2000); // Wait for 2 seconds before starting the next text
        } else {
            setTimeout(type, 200); // Speed of typing
        }
    }());
});
