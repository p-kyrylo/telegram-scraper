document.getElementById('scrape-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    const channelName = document.getElementById('channel-name').value;
    const limit = document.getElementById('limit').value;
    const format = document.getElementById('format').value;
    const statusMessage = document.getElementById('status-message');
    const downloadMedia = document.getElementById("download-media").checked;
    statusMessage.textContent = 'Scraping...';
    let showMediaButton = false;

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
            showMediaButton = true;
        }

        // Send GET request to the FastAPI backend
        let file_name = null
        const response = await fetch(url);
        console.log(response.headers.get("Content-Disposition"))
        if (response.headers.get("Content-Disposition").split("=")[1] != "None") {
            const content = response.headers.get("Content-Disposition").split("=");
            fileName = content[1];
        }
        
        if (!response.ok) {
            throw new Error('Failed to scrape channel: ' + response.statusText);
        }

        statusMessage.textContent = "Scraping finished.";
        const downloadButton = document.getElementById("download-content");
        downloadButton.style.display = "block";
        downloadButton.addEventListener("click", download);

        if (showMediaButton){
            const mediaButton = document.getElementById("media");
            mediaButton.style.display = "block";
            mediaButton.addEventListener("click", get_media);
        }

        async function download() {
            const fileBlob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(fileBlob);

            // Create a download link and click it to download the file
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `${channelName}_messages.${format}`;
            document.body.appendChild(a);
            a.click();

            // Clean up
            document.body.removeChild(a);
            window.URL.revokeObjectURL(downloadUrl);
        }

        async function get_media() {
            const url = `/dowload_media_files/${fileName}`;

            const response = await fetch(url);
            const fileBlob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(fileBlob);

            // Create a download link and click it to download the file
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `${channelName}_messages.zip`;
            document.body.appendChild(a);
            a.click();

            // Clean up
            document.body.removeChild(a);
            window.URL.revokeObjectURL(downloadUrl);
        }

     } catch (error) {
         errorMessage.textContent = error.message;
    }
});
