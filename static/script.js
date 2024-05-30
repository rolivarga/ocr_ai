document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    document.getElementById('result').innerText = result.message;
    
    if (response.ok) {
        const uploadedImages = document.getElementById('uploadedImages');
        const newImage = document.createElement('div');
        newImage.classList.add('image');
        newImage.innerHTML = `<img src="/${result.file_path.replace(/\\/g, '/')}" alt="${result.file_path}">`;
        uploadedImages.appendChild(newImage);
    }
});

document.getElementById('generateButton').addEventListener('click', async function() {
    const response = await fetch('/generate');
    const result = await response.json();
    document.getElementById('generatedText').innerText = result.text;
});
