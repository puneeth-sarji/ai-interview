document.addEventListener('DOMContentLoaded', () => {
    // Basic setup
    const room_id = 'room-' + Math.random().toString(36).substr(2, 6);
    document.getElementById('room-display').textContent = room_id;
    
    // UI Elements
    const codeEditor = document.getElementById('code-editor');
    const runBtn = document.getElementById('run-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const langSelect = document.getElementById('language-select');
    const outputTerminal = document.getElementById('output-terminal');
    const aiFeedback = document.getElementById('ai-feedback');
    
    // WebSocket Setup
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//localhost:8000/ws/${room_id}`;
    let ws = new WebSocket(wsUrl);
    
    let isEditing = false;
    
    ws.onopen = () => {
        console.log('Connected to WebSocket room:', room_id);
    };
    
    ws.onmessage = (event) => {
        const data = event.data;
        
        if (data.startsWith('OUTPUT:\n')) {
            outputTerminal.textContent = data.replace('OUTPUT:\n', '');
            runBtn.disabled = false;
            runBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Run Code`;
        } else if (data.startsWith('AI_FEEDBACK:\n')) {
            aiFeedback.textContent = data.replace('AI_FEEDBACK:\n', '');
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path></svg> AI Analysis`;
        } else {
            // It's a code update
            if (!isEditing) {
                const cursorPosition = codeEditor.selectionStart;
                codeEditor.value = data;
                codeEditor.setSelectionRange(cursorPosition, cursorPosition);
            }
        }
    };
    
    ws.onclose = () => {
        console.log('WebSocket disconnected');
        outputTerminal.textContent = "Connection lost. Please refresh.";
    };
    
    // Editor sync
    codeEditor.addEventListener('input', () => {
        isEditing = true;
        ws.send(codeEditor.value);
        setTimeout(() => isEditing = false, 500); // rudimentary debounce flag
    });
    
    // Actions
    runBtn.addEventListener('click', () => {
        const lang = langSelect.value;
        ws.send(`RUN:${lang}`);
        
        outputTerminal.textContent = "Executing code...";
        runBtn.disabled = true;
        runBtn.innerHTML = "Running...";
    });
    
    analyzeBtn.addEventListener('click', () => {
        ws.send(`ANALYZE`);
        
        aiFeedback.textContent = "Gemini is analyzing your code...";
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = "Analyzing...";
    });
});
