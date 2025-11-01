document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const analyzeBtn = document.getElementById('analyze-btn');
    const amazonUrlInput = document.getElementById('amazon-url');
    const urlError = document.getElementById('url-error');
    const processingSection = document.getElementById('processing-section');
    const resultsSection = document.getElementById('results-section');
    const errorSection = document.getElementById('error-section');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');
    const tryAgainBtn = document.getElementById('try-again-btn');
    
    // Processing step elements
    const stepScraping = document.getElementById('step-scraping');
    const stepAnalyzing = document.getElementById('step-analyzing');
    const stepSummarizing = document.getElementById('step-summarizing');
    
    // Results elements
    const reviewsCount = document.getElementById('reviews-count');
    const fakeCount = document.getElementById('fake-count');
    const realCount = document.getElementById('real-count');
    const summaryText = document.getElementById('summary-text');
    const positiveCount = document.getElementById('positive-count');
    const neutralCount = document.getElementById('neutral-count');
    const negativeCount = document.getElementById('negative-count');
    
    // Sentiment chart
    let sentimentChart = null;
    
    // Error elements
    const errorTitle = document.getElementById('error-title');
    const errorMessage = document.getElementById('error-message');
    
    // Variables to store analysis data
    let currentProductUrl = null;
    let analysisCancelled = false;
    
    // Walmart URL validation regex
    const ecommerceUrlRegex = /^(https?:\/\/)?(www\.)?walmart\.com/i;
    
    // Event listeners
    analyzeBtn.addEventListener('click', startAnalysis);
    newAnalysisBtn.addEventListener('click', resetAnalysis);
    tryAgainBtn.addEventListener('click', resetAnalysis);
    
    // Press Enter to start analysis
    amazonUrlInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            startAnalysis();
        }
    });
    
    // Animation preloading
    preloadAnimations();
    
    /**
     * Start the review analysis process
     */
    function startAnalysis() {
        console.log('Analyze button clicked!');
        const amazonUrl = amazonUrlInput.value.trim();
        console.log('URL entered:', amazonUrl);
        
        // Validate URL
        if (!amazonUrl || !ecommerceUrlRegex.test(amazonUrl)) {
            console.log('URL validation failed');
            urlError.classList.remove('d-none');
            return;
        }
        console.log('URL validation passed');
        
        // Reset UI
        urlError.classList.add('d-none');
        hideAllSections();
        processingSection.classList.remove('d-none');
        
        // Reset steps
        resetSteps();
        analysisCancelled = false;
        
        // Step 1: Validate product URL
        activateStep(stepScraping, 'Validating product URL...');
        
        // Start the animated progress bar
        let progress = 5;
        const progressInterval = setInterval(() => {
            progress += 1;
            if (progress > 95) progress = 95;
            updateProgress(stepScraping, progress);
        }, 300);
        
        // Send the URL to the server to extract ASIN
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amazon_url: amazonUrl }),
        })
        .then(response => {
            if (!response.ok) {
                clearInterval(progressInterval);
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to extract ASIN');
                });
            }
            return response.json();
        })
        .then(data => {
            if (analysisCancelled) {
                clearInterval(progressInterval);
                return;
            }
            
            clearInterval(progressInterval);
            currentProductUrl = data.product_url;
            updateProgress(stepScraping, 100);
            completeStep(stepScraping, `Product URL validated`);
            
            // Proceed to step 2: Scrape reviews
            setTimeout(() => {
                if (analysisCancelled) return;
                scrapeReviews(currentProductUrl);
            }, 500);
        })
        .catch(error => {
            clearInterval(progressInterval);
            showError('URL Analysis Failed', error.message);
        });
    }
    
    /**
     * Step 2: Scrape reviews from the product URL
     */
    function scrapeReviews(productUrl) {
        if (analysisCancelled) {
            return;
        }
        
        activateStep(stepAnalyzing, 'Scraping reviews...');
        
        setTimeout(() => {
            if (analysisCancelled) {
                return;
            }
            
            const statusText = stepAnalyzing.querySelector('.status-text');
            statusText.textContent = 'Scraping product reviews...';
        }, 1000);
        
        fetch('/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_url: productUrl }),
        })
        .then(response => response.json())
        .then(data => {
            if (analysisCancelled) {
                return;
            }

            if (data.error) {
                throw new Error(data.error);
            }

            completeStep(stepAnalyzing, 'Reviews scraped successfully');

            // Step 3: Analyze reviews
            setTimeout(() => {
                if (!analysisCancelled) {
                    identifyFakeReviews();
                }
            }, 500);
        })
        .catch(error => {
            showError('Scraping Failed', error.message);
        });
    }
    
    /**
     * Step 3: Identify fake reviews
     */
    function identifyFakeReviews() {
        if (analysisCancelled) return;
        
        activateStep(stepAnalyzing, 'Analyzing reviews for authenticity...');
        
        // Start the animated progress bar
        let progress = 5;
        const progressInterval = setInterval(() => {
            progress += 1;
            if (progress > 95) progress = 95;
            updateProgress(stepAnalyzing, progress);
        }, 300);
        
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                clearInterval(progressInterval);
                throw new Error(data.error);
            }
            
            // Got job_id, start polling
            const jobId = data.job_id;
            pollPredictStatus(jobId, progressInterval);
        })
        .catch(error => {
            clearInterval(progressInterval);
            showError('Review Analysis Failed', error.message);
        });
    }
    
    function pollPredictStatus(jobId, progressInterval) {
        const pollInterval = setInterval(() => {
            if (analysisCancelled) {
                clearInterval(pollInterval);
                clearInterval(progressInterval);
                return;
            }
            
            fetch(`/predict_status/${jobId}`)
                .then(response => response.json())
                .then(data => {
                    const statusText = stepAnalyzing.querySelector('.status-text');
                    if (data.message) {
                        statusText.textContent = data.message;
                    }
                    
                    if (data.status === 'completed') {
                        clearInterval(pollInterval);
                        clearInterval(progressInterval);
                        updateProgress(stepAnalyzing, 100);
                        completeStep(stepAnalyzing, 'Fake reviews identified');
                        
                        // Proceed to step 4: Generate summary
                        setTimeout(() => {
                            if (analysisCancelled) return;
                            generateSummary();
                        }, 500);
                    } else if (data.status === 'failed') {
                        clearInterval(pollInterval);
                        clearInterval(progressInterval);
                        throw new Error(data.error || 'Analysis failed');
                    }
                })
                .catch(error => {
                    clearInterval(pollInterval);
                    clearInterval(progressInterval);
                    showError('Review Analysis Failed', error.message);
                });
        }, 2000); // Poll every 2 seconds
    }
    
    /**
     * Step 4: Generate summary
     */
    function generateSummary() {
        if (analysisCancelled) return;
        
        activateStep(stepSummarizing, 'Generating insights from real reviews...');
        
        // Start the animated progress bar
        let progress = 5;
        const progressInterval = setInterval(() => {
            progress += 1;
            if (progress > 95) progress = 95;
            updateProgress(stepSummarizing, progress);
        }, 300);
        
        fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                clearInterval(progressInterval);
                throw new Error(data.error);
            }
            
            // Got job_id, start polling
            const jobId = data.job_id;
            pollSummarizeStatus(jobId, progressInterval);
        })
        .catch(error => {
            clearInterval(progressInterval);
            showError('Summarization Failed', error.message);
        });
    }
    
    function pollSummarizeStatus(jobId, progressInterval) {
        const pollInterval = setInterval(() => {
            if (analysisCancelled) {
                clearInterval(pollInterval);
                clearInterval(progressInterval);
                return;
            }
            
            fetch(`/summarize_status/${jobId}`)
                .then(response => response.json())
                .then(data => {
                    const statusText = stepSummarizing.querySelector('.status-text');
                    if (data.message) {
                        statusText.textContent = data.message;
                    }
                    
                    if (data.status === 'completed') {
                        clearInterval(pollInterval);
                        clearInterval(progressInterval);
                        updateProgress(stepSummarizing, 100);
                        completeStep(stepSummarizing, 'Summary generated');
                        
                        // Display results
                        setTimeout(() => {
                            if (analysisCancelled) return;
                            
                            // Update result stats using the real values from the backend
                            const stats = data.result.sentiment_stats;
                const totalReviews = stats.total_reviews || 0;
                const realReviewsCount = stats.real_reviews_count || 0;
                const fakeReviewsCount = stats.fake_reviews_count || 0;
                
                            reviewsCount.textContent = `${totalReviews} reviews processed`;
                            fakeCount.textContent = `${fakeReviewsCount} fake reviews removed`;
                            realCount.textContent = `${realReviewsCount} genuine reviews analyzed`;
                            
                            // Display summary
                            summaryText.innerHTML = data.result.summary;
                            
                            // Create or update sentiment chart
                            updateSentimentChart(stats);
                            
                            // Load and display individual reviews
                            loadReviews();
                            
                            // Show results section
                            hideAllSections();
                            resultsSection.classList.remove('d-none');
                        }, 1000);
                    } else if (data.status === 'failed') {
                        clearInterval(pollInterval);
                        clearInterval(progressInterval);
                        throw new Error(data.error || 'Summarization failed');
                    }
                })
                .catch(error => {
                    clearInterval(pollInterval);
                    clearInterval(progressInterval);
                    showError('Summary Generation Failed', error.message);
                });
        }, 2000); // Poll every 2 seconds
    }
    
    /**
     * Create or update the sentiment chart
     */
    function updateSentimentChart(sentimentData) {
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        
        // If chart already exists, destroy it
        if (sentimentChart) {
            sentimentChart.destroy();
        }
        
        // Get sentiment counts
        const positive = sentimentData.sentiment_counts.positive || 0;
        const neutral = sentimentData.sentiment_counts.neutral || 0;
        const negative = sentimentData.sentiment_counts.negative || 0;
        
        // Update count badges
        positiveCount.textContent = positive;
        neutralCount.textContent = neutral;
        negativeCount.textContent = negative;
        
        // Create chart
        sentimentChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [positive, neutral, negative],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',  // Green for positive
                        'rgba(108, 117, 125, 0.8)', // Gray for neutral
                        'rgba(220, 53, 69, 0.8)'    // Red for negative
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(108, 117, 125, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Reset the analysis process
     */
    function resetAnalysis() {
        analysisCancelled = true;
        hideAllSections();
        amazonUrlInput.value = '';
        urlError.classList.add('d-none');
        resetSteps();
        
        // Clear result elements
        reviewsCount.textContent = '0 reviews processed';
        fakeCount.textContent = '0 fake reviews removed';
        realCount.textContent = '0 genuine reviews analyzed';
        summaryText.innerHTML = '';
        positiveCount.textContent = '0';
        neutralCount.textContent = '0';
        negativeCount.textContent = '0';
        
        // Destroy chart if it exists
        if (sentimentChart) {
            sentimentChart.destroy();
            sentimentChart = null;
        }
    }
    
    /**
     * Load and display individual reviews
     */
    function loadReviews() {
        fetch('/reviews')
            .then(response => response.json())
            .then(data => {
                const reviewsList = document.getElementById('reviews-list');
                reviewsList.innerHTML = ''; // Clear existing reviews
                
                if (data.reviews && data.reviews.length > 0) {
                    data.reviews.forEach((review, index) => {
                        const reviewCard = createReviewCard(review, index + 1);
                        reviewsList.appendChild(reviewCard);
                    });
                } else {
                    reviewsList.innerHTML = '<div class="col-12"><p class="text-muted text-center">No reviews found.</p></div>';
                }
            })
            .catch(error => {
                console.error('Error loading reviews:', error);
                const reviewsList = document.getElementById('reviews-list');
                reviewsList.innerHTML = '<div class="col-12"><p class="text-danger text-center">Failed to load reviews.</p></div>';
            });
    }
    
    /**
     * Create a review card element
     */
    function createReviewCard(review, index) {
        const col = document.createElement('div');
        col.className = 'col-md-6';
        
        // Determine sentiment color and icon
        let sentimentClass = 'secondary';
        let sentimentIcon = 'fa-meh';
        if (review.sentiment === 'positive') {
            sentimentClass = 'success';
            sentimentIcon = 'fa-smile';
        } else if (review.sentiment === 'negative') {
            sentimentClass = 'danger';
            sentimentIcon = 'fa-frown';
        }
        
        // Create star rating HTML
        const stars = createStarRating(review.rating);
        
        // Format confidence percentage
        const confidencePercent = (review.confidence * 100).toFixed(1);
        
        col.innerHTML = `
            <div class="card h-100 review-card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span class="badge bg-${sentimentClass}">
                        <i class="fas ${sentimentIcon}"></i> ${review.sentiment.charAt(0).toUpperCase() + review.sentiment.slice(1)}
                    </span>
                    <span class="text-muted">#${index}</span>
                </div>
                <div class="card-body">
                    <div class="mb-2">
                        <strong>Rating:</strong> ${stars} <span class="text-muted">(${review.rating}/5)</span>
                    </div>
                    <div class="mb-2">
                        <strong>Confidence:</strong> 
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-${sentimentClass}" role="progressbar" 
                                 style="width: ${confidencePercent}%" 
                                 aria-valuenow="${confidencePercent}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                ${confidencePercent}%
                            </div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <strong>Review:</strong>
                        <p class="text-muted mb-0 mt-1">${escapeHtml(review.text)}</p>
                    </div>
                </div>
            </div>
        `;
        
        return col;
    }
    
    /**
     * Create star rating HTML
     */
    function createStarRating(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars += '<i class="fas fa-star text-warning"></i>';
            } else {
                stars += '<i class="far fa-star text-warning"></i>';
            }
        }
        return stars;
    }
    
    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    /**
     * Reset all processing steps to initial state
     */
    function resetSteps() {
        const steps = [stepScraping, stepAnalyzing, stepSummarizing];
        
        steps.forEach(step => {
            step.classList.remove('active', 'completed', 'error');
            const progressBar = step.querySelector('.progress-bar');
            const statusText = step.querySelector('.status-text');
            
            progressBar.style.width = '0%';
            progressBar.setAttribute('aria-valuenow', '0');
            statusText.textContent = 'Waiting to start...';
        });
    }
    
    /**
     * Activate a step
     */
    function activateStep(stepElement, statusMessage) {
        stepElement.classList.add('active');
        stepElement.classList.remove('completed', 'error');
        const statusText = stepElement.querySelector('.status-text');
        statusText.textContent = statusMessage;
    }
    
    /**
     * Update progress for a step
     */
    function updateProgress(stepElement, percentage) {
        const progressBar = stepElement.querySelector('.progress-bar');
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }
    
    /**
     * Mark a step as completed
     */
    function completeStep(stepElement, statusMessage) {
        stepElement.classList.remove('active');
        stepElement.classList.add('completed');
        const statusText = stepElement.querySelector('.status-text');
        statusText.textContent = statusMessage;
    }
    
    /**
     * Mark a step as error
     */
    function errorStep(stepElement, statusMessage) {
        stepElement.classList.remove('active');
        stepElement.classList.add('error');
        const statusText = stepElement.querySelector('.status-text');
        statusText.textContent = statusMessage;
    }
    
    /**
     * Hide all main content sections
     */
    function hideAllSections() {
        processingSection.classList.add('d-none');
        resultsSection.classList.add('d-none');
        errorSection.classList.add('d-none');
    }
    
    /**
     * Show error section with appropriate message
     */
    function showError(title, message) {
        errorTitle.textContent = title;
        errorMessage.textContent = message;
        hideAllSections();
        errorSection.classList.remove('d-none');
    }
    
    /**
     * Preload animation files
     */
    function preloadAnimations() {
        // Define lottie animation data
        const scrapingAnimationData = {
            "v": "5.7.8",
            "fr": 30,
            "ip": 0,
            "op": 60,
            "w": 200,
            "h": 200,
            "nm": "Scraping Animation",
            "ddd": 0,
            "assets": [],
            "layers": [
                {
                    "ddd": 0,
                    "ind": 1,
                    "ty": 4,
                    "nm": "Search Icon",
                    "sr": 1,
                    "ks": {
                        "o": { "a": 0, "k": 100 },
                        "r": {
                            "a": 1,
                            "k": [
                                { "t": 0, "s": [0] },
                                { "t": 30, "s": [180] },
                                { "t": 60, "s": [360] }
                            ]
                        },
                        "p": { "a": 0, "k": [100, 100] },
                        "a": { "a": 0, "k": [0, 0] },
                        "s": { "a": 0, "k": [100, 100, 100] }
                    },
                    "ao": 0,
                    "shapes": [
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "el",
                                    "p": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [60, 60] },
                                    "d": 1,
                                    "nm": "Ellipse Path 1"
                                },
                                {
                                    "ty": "st",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": { "a": 0, "k": 100 },
                                    "w": { "a": 0, "k": 8 },
                                    "lc": 2,
                                    "lj": 1,
                                    "ml": 4,
                                    "nm": "Stroke 1"
                                },
                                {
                                    "ty": "tr",
                                    "p": { "a": 0, "k": [0, 0] },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Circle"
                        },
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [20, 8] },
                                    "p": { "a": 0, "k": [40, 40] },
                                    "r": { "a": 0, "k": 0 },
                                    "nm": "Rectangle Path 1"
                                },
                                {
                                    "ty": "fl",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": { "a": 0, "k": 100 },
                                    "r": 1,
                                    "nm": "Fill 1"
                                },
                                {
                                    "ty": "tr",
                                    "p": { "a": 0, "k": [0, 0] },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 45 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Handle"
                        }
                    ],
                    "ip": 0,
                    "op": 60,
                    "st": 0,
                    "bm": 0
                }
            ]
        };
        
        const analyzingAnimationData = {
            "v": "5.7.8",
            "fr": 30,
            "ip": 0,
            "op": 60,
            "w": 200,
            "h": 200,
            "nm": "Analyzing Animation",
            "ddd": 0,
            "assets": [],
            "layers": [
                {
                    "ddd": 0,
                    "ind": 1,
                    "ty": 4,
                    "nm": "Brain Icon",
                    "sr": 1,
                    "ks": {
                        "o": { "a": 0, "k": 100 },
                        "r": { "a": 0, "k": 0 },
                        "p": { "a": 0, "k": [100, 100] },
                        "a": { "a": 0, "k": [0, 0] },
                        "s": {
                            "a": 1,
                            "k": [
                                { "t": 0, "s": [100, 100, 100] },
                                { "t": 15, "s": [110, 110, 100] },
                                { "t": 30, "s": [100, 100, 100] },
                                { "t": 45, "s": [110, 110, 100] },
                                { "t": 60, "s": [100, 100, 100] }
                            ]
                        }
                    },
                    "ao": 0,
                    "shapes": [
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [80, 60] },
                                    "p": { "a": 0, "k": [0, 0] },
                                    "r": { "a": 0, "k": 30 },
                                    "nm": "Brain Shape"
                                },
                                {
                                    "ty": "st",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": { "a": 0, "k": 100 },
                                    "w": { "a": 0, "k": 8 },
                                    "lc": 2,
                                    "lj": 1,
                                    "ml": 4,
                                    "nm": "Stroke 1"
                                },
                                {
                                    "ty": "tr",
                                    "p": { "a": 0, "k": [0, 0] },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Brain"
                        },
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [10, 10] },
                                    "p": { "a": 0, "k": [-20, -10] },
                                    "r": { "a": 0, "k": 5 },
                                    "nm": "Dot 1"
                                },
                                {
                                    "ty": "fl",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": {
                                        "a": 1,
                                        "k": [
                                            { "t": 0, "s": [100] },
                                            { "t": 20, "s": [30] },
                                            { "t": 40, "s": [100] },
                                            { "t": 60, "s": [30] }
                                        ]
                                    },
                                    "r": 1,
                                    "nm": "Fill 1"
                                },
                                {
                                    "ty": "tr",
                                    "p": { "a": 0, "k": [0, 0] },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Pulse Dot 1"
                        },
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [10, 10] },
                                    "p": { "a": 0, "k": [20, -10] },
                                    "r": { "a": 0, "k": 5 },
                                    "nm": "Dot 2"
                                },
                                {
                                    "ty": "fl",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": {
                                        "a": 1,
                                        "k": [
                                            { "t": 0, "s": [30] },
                                            { "t": 20, "s": [100] },
                                            { "t": 40, "s": [30] },
                                            { "t": 60, "s": [100] }
                                        ]
                                    },
                                    "r": 1,
                                    "nm": "Fill 2"
                                },
                                {
                                    "ty": "tr",
                                    "p": { "a": 0, "k": [0, 0] },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Pulse Dot 2"
                        }
                    ],
                    "ip": 0,
                    "op": 60,
                    "st": 0,
                    "bm": 0
                }
            ]
        };
        
        const summarizingAnimationData = {
            "v": "5.7.8",
            "fr": 30,
            "ip": 0,
            "op": 60,
            "w": 200,
            "h": 200,
            "nm": "Summarizing Animation",
            "ddd": 0,
            "assets": [],
            "layers": [
                {
                    "ddd": 0,
                    "ind": 1,
                    "ty": 4,
                    "nm": "Document Icon",
                    "sr": 1,
                    "ks": {
                        "o": { "a": 0, "k": 100 },
                        "r": { "a": 0, "k": 0 },
                        "p": { "a": 0, "k": [100, 100] },
                        "a": { "a": 0, "k": [0, 0] },
                        "s": { "a": 0, "k": [100, 100, 100] }
                    },
                    "ao": 0,
                    "shapes": [
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [70, 90] },
                                    "p": { "a": 0, "k": [0, 0] },
                                    "r": { "a": 0, "k": 10 },
                                    "nm": "Document Shape"
                                },
                                {
                                    "ty": "st",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": { "a": 0, "k": 100 },
                                    "w": { "a": 0, "k": 8 },
                                    "lc": 2,
                                    "lj": 1,
                                    "ml": 4,
                                    "nm": "Stroke 1"
                                },
                                {
                                    "ty": "tr",
                                    "p": { "a": 0, "k": [0, 0] },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Document"
                        },
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [50, 6] },
                                    "p": { "a": 0, "k": [0, -20] },
                                    "r": { "a": 0, "k": 3 },
                                    "nm": "Line 1"
                                },
                                {
                                    "ty": "fl",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": { "a": 0, "k": 100 },
                                    "r": 1,
                                    "nm": "Fill 1"
                                },
                                {
                                    "ty": "tr",
                                    "p": { 
                                        "a": 1,
                                        "k": [
                                            { "t": 0, "s": [0, -20] },
                                            { "t": 15, "s": [0, -20] },
                                            { "t": 30, "s": [0, 0] },
                                            { "t": 45, "s": [0, 20] },
                                            { "t": 60, "s": [0, -20] }
                                        ]
                                    },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Line 1"
                        },
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [50, 6] },
                                    "p": { "a": 0, "k": [0, 0] },
                                    "r": { "a": 0, "k": 3 },
                                    "nm": "Line 2"
                                },
                                {
                                    "ty": "fl",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": { "a": 0, "k": 100 },
                                    "r": 1,
                                    "nm": "Fill 2"
                                },
                                {
                                    "ty": "tr",
                                    "p": { 
                                        "a": 1,
                                        "k": [
                                            { "t": 0, "s": [0, 0] },
                                            { "t": 15, "s": [0, -20] },
                                            { "t": 30, "s": [0, 0] },
                                            { "t": 45, "s": [0, 20] },
                                            { "t": 60, "s": [0, 0] }
                                        ]
                                    },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Line 2"
                        },
                        {
                            "ty": "gr",
                            "it": [
                                {
                                    "ty": "rc",
                                    "d": 1,
                                    "s": { "a": 0, "k": [50, 6] },
                                    "p": { "a": 0, "k": [0, 20] },
                                    "r": { "a": 0, "k": 3 },
                                    "nm": "Line 3"
                                },
                                {
                                    "ty": "fl",
                                    "c": { "a": 0, "k": [0.294, 0.424, 0.718] },
                                    "o": { "a": 0, "k": 100 },
                                    "r": 1,
                                    "nm": "Fill 3"
                                },
                                {
                                    "ty": "tr",
                                    "p": { 
                                        "a": 1,
                                        "k": [
                                            { "t": 0, "s": [0, 20] },
                                            { "t": 15, "s": [0, -20] },
                                            { "t": 30, "s": [0, 0] },
                                            { "t": 45, "s": [0, 20] },
                                            { "t": 60, "s": [0, 20] }
                                        ]
                                    },
                                    "a": { "a": 0, "k": [0, 0] },
                                    "s": { "a": 0, "k": [100, 100] },
                                    "r": { "a": 0, "k": 0 },
                                    "o": { "a": 0, "k": 100 }
                                }
                            ],
                            "nm": "Line 3"
                        }
                    ],
                    "ip": 0,
                    "op": 60,
                    "st": 0,
                    "bm": 0
                }
            ]
        };
        
        // Save animations to files
        saveToFile('/static/animations/scraping.json', scrapingAnimationData);
        saveToFile('/static/animations/analyzing.json', analyzingAnimationData);
        saveToFile('/static/animations/summarizing.json', summarizingAnimationData);
    }
    
    /**
     * Helper function to simulate saving animation data
     */
    function saveToFile(path, data) {
        // This function doesn't actually save files in the browser
        // In a real implementation, these files would be saved on the server
        console.log(`Animation loaded: ${path}`);
    }
});
