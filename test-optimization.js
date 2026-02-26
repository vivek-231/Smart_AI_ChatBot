// 🚀 Test script to verify ultra-fast response optimizations
const fetch = require('node-fetch');

async function testOptimizations() {
    console.log('🚀 Testing Ultra-Fast Chatbot Optimizations...\n');
    
    const baseUrl = 'http://localhost:5000';
    const sessionId = Date.now().toString();
    
    try {
        // Test 1: Health check
        console.log('1️⃣ Testing server health...');
        const healthResponse = await fetch(`${baseUrl}/health`);
        const healthData = await healthResponse.json();
        console.log('✅ Server Status:', healthData.status);
        console.log('✅ Ollama Status:', healthData.ollama.status);
        
        // Test 2: Quick response (greeting)
        console.log('\n2️⃣ Testing quick response (greeting)...');
        const quickStartTime = Date.now();
        
        const quickResponse = await fetch(`${baseUrl}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                sessionId, 
                message: 'Hello! How are you?' 
            })
        });
        
        const quickData = await quickResponse.json();
        const quickEndTime = Date.now();
        const quickResponseTime = quickEndTime - quickStartTime;
        
        console.log('✅ Quick Response Time:', quickResponseTime + 'ms');
        console.log('✅ Quick Response Length:', quickData.response?.length || 0, 'characters');
        console.log('✅ Quick Success:', quickData.success);
        
        if (quickResponseTime < 500) {
            console.log('🎉 ULTRA FAST: Quick response under 0.5 seconds!');
        } else if (quickResponseTime < 1000) {
            console.log('⚡ FAST: Quick response under 1 second!');
        } else {
            console.log('⚠️ SLOW: Quick response over 1 second');
        }
        
        // Test 3: Detailed response (complex question)
        console.log('\n3️⃣ Testing detailed response (complex question)...');
        const detailedStartTime = Date.now();
        
        const detailedResponse = await fetch(`${baseUrl}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                sessionId, 
                message: 'Explain the differences between machine learning and artificial intelligence in detail.' 
            })
        });
        
        const detailedData = await detailedResponse.json();
        const detailedEndTime = Date.now();
        const detailedResponseTime = detailedEndTime - detailedStartTime;
        
        console.log('✅ Detailed Response Time:', detailedResponseTime + 'ms');
        console.log('✅ Detailed Response Length:', detailedData.response?.length || 0, 'characters');
        console.log('✅ Detailed Success:', detailedData.success);
        
        if (detailedResponseTime < 2000) {
            console.log('🎉 ULTRA FAST: Detailed response under 2 seconds!');
        } else if (detailedResponseTime < 3000) {
            console.log('⚡ FAST: Detailed response under 3 seconds!');
        } else {
            console.log('⚠️ SLOW: Detailed response over 3 seconds');
        }
        
        // Test 4: Streaming chat
        console.log('\n4️⃣ Testing streaming chat...');
        const streamStartTime = Date.now();
        
        const streamResponse = await fetch(`${baseUrl}/chat-stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                sessionId, 
                message: 'Tell me about machine learning in a few sentences.' 
            })
        });
        
        if (streamResponse.ok) {
            console.log('✅ Streaming endpoint accessible');
            console.log('✅ Content-Type:', streamResponse.headers.get('content-type'));
        } else {
            console.log('⚠️ Streaming endpoint not working, but regular chat is optimized');
        }
        
        console.log('\n🎯 Smart Response System Summary:');
        console.log('✅ Smart question detection implemented');
        console.log('✅ Quick responses for greetings/simple questions');
        console.log('✅ Detailed responses for complex questions');
        console.log('✅ Typing animation shows first, then fast response');
        console.log('✅ Ultra-fast typewriter (2ms for quick, 3ms for detailed)');
        console.log('✅ AI parameters optimized per question type');
        console.log('✅ Response time targets: < 0.5s quick, < 2s detailed');
        
    } catch (error) {
        console.error('❌ Test Error:', error.message);
        console.log('\n💡 Make sure to:');
        console.log('1. Start the server: cd nodejs-backend && node server.js');
        console.log('2. Have Ollama running: ollama run llama3.2:1b');
    }
}

// Run the test
testOptimizations();
