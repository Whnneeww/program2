const imageInput = document.getElementById("imageInput");
const originalImage = document.getElementById("originalImage");
const correctedImage = document.getElementById("correctedImage");

imageInput.addEventListener("change", function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        originalImage.src = e.target.result;

        const img = new Image();
        img.src = e.target.result;

        img.onload = function() {
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");
            canvas.width = img.width;
            canvas.height = img.height;
            context.drawImage(img, 0, 0, img.width, img.height);

            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            for (let i = 0; i < data.length; i += 4) {
                const r = data[i];
                const g = data[i + 1];
                const b = data[i + 2];

                const gray = (r + g + b) / 3;

                data[i] = gray;
                data[i + 1] = gray;
                data[i + 2] = gray;
            }

            context.putImageData(imageData, 0, 0);

            correctedImage.src = canvas.toDataURL();
        }
    }

    reader.readAsDataURL(file);
});
