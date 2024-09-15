document.getElementById('downloadForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    const videoUrl = document.getElementById('videoUrl').value;
    const format = document.getElementById('format').value;
    
    const formData = new FormData();
    formData.append('url', videoUrl);
    formData.append('format', format);
    
    const response = await fetch('/download', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    document.getElementById('message').textContent = result.message;
});
