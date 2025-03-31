document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const endpointInput = document.getElementById('endpoint');
    const requestMethodButtons = document.querySelectorAll('.method-btn');
    const sendRequestBtn = document.getElementById('sendRequestBtn');
    const requestBodyTextarea = document.getElementById('requestBody');
    const responseContainer = document.getElementById('responseContainer');
    const requestHeadersContainer = document.getElementById('requestHeaders');
    const responseHeadersContainer = document.getElementById('responseHeaders');
    const responseBodyContainer = document.getElementById('responseBody');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const clearResponseBtn = document.getElementById('clearResponseBtn');
    const customHeadersBtn = document.getElementById('customHeadersBtn');
    const customHeadersContainer = document.getElementById('customHeadersContainer');
    const addHeaderBtn = document.getElementById('addHeaderBtn');
    const headersList = document.getElementById('headersList');

    // Default endpoints for demo
    const demoEndpoints = [
        { name: 'Get All Items', method: 'GET', url: '/api/items', body: '' },
        { name: 'Get Single Item', method: 'GET', url: '/api/items/1', body: '' },
        { name: 'Create Item', method: 'POST', url: '/api/items', body: '{\n  "name": "New Item",\n  "description": "This is a new item"\n}' },
        { name: 'Update Item', method: 'PUT', url: '/api/items/1', body: '{\n  "name": "Updated Item",\n  "description": "This item was updated"\n}' },
        { name: 'Delete Item', method: 'DELETE', url: '/api/items/1', body: '' },
        { name: 'CORS Test', method: 'GET', url: '/api/cors-test', body: '' },
        { name: 'Echo Headers', method: 'GET', url: '/api/echo-headers', body: '' }
    ];

    // Create demo endpoint cards
    const endpointsContainer = document.getElementById('demoEndpoints');
    demoEndpoints.forEach(endpoint => {
        const card = document.createElement('div');
        card.className = 'card endpoint-card';
        card.innerHTML = `
            <div class="card-body p-3">
                <h6 class="card-title">${endpoint.name}</h6>
                <div class="d-flex align-items-center">
                    <span class="badge bg-${getMethodColor(endpoint.method)} me-2">${endpoint.method}</span>
                    <code>${endpoint.url}</code>
                </div>
                <button class="btn btn-sm btn-outline-secondary mt-2 try-endpoint">Try it</button>
            </div>
        `;
        endpointsContainer.appendChild(card);

        // Add event listener to the "Try it" button
        card.querySelector('.try-endpoint').addEventListener('click', () => {
            // Set the form values based on the endpoint
            endpointInput.value = getFullUrl(endpoint.url);
            setActiveMethod(endpoint.method);
            requestBodyTextarea.value = endpoint.body;
        });
    });

    // Initialize currently selected method
    let currentMethod = 'GET';

    // Add event listeners to method buttons
    requestMethodButtons.forEach(button => {
        button.addEventListener('click', function() {
            currentMethod = this.textContent;
            setActiveMethod(currentMethod);
            
            // Show/hide request body for methods that support it
            toggleRequestBodyVisibility(currentMethod);
        });
    });

    // Function to set the active method button
    function setActiveMethod(method) {
        requestMethodButtons.forEach(btn => {
            if (btn.textContent === method) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        currentMethod = method;
        toggleRequestBodyVisibility(method);
    }

    // Toggle request body visibility based on method
    function toggleRequestBodyVisibility(method) {
        const requestBodyContainer = document.getElementById('requestBodyContainer');
        if (method === 'POST' || method === 'PUT') {
            requestBodyContainer.style.display = 'block';
        } else {
            requestBodyContainer.style.display = 'none';
        }
    }

    // Add event listener to the send request button
    sendRequestBtn.addEventListener('click', sendRequest);

    // Add event listener to the clear response button
    clearResponseBtn.addEventListener('click', clearResponse);

    // Add event listener to the custom headers button
    customHeadersBtn.addEventListener('click', function() {
        customHeadersContainer.classList.toggle('d-none');
    });

    // Add event listener to the add header button
    addHeaderBtn.addEventListener('click', addCustomHeader);

    // Function to send the request
    async function sendRequest() {
        try {
            // Show loading spinner
            loadingSpinner.style.display = 'inline-block';
            sendRequestBtn.disabled = true;
            
            // Clear previous response
            clearResponse();
            
            // Get the endpoint URL
            const endpoint = endpointInput.value;
            
            // Create request options
            const options = {
                method: currentMethod,
                headers: {
                    'Content-Type': 'application/json'
                },
                // Add custom headers
                ...getCustomHeaders()
            };
            
            // Add request body for POST and PUT requests
            if (currentMethod === 'POST' || currentMethod === 'PUT') {
                options.body = requestBodyTextarea.value;
            }
            
            // Log request details
            console.log(`Sending ${currentMethod} request to ${endpoint}`);
            console.log('Request options:', options);
            
            // Send the request
            const response = await fetch(endpoint, options);
            
            // Get response headers
            const responseHeaders = {};
            response.headers.forEach((value, name) => {
                responseHeaders[name] = value;
            });
            
            // Get response body
            const responseBody = await response.text();
            let formattedResponseBody;
            
            try {
                // Try to parse as JSON
                const jsonResponse = JSON.parse(responseBody);
                formattedResponseBody = JSON.stringify(jsonResponse, null, 2);
            } catch (e) {
                // If not JSON, just use the raw text
                formattedResponseBody = responseBody;
            }
            
            // Display the response
            displayResponse({
                status: response.status,
                statusText: response.statusText,
                headers: responseHeaders,
                body: formattedResponseBody,
                requestHeaders: options.headers
            });
            
        } catch (error) {
            console.error('Error sending request:', error);
            
            // Display error message
            const errorMessage = document.createElement('div');
            errorMessage.className = 'alert alert-danger';
            errorMessage.textContent = `Error: ${error.message}`;
            responseContainer.appendChild(errorMessage);
            
        } finally {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            sendRequestBtn.disabled = false;
        }
    }

    // Function to display the response
    function displayResponse(response) {
        // Set response visible
        responseContainer.classList.remove('d-none');
        
        // Display request headers
        displayHeaders(requestHeadersContainer, response.requestHeaders);
        
        // Display response headers
        displayHeaders(responseHeadersContainer, response.headers);
        
        // Display response body
        responseBodyContainer.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="mb-0">Status: ${response.status} ${response.statusText}</h6>
            </div>
            <pre class="code-block">${escapeHtml(response.body)}</pre>
        `;
    }

    // Function to display headers
    function displayHeaders(container, headers) {
        container.innerHTML = '';
        
        // Create header cards for each header
        for (const [name, value] of Object.entries(headers)) {
            const headerCard = document.createElement('div');
            headerCard.className = 'card header-card';
            headerCard.innerHTML = `
                <div class="card-body p-2">
                    <strong>${escapeHtml(name)}:</strong>
                    <span class="header-value">${escapeHtml(value)}</span>
                </div>
            `;
            container.appendChild(headerCard);
        }
    }

    // Function to clear the response
    function clearResponse() {
        requestHeadersContainer.innerHTML = '';
        responseHeadersContainer.innerHTML = '';
        responseBodyContainer.innerHTML = '';
        responseContainer.classList.add('d-none');
    }

    // Function to add a custom header
    function addCustomHeader() {
        const headerItem = document.createElement('div');
        headerItem.className = 'input-group mb-2';
        headerItem.innerHTML = `
            <input type="text" class="form-control header-name" placeholder="Header Name">
            <input type="text" class="form-control header-value" placeholder="Header Value">
            <button class="btn btn-outline-danger remove-header" type="button">Remove</button>
        `;
        headersList.appendChild(headerItem);
        
        // Add event listener to the remove button
        headerItem.querySelector('.remove-header').addEventListener('click', function() {
            headersList.removeChild(headerItem);
        });
    }

    // Function to get custom headers
    function getCustomHeaders() {
        const headers = {};
        const headerItems = headersList.querySelectorAll('.input-group');
        
        headerItems.forEach(item => {
            const name = item.querySelector('.header-name').value.trim();
            const value = item.querySelector('.header-value').value.trim();
            
            if (name && value) {
                headers[name] = value;
            }
        });
        
        return { headers };
    }

    // Function to escape HTML
    function escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Function to get the color for a method badge
    function getMethodColor(method) {
        const colors = {
            'GET': 'success',
            'POST': 'primary',
            'PUT': 'warning',
            'DELETE': 'danger',
            'OPTIONS': 'info'
        };
        return colors[method] || 'secondary';
    }

    // Function to get the full URL by combining the base URL with the endpoint
    function getFullUrl(endpoint) {
        // Get the current URL
        const currentUrl = window.location.href;
        
        // Parse the URL
        const url = new URL(currentUrl);
        
        // Check if it's a relative URL
        if (endpoint.startsWith('/')) {
            // Use the same port as the current page since both frontend and API are served from the same server
            return `${url.protocol}//${url.hostname}${endpoint}`;
        }
        
        // If it's already a full URL, return it as is
        return endpoint;
    }

    // Update host port in the endpoint input field placeholder
    const hostPortPlaceholder = `${window.location.protocol}//${window.location.hostname}/api/items`;
    endpointInput.placeholder = hostPortPlaceholder;
    
    // Set default endpoint
    endpointInput.value = hostPortPlaceholder;
});
