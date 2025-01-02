exports.handler = async (event) => {
    // CORS headers
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*', // Or specify your domain
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    };
    
    // Handle preflight OPTIONS request
    if (event.requestContext.http.method === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: corsHeaders,
            body: ''
        };
    }
    
    try {
        // Your existing Lambda logic here
        // ...
        
        return {
            statusCode: 200,
            headers: {
                ...corsHeaders,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(/* your response data */)
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers: {
                ...corsHeaders,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ error: error.message })
        };
    }
}; 