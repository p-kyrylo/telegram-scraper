document.getElementById('scrape-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    const channelName = document.getElementById('channel-name').value;
    const limit = document.getElementById('limit').value;
    const format = document.getElementById('format').value;
    const statusMessage = document.getElementById('status-message');
    const downloadMedia = document.getElementById("download-media").checked;
    statusMessage.textContent = 'Scraping...';

    // Clear previous error messages
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = '';

    try {
        
        let url = `/scrape_channel/${encodeURIComponent(channelName)}?format=${format}`;

        if (limit) {
            url += `&limit=${limit}`;
        }

        if (downloadMedia) {
            url += `&download_media=true`;
        }
        // Send GET request to the FastAPI backend
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Failed to scrape channel: ' + response.statusText);
        }
        statusMessage.textContent = 'Scraping is finished!';

     } catch (error) {
         errorMessage.textContent = error.message;
    }
});
